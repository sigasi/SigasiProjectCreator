# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import platform
import subprocess
from SigasiProjectCreator import SigasiProjectCreator
from ArgsAndFileParser import ArgsAndFileParser


def get_parts(pth):
    parts = []
    while True:
        pth, last = os.path.split(pth)
        if not last:
            break
        parts.append(last)
    return parts


def running_in_cyg_win():
    return platform.system().startswith("CYGWIN")


def convert_cygwin_path(cygwin_path):
    cygwin_process = subprocess.Popen(['/usr/bin/cygpath', '--windows', cygwin_path], stdout=subprocess.PIPE)
    cygwin_location = cygwin_process.communicate()[0].rstrip()
    cygwin_location = cygwin_location.replace('\\', '/')
    return cygwin_location


def parse_and_create_project(usage, parse_file):
    parser = ArgsAndFileParser(usage)
    (project_name, _, destination, entries) = parser.parse_args_and_file(parse_file)
    print(entries)

    sigasi_project_file_creator = SigasiProjectCreator(project_name)
    sigasi_project_file_creator.unmap("/")

    linked_folders = dict()
    for path, library in entries.items():
        abs_destination = os.path.normcase(os.path.abspath(destination))
        abs_path = os.path.normcase(os.path.abspath(path))
        relative_path = os.path.relpath(abs_path, abs_destination)
        if not relative_path.startswith(".."):
            sigasi_project_file_creator.add_mapping(relative_path, library)
        else:
            common_prefix = os.path.dirname(os.path.commonprefix([p + os.path.sep for p in [abs_path, abs_destination]]))
            eclipse_path = os.path.relpath(abs_path, common_prefix)
            directory_name = get_parts(eclipse_path)[-1]
            target = os.path.join(common_prefix, directory_name)

            linked_folders[directory_name] = target

            sigasi_project_file_creator.add_mapping(eclipse_path, library)

    # Adding custom items to libraries.
    # sigasi_project_file_creator.add_unisim("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unisims")
    # sigasi_project_file_creator.add_unimacro("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unimacro")

    for folder, location in linked_folders.items():
        if running_in_cyg_win():
            location = convert_cygwin_path(location)
        sigasi_project_file_creator.add_link(folder, location, True)

    sigasi_project_file_creator.write(destination)
