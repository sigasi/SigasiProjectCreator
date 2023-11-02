# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import argparse
import pathlib

from SigasiProjectCreator import VerilogVersion, VhdlVersion, ProjectCreator, ProjectFileParser


class ProjectOptions:
    def __init__(self, args_list=None):
        parser = argparse.ArgumentParser(prog='SigasiProjectCreator')
        parser.add_argument('project_name', help='Project name')
        parser.add_argument('input_file', help='Input file or comma-separated list of input files', nargs='+')
        parser.add_argument('-d', '--destination', action='store', dest='destination_folder',
                            help='Root folder of created project', type=pathlib.Path, default=pathlib.Path.cwd())
        parser.add_argument('-l', '--layout', choices=ProjectCreator.project_creators.keys(), default='in-place',
                            help=('Any of the following layouts: ' + ', '.join(
                                f'{key} ({cls.__doc__})' for key, cls in ProjectCreator.project_creators.items())))
        parser.add_argument('--uvm', help='Add UVM to the project, using UVM from the given install path',
                            dest='uvm', type=pathlib.Path)
        parser.add_argument('--use-uvm-home', help='Add UVM to the project. Sigasi Studio will use the UVM_HOME '
                                                   'environment variable to find your UVM installation',
                            dest='uvmhome', action='store_true')
        parser.add_argument('--uvmlib', help='Library in which to compile the UVM package (default: the library '
                                             'set with `--work`, or `work`)',
                            dest='uvmlib', default=None)
        parser.add_argument('--format', action='store', dest='format',
                            choices=ProjectFileParser.project_file_parsers.keys(), default=None,
                            help='Force input format (ignore file extension): ' + ', '.join(
                                f'{key} ({cls.__doc__})' for key, cls in ProjectFileParser.project_file_parsers.items()))
        parser.add_argument('--mapping', action='store', dest='mapping',
                            choices=['file', 'folder'], default='file',
                            help='Library mapping style: `folder` = map folders where possible, `file` = map '
                                 'individual files (default). Option `folder` requires that files are actually '
                                 'available. Only relevant with `default`, `linked-files-tree` and '
                                 '`linked-folders` project layouts')
        parser.add_argument('--enable-vhdl', action='store_true', dest='enable_vhdl',
                            help='Force VHDL support (regardless of VHDL file presence)')
        parser.add_argument('--vhdl-version', action='store', dest='vhdl_version',
                            choices=VhdlVersion.get_str_enums(), default=str(VhdlVersion.TWENTY_O_EIGHT),
                            help='Set VHDL version (default VHDL-2008)')
        parser.add_argument('--enable-verilog', action='store_true', dest='enable_verilog',
                            help='Force (System)Verilog support (regardless of (System)Verilog file presence)')
        parser.add_argument('--verilog-as-sv', action='store_true', dest='system_verilog',
                            help='Treat .v files as SystemVerilog')
        parser.add_argument('--enable-vunit', action='store_true', dest='enable_vunit',
                            help='Enable VUnit support')
        parser.add_argument('-w', '--work', help='Main HDL library name (default `work`)',
                            dest='worklib', default='work')
        parser.add_argument('--skip-check-exists', action='store_true', dest='skip_check_exists',
                            help='Skip checking whether files and folders exist')
        parser.add_argument('--encoding', action='store', dest='encoding',
                            default='UTF-8', help='Set unicode character encoding (default: UTF-8)')
        parser.add_argument('-f', '--force', action='store_true', dest='force_write',
                            help='Overwrite existing project files')
        parser.add_argument('--rel-path', action='store', dest='rel_path_root',
                            nargs='*', type=pathlib.Path,
                            help='Use relative paths for links to files in this folder and its sub-folders')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                            help='Verbose output')

        # Run the command line parser
        args = parser.parse_args(args_list)

        # Transfer parsed arguments to attributes
        self.project_name = args.project_name
        self.input_file = args.input_file
        self.input_format = args.format

        for infile in self.input_file:
            if not pathlib.Path(infile).is_file():
                parser.exit(1, f'Input file \'{infile}\' does not exist or is not a file\n')
            if args.format is None:
                # Only check the file type if it's not overridden
                if self.input_format is None:
                    self.input_format = get_file_type(infile)
                else:
                    if self.input_format != get_file_type(infile):
                        parser.error('Mixed input file types are not supported')
        if len(self.input_file) == 1:
            self.input_file = self.input_file[0]

        if args.destination_folder.exists():
            if not args.destination_folder.is_dir():
                parser.exit(1, f'Cannot create project folder {args.destination_folder}: a file with that name '
                               f'exists\n')
        else:
            if not args.destination_folder.parent.is_dir():
                parser.exit(1, f'Cannot create project folder {args.destination_folder.name} in '
                               f'{args.destination_folder.parent}\n')
            args.destination_folder.mkdir()
        self.destination_folder = args.destination_folder.absolute().resolve()

        self.uvm = None
        if args.uvmhome:
            if args.uvm is not None:
                parser.error('Conflicting options --uvm and --use-uvm-home used')
            self.uvm = pathlib.Path('ENV-UVM_HOME')
        elif args.uvm is not None:
            uvm_path = pathlib.Path(args.uvm)
            if not uvm_path.is_dir():
                parser.exit(1, f'UVM home \'{args.uvm}\' must be a folder\n')
            if (not uvm_path.joinpath('src/uvm_macros.svh').is_file()) \
                    or not (uvm_path.joinpath('src/uvm_pkg.sv').is_file()):
                parser.exit(1, f'UVM folder \'{args.uvm}/src\' must contain uvm_macros.svh and uvm_pkg.sv\n')
            self.uvm = uvm_path

        if args.uvmlib is None:
            self.uvm_lib = args.worklib
        else:
            self.uvm_lib = args.uvmlib

        self.rel_path_root = None
        if args.rel_path_root:
            self.rel_path_root = [pathlib.Path(folder).absolute().resolve() for folder in args.rel_path_root]

        self.layout = args.layout
        self.mapping = args.mapping
        self.enable_vhdl = args.enable_vhdl
        self.enable_verilog = args.enable_verilog
        self.enable_vunit = args.enable_vunit
        self.work_lib = args.worklib
        self.encoding = args.encoding
        self.vhdl_version = int(args.vhdl_version)
        self.verilog_version = VerilogVersion.TWENTY_TWELVE if args.system_verilog else VerilogVersion.TWENTY_O_FIVE
        self.force_overwrite = args.force_write
        self.skip_check_exists = args.skip_check_exists
        self.verbose = args.verbose

    def use_relative_path(self, my_path):
        # TODO figure out path/purepath mess (windows related??)
        pure_path = pathlib.PurePath(pathlib.Path(my_path).absolute())
        if self.rel_path_root:
            for path_root in self.rel_path_root:
                if pure_path.is_relative_to(path_root):
                    return True
        return False


def get_file_type(filename):
    file_ext = str(pathlib.Path(filename).suffix).lower()
    if file_ext.startswith('.'):
        file_ext = file_ext[1:]
    if file_ext == 'f':
        return 'dotf'
    if file_ext in ['csv', 'hdp']:
        return file_ext
    return 'filelist'
