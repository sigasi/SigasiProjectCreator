#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import os
import platform
import subprocess
import ConfigParser

from SigasiProjectCreator import SigasiProjectCreator

def parse_hdp_file(hdp_file):
    config = ConfigParser.SafeConfigParser()
    config.read(hdp_file)
    entries = config.items("hdl")
    return {lib: path for path, lib in entries}

def main():
    usage = """usage: %prog project-name hdp-file [destination]

destination is the current directory by default
example: %prog myproject.hdp
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len (args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    hdp_file = args[1]

    destination = os.getcwd()
    if len (args) > 2:
        destination = args[2]
        if not os.path.isdir(destination):
            parser.error("destination has to be a folder")

    entries = parse_hdp_file(hdp_file)

    print entries

    def getParts(pth):
        parts = []
        while True:
            pth, last = os.path.split(pth)
            if not last:
                break
            parts.append(last)
        return parts

    sigasProjectFileCreator = SigasiProjectCreator(project_name)
    sigasProjectFileCreator.unmap("/")

    linkedFolders = dict()
    for path, library in entries.iteritems():
        abs_destination = os.path.abspath(destination)
        abs_path = os.path.abspath(path)
        relativePath = os.path.relpath(abs_path, abs_destination)
        if (not relativePath.startswith("..")):
            sigasProjectFileCreator.add_mapping(relativePath, library)
        else:
            common_prefix = os.path.commonprefix([abs_path,abs_destination])
            eclipse_path = os.path.relpath(abs_path,common_prefix)
            directoryName = getParts(eclipse_path)[-1]
            target = os.path.join(common_prefix,directoryName)

            linkedFolders[directoryName] = target

            sigasProjectFileCreator.add_mapping(eclipse_path, library)

    # adding custom items to libraries.
    # sigasProjectFileCreator.add_unisim("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unisims")
    # sigasProjectFileCreator.add_unimacro("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unimacro")

    def runningInCygWin():
        return platform.system().startswith("CYGWIN")

    def convertCygwinPath(cygwinPath):
        cygwin_process = subprocess.Popen(['/usr/bin/cygpath', '--windows', cygwinPath], stdout=subprocess.PIPE)
        location = cygwin_process.communicate()[0].rstrip()
        location = location.replace('\\','/')
        return location

    for folder, location in linkedFolders.iteritems():
        if runningInCygWin():
            location = convertCygwinPath(location)
        sigasProjectFileCreator.add_link(folder, location, 2)

    sigasProjectFileCreator.write(destination)

if __name__ == '__main__':
    main()
