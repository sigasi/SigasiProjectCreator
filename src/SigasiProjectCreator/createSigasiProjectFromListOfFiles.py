#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os

from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator import VhdlVersion
import argparse

usage = """usage: %prog project-name hdl-file hdl-file...

    this script creates a Sigasi project in the current working directory:
        * adds one linked folder to the project that points to the common
          folder of all listed hdl-files
        * unmaps all hdl-files in the common folder, except the listed files.
          These files are mapped to the 'work' library
example: %prog MyProjectName foo.vhdl bar.sv
"""


def main():
    parser = argparse.ArgumentParser(prog='SigasiProjectCreator')
    parser.add_argument('project_name', help='project name')
    parser.add_argument('input_files', help='input files', nargs='+')
    args = parser.parse_args()
    project_name = args.project_name
    hdl_files = args.input_files
    destination = os.getcwd()

    # Find common directory of the hdl files
    abs_paths = [os.path.abspath(x) for x in hdl_files]
    folder = os.path.dirname(os.path.commonprefix([p + os.path.sep for p in abs_paths]))

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
