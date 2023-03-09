# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import platform
import subprocess

from SigasiProjectCreator import absnormpath, posixpath
from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser


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
    return posixpath(cygwin_location)


def parse_and_create_project(usage, parse_file):
    parser = ArgsAndFileParser(usage)
    (project_name, _, destination, parser_output) = parser.parse_args_and_file(parse_file)

    verilog_includes = None
    verilog_defines = None
    linked_files = None
    if not isinstance(parser_output, dict):
        verilog_includes = parser_output.includes
        verilog_defines = parser_output.defines
        entries = parser_output.library_mapping
        if verilog_includes is not None and len(verilog_includes) > 0:
            print("Includes: " + str(verilog_includes))
        if verilog_defines is not None and len(verilog_defines) > 0:
            print("Defines: " + str(verilog_defines))
        linked_files = parser_output.linked_file_mapping
        if linked_files is not None and len(linked_files) > 0:
            print("Linked files: " + str(linked_files))
    else:
        entries = parser_output
    print("Library mapping: " + str(entries))

    sigasi_project_file_creator = SigasiProjectCreator(project_name)
    sigasi_project_file_creator.unmap("/")

    forceVHDL = False
    forceVerilog = False
    forceVUnit = False

    linked_folders = dict()
    abs_destination = absnormpath(destination)
    for path, library in entries.items():
        abs_path = absnormpath(path)
        relative_path = os.path.relpath(abs_path, abs_destination)
        if (not forceVerilog) and (relative_path.endswith('.v') or relative_path.endswith('.sv')):
            forceVerilog = True
        if (not forceVHDL) and (relative_path.endswith('.vhd') or relative_path.endswith('.vhdl')):
            forceVHDL = True
        if not relative_path.startswith(".."):
            sigasi_project_file_creator.add_mapping(relative_path, library)
        else:
            common_prefix = os.path.dirname(os.path.commonprefix([p + os.path.sep for p in [abs_path, abs_destination]]))
            eclipse_path = os.path.relpath(abs_path, common_prefix)
            directory_name = get_parts(eclipse_path)[-1]
            if str(ArgsAndFileParser.get_layout_option()) == 'default':
                target = os.path.join(common_prefix, directory_name)
            else:
                target = 'virtual:/virtual'

            linked_folders[directory_name] = target

            sigasi_project_file_creator.add_mapping(eclipse_path, library)
    print("Linked folders: " + str(linked_folders))

    # Update verilog includes: if they are in a linked folder, use the link name
    if verilog_includes is not None and linked_folders:
        new_verilog_includes = []
        for include_folder in verilog_includes:
            match_found = False
            for linked_folder, dest_folder in linked_folders.items():
                abs_dest_folder = absnormpath(dest_folder)
                abs_incl_folder = absnormpath(include_folder)
                common_prefix = os.path.commonprefix([abs_dest_folder, abs_incl_folder])
                if len(str(common_prefix)) > 0 and os.path.samefile(dest_folder, common_prefix):
                    prefixlen = len(str(common_prefix))
                    include_subpath = abs_incl_folder[prefixlen:]
                    new_inlcude_path = os.path.join(linked_folder, include_subpath.lstrip('/\\'))
                    new_verilog_includes.append(new_inlcude_path)
                    match_found = True
            if not match_found:
                new_verilog_includes.append(include_folder)
        verilog_includes = new_verilog_includes
    print("Includes (updated): " + str(verilog_includes))

    # Adding custom items to libraries.
    # sigasi_project_file_creator.add_unisim("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unisims")
    # sigasi_project_file_creator.add_unimacro("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unimacro")

    for folder, location in linked_folders.items():
        if running_in_cyg_win() and not location.startswith('virtual'):
            location = convert_cygwin_path(location)
        sigasi_project_file_creator.add_link(folder, location, True)

    if linked_files is not None:
        for file, location in linked_files.items():
            abs_location = absnormpath(location)
            relative_location_path = make_project_location_path(os.path.relpath(abs_location, abs_destination))
            if running_in_cyg_win():
                relative_location_path = convert_cygwin_path(relative_location_path)

            if str(ArgsAndFileParser.get_layout_option()) == 'default':
                abs_file = absnormpath(file)
                relative_file_path = os.path.relpath(abs_file, abs_destination)
                if running_in_cyg_win():
                    relative_file_path = convert_cygwin_path(relative_file_path)
            else:
                relative_file_path = file

            sigasi_project_file_creator.add_link(relative_file_path, relative_location_path)

    sigasi_project_file_creator.write(destination, forceVHDL, forceVerilog, verilog_includes, verilog_defines,
                                      forceVUnit)


def make_project_location_path(rel_path):
    parent_level = 0
    while rel_path.startswith('..'):
        parent_level += 1
        rel_path = rel_path[3::]
    if parent_level == 0:
        return 'PROJECT_LOC/' + rel_path
    return 'PARENT-' + str(parent_level) + '-PROJECT_LOC/' + rel_path