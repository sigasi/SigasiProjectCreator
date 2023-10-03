# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import pathlib

from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from pathlib import Path
from SigasiProjectCreator import CsvParser
from SigasiProjectCreator.DotF import DotFfileParser
from SigasiProjectCreator.convertHdpProjectToSigasiProject import parse_hdp_file
from SigasiProjectCreator.convertXilinxISEToSigasiProject import parse_xilinx_file


# def running_in_cyg_win():
#     return platform.system().startswith("CYGWIN")


# def convert_cygwin_path(cygwin_path):
#     cygwin_process = subprocess.Popen(['/usr/bin/cygpath', '--windows', cygwin_path], stdout=subprocess.PIPE)
#     cygwin_location = cygwin_process.communicate()[0].rstrip()
#     return posixpath(cygwin_location)


def get_rel_or_abs_path(my_path: pathlib.Path, destination: pathlib.Path):
    # This function accepts an absolute path and checks whether a relative path is expected.
    # If a relative path is expected, the relative path is returned.
    destination_path = pathlib.Path(destination).absolute()
    if my_path.is_relative_to(destination_path) or ArgsAndFileParser.get_use_relative_path(my_path):
        # return input_path.relative_to(destination_path)
        return Path(os.path.relpath(my_path, destination))
    return my_path.absolute()


virtual_folders = [pathlib.Path('Common Libraries')]


def check_and_create_virtual_folder(project_creator, file_name: pathlib.Path):
    if not isinstance(file_name, pathlib.Path):
        raise TypeError
    filepath = file_name.parent
    if filepath not in virtual_folders:
        new_folders = []
        while filepath and (str(filepath) != '.') and (filepath not in virtual_folders):
            new_folders.insert(0, filepath)
            filepath = filepath.parent
        for new_path in new_folders:
            virtual_folders.append(new_path)
            project_creator.add_link(new_path, None, True)


def check_and_create_linked_folder(project_creator, folder_name: pathlib.Path, folder_path: pathlib.Path):
    if not (isinstance(folder_name, pathlib.Path) and isinstance(folder_path, pathlib.Path)):
        raise TypeError
    # TODO future work: map some folders into Common Libraries
    # if folder_name.startswith('dependencies'):
    #     virtual_path_name = posixpath(os.path.join('Common Libraries', folder_name))
    check_and_create_virtual_folder(project_creator, folder_name)
    project_creator.add_link(folder_name, get_rel_or_abs_path(folder_path, project_root), True)


def uniquify_project_path(path: pathlib.Path, existing_path_list):
    if path not in existing_path_list:
        return path
    seq = 1
    new_path = path
    path_base = path.stem
    path_ext = path.suffix
    while new_path in existing_path_list and seq < 1000:
        new_path = Path(f'{path_base}_{seq}{path_ext}')
        seq += 1
    assert new_path not in existing_path_list, f'*ERROR* Cannot uniquify {path}'
    return new_path


def set_project_root(destination):
    global project_root
    project_root = pathlib.Path(destination).absolute()


def parse_and_create_project():
    (project_name, _, destination, parser_output) = ArgsAndFileParser.parse_input_file(
        get_parser_for_type(ArgsAndFileParser.get_input_format()))

    verilog_includes = None
    verilog_defines = None

    set_project_root(destination)

    if not isinstance(parser_output, dict):
        verilog_includes = parser_output.includes
        verilog_defines = parser_output.defines
        entries = parser_output.library_mapping
        if verilog_includes is not None and len(verilog_includes) > 0:
            verilog_includes = [pathlib.Path(include_path) for include_path in verilog_includes]
            print("Includes: " + str(verilog_includes))
        if verilog_defines is not None and len(verilog_defines) > 0:
            print("Defines: " + str(verilog_defines))
    else:
        entries = parser_output

    new_entries = dict()
    for path, library in entries.items():
        new_entries[pathlib.Path(path)] = library
    entries = new_entries
    print("Library mapping: " + str(entries))

    if not ArgsAndFileParser.get_skip_check_exists():
        for file in entries.keys():
            assert file.is_file(), f'*ERROR* file {file} does not exist'

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
    elif project_layout == 'in-place':
        (has_vhdl, has_verilog) = create_project_in_place(sigasi_project_file_creator, entries)
    else:
        print(f'*ERROR* Unsupported project layout {project_layout}')
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
            assert ArgsAndFileParser.get_skip_check_exists() or \
                   include_folder.is_dir(), f'*ERROR* include folder does not exist: {include_folder} '
            local_include_folder = None
            if not include_folder.is_relative_to(project_root):
                if not has_includes_folder:
                    sigasi_project_file_creator.add_link('include_folders', None, True)
                    has_includes_folder = True
                local_path = Path(include_folder.name)
                local_path = uniquify_project_path(local_path, linked_include_folders)
                linked_include_folders.append(local_path)
                local_include_folder = Path('include_folders').joinpath(local_path)
                sigasi_project_file_creator.add_link(local_include_folder,
                                                     get_rel_or_abs_path(include_folder, project_root), True)
            else:
                local_include_folder = pathlib.Path(os.path.relpath(include_folder, project_root))
            sigasi_project_file_creator.add_verilog_include(local_include_folder)

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
        file_ext = my_file.suffix.lower()
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


linked_paths_simulator_layout = []


def create_project_simulator_add_single(project_creator, my_library, libraries, my_file):
    global linked_paths_simulator_layout
    if my_library not in libraries:
        project_creator.add_link(my_library, None, True)  # virtual folder named after the library
        project_creator.add_mapping(my_library, my_library)
        libraries.append(my_library)
    linked_path = uniquify_project_path(pathlib.Path(my_library).joinpath(my_file.name), linked_paths_simulator_layout)
    linked_paths_simulator_layout.append(linked_path)
    project_creator.add_link(linked_path, get_rel_or_abs_path(my_file, project_root), False)


def create_project_links_flat(project_creator, entries):
    has_vhdl = False
    has_verilog = False
    linked_paths = []
    for path, library in entries.items():
        assert not pathlib.Path(path).is_relative_to(project_root), \
            f'*ERROR* linked project: destination folder {project_root} may not contain design file {path}'
        file_ext = path.suffix.lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        ref_path = None
        if isinstance(library, dict):
            ref_path = library['reference']
            library = library['library']
        linked_path = uniquify_project_path(path.name, linked_paths)
        linked_paths.append(linked_path)
        project_creator.add_link(linked_path, get_rel_or_abs_path(path, project_root), False)
        project_creator.add_mapping(linked_path, library)
    return has_vhdl, has_verilog


def get_design_folders(entries) -> list[pathlib.Path]:
    folders = []
    for path, library in entries.items():
        folder = path.parent
        if folder not in folders:
            folders.append(folder)
    folders.sort()
    return folders


def get_design_root_folder(folder_list) -> pathlib.Path:
    return pathlib.Path(os.path.commonpath(folder_list))


def get_design_subtrees(folder_list):
    # Design subtrees are folders which contain design files, while none of their parent folders contain design files
    folder_list.sort()
    design_root_folders = []
    current_folder = None
    for my_folder in folder_list:
        if (current_folder is None) or (not my_folder.is_relative_to(current_folder)):
            design_root_folders.append(my_folder)
            current_folder = my_folder
    return design_root_folders


def create_project_links_tree(project_creator, entries):
    has_vhdl = False
    has_verilog = False

    design_folders = get_design_folders(entries)
    design_root = get_design_root_folder(design_folders)
    abs_to_rel_file = {}

    for path, library in entries.items():
        assert not pathlib.Path(path).is_relative_to(project_root), \
            f'*ERROR* linked project: destination folder {project_root} may not contain design file {path}'
        file_ext = path.suffix.lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True

        rel_path = path.relative_to(design_root)
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
    print(f'\n\n*create_library_mapping_folders* design folders: {design_folders}')
    design_root = get_design_root_folder(design_folders)
    print(f'*create_library_mapping_folders* design root: {design_root}')
    for design_folder in design_folders:
        print(f'*create_library_mapping_folders* current folder: {design_folder}')
        folder_library = None
        folder_list = os.listdir(design_folder)
        design_folder_relpath = pathlib.Path(os.path.relpath(design_folder, design_root))
        for folder_item in folder_list:
            folder_item_with_path = design_folder.joinpath(folder_item)
            if folder_item_with_path.is_dir():
                local_folder = pathlib.Path(os.path.relpath(folder_item_with_path, design_root))
                project_creator.unmap(local_folder)
            elif folder_item_with_path.is_file():
                if folder_item_with_path.suffix in ['.vhd', '.vhdl', '.v', '.sv']:
                    file_with_path = design_folder.joinpath(folder_item)
                    file_with_path_relpath = pathlib.Path(os.path.relpath(file_with_path, design_root))
                    if file_with_path in entries:
                        my_lib = entries[file_with_path]
                        if isinstance(my_lib, list):
                            file_is_mapped = False
                            if folder_library is not None and folder_library in my_lib:
                                file_is_mapped = True
                            for single_lib in my_lib:
                                if folder_library is None:
                                    # if parent folder is mapped to this library, clear mapping of the current folder
                                    design_parent_folder = design_folder.parent
                                    parent_lib = project_creator.get_mapping(design_parent_folder)
                                    if parent_lib is None or parent_lib != single_lib:
                                        project_creator.add_mapping(design_folder_relpath, single_lib)
                                    else:
                                        project_creator.remove_mapping(design_folder_relpath)
                                    folder_library = single_lib
                                    file_is_mapped = True
                                elif single_lib != folder_library:
                                    if file_is_mapped:
                                        new_file = f'{file_with_path_relpath.stem}_{single_lib}'\
                                                f'{file_with_path_relpath.suffix} '
                                        project_creator.add_link(new_file,
                                                                 get_rel_or_abs_path(file_with_path, project_root))
                                        project_creator.add_mapping(new_file, single_lib)
                                    else:
                                        project_creator.add_mapping(file_with_path_relpath, single_lib)
                                    file_is_mapped = True
                        else:
                            if folder_library is None:
                                # if parent folder is mapped to this library, clear the mapping of the current folder
                                parent_lib = project_creator.get_mapping(design_folder.parent)
                                if parent_lib is None or parent_lib != my_lib:
                                    project_creator.add_mapping(design_folder_relpath, my_lib)
                                else:
                                    project_creator.remove_mapping(design_folder_relpath)
                                folder_library = my_lib
                            elif folder_library != my_lib:
                                project_creator.add_mapping(file_with_path_relpath, my_lib)
                    elif ArgsAndFileParser.get_layout_option() != 'linked-files-tree':
                        project_creator.unmap(file_with_path_relpath)


def create_library_mapping_per_file(project_creator, mapping_entries, filesystem_to_project_mapping):
    for item, library in mapping_entries.items():
        add_library_mapping(project_creator, filesystem_to_project_mapping[item], library, item)


def create_project_links_folders(project_creator, entries):
    has_vhdl = False
    has_verilog = False

    # design_folders is a list of folders with actual design files
    design_folders = get_design_folders(entries)
    design_root = get_design_root_folder(design_folders)
    design_subtrees = get_design_subtrees(design_folders)
    for subtree in design_subtrees:
        check_and_create_linked_folder(project_creator, pathlib.Path(os.path.relpath(subtree, design_root)), subtree)

    abs_to_rel_file = {}
    for path, library in entries.items():
        assert not path.is_relative_to(project_root), \
            f'*ERROR* linked project: destination folder {project_root} may not contain design file {path}'
        file_ext = path.suffix.lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        abs_to_rel_file[path] = pathlib.Path(os.path.relpath(path))

    if ArgsAndFileParser.get_mapping_option() == 'file':
        create_library_mapping_per_file(project_creator, entries, abs_to_rel_file)
    else:
        create_library_mapping_folders(project_creator, entries, abs_to_rel_file)

    return has_vhdl, has_verilog


def create_project_in_place(project_creator, entries):
    # In place means that we assume that the design files are in the "destination" tree.
    # TODO future work: handle files not in the destination tree: link in some way (out of scope of ticket #23)
    mapping_style = ArgsAndFileParser.get_mapping_option()
    map_folders = (mapping_style == 'folder')
    destination_folder = ArgsAndFileParser.get_destination_folder()

    has_vhdl = False
    has_verilog = False
    for my_file, my_library in entries.items():
        if not my_file.is_relative_to(destination_folder):
            raise ValueError(f'*In-place layout* file {my_file} is not in destination folder {destination_folder}')
        file_ext = my_file.suffix.lower()
        if file_ext in ['.vhd', '.vhdl']:
            has_vhdl = True
        elif file_ext in ['.v', '.sv']:
            has_verilog = True
        local_file = my_file.relative_to(destination_folder)
        if not map_folders:
            add_library_mapping(project_creator, local_file, my_library, local_file)

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


def get_parser_for_type(input_type):
    print(f'*get_parser_for_type* {input_type}')
    if input_type == 'dotf':
        return DotFfileParser.parse_file
    if input_type == 'csv':
        return CsvParser.parse_file
    if input_type == 'hdp':
        return parse_hdp_file
    if input_type == 'filelist':
        return None
    if input_type == 'xise':
        return parse_xilinx_file
