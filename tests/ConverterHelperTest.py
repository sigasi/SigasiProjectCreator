import pathlib
import unittest
import os

from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from SigasiProjectCreator.ConverterHelper import get_rel_or_abs_path, check_and_create_virtual_folder, \
    check_and_create_linked_folder, set_project_root, reset_for_unit_testing, uniquify_project_path, \
    create_project_simulator, create_project_links_flat, get_design_folders, get_design_root_folder, get_design_subtrees
from SigasiProjectCreator.Creator import SigasiProjectCreator


class ConverterHelperTest(unittest.TestCase):
    def setUp(self):
        self.args_parser = ArgsAndFileParser()
        self.project_creator = SigasiProjectCreator('the_project')
        reset_for_unit_testing()

    def test_abs_or_rel_path_abs(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        destination_folder = pathlib.Path('foo').absolute()
        design_path = pathlib.Path('tests/test-files/tutorial/testbench.vhd')
        result = get_rel_or_abs_path(design_path, destination_folder)
        self.assertEqual(result, design_path.absolute())

    def test_abs_or_rel_path_rel(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv',
                                '--rel-path', 'fooh',
                                '--rel-path', 'tests/test-files']
        self.args_parser.parse_args(command_line_options)
        destination_folder = pathlib.Path('foo').absolute()
        design_path = pathlib.Path('tests/test-files/tutorial/testbench.vhd')
        self.assertTrue(ArgsAndFileParser.get_use_relative_path(design_path))
        result = get_rel_or_abs_path(design_path, destination_folder)
        self.assertEqual(result, pathlib.Path(os.path.relpath(design_path, destination_folder)))

    def test_check_and_create_virtual_folder(self):
        result = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        self.assertEqual(result, [])
        check_and_create_virtual_folder(self.project_creator, pathlib.Path('foo/bar/file.vhd'))
        result = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        expected = [[pathlib.Path('foo'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/bar'), 'virtual:/virtual', True, False]]
        self.assertEqual(result, expected)

    def test_check_and_create_linked_folder(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
        self.args_parser.parse_args(command_line_options)

        set_project_root('project_folder')
        check_and_create_linked_folder(self.project_creator, pathlib.Path('foo/bar/file.vhd'),
                                       pathlib.Path('/here/there'))
        result = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        expected = [[pathlib.Path('foo'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/bar'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/bar/file.vhd'), '/here/there', True, True]]
        self.assertEqual(result, expected)

    def test_uniquify_project_path_none(self):
        result = uniquify_project_path(pathlib.Path('/my/path/foo/bar.vhd'), None)
        self.assertEqual(result, pathlib.Path('/my/path/foo/bar.vhd'))

    def test_uniquify_project_path_empty_list(self):
        result = uniquify_project_path(pathlib.Path('/my/path/foo/bar.vhd'), [])
        self.assertEqual(result, pathlib.Path('/my/path/foo/bar.vhd'))

    def test_uniquify_project_path_not_in_list(self):
        path_list = [
            pathlib.Path('/my/path/foo/bar.v'),
            pathlib.Path('/my/path/foo/bar.vhdl')
        ]
        result = uniquify_project_path(pathlib.Path('/my/path/foo/bar.vhd'), path_list)
        self.assertEqual(result, pathlib.Path('/my/path/foo/bar.vhd'))

    def test_uniquify_project_path_in_list(self):
        path_list = [
            pathlib.Path('/my/path/foo/bar.v'),
            pathlib.Path('/my/path/foo/bar.vhd'),
            pathlib.Path('/my/path/foo/bar.vhdl')
        ]
        result = uniquify_project_path(pathlib.Path('/my/path/foo/bar.vhd'), path_list)
        self.assertEqual(result, pathlib.Path('/my/path/foo/bar_1.vhd'))

    def test_uniquify_project_path_in_list_multi(self):
        path_list = [
            pathlib.Path('/my/path/foo/bar.v'),
            pathlib.Path('/my/path/foo/bar.vhd'),
            pathlib.Path('/my/path/foo/bar_1.vhd'),
            pathlib.Path('/my/path/foo/bar_2.vhd'),
            pathlib.Path('/my/path/foo/bar_3.vhd'),
            pathlib.Path('/my/path/foo/bar.vhdl')
        ]
        result = uniquify_project_path(pathlib.Path('/my/path/foo/bar.vhd'), path_list)
        self.assertEqual(result, pathlib.Path('/my/path/foo/bar_4.vhd'))

    def test_create_project_simulator(self):
        self.maxDiff = None
        entries = {
            pathlib.Path('/my/path/foo/bar.v'): 'work',
            pathlib.Path('/my/path/foo/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo1/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo2/bar.vhd'): 'labor',
            pathlib.Path('/my/path/foo3/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/bar.vhdl'): 'work',
            pathlib.Path('/my/path/foo/bahr.vhdl'): ['work', 'travail']
        }
        has_vhdl, has_verilog = create_project_simulator(self.project_creator, entries)
        self.assertTrue(has_vhdl)
        self.assertTrue(has_verilog)
        file_mapping = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        expected = [['work', 'virtual:/virtual', True, False],
                    [pathlib.Path('work/bar.v'), '/my/path/foo/bar.v', False, True],
                    [pathlib.Path('work/bar.vhd'), '/my/path/foo/bar.vhd', False, True],
                    [pathlib.Path('work/bar_1.vhd'), '/my/path/foo1/bar.vhd', False, True],
                    ['labor', 'virtual:/virtual', True, False],
                    [pathlib.Path('labor/bar.vhd'), '/my/path/foo2/bar.vhd', False, True],
                    [pathlib.Path('work/bar_2.vhd'), '/my/path/foo3/bar.vhd', False, True],
                    [pathlib.Path('work/bar.vhdl'), '/my/path/foo/bar.vhdl', False, True],
                    [pathlib.Path('work/bahr.vhdl'), '/my/path/foo/bahr.vhdl', False, True],
                    ['travail', 'virtual:/virtual', True, False],
                    [pathlib.Path('travail/bahr.vhdl'), '/my/path/foo/bahr.vhdl', False, True]
                    ]
        self.assertEqual(file_mapping, expected)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'work': 'work',
            'labor': 'labor',
            'travail': 'travail'
        }
        self.assertEqual(lib_mapping, lib_expected)

    def test_create_project_links_flat(self):
        self.maxDiff = None
        entries = {
            pathlib.Path('/my/path/foo/bar.v'): 'work',
            pathlib.Path('/my/path/foo/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo1/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo2/bar.vhd'): 'labor',
            pathlib.Path('/my/path/foo3/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/bar.vhdl'): 'work',
            pathlib.Path('/my/path/foo/bahr.vhdl'): ['work', 'travail']
        }
        has_vhdl, has_verilog = create_project_links_flat(self.project_creator, entries)
        self.assertTrue(has_vhdl)
        self.assertTrue(has_verilog)
        file_mapping = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        print(f'**file mapping** {file_mapping}')
        expected = [[pathlib.Path('bar.v'), '/my/path/foo/bar.v', False, True],
                    [pathlib.Path('bar.vhd'), '/my/path/foo/bar.vhd', False, True],
                    [pathlib.Path('bar_1.vhd'), '/my/path/foo1/bar.vhd', False, True],
                    [pathlib.Path('bar_2.vhd'), '/my/path/foo2/bar.vhd', False, True],
                    [pathlib.Path('bar_3.vhd'), '/my/path/foo3/bar.vhd', False, True],
                    [pathlib.Path('bar.vhdl'), '/my/path/foo/bar.vhdl', False, True],
                    [pathlib.Path('bahr.vhdl'), '/my/path/foo/bahr.vhdl', False, True],
                    [pathlib.Path('bahr_1.vhdl'), '/my/path/foo/bahr.vhdl', False, True]
                    ]
        print(f'##file mapping## {expected}')
        self.assertEqual(file_mapping, expected)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'bahr.vhdl': 'work',
            'bahr_1.vhdl': 'travail',
            'bar.v': 'work',
            'bar.vhd': 'work',
            'bar.vhdl': 'work',
            'bar_1.vhd': 'work',
            'bar_2.vhd': 'labor',
            'bar_3.vhd': 'work'
        }
        self.assertEqual(lib_mapping, lib_expected)

    def test_get_design_folders(self):
        self.maxDiff = None
        entries = {
            pathlib.Path('/my/path/foo/bar.v'): 'work',
            pathlib.Path('/my/path/foo/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo1/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo2/bar.vhd'): 'labor',
            pathlib.Path('/my/path/foo3/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/bar.vhdl'): 'work',
            pathlib.Path('/my/path/foo/bahr.vhdl'): ['work', 'travail']
        }
        design_folders = get_design_folders(entries)
        expected_folders = [
            pathlib.Path('/my/path/foo'),
            pathlib.Path('/my/path/foo1'),
            pathlib.Path('/my/path/foo2'),
            pathlib.Path('/my/path/foo3')
        ]
        self.assertEqual(design_folders, expected_folders)

    def test_get_design_root_folder(self):
        design_folders = [
            pathlib.Path('/my/path/foo'),
            pathlib.Path('/my/path/brol/foo1'),
            pathlib.Path('/my/path/foo2'),
            pathlib.Path('/my/path/some/deeper/path/foo3')
        ]
        self.assertEqual(get_design_root_folder(design_folders), pathlib.Path('/my/path'))

    def test_get_design_subtrees(self):
        # Note: folder lists must be sorted!
        design_folders = [
            pathlib.Path('/my/path/brol/foo1'),
            pathlib.Path('/my/path/brol/foo1/foo2'),
            pathlib.Path('/my/path/foo'),
            pathlib.Path('/my/path/foo2'),
            pathlib.Path('/my/path/some/deeper/path/foo3')
        ]
        design_subtrees = get_design_subtrees(design_folders)
        expected_folders = [
            pathlib.Path('/my/path/brol/foo1'),
            pathlib.Path('/my/path/foo'),
            pathlib.Path('/my/path/foo2'),
            pathlib.Path('/my/path/some/deeper/path/foo3')
        ]
        self.assertEqual(design_subtrees, expected_folders)


if __name__ == '__main__':
    unittest.main()
