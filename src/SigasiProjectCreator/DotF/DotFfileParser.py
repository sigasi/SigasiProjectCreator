"""
    :copyright: (c) 2008-2021 Sigasi
    :license: BSD, see LICENSE for more details.
"""

# Exit codes:
# 3 : input file not found

import os
import sys
import glob

from .parseFile import parse_dotf
from ..convertDotFtoCsv import rebase_file


class DotFfileParser:

    def __init__(self, filename):

        self.library_mapping = dict()
        self.includes = set()
        self.defines = []
        self.filename = ""
        self.dotfdir = ""
        self.dotfname = ""
        self.csvfname = ""
        self.filecontent = []

        self.filename = filename
        if not os.path.isfile(filename):
            print("*ERROR* File " + filename + " does not exist")
            sys.exit(1)
        if os.path.isabs(filename):
            filename = os.path.relpath(filename)

        self.dotfdir = os.path.dirname(filename)
        self.dotfname = os.path.basename(filename)
        self.csvfname = str(os.path.splitext(self.dotfname)[0]) + ".csv"

        self.filecontent = parse_dotf(filename)
        for option in self.filecontent:
            if isinstance(option, list):
                if option[0].startswith("-makelib"):
                    newlib = option[0].split(' ')[1].split('/')[-1]
                    for fn in option:
                        if not (fn.startswith("+") or fn.startswith("-")):
                            if "*" in fn:
                                expanded_option = glob.glob(rebase_file(fn, self.dotfdir), recursive=True)
                                for f in expanded_option:
                                    self.library_mapping[f] = newlib
                            else:
                                self.library_mapping[rebase_file(fn, self.dotfdir)] = newlib
                elif option[0] == "+incdir":
                    for fn in option[1:]:
                        self.includes.add(rebase_file(fn[1:], self.dotfdir))
                elif option[0] == "+define":
                    for df in option[1:]:
                        self.defines.append(df[1:].strip())
                else:
                    print('Unknown multiline option (ignored) : ' + option[0])
            else:
                bare_option = str(option).strip('"')
                if bare_option.startswith("-endlib"):
                    pass
                elif bare_option.startswith("-f "):
                    # Parse included .f file
                    subfile = os.path.expandvars(bare_option.split()[1])
                    if not os.path.isabs(subfile):
                        subfile = os.path.join(self.dotfdir, subfile)
                    subparser = DotFfileParser(subfile)
                    self.library_mapping.update(subparser.library_mapping)
                    self.includes |= subparser.includes
                    self.defines.extend(subparser.defines)
                elif bare_option.startswith("+") or bare_option.startswith("-"):
                    print("Unknown option (ignored) : " + bare_option)
                else:
                    # Design file: add to library mapping
                    if "*" in bare_option:
                        expanded_option = glob.glob(rebase_file(bare_option, self.dotfdir), recursive=True)
                        for f in expanded_option:
                            self.library_mapping[f] = 'work'
                    else:
                        self.library_mapping[rebase_file(bare_option, self.dotfdir)] = 'work'

def parse_file(filename):
    parser = None
    if ',' in filename:
        filenames = filename.split(',')
        parser = DotFfileParser(filenames[0])
        for fn in filenames[1:]:
            subparser = DotFfileParser(fn)
            parser.library_mapping.update(subparser.library_mapping)
            parser.includes |= subparser.includes
            parser.defines.extend(subparser.defines)
    else:
        parser = DotFfileParser(filename)

    return parser

usage = """usage: %prog project-name dot-f-file [destination]

destination is the current directory by default
example: %prog MyProjectName filelist.f
use a relative path to the .f file
multiple .f files can be specified as a comma-separated list
"""
