#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import os
from SigasiProjectCreator import SigasiProjectCreator

def main():
    usage = """usage: %prog project-name vhdl-file vhdl-file...

    this scripts creates a sigasi project in the current working directory:
        * adds one linked folder to the project that points to the common
          folder of all listed vhdl-files
        * unmaps all vhdl-files in the common folder, except the listed files.
          These files are mapped to the 'work' library
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len (args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    vhdl_files = args[1:]
    destination = os.getcwd()

    #find common directory of the vhdl files
    abs_paths = map(lambda x: os.path.abspath(x), vhdl_files)
    folder = os.path.commonprefix(abs_paths)

    sigasProjectFileCreator = SigasiProjectCreator(project_name, 93)
    #Create Project File and add a link the common source folder
    folderName = os.path.basename(os.path.normpath(folder))
    sigasProjectFileCreator.add_link(folderName, folder, 2)

    #Create Library Mapping File
    # unmap everything except the list of files (map those to work)
    sigasProjectFileCreator.unmap("/")
    for path in abs_paths:
        relativeFilePath = os.path.relpath(path, folder)
        sigasProjectFileCreator.add_mapping(folderName + "/" + relativeFilePath, "work")

    sigasProjectFileCreator.write(destination)

if __name__ == '__main__':
    main()