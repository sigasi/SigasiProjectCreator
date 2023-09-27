"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""

# Exit codes:
# 3 : input file not found

import os
import glob
import pathlib
import re

from .parseFile import parse_dotf
from .. import ArgsAndFileParser


def abspath(path):
    s_path = str(path)
    if s_path.startswith('\\') or s_path.startswith('/') or s_path[1] == ':' or s_path.startswith('$'):
        # this is an absolute path in Linux or Windows
        return path
    return pathlib.Path(path).absolute()


def expandvars_plus(s) -> pathlib.Path:
    return pathlib.Path(os.path.expandvars(re.sub(r'\$\((.*)\)', r'${\1}', str(s))))


class DotFfileParser:

    def __init__(self, filename):

        self.library_mapping = dict()
        self.includes = set()
        self.defines = []
        self.dotfdir = ""
        self.file_content = []
        self.linked_file_mapping = dict()

        assert pathlib.Path(filename).is_file(), f'*ERROR* File {filename} does not exist'
        input_file = pathlib.Path(expandvars_plus(filename)).absolute().resolve()
        self.dotfdir = input_file.parent

        self.file_content = parse_dotf(input_file)
        parser_expect_library = False
        parser_expect_dot_f = False

        default_work_library = ArgsAndFileParser.ArgsAndFileParser.get_work_library()
        new_library = default_work_library
        for option in self.file_content:
            if isinstance(option, list):
                if option[0] == "+incdir":
                    for include_folder in option[1:]:
                        while include_folder.startswith('+'):
                            include_folder = include_folder[1:]
                        include_folder_path = pathlib.Path(include_folder)
                        include_folder_path = expandvars_plus(include_folder_path)
                        if not include_folder_path.is_absolute():
                            # self.dotfdir is an absolute path
                            include_folder = self.dotfdir.joinpath(include_folder)
                        self.includes.add(include_folder_path.resolve())
                elif option[0] == "+define":
                    for df in option[1:]:
                        self.defines.append(df[1:].strip())
                else:
                    print('Unknown multiline option (ignored) : ' + option[0])
            else:
                bare_option = str(option).strip('"')
                if bare_option == "-makelib" or bare_option == "-work":
                    parser_expect_library = True
                elif bare_option == "-endlib":
                    new_library = default_work_library
                elif bare_option == "-f":
                    parser_expect_dot_f = True
                elif bare_option.startswith("+") or bare_option.startswith("-"):
                    print(f'*.f parse* unknown option (ignored) : {bare_option}')
                elif parser_expect_dot_f:
                    parser_expect_dot_f = False
                    # Parse included .f file
                    sub_file = expandvars_plus(bare_option)
                    if not sub_file.is_absolute():
                        sub_file = self.dotfdir.joinpath(sub_file)
                    subparser = DotFfileParser(sub_file)
                    self.library_mapping.update(subparser.library_mapping)
                    self.includes |= subparser.includes
                    self.defines.extend(subparser.defines)
                elif parser_expect_library:
                    # new library name
                    parser_expect_library = False
                    new_library = bare_option.split('/')[-1]
                else:
                    # Design file: add to library mapping
                    design_file = pathlib.Path(bare_option)
                    if design_file.suffix.lower() in ['.vhd', '.vhdl', '.v', '.sv']:
                        self.add_to_library_mapping(design_file, new_library)
                    else:
                        print(f'*.f parse* skipping {bare_option}')

    def add_to_library_mapping(self, file: pathlib.Path, library):
        # Note: we used to handle project layout ("standard in-place" and "simulator" layout) here
        # Now we make the library mapping "just" a list of files and libraries, and we'll handle the project
        # layout later.

        # File paths in a .f file seem to be relative to the location of the .f file.
        # Projects may contain multiple .f files in different locations.
        # We make all paths absolute here. At a later stage, relative paths to the project root will be introduced
        file = expandvars_plus(file)
        if not file.is_absolute():
            # self.dotfdir is an absolute path
            file = self.dotfdir.joinpath(file)
        if "*" in str(file):
            expanded_file = glob.glob(str(file), recursive=True)
            if not expanded_file:
                print(f'**warning** wildcard expression {file} does not match anything, skipping')
                return
            for f in expanded_file:
                self.add_file_to_library_mapping(pathlib.Path(f), library)
            return
        self.add_file_to_library_mapping(file, library)

    def add_file_to_library_mapping(self, file: pathlib.Path, library):
        file = file.resolve()

        if file in self.library_mapping:
            if not isinstance(self.library_mapping[file], list):
                # Check against duplicates
                if library != self.library_mapping[file]:
                    # Case: file mapped a second time
                    self.library_mapping[file] = [self.library_mapping[file], library]
            else:
                # Check against duplicates
                if library not in self.library_mapping[file]:
                    # Case: file mapped a third time (or more)
                    self.library_mapping[file].append(library)
        else:
            # General case: file mapped once
            self.library_mapping[file] = library


def parse_file(filename):
    parser = None
    if isinstance(filename, list):
        parser = DotFfileParser(filename[0])
        for fn in filename[1:]:
            subparser = DotFfileParser(fn)
            parser.library_mapping.update(subparser.library_mapping)
            parser.includes |= subparser.includes
            parser.defines.extend(subparser.defines)
    else:
        parser = DotFfileParser(filename)

    return parser


usage = """usage: %prog [--layout=default|simulator] project-name dot-f-file [destination]

destination is the current directory by default
example: %prog MyProjectName filelist.f
use a relative path to the .f file
multiple .f files can be specified as a comma-separated list

project layout: default  : files are referenced in their current location.
                           HDL files must reside in the destination folder or a sub-folder thereof.
                simulator: project consists of a virtual folder per library, into which HDL files are linked.
                           Destination folder must be empty for 'simulator' project layout.
"""
