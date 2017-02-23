#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
from ArgsAndFileParser import ArgsAndFileParser
from SigasiProjectCreator import SigasiProjectCreator
import VhdlVersion

usage = """usage: %prog project-name hdl-file hdl-file...

    this script creates a sigasi project in the current working directory:
        * adds one linked folder to the project that points to the common
          folder of all listed hdl-files
        * unmaps all hdl-files in the common folder, except the listed files.
          These files are mapped to the 'work' library
example: %prog MyProjectName foo.vhdl bar.sv
"""


def main():
    parser = ArgsAndFileParser(usage)
    args = parser.parse_args(2)
    project_name = args[0]
    hdl_files = args[1:]
    destination = os.getcwd()

    # Find common directory of the hdl files
    abs_paths = [os.path.abspath(x) for x in hdl_files]
    folder = os.path.commonprefix(abs_paths)

    sigasi_project_file_creator = SigasiProjectCreator(project_name, VhdlVersion.NINETY_THREE)
    # Create Project File and add a link the common source folder
    folder_name = os.path.basename(os.path.normpath(folder))
    sigasi_project_file_creator.add_link(folder_name, folder, True)

    # Create Library Mapping File
    # Unmap everything except the list of files (map those to work)
    sigasi_project_file_creator.unmap("/")
    for path in abs_paths:
        relative_file_path = os.path.relpath(path, folder)
        sigasi_project_file_creator.add_mapping(folder_name + "/" + relative_file_path, "work")

    sigasi_project_file_creator.write(destination)


if __name__ == '__main__':
    main()
