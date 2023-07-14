"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""

# Exit codes:
# 1 : file not found
# 2 : relative path expected, but absolute path given

from SigasiProjectCreator.DotF.parseFile import parse_dotf
import sys
import os
import csv

def isabspath(path):
    s_path = str(path)
    if s_path.startswith('\\') or s_path.startswith('/') or s_path[1] == ':' or s_path.startswith('$'):
        return True
    return os.path.isabs(path)


def rebase_file(filename, dotfdir):
    hdlpath = os.path.expandvars(filename)
    if not isabspath(hdlpath):
        hdlpath = os.path.join(dotfdir, hdlpath)
    hdlpath = os.path.normpath(hdlpath)
    return hdlpath


def convertDotFtoCsv(filename):
    if not os.path.isfile(filename):
        print("*ERROR* File " + filename + " does not exist")
        sys.exit(1)
    if os.path.isabs(filename):
        print("*ERROR* must use a relative path, but " + filename + " is absolute")
        sys.exit(2)
    
    dotfdir = os.path.dirname(filename)
    dotfname = os.path.basename(filename)
    csvfname = str(os.path.splitext(dotfname)[0]) + ".csv"
    
    include_path = []
    filecontent = parse_dotf(filename)

    print("Writing CSV: " + csvfname)

    with open(csvfname, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for option in filecontent:
            if isinstance(option, list):
                if option[0].startswith("-makelib"):
                    newlib = option[0].split(' ')[1].split('/')[-1]
                    print('Library ' + newlib)
                    for fn in option:
                        if not (fn.startswith("+") or fn.startswith("-")):
                            csvwriter.writerow([newlib, rebase_file(str(fn).strip('"'), dotfdir)])
                else:
                    print('Unexpected multiline option: ' + option[0])
            else:
                bare_option = str(option).strip('"')
                if bare_option.startswith("+incdir"):
                    print("*include path* " + rebase_file(bare_option[8:], dotfdir))
                    include_path.append(bare_option[8:])
                elif bare_option.startswith("+") or bare_option.startswith("-"):
                    print("*unknown option* " + bare_option)
                else:
    #                 print("*file* " + bare_option + " => " + rebase_file(bare_option, dotfdir))
                    csvwriter.writerow(['work', rebase_file(bare_option, dotfdir)])

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        convertDotFtoCsv(sys.argv[1])
    else:
        print('Usage: convertDotFtoCsv.py <input_file>')
        exit(1)
