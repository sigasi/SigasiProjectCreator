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
import xml.etree.ElementTree as eT

from SigasiProjectCreator import SigasiProjectCreator


def parse_xilinx_file(xilinx_file):
    entries = dict()
    tree = eT.parse(xilinx_file)
    root = tree.getroot()

    schema = '{http://www.xilinx.com/XMLSchema}'

    for f in root.findall('*/' + schema + 'file'):
        if schema + 'type' in f.attrib:
            schema_type = f.attrib[schema + 'type']
            if schema_type == 'FILE_VHDL':
                name = f.attrib[schema + 'name']
                lib = f.find(schema + 'library')
                library = lib.attrib[schema + 'name'] if (lib is not None) else "work"
                entries[name] = library

    return entries


def main():
    usage = """usage: %prog project-name Xilinx-file [destination]

destination is the current directory by default
example: %prog MyProjectName project.xise
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    xilinx_file = args[1]

    destination = os.getcwd()
    if len(args) > 2:
        destination = args[2]
        if not os.path.isdir(destination):
            parser.error("destination has to be a folder")

    entries = parse_xilinx_file(xilinx_file)

    print entries

    def get_parts(pth):
        parts = []
        while True:
            pth, last = os.path.split(pth)
            if not last:
                break
            parts.append(last)
        return parts

    sigasi_project_file_creator = SigasiProjectCreator(project_name)
    sigasi_project_file_creator.unmap("/")

    linked_folders = dict()
    for path, library in entries.iteritems():
        abs_destination = os.path.abspath(destination)
        abs_path = os.path.abspath(path)
        relative_path = os.path.relpath(abs_path, abs_destination)
        if not relative_path.startswith(".."):
            sigasi_project_file_creator.add_mapping(relative_path, library)
        else:
            common_prefix = os.path.commonprefix([abs_path, abs_destination])
            eclipse_path = os.path.relpath(abs_path, common_prefix)
            directory_name = get_parts(eclipse_path)[-1]
            target = os.path.join(common_prefix, directory_name)

            linked_folders[directory_name] = target

            sigasi_project_file_creator.add_mapping(eclipse_path, library)

    # Adding custom items to libraries.
    # sigasi_project_file_creator.add_unisim("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unisims")
    # sigasi_project_file_creator.add_unimacro("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unimacro")

    def running_in_cyg_win():
        return platform.system().startswith("CYGWIN")

    def convert_cygwin_path(cygwin_path):
        cygwin_process = subprocess.Popen(['/usr/bin/cygpath', '--windows', cygwin_path], stdout=subprocess.PIPE)
        cygwin_location = cygwin_process.communicate()[0].rstrip()
        cygwin_location = cygwin_location.replace('\\', '/')
        return cygwin_location

    for folder, location in linked_folders.iteritems():
        if running_in_cyg_win():
            location = convert_cygwin_path(location)
        sigasi_project_file_creator.add_link(folder, location, 2)

    sigasi_project_file_creator.write(destination)

if __name__ == '__main__':
    main()
