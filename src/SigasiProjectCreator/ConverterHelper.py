# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import pathlib
import platform
import subprocess

from SigasiProjectCreator import absnormpath, posixpath
from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from pathlib import Path, PurePath


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


def set_common_libraries(my_path):
    # if not str(my_path).startswith('dependencies'):
    return my_path
    # return posixpath(os.path.join('Common Libraries', my_path))


def get_rel_or_abs_path(my_path, destination):
    # This function accepts an absolute path and checks whether a relative path is expected.
    # If a relative path is expected, the relative path is returned.
    input_path = pathlib.PurePath(my_path)
    if input_path.is_relative_to(destination) or ArgsAndFileParser.get_use_relative_path(input_path):
        return input_path.relative_to(destination)
    return input_path


def convert_cygwin_path(cygwin_path):
    cygwin_process = subprocess.Popen(['/usr/bin/cygpath', '--windows', cygwin_path], stdout=subprocess.PIPE)
    cygwin_location = cygwin_process.communicate()[0].rstrip()
    return posixpath(cygwin_location)


virtual_folders = ['Common Libraries']


def check_and_create_virtual_folder(project_creator, file_name):
    filepath = os.path.dirname(file_name)
    if filepath not in virtual_folders:
        new_folders = []
        while filepath and (filepath not in virtual_folders):
            new_folders.insert(0, filepath)
            # print('folder to add: ' + str(filepath))
            filepath = os.path.split(filepath)[0]
        # TODO: optimize: do everything in the while loop
        # print('New folders: ' + str(new_folders))
        for new_path in new_folders:
            virtual_folders.append(new_path)
            project_creator.add_link(new_path, None, True)
    # print('Virtual folders: ' + str(virtual_folders))


def check_and_create_linked_folder(project_creator, folder_name):
    virtual_path_name = folder_name
    # TODO future work: map some folders into Common Libraries
    # if folder_name.startswith('dependencies'):
    #     virtual_path_name = posixpath(os.path.join('Common Libraries', folder_name))
    check_and_create_virtual_folder(project_creator, virtual_path_name)
    # TODO it's not always PARENT-1- => improve code!
    link_folder_name = posixpath(os.path.join('PARENT-1-PROJECT_LOC', folder_name))
    # print('Adding linked folder: ' + str(virtual_path_name) + ' => ' + link_folder_name)
    project_creator.add_link(virtual_path_name, link_folder_name, True)


project_root = None


def parse_and_create_project():
    (project_name, _, destination, parser_output) = ArgsAndFileParser.parse_input_file()

    verilog_includes = None
    verilog_defines = None

    global project_root
    project_root = destination

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

    if not ArgsAndFileParser.get_skip_check_exists():
        for file in entries.keys():
            assert os.path.exists(file), f'*ERROR* file {file} does not exist'

    sigasi_project_file_creator = SigasiProjectCreator(project_name)
    sigasi_project_file_creator.unmap("/")

    has_vhdl = False
    has_verilog = False
    project_layout = ArgsAndFileParser.get_layout_option()
    if project_layout == 'simulator':
        (has_vhdl, has_verilog) = create_project_simulator(sigasi_project_file_creator, entries)
    elif project_layout == 'linked-files-flat':
        (has_vhdl, has_verilog) = create_project_links_flat(sigasi_project_file_creator, entries)
    elif project_layout == 'linked-files-tree':
        (has_vhdl, has_verilog) = create_project_links_tree(sigasi_project_file_creator, entries)
    elif project_layout == 'linked-folders':
        (has_vhdl, has_verilog) = create_project_links_folders(sigasi_project_file_creator, entries)
    elif project_layout == 'default':
        (has_vhdl, has_verilog) = create_project_in_place(sigasi_project_file_creator, entries)
    else:
        print(f'Unsupported project layout {project_layout}')
        exit(1)

    # From here we need to structure the project according to the layout setting
    # Input: lists of design files, include files, verilog defines, some options
    # Output: definition of .project, library mapping, other options
    #  depending on requested layout
    #  special care is required for PATH handling:
    #  * which files are in the project tree, which ones need linking?
    #  * up to 4 paths may have importance: cwd, (design/include) file location,
    #    project destination, input file location (e.g. .f : relative paths are relative to .f location)

    # Update verilog includes
    # Incoming are absolute paths
    # If the path is a sub-path of the project folder, use the relative path
    # If not:
    #   * make an `include_folders` folder
    #   * in it, make a link to the include folder, making sure to not have name clashes
    #   * use the project path
    if verilog_includes is not None:
        has_includes_folder = False
        linked_include_folders = []
        for include_folder in verilog_includes:
            assert ArgsAndFileParser.get_skip_check_exists() or os.path.isdir(include_folder), '*ERROR* include ' \
                                                                                               'folder does not ' \
                                                                                               'exist: ' \
                                                                                               f'{include_folder} '
            # TODO check for and eliminate duplicates
            local_include_folder = None
            if not PurePath(include_folder).is_relative_to(destination):
                if not has_includes_folder:
                    sigasi_project_file_creator.add_link('include_folders', None, True)
                    has_includes_folder = True
                local_path = None
                parent_path = include_folder
                while not local_path:  # deal with trailing path separators
                    parent_path, local_path = os.path.split(parent_path)
                if local_path in linked_include_folders:
                    # TODO support this case
                    print(f'*Include path* name clash for {include_folder}')
                    exit(1)
                linked_include_folders.append(local_path)
                local_include_folder = os.path.join('include_folders', local_path)
                sigasi_project_file_creator.add_link(local_include_folder,
                                                     get_rel_or_abs_path(include_folder, destination), True)
            else:
                local_include_folder = os.path.relpath(include_folder, destination)
            sigasi_project_file_creator.add_verilog_include(local_include_folder)

    # For the time being, we assume that absolute paths are used here (e.g. in a simulator install tree)
    # TODO support relative paths (should be part of a more general path handling overhaul?)

    uvm_location, uvm_library = ArgsAndFileParser.get_uvm_option()
    if uvm_location is not None:
        sigasi_project_file_creator.add_uvm(uvm_location, uvm_library)

    sigasi_project_file_creator.set_languages(has_vhdl, has_verilog)
    force_vunit = ArgsAndFileParser.get_enable_vunit()
    sigasi_project_file_creator.write(destination, None, verilog_defines, force_vunit)


def create_project_simulator(project_creator, entries):
    # In this layout, the project contains one virtual folder per HDL library, which in turn contains
    # links to each relevant file. Virtual folders are mapped to libraries.
    libraries = []
    has_vhdl = False
    has_verilog = False
    for my_file, my_library in entries.items():
        file_ext = str(os.path.splitext(my_file)[1]).lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        ref_path = None
        if isinstance(my_library, list):
            for my_lib in my_library:
                create_project_simulator_add_single(project_creator, my_lib, libraries, my_file)
        else:
            create_project_simulator_add_single(project_creator, my_library, libraries, my_file)
    return has_vhdl, has_verilog


def create_project_simulator_add_single(project_creator, my_library, libraries, my_file):
    if my_library not in libraries:
        project_creator.add_link(my_library, None, True)  # virtual folder named after the library
        project_creator.add_mapping(my_library, my_library)
        libraries.append(my_library)
    file_path, file_name = os.path.split(my_file)
    linked_path = my_library + '/' + file_name
    # TODO: my_file handling, avoid filename clashes
    project_creator.add_link(linked_path, get_rel_or_abs_path(my_file, project_root), False)


def create_project_links_flat(project_creator, entries):
    has_vhdl = False
    has_verilog = False
    # TODO check that the destination folder does not contain the design files
    for path, library in entries.items():
        file_ext = str(os.path.splitext(path)[1]).lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        ref_path = None
        if isinstance(library, dict):
            ref_path = library['reference']
            library = library['library']
        file_path, file_name = os.path.split(path)
        linked_path = file_name
        # TODO: path handling, avoid filename clashes
        project_creator.add_link(linked_path, get_rel_or_abs_path(path, project_root), False)
        project_creator.add_mapping(linked_path, library)
    return has_vhdl, has_verilog


def get_design_folders(entries):
    folders = []
    for path, library in entries.items():
        # TODO actual PATH handling
        folder = os.path.split(path)[0]
        if folder not in folders:
            folders.append(folder)
    folders.sort()
    return folders


def get_design_root_folder(folder_list):
    # TODO clean up paths to avoid ValueError from os.path.commonpath
    return os.path.commonpath(folder_list)


def get_design_subtrees(folder_list):
    # Design subtrees are folders which contain design files, while none of their parent folders contain design files
    folder_list.sort()
    design_root_folders = []
    current_folder = None
    for my_folder in folder_list:
        if (current_folder is None) or (not my_folder.startswith(current_folder)):
            design_root_folders.append(my_folder)
            current_folder = my_folder
    return design_root_folders


def create_project_links_tree(project_creator, entries):
    has_vhdl = False
    has_verilog = False
    # TODO check that the destination folder does not contain the design files
    # TODO more extended PATH handling

    design_folders = get_design_folders(entries)
    design_root = get_design_root_folder(design_folders)
    abs_to_rel_file = {}

    for path, library in entries.items():
        file_ext = str(os.path.splitext(path)[1]).lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True

        rel_path = os.path.relpath(path, design_root)
        check_and_create_virtual_folder(project_creator, rel_path)
        project_creator.add_link(rel_path, get_rel_or_abs_path(path, project_root), False)
        abs_to_rel_file[path] = rel_path

    if ArgsAndFileParser.get_mapping_option() == 'file':
        create_library_mapping_per_file(project_creator, entries, abs_to_rel_file)
    else:
        create_library_mapping_folders(project_creator, entries, abs_to_rel_file)

    return has_vhdl, has_verilog


def create_library_mapping_folders(project_creator, entries, file_to_project_map):
    # design_folders is a list of folders with actual design files in them
    design_folders = get_design_folders(entries)
    design_root = get_design_root_folder(design_folders)
    for design_folder in design_folders:
        folder_library = None
        folder_list = os.listdir(design_folder)
        for folder_item in folder_list:
            folder_item_with_path = os.path.join(design_folder, folder_item)
            if os.path.isdir(folder_item_with_path):
                local_folder = os.path.relpath(folder_item_with_path, design_root)
                project_creator.unmap(local_folder)
            elif os.path.isfile(folder_item_with_path):
                if os.path.splitext(folder_item_with_path)[1] in ['.vhd', '.vhdl', '.v', '.sv']:
                    file_with_path = str(posixpath(os.path.join(design_folder, folder_item)))
                    if file_with_path in entries:
                        my_lib = entries[file_with_path]
                        if isinstance(my_lib, list):
                            file_is_mapped = False
                            if folder_library is not None and folder_library in my_lib:
                                file_is_mapped = True
                            for single_lib in my_lib:
                                if folder_library is None:
                                    # if parent folder is mapped to this library, clear mapping of the current folder
                                    design_parent_folder = os.path.split(design_folder)[0]
                                    parent_lib = project_creator.get_mapping(design_parent_folder)
                                    if parent_lib is None or parent_lib != single_lib:
                                        project_creator.add_mapping(os.path.relpath(design_folder, design_root),
                                                                    single_lib)
                                    else:
                                        project_creator.remove_mapping(os.path.relpath(design_folder, design_root))
                                    folder_library = single_lib
                                    file_is_mapped = True
                                elif single_lib != folder_library:
                                    if file_is_mapped:
                                        local_file = os.path.relpath(file_with_path, design_root)
                                        file_parts = os.path.splitext(local_file)
                                        new_file = f'{file_parts[0]}_{single_lib}{file_parts[1]}'
                                        project_creator.add_link(new_file,
                                                                 get_rel_or_abs_path(file_with_path, project_root))
                                        project_creator.add_mapping(new_file, single_lib)
                                    else:
                                        project_creator.add_mapping(os.path.relpath(file_with_path, design_root),
                                                                    single_lib)
                                    file_is_mapped = True
                        else:
                            if folder_library is None:
                                # if parent folder is mapped to this library, clear the mapping of the current folder
                                design_parent_folder = os.path.split(design_folder)[0]
                                parent_lib = project_creator.get_mapping(design_parent_folder)
                                if parent_lib is None or parent_lib != my_lib:
                                    project_creator.add_mapping(os.path.relpath(design_folder, design_root), my_lib)
                                else:
                                    project_creator.remove_mapping(os.path.relpath(design_folder, design_root))
                                folder_library = my_lib
                            elif folder_library != my_lib:
                                project_creator.add_mapping(os.path.relpath(file_with_path, design_root), my_lib)
                    elif ArgsAndFileParser.get_layout_option() != 'linked-files-tree':
                        project_creator.unmap(os.path.relpath(file_with_path, design_root))


def create_library_mapping_per_file(project_creator, mapping_entries, filesystem_to_project_mapping):
    # TODO not OK: need file path (absolute or relative)!
    for item, library in mapping_entries.items():
        add_library_mapping(project_creator, filesystem_to_project_mapping[item], library, item)


def create_project_links_folders(project_creator, entries):
    has_vhdl = False
    has_verilog = False
    # TODO check that the destination folder does not contain the design files
    # TODO more extended PATH handling

    # design_folders is a list of folders with actual design files
    design_folders = get_design_folders(entries)
    design_root = get_design_root_folder(design_folders)
    design_subtrees = get_design_subtrees(design_folders)
    for subtree in design_subtrees:
        # TODO check PATH handling in next line! relpath or abspath depending ...
        # TODO check PATH handling in check_and_create_linked_folder!
        check_and_create_linked_folder(project_creator, os.path.relpath(subtree, design_root))

    abs_to_rel_file = {}
    for path, library in entries.items():
        file_ext = str(os.path.splitext(path)[1]).lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        # TODO following code copied from customer project
        # TODO relpath: base is PWD?
        my_rel_file = os.path.relpath(path)
        # my_folder = os.path.dirname(my_rel_file)
        # if my_folder not in design_folders:
        #     design_folders.append(my_folder)
        my_rel_file = str(posixpath(my_rel_file))
        abs_to_rel_file[path] = my_rel_file

    if ArgsAndFileParser.get_mapping_option() == 'file':
        create_library_mapping_per_file(project_creator, entries, abs_to_rel_file)
    else:
        create_library_mapping_folders(project_creator, entries, abs_to_rel_file)

    return has_vhdl, has_verilog


def create_project_in_place(project_creator, entries):
    # In place means that we assume that (most) design files are in the "destination" tree.
    # TODO handle files not in the destination tree: link in some way (future work, out of scope of ticket #23)
    mapping_style = ArgsAndFileParser.get_mapping_option()
    map_folders = (mapping_style == 'folder')
    destination_folder = ArgsAndFileParser.get_destination_folder()
    file_base_path = os.getcwd() # default base my_file, may be overridden
    design_folders = []
    folder_mapping = dict()

    has_vhdl = False
    has_verilog = False
    for my_file, my_library in entries.items():
        if not PurePath(my_file).is_relative_to(destination_folder):
            raise ValueError(f'*In-place layout* file {my_file} is not in destination folder {destination_folder}')
        file_ext = str(os.path.splitext(my_file)[1]).lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        local_file = os.path.relpath(my_file, destination_folder)
        if not map_folders:
            add_library_mapping(project_creator, local_file, my_library, os.path.join('PROJECT_LOC', local_file))

    if map_folders:
        create_library_mapping_folders(project_creator, entries, None)

    return has_vhdl, has_verilog


def add_library_mapping(project_creator, project_file, libraries, filesystem_file):
    if isinstance(libraries, list):
        first_library = True
        for library in libraries:
            if first_library:
                project_creator.add_mapping(project_file, library)
                first_library = False
            else:
                file_parts = os.path.splitext(project_file)
                new_file = f'{file_parts[0]}_{library}{file_parts[1]}'
                project_creator.add_link(new_file, get_rel_or_abs_path(filesystem_file, project_root))
                project_creator.add_mapping(new_file, library)
    else:
        project_creator.add_mapping(project_file, libraries)
