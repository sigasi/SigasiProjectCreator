"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""

# Exit codes:
# 3 : input file not found

import os
import sys
import glob
import re

# from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from .parseFile import parse_dotf
from .. import ArgsAndFileParser
from ..convertDotFtoCsv import rebase_file


def abspath(path):
    s_path = str(path)
    if s_path.startswith('\\') or s_path.startswith('/') or s_path[1] == ':' or s_path.startswith('$'):
        # this is an absolute path in Linux or Windows
        return path
    return os.path.abspath(path)


def expandvars_plus(s):
    return os.path.expandvars(re.sub(r'\$\((.*)\)', r'${\1}', s))


class DotFfileParser:

    def __init__(self, filename):

        self.library_mapping = dict()
        self.includes = set()
        self.defines = []
        self.filename = ""
        self.dotfdir = ""
        self.dotfname = ""
        self.filecontent = []
        self.linked_file_mapping = dict()

        default_work_library = ArgsAndFileParser.ArgsAndFileParser.get_work_library()

        self.filename = filename
        if not os.path.isfile(filename):
            print("*ERROR* File " + filename + " does not exist")
            sys.exit(1)

        # TODO abs => rel => => abs path? clean up!
        if os.path.isabs(filename):
            filename = os.path.relpath(filename)

        # dotfdir is an absolute path to avoid confusion later
        self.dotfdir = os.path.realpath(os.path.abspath(expandvars_plus(os.path.dirname(filename))))
        self.dotfname = os.path.basename(filename)

        self.filecontent = parse_dotf(filename)
        parser_expect_library = False
        parser_expect_dot_f = False
        newlib = 'work'
        for option in self.filecontent:
            if isinstance(option, list):
                if option[0] == "+incdir":
                    for fn in option[1:]:
                        self.includes.add(rebase_file(fn[1:], self.dotfdir))
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
                    newlib = 'work'
                elif bare_option == "-f":
                    parser_expect_dot_f = True
                elif bare_option.startswith("+") or bare_option.startswith("-"):
                    print(f'*.f parse* unknown option (ignored) : {bare_option}')
                elif parser_expect_dot_f:
                    parser_expect_dot_f = False
                    # Parse included .f file
                    subfile = expandvars_plus(bare_option)
                    if not os.path.isabs(subfile):
                        subfile = os.path.join(self.dotfdir, subfile)
                    subparser = DotFfileParser(subfile)
                    self.library_mapping.update(subparser.library_mapping)
                    self.includes |= subparser.includes
                    self.defines.extend(subparser.defines)
                elif parser_expect_library:
                    # new library name
                    parser_expect_library = False
                    newlib = bare_option.split('/')[-1]
                else:
                    # Design file: add to library mapping
                    if str(os.path.splitext(bare_option)[1]).lower() in ['.vhd', '.vhdl', '.v', '.sv']:
                        self.add_to_library_mapping(bare_option, newlib)
                    else:
                        print(f'*.f parse* skipping {bare_option}')

    def add_to_library_mapping(self, file, library):
        # Note: we used to handle project layout ("standard in-place" and "simulator" layout) here
        # Now we make the library mapping "just" a list of files and libraries, and we'll handle the project
        # layout later.

        # File paths in a .f file seem to be relative to the location of the .f file.
        # Projects may contain multiple .f files in different locations.
        # We make all paths absolute here. At a later stage, relative paths to the project root will be introduced
        print(f'*dotf_add_to_library_mapping* {file} => {library}')
        if not os.path.isabs(file):
            # self.dotfdir is an absolute path
            file = os.path.join(self.dotfdir, file)
        file = os.path.realpath(file)

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
