import os
import sys

from SigasiProjectCreator.DotF.parseFile import parse_dotf
from SigasiProjectCreator.convertDotFtoCsv import rebase_file


class DotFfileParser:
    library_mapping = dict()
    includes = []
    defines = dict()
    filename = ""
    dotfdir = ""
    dotfname = ""
    csvfname = ""

    filecontent = []

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
            print("*ERROR* File " + filename + " does not exist")
            sys.exit(1)
        if os.path.isabs(filename):
            print("*ERROR* must use a relative path, but " + filename + " is absolute")
            sys.exit(1)

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
                            self.library_mapping[rebase_file(fn, self.dotfdir)] = newlib
                else:
                    print('Unexpected multiline option: ' + option[0])
            else:
                bare_option = str(option).strip('"')
                if bare_option.startswith("+incdir"):
                    print("*include path* " + rebase_file(bare_option[8:], self.dotfdir)) # TODO may contain multiple entries!
                    self.include_path.append(bare_option[8:])
                elif bare_option.startswith("-endlib"):
                    pass
                elif bare_option.startswith("+") or bare_option.startswith("-"):
                    print("*unknown option* " + bare_option)
                else:
                    self.library_mapping[rebase_file(bare_option, self.dotfdir)] = 'work'

def parse_file(filename):
    parser = DotFfileParser(filename)
    return parser.library_mapping

usage = """usage: %prog project-name dot-f-file [destination]

destination is the current directory by default
example: %prog MyProjectName filelist.f
"""
