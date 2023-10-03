import pathlib
import unittest

from SigasiProjectCreator import VhdlVersion, VerilogVersion, CsvParser
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser


class MyTestCase(unittest.TestCase):
    def test_dotf_file(self):
        self.assertEqual(ArgsAndFileParser.get_file_type('foo/bahr/hello.f'), 'dotf')

    def test_csv_file(self):
        self.assertEqual(ArgsAndFileParser.get_file_type('foo/rab/hello.csV'), 'csv')

    def test_hdp_file(self):
        self.assertEqual(ArgsAndFileParser.get_file_type('foo/bahr/hello-oh.hdp'), 'hdp')

    def test_file_list(self):
        self.assertEqual(ArgsAndFileParser.get_file_type('foo/bahr/hello.v'), 'filelist')

    def test_constructor(self):
        args_parser = ArgsAndFileParser()
        self.assertTrue(isinstance(args_parser, ArgsAndFileParser))

    def test_parser_minimal(self):
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(['my_project', 'tests/test-files/compilation_order.csv'])
        self.assertEqual(args_parser.get_input_format(), 'csv')
        self.assertEqual(args_parser.get_layout_option(), 'in-place')
        self.assertEqual(args_parser.get_destination_folder(), pathlib.Path.cwd())
        self.assertFalse(args_parser.get_enable_vhdl())
        self.assertFalse(args_parser.get_enable_verilog())
        self.assertFalse(args_parser.get_enable_vunit())
        self.assertEqual(args_parser.get_encoding(), 'UTF-8')
        self.assertEqual(args_parser.get_vhdl_version(), VhdlVersion.TWENTY_O_EIGHT)
        self.assertEqual(args_parser.get_verilog_version(), str(VerilogVersion.TWENTY_O_FIVE))
        self.assertFalse(args_parser.get_force_overwrite())
        self.assertFalse(args_parser.get_skip_check_exists())
        self.assertFalse(args_parser.get_use_relative_path(pathlib.Path.cwd()))

    def test_parser_many_options(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', 'tests',
                                '--layout', 'simulator',
                                # '--uvm', 'src',
                                '--use-uvm-home',
                                '--uvmlib', 'uvm_lib',
                                '--format', 'csv',
                                '--mapping', 'folder',
                                '--enable-vhdl',
                                '--vhdl-version', '2002',
                                '--enable-verilog',
                                '--verilog-as-sv',
                                '--enable-vunit',
                                '--work', 'worklib',
                                '--skip-check-exists',
                                '--encoding', 'UTF-9',
                                '--force',
                                '--rel-path', 'src'
                                ]
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        self.assertEqual(args_parser.get_input_format(), 'csv')
        self.assertEqual(args_parser.get_layout_option(), 'simulator')
        self.assertEqual(args_parser.get_destination_folder(), pathlib.Path('tests').absolute())
        self.assertTrue(args_parser.get_enable_vhdl())
        self.assertTrue(args_parser.get_enable_verilog())
        self.assertTrue(args_parser.get_enable_vunit())
        self.assertEqual(args_parser.get_encoding(), 'UTF-9')
        self.assertEqual(args_parser.get_vhdl_version(), VhdlVersion.TWENTY_O_TWO)
        self.assertEqual(args_parser.get_verilog_version(), str(VerilogVersion.TWENTY_TWELVE))
        self.assertTrue(args_parser.get_force_overwrite())
        self.assertTrue(args_parser.get_skip_check_exists())
        self.assertFalse(args_parser.get_use_relative_path(pathlib.Path.cwd()))
        self.assertTrue(args_parser.get_use_relative_path(pathlib.Path('src').absolute()))
        uvm_home, uvm_lib = args_parser.get_uvm_option()
        self.assertEqual(uvm_home, pathlib.Path('ENV-UVM_HOME'))
        self.assertEqual(uvm_lib, 'uvm_lib')
        self.assertEqual(args_parser.get_mapping_option(), 'folder')

    def test_parser_multiple_input_files(self):
        command_line_options = ['the_project',
                                'tests/test-files/dotFparser/continuation.f,tests/test-files/dotFparser/filelist.f']
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        self.assertEqual(args_parser.get_input_format(), 'dotf')

    def test_parser_nonexistent_single_input_file(self):
        command_line_options = ['the_project',
                                'notexist.f']
        args_parser = ArgsAndFileParser()
        with self.assertRaises(SystemExit) as context:
            args_parser.parse_args(command_line_options)
        self.assertEqual('2', str(context.exception))  # exit code 2 from argparse error handling

    def test_parser_nonexistent_multiple_input_files(self):
        command_line_options = ['the_project',
                                'continuation.f,tests/test-files/dotFparser/filelist.f']
        args_parser = ArgsAndFileParser()
        with self.assertRaises(SystemExit) as context:
            args_parser.parse_args(command_line_options)
        self.assertEqual('2', str(context.exception))  # exit code 2 from argparse error handling

    def test_parser_mixed_input_types(self):
        command_line_options = ['the_project',
                                'tests/test-files/tree/compilation_order.csv,tests/test-files/dotFparser/filelist.f']
        args_parser = ArgsAndFileParser()
        with self.assertRaises(SystemExit) as context:
            args_parser.parse_args(command_line_options)
        self.assertEqual('2', str(context.exception))  # exit code 2 from argparse error handling

    def test_parser_cant_create_destination_folder(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', 'phoo/bahr']
        args_parser = ArgsAndFileParser()
        with self.assertRaises(AssertionError) as context:
            args_parser.parse_args(command_line_options)
        self.assertEqual('*ERROR* Cannot create project folder phoo/bahr, parent is not an existing folder',
                         str(context.exception))

    def test_parser_do_create_destination_folder(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', 'phoobahr']
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        destination_folder = pathlib.Path('phoobahr')
        self.assertTrue(destination_folder.is_dir())
        destination_folder.rmdir()

    def test_parser_parse_file(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        project_name, input_file, dest_folder, project_entries = args_parser.parse_input_file(CsvParser.parse_file)
        self.assertEqual(project_name, 'the_project')
        self.assertEqual(input_file, 'tests/test-files/tree/compilation_order.csv')
        self.assertEqual(dest_folder, pathlib.Path.cwd().absolute())
        self.assertTrue(isinstance(project_entries, dict))

    def test_parser_parse_list(self):
        command_line_options = ['the_project', 'tests/test-files/tutorial/clock_generator.vhd,tests/test-files/tutorial/dut.vhd']
        args_parser = ArgsAndFileParser()
        args_parser.parse_args(command_line_options)
        project_name, input_file, dest_folder, project_entries = args_parser.parse_input_file(None)
        self.assertEqual(project_name, 'the_project')
        self.assertTrue(input_file is None)
        self.assertEqual(dest_folder, pathlib.Path.cwd().absolute())
        self.assertTrue(isinstance(project_entries, dict))


if __name__ == '__main__':
    unittest.main()
