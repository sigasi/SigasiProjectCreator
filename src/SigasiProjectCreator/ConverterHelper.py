# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import platform
import subprocess

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
    cygwin_location = cygwin_location.replace('\\', '/')
    return cygwin_location


def parse_and_create_project(usage, parse_file):
    parser = ArgsAndFileParser(usage)
    (project_name, _, destination, parser_output) = parser.parse_args_and_file(parse_file)

    verilog_includes = None
    verilog_defines = None
    if not isinstance(parser_output, dict):
        verilog_includes = parser_output.includes
        verilog_defines = parser_output.defines
        entries = parser_output.library_mapping
        if verilog_includes is not None and len(verilog_includes) > 0:
            print("Includes: " + str(verilog_includes))
        if verilog_defines is not None and len(verilog_defines) > 0:
            print("Defines: " + str(verilog_defines))
    else:
        entries = parser_output
    print("Library mapping: " + str(entries))

    sigasi_project_file_creator = SigasiProjectCreator(project_name)
    sigasi_project_file_creator.unmap("/")

    forceVHDL = False
    forceVerilog = False

    linked_folders = dict()
    for path, library in entries.items():
        abs_destination = os.path.normcase(os.path.abspath(destination))
        abs_path = os.path.normcase(os.path.abspath(path))
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
            target = os.path.join(common_prefix, directory_name)

            linked_folders[directory_name] = target

            sigasi_project_file_creator.add_mapping(eclipse_path, library)
    print("Linked folders: " + str(linked_folders))

    # Update verilog includes: if they are in a linked folder, use the link name
    if verilog_includes is not None:
        new_verilog_includes = []
        for include_folder in verilog_includes:
            for linked_folder, dest_folder in linked_folders.items():
                abs_dest_folder = os.path.normcase(os.path.normpath(os.path.abspath(dest_folder)))
                abs_incl_folder = os.path.normcase(os.path.normpath(os.path.abspath(include_folder)))
                common_prefix = os.path.commonprefix([abs_dest_folder, abs_incl_folder])
                if len(str(common_prefix)) > 0 and os.path.samefile(dest_folder, common_prefix):
                    prefixlen = len(str(common_prefix))
                    include_subpath = abs_incl_folder[prefixlen:]
                    new_inlcude_path = os.path.join(linked_folder, include_subpath.lstrip('/\\'))
                    new_verilog_includes.append(new_inlcude_path)
                else:
                    new_verilog_includes.append(include_folder)
        verilog_includes = new_verilog_includes
        print("Includes (updated): " + str(verilog_includes))

    # Adding custom items to libraries.
    # sigasi_project_file_creator.add_unisim("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unisims")
    # sigasi_project_file_creator.add_unimacro("C:/xilinx/14.5/ISE_DS/ISE/vhdl/src/unimacro")

    for folder, location in linked_folders.items():
        if running_in_cyg_win():
            location = convert_cygwin_path(location)
        sigasi_project_file_creator.add_link(folder, location, True)

    sigasi_project_file_creator.write(destination, forceVHDL, forceVerilog, verilog_includes, verilog_defines)
