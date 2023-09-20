# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import argparse
import pathlib

from SigasiProjectCreator import CsvParser, VerilogVersion, VhdlVersion
from SigasiProjectCreator.DotF import DotFfileParser
from SigasiProjectCreator.convertHdpProjectToSigasiProject import parse_hdp_file
from SigasiProjectCreator.convertXilinxISEToSigasiProject import parse_xilinx_file


def get_parser_for_type(input_type):
    print(f'*get_parser_for_type* {input_type}')
    if input_type == 'dotf':
        return DotFfileParser.parse_file
    if input_type == 'csv':
        return CsvParser.parse_file
    if input_type == 'hdp':
        return parse_hdp_file
    if input_type == 'filelist':
        return None
    if input_type == 'xise':
        return parse_xilinx_file


class ArgsAndFileParser:
    options = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='SigasiProjectCreator')
        self.parser.add_argument('project_name', help='Project name')
        self.parser.add_argument('input_file', help='Input file or comma-separated list of input files')
        self.parser.add_argument('destination_folder', help='Root folder of created project', type=pathlib.Path,
                                 nargs='?')
        self.parser.add_argument('-l', '--layout', action='store', dest='layout',
                                 choices=['default', 'simulator', 'linked-files-flat', 'linked-files-tree',
                                          'linked-folders'], default='default',
                                 help='Project layout: default (in place), simulator (one folder per library with '
                                      'linked files), linked-files-flat (one folder with links to all files), '
                                      'linked-files-tree (virtual folders like the source tree, with links to files), '
                                      'or linked-folders (mix of virtual and linked folders)')
        self.parser.add_argument('--uvm', help='Add UVM to the project, using UVM from the given install path',
                                 dest='uvm', type=pathlib.Path)
        self.parser.add_argument('--use-uvm-home', help='Add UVM to the project. Sigasi Studio will use the UVM_HOME '
                                                        'environment variable to find your UVM installation',
                                 dest='uvmhome', action='store_true')
        self.parser.add_argument('--uvmlib', help='Library in which to compile the UVM package (default: the library '
                                                  'set with `--work`, or `work`)',
                                 dest='uvmlib', default=None)
        self.parser.add_argument('--format', action='store', dest='format',
                                 choices=['dotf', 'csv', 'filelist', 'hdp'], default=None,
                                 help='Force input format (ignore file extension)')
        self.parser.add_argument('--mapping', action='store', dest='mapping',
                                 choices=['file', 'folder'], default='file',
                                 help='Library mapping style: `folder` = map folders where possible, `file` = map '
                                      'individual files (default). Option `folder` requires that files are actually '
                                      'available. Only relevant with `default`, `linked-files-tree` and '
                                      '`linked-folders` project layouts')
        self.parser.add_argument('--enable-vhdl', action='store_true', dest='enable_vhdl',
                                 help='Force VHDL support (regardless of VHDL file presence)')
        self.parser.add_argument('--vhdl-version', action='store', dest='vhdl_version',
                                 choices=VhdlVersion.get_str_enums(), default=str(VhdlVersion.TWENTY_O_EIGHT),
                                 help='Set VHDL version')
        self.parser.add_argument('--enable-verilog', action='store_true', dest='enable_verilog',
                                 help='Force (System)Verilog support (regardless of (System)Verilog file presence)')
        self.parser.add_argument('--verilog-as-sv', action='store_true', dest='system_verilog',
                                 help='Treat .v files as SystemVerilog')
        self.parser.add_argument('--enable-vunit', action='store_true', dest='enable_vunit',
                                 help='Enable VUnit support')
        self.parser.add_argument('-w', '--work', help='Main HDL library name (default `work`)',
                                 dest='worklib', default='work')
        self.parser.add_argument('--skip-check-exists', action='store_true', dest='skip-check-exists',
                                 help='Don\'t check whether files actually exist')
        self.parser.add_argument('--encoding', action='store', dest='encoding',
                                 default='UTF-8', help='Set unicode character encoding (default: UTF-8)')

    @staticmethod
    def get_file_type(filename):
        file_ext = str(pathlib.Path(filename).suffix).lower()
        if file_ext.startswith('.'):
            file_ext = file_ext[1:]
        if file_ext == 'f':
            return 'dotf'
        if file_ext in ['csv', 'hdp']:
            return file_ext
        return 'filelist'

    def parse_args(self):
        args = self.parser.parse_args()
        filetype = None
        if ',' in args.input_file:
            args.input_file = args.input_file.split(',')
            for infile in args.input_file:
                if not os.path.isfile(infile):
                    self.parser.error(f'Input file \'{infile}\' does not exist')
                if args.format is None:
                    # Only check the file type if it's not overridden
                    if filetype is None:
                        filetype = self.get_file_type(infile)
                    else:
                        if filetype != self.get_file_type(infile):
                            self.parser.error('Unsupported: mixed input file types')
        elif not os.path.isfile(args.input_file):
            self.parser.error(f'Input file \'{args.input_file}\' does not exist')
        else:
            if args.format is None:
                # Only check the file type if it's not overridden
                filetype = self.get_file_type(args.input_file)
        vars(args)['filetype'] = filetype

        if args.destination_folder is not None:
            if not args.destination_folder.is_dir():
                self.parser.error('destination folder has to be a folder')
        if args.uvmhome:
            if args.uvm is not None:
                self.parser.error('Conflicting options --uvm and --use-uvm-home used')
            args.uvm = 'ENV-UVM_HOME'
        elif args.uvm is not None:
            if not os.path.isdir(args.uvm):
                self.parser.error(f'UVM home \'{args.uvm}\' must be a folder')
            if not os.path.isfile(os.path.join(args.uvm, 'src/uvm_macros.svh')):
                self.parser.error(f'Could not find uvm_macros.svh in \'{args.uvm}/src\'')
            if not os.path.isfile(os.path.join(args.uvm, 'src/uvm_pkg.sv')):
                self.parser.error(f'Could not find uvm_pkg.sv in \'{args.uvm}/src\'')

        ArgsAndFileParser.options = args
        return args

    @staticmethod
    def parse_input_file():
        args = ArgsAndFileParser.options
        parse_file = ArgsAndFileParser.get_file_parser()
        destination = args.destination_folder if args.destination_folder is not None else os.getcwd()
        if parse_file is not None:
            entries = parse_file(args.input_file)
            return args.project_name, args.input_file, destination, entries
        # If the parser is None, we assume that input_file contains a (list of) HDL files

        entries = {os.path.realpath(os.path.abspath(entry)): args.worklib for entry in args.input_file}
        return args.project_name, None, destination, entries

    @staticmethod
    def get_layout_option():
        return ArgsAndFileParser.options.layout

    @staticmethod
    def get_mapping_option():
        return ArgsAndFileParser.options.mapping

    @staticmethod
    def get_destination_folder():
        if ArgsAndFileParser.options.destination_folder is not None:
            return os.path.realpath(os.path.abspath(ArgsAndFileParser.options.destination_folder))
        return os.getcwd()

    @staticmethod
    def get_uvm_option():
        return ArgsAndFileParser.options.uvm, ArgsAndFileParser.options.uvmlib

    @staticmethod
    def get_input_format():
        if ArgsAndFileParser.options.format is not None:
            return ArgsAndFileParser.options.format
        return ArgsAndFileParser.options.filetype

    @staticmethod
    def get_file_parser():
        return get_parser_for_type(ArgsAndFileParser.get_input_format())

    @staticmethod
    def get_enable_vhdl():
        return ArgsAndFileParser.options.enable_vhdl

    @staticmethod
    def get_enable_verilog():
        return ArgsAndFileParser.options.enable_verilog

    @staticmethod
    def get_enable_vunit():
        return ArgsAndFileParser.options.enable_vunit

    @staticmethod
    def get_work_library():
        return ArgsAndFileParser.options.worklib

    @staticmethod
    def get_encoding():
        return ArgsAndFileParser.options.encoding

    @staticmethod
    def get_vhdl_version():
        return int(ArgsAndFileParser.options.vhdl_version)

    @staticmethod
    def get_verilog_version():
        if ArgsAndFileParser.options.system_verilog:
            return VerilogVersion.TWENTY_TWELVE
        return VerilogVersion.TWENTY_O_FIVE
