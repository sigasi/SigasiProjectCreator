import pathlib
import shutil
import unittest
import os

from SigasiProjectCreator import CsvParser
from SigasiProjectCreator.ProjectOptions import ProjectOptions
from SigasiProjectCreator.ConverterHelper import get_rel_or_abs_path, check_and_create_virtual_folder, \
    check_and_create_linked_folder, set_project_root, reset_for_unit_testing, uniquify_project_path, \
    create_project_simulator, create_project_links_flat, get_design_folders, get_design_root_folder, \
    get_design_subtrees, create_project_links_tree, get_parser_for_type, create_project_links_folders, \
    create_project_in_place, create_library_mapping_folders, parse_and_create_project
from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator.DotF import DotFfileParser
from SigasiProjectCreator.convertHdpProjectToSigasiProject import parse_hdp_file
from SigasiProjectCreator.convertXilinxISEToSigasiProject import parse_xilinx_file


class ConverterHelperTest(unittest.TestCase):
    def setUp(self):
        self.args_parser = ProjectOptions()
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
        self.args_parser.parse_args(command_line_options)
        self.project_creator = SigasiProjectCreator('the_project')
        reset_for_unit_testing()

    def test_abs_or_rel_path_rel_in(self):
        destination_folder = pathlib.Path('foo').absolute()
        design_path = pathlib.Path('tests/test-files/tutorial/testbench.vhd')
        result = get_rel_or_abs_path(design_path, destination_folder)
        self.assertEqual(result, design_path)

    def test_abs_or_rel_path_abs(self):
        destination_folder = pathlib.Path('foo').absolute()
        design_path = pathlib.Path('tests/test-files/tutorial/testbench.vhd').absolute()
        result = get_rel_or_abs_path(design_path, destination_folder)
        self.assertEqual(result, design_path.absolute())

    def test_abs_or_rel_path_rel(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv',
                                '--rel-path', 'fooh',
                                '--rel-path', 'tests/test-files']
        self.args_parser.parse_args(command_line_options)
        destination_folder = pathlib.Path('foo').absolute()
        design_path = pathlib.Path('tests/test-files/tutorial/testbench.vhd').absolute()
        self.assertTrue(ProjectOptions.get_use_relative_path(design_path))
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
        expected = [[pathlib.Path('bar.v'), '/my/path/foo/bar.v', False, True],
                    [pathlib.Path('bar.vhd'), '/my/path/foo/bar.vhd', False, True],
                    [pathlib.Path('bar_1.vhd'), '/my/path/foo1/bar.vhd', False, True],
                    [pathlib.Path('bar_2.vhd'), '/my/path/foo2/bar.vhd', False, True],
                    [pathlib.Path('bar_3.vhd'), '/my/path/foo3/bar.vhd', False, True],
                    [pathlib.Path('bar.vhdl'), '/my/path/foo/bar.vhdl', False, True],
                    [pathlib.Path('bahr.vhdl'), '/my/path/foo/bahr.vhdl', False, True],
                    [pathlib.Path('bahr_1.vhdl'), '/my/path/foo/bahr.vhdl', False, True]
                    ]
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

    def test_create_project_links_tree(self):
        self.maxDiff = None
        entries = {
            pathlib.Path('/my/path/foo/bar.v'): 'work',
            pathlib.Path('/my/path/foo/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/bars.vhd'): 'labor',
            pathlib.Path('/my/path/foo2/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/two/bar.vhdl'): 'work',
            pathlib.Path('/my/path/foo/bahr.vhdl'): ['work', 'travail']
        }
        has_vhdl, has_verilog = create_project_links_tree(self.project_creator, entries)
        self.assertTrue(has_vhdl)
        self.assertTrue(has_verilog)
        file_mapping = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        print(f'**file mapping** {file_mapping}')
        expected = [[pathlib.Path('foo'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/bar.v'), '/my/path/foo/bar.v', False, True],
                    [pathlib.Path('foo/bar.vhd'), '/my/path/foo/bar.vhd', False, True],
                    [pathlib.Path('foo/one'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/one/bar.vhd'), '/my/path/foo/one/bar.vhd', False, True],
                    [pathlib.Path('foo/one/bars.vhd'), '/my/path/foo/one/bars.vhd', False, True],
                    [pathlib.Path('foo2'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo2/bar.vhd'), '/my/path/foo2/bar.vhd', False, True],
                    [pathlib.Path('foo/one/two'), 'virtual:/virtual', True, False],
                    [pathlib.Path('foo/one/two/bar.vhdl'), '/my/path/foo/one/two/bar.vhdl', False, True],
                    [pathlib.Path('foo/bahr.vhdl'), '/my/path/foo/bahr.vhdl', False, True],
                    [pathlib.Path('foo/bahr_travail.vhdl'), '/my/path/foo/bahr.vhdl', False, True]
                    ]
        print(f'##file mapping## {expected}')
        self.assertEqual(file_mapping, expected)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'foo/bahr.vhdl': 'work',
            'foo/bahr_travail.vhdl': 'travail',
            'foo/bar.v': 'work',
            'foo/bar.vhd': 'work',
            'foo/one/two/bar.vhdl': 'work',
            'foo/one/bar.vhd': 'work',
            'foo/one/bars.vhd': 'labor',
            'foo2/bar.vhd': 'work'
        }
        self.assertEqual(lib_mapping, lib_expected)

    def test_create_project_links_folders(self):
        self.maxDiff = None
        base_path = pathlib.Path('test_create_project_in_folders')
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', base_path.as_posix(),
                                '--skip-check-exists']
        self.args_parser.parse_args(command_line_options)
        entries = {
            pathlib.Path('/my/path/foo/bar.v'): 'work',
            pathlib.Path('/my/path/foo/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/bars.vhd'): 'labor',
            pathlib.Path('/my/path/foo2/bar.vhd'): 'work',
            pathlib.Path('/my/path/foo/one/two/bar.vhdl'): 'work',
            pathlib.Path('/my/path/foo/bahr.vhdl'): ['work', 'travail']
        }
        has_vhdl, has_verilog = create_project_links_folders(self.project_creator, entries)
        self.assertTrue(has_vhdl)
        self.assertTrue(has_verilog)
        file_mapping = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        print(f'**file mapping** {file_mapping}')
        expected = [[pathlib.Path('foo'), '/my/path/foo', True, True],
                    [pathlib.Path('foo2'), '/my/path/foo2', True, True],
                    [pathlib.Path('foo/bahr_travail.vhdl'), '/my/path/foo/bahr.vhdl', False, True]
                    ]
        print(f'##file mapping## {expected}')
        self.assertEqual(file_mapping, expected)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'foo/bahr.vhdl': 'work',
            'foo/bahr_travail.vhdl': 'travail',
            'foo/bar.v': 'work',
            'foo/bar.vhd': 'work',
            'foo/one/two/bar.vhdl': 'work',
            'foo/one/bar.vhd': 'work',
            'foo/one/bars.vhd': 'labor',
            'foo2/bar.vhd': 'work'
        }
        self.assertEqual(lib_mapping, lib_expected)

    # @unittest.skip  # Path handling not OK!
    def test_create_project_in_place(self):
        self.maxDiff = None
        base_path = pathlib.Path.cwd().joinpath('test_create_project_in_place')
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', base_path.as_posix(),
                                '--skip-check-exists']
        self.args_parser.parse_args(command_line_options)

        entries = {
            base_path.joinpath('foo/bar.v'): 'work',
            base_path.joinpath('foo/bar.vhd'): 'work',
            base_path.joinpath('foo/one/bar.vhd'): 'work',
            base_path.joinpath('foo/one/bars.vhd'): 'labor',
            base_path.joinpath('foo2/bar.vhd'): 'work',
            base_path.joinpath('foo/one/two/bar.vhdl'): 'work',
            base_path.joinpath('foo/bahr.vhdl'): ['work', 'travail']
        }
        has_vhdl, has_verilog = create_project_in_place(self.project_creator, entries)
        self.assertTrue(has_vhdl)
        self.assertTrue(has_verilog)
        file_mapping = self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        print(f'**file mapping** {file_mapping}')
        expected = [
            [pathlib.Path('foo/bahr_travail.vhdl'), pathlib.Path('foo/bahr.vhdl').as_posix(), False, True]
        ]
        print(f'##file mapping## {expected}')
        self.assertEqual(file_mapping, expected)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'foo/bahr.vhdl': 'work',
            'foo/bahr_travail.vhdl': 'travail',
            'foo/bar.v': 'work',
            'foo/bar.vhd': 'work',
            'foo/one/two/bar.vhdl': 'work',
            'foo/one/bar.vhd': 'work',
            'foo/one/bars.vhd': 'labor',
            'foo2/bar.vhd': 'work'
        }
        self.assertEqual(lib_mapping, lib_expected)

    def test_get_parser_for_type(self):
        self.assertEqual(get_parser_for_type('dotf'), DotFfileParser.parse_file)
        self.assertEqual(get_parser_for_type('csv'), CsvParser.parse_file)
        self.assertEqual(get_parser_for_type('hdp'), parse_hdp_file)
        self.assertEqual(get_parser_for_type('xise'), parse_xilinx_file)
        self.assertIsNone(get_parser_for_type('filelist'))

    @staticmethod
    def set_up_simple_project(base_path: pathlib.Path):
        base_path.mkdir()
        base_path.joinpath('foo').mkdir()
        base_path.joinpath('bar').mkdir()
        base_path.joinpath('foo/one').mkdir()
        base_path.joinpath('foo/one/two').mkdir()
        base_path.joinpath('foo/bhar.v').touch()
        base_path.joinpath('foo/bhar.vhd').touch()
        base_path.joinpath('foo/bhar.v').touch()
        base_path.joinpath('foo/barh.v').touch()
        base_path.joinpath('foo/one/bar.v').touch()
        base_path.joinpath('foo/one/two/bar.v').touch()
        base_path.joinpath('bar/foo.vhdl').touch()

    def test_create_library_mapping_folders(self):
        base_path = pathlib.Path.cwd().joinpath('test_create_library_mapping_folders')
        shutil.rmtree(base_path, True)
        self.set_up_simple_project(base_path)
        entries = {
            base_path.joinpath('foo/bhar.v'): 'main',
            base_path.joinpath('foo/bhar.vhd'): 'main',
            base_path.joinpath('foo/barh.v'): 'other',
            base_path.joinpath('foo/one/two/bar.v'): 'main',
            base_path.joinpath('bar/foo.vhdl'): ['main', 'some']
        }
        create_library_mapping_folders(self.project_creator, entries, None)
        lib_mapping = self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            'foo': 'main',
            'foo/barh.v': 'other',
            'foo/one': 'not mapped',
            'foo/one/two': 'main',
            'bar': 'main',
            'bar/foo_some.vhdl': 'some'
        }
        self.assertEqual(lib_mapping, lib_expected)

    @staticmethod
    def setup_fake_uvm_folder(uvm_path: pathlib.Path):
        if uvm_path.exists():
            return
        uvm_path.mkdir()
        uvm_path.joinpath('src').mkdir()
        uvm_path.joinpath('src/uvm_pkg.sv').touch()
        uvm_path.joinpath('src/uvm_macros.svh').touch()

    def test_parse_and_create_project(self):
        self.maxDiff = None
        base_path = pathlib.Path.cwd()
        uvm_path = base_path.joinpath('uvm').absolute()
        self.setup_fake_uvm_folder(uvm_path)
        command_line_options = ['the_project', 'tests/test-files/dotFparser/features.f', base_path.as_posix(),
                                '--skip-check-exists', '--layout', 'in-place', '-f', '--uvm', str(uvm_path),
                                '--uvmlib', 'uvm']
        self.args_parser.parse_args(command_line_options)
        os.environ['SIM'] = 'simulator'
        os.environ['FUBAR_HOME'] = 'phoo/barh/ome'
        (self.project_creator, verilog_defines) = parse_and_create_project()
        del os.environ['SIM']
        del os.environ['FUBAR_HOME']
        file_mapping = \
            self.project_creator._SigasiProjectCreator__projectFileCreator._ProjectFileCreator__links
        expected = [
            ['include_folders', 'virtual:/virtual', True, False],
            [pathlib.Path('include_folders/verilog'), '/somelib/verilog', True, True],
            [pathlib.Path('Common Libraries/uvm'), '/home/wmeeus/git/SigasiProjectCreator_github/uvm/src', True, True],
            ['Common Libraries', 'virtual:/virtual', True, False],
            ['Common Libraries/IEEE', 'sigasiresource:/vhdl/2008/IEEE', True, False],
            ['Common Libraries/IEEE Synopsys', 'sigasiresource:/vhdl/2008/IEEE%20Synopsys', True, False],
            ['Common Libraries/STD', 'sigasiresource:/vhdl/2008/STD', True, False]
        ]
        self.assertEqual(file_mapping, expected)
        lib_mapping = \
            self.project_creator._SigasiProjectCreator__libraryMappingFileCreator._LibraryMappingFileCreator__entries
        lib_expected = {
            '/': 'not mapped',
            '': 'not mapped',
            'Common Libraries': 'not mapped',
            'Common Libraries/IEEE': 'ieee',
            'Common Libraries/IEEE Synopsys': 'ieee',
            'Common Libraries/STD': 'std',
            'Common Libraries/uvm/uvm_pkg.sv': 'uvm',
            'ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_conv.v': 'foolib',
            'ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b_downsizer.v': 'foolib',
            'ipstatic/some_protocol_converter_v2_1/hdl/verilog/foo_b2s.v': 'b2s',
            'ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_some_protocol_converter.v': 'work',
            'bd/design_1/ip/design_1_auto_pc_0/simulator/design_1_auto_pc_0.v': 'work',
            'bd/design_1/hdl/design_all.vhd': 'work',
            'tests/test-files/dotFparser/glbl.v': 'work'
        }
        self.assertEqual(lib_mapping, lib_expected)
        self.assertTrue(base_path.joinpath('.project').is_file())
        self.assertTrue(base_path.joinpath('.library_mapping.xml').is_file())
        self.assertTrue(base_path.joinpath('.settings').is_dir())
        expected_includes = [
            pathlib.Path('tests/rtl/phoo/barh/ome/pkg'),
            pathlib.Path('tests/bench/verilog'),
            pathlib.Path('tests/verilog'),
            pathlib.Path('include_folders/verilog'),
            pathlib.Path('Common Libraries/uvm')
        ]
        expected_includes.sort()
        actual_includes = self.project_creator.verilog_includes
        actual_includes.sort()
        print(f'**includes** {expected_includes}')
        print(f'##includes## {actual_includes}')
        self.assertEqual(actual_includes, expected_includes)
        expected_defines = [
            'SIGASI="yes"',
            'FOOOOOOOH'
        ]
        self.assertEqual(verilog_defines, expected_defines)


if __name__ == '__main__':
    unittest.main()
