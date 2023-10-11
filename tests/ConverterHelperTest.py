import pathlib
import unittest
import os

from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from SigasiProjectCreator.ConverterHelper import get_rel_or_abs_path, check_and_create_virtual_folder, \
    check_and_create_linked_folder, set_project_root, reset_for_unit_testing, uniquify_project_path
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
        print(f'result is {result}')
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


if __name__ == '__main__':
    unittest.main()
