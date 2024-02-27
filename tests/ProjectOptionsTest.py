"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import pathlib
import unittest

from SigasiProjectCreator import VhdlVersion, VerilogVersion, CsvParser
from SigasiProjectCreator.ProjectOptions import ProjectOptions, get_file_type


class TestProjectOptions(unittest.TestCase):
    def test_dotf_file(self):
        self.assertEqual(get_file_type('foo/bahr/hello.f'), 'dotf')

    def test_csv_file(self):
        self.assertEqual(get_file_type('foo/rab/hello.csV'), 'csv')

    def test_hdp_file(self):
        self.assertEqual(get_file_type('foo/bahr/hello-oh.hdp'), 'hdp')

    def test_file_list(self):
        self.assertEqual(get_file_type('foo/bahr/hello.v'), 'filelist')

    def test_constructor(self):
        args_parser = ProjectOptions(['foo', 'tests/test-files/compilation_order.csv'])
        self.assertTrue(isinstance(args_parser, ProjectOptions))

    def test_parser_minimal(self):
        options = ProjectOptions(['my_project', 'tests/test-files/compilation_order.csv'])
        self.assertEqual(options.input_format, 'csv')
        self.assertEqual(options.layout, 'in-place')
        self.assertEqual(options.destination_folder, pathlib.Path.cwd())
        self.assertFalse(options.enable_vhdl)
        self.assertFalse(options.enable_verilog)
        self.assertFalse(options.enable_vunit)
        self.assertEqual(options.encoding, 'UTF-8')
        self.assertEqual(options.vhdl_version, VhdlVersion.TWENTY_O_EIGHT)
        self.assertEqual(options.verilog_version, str(VerilogVersion.TWENTY_O_FIVE))
        self.assertFalse(options.force_overwrite)
        self.assertFalse(options.skip_check_exists)
        self.assertFalse(options.use_relative_path(pathlib.Path.cwd()))

    def test_parser_many_options(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', '-d', 'tests',
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
        options = ProjectOptions(command_line_options)
        self.assertEqual(options.input_format, 'csv')
        self.assertEqual(options.layout, 'simulator')
        self.assertEqual(options.destination_folder, pathlib.Path('tests').absolute())
        self.assertTrue(options.enable_vhdl)
        self.assertTrue(options.enable_verilog)
        self.assertTrue(options.enable_vunit)
        self.assertEqual(options.encoding, 'UTF-9')
        self.assertEqual(options.vhdl_version, VhdlVersion.TWENTY_O_TWO)
        self.assertEqual(options.verilog_version, str(VerilogVersion.TWENTY_TWELVE))
        self.assertTrue(options.force_overwrite)
        self.assertTrue(options.skip_check_exists)
        self.assertFalse(options.use_relative_path(pathlib.Path.cwd()))
        self.assertTrue(options.use_relative_path(pathlib.Path('src').absolute()))
        self.assertEqual(options.uvm, pathlib.Path('ENV-UVM_HOME'))
        self.assertEqual(options.uvm_lib, 'uvm_lib')
        self.assertEqual(options.mapping, 'folder')

    def test_parser_multiple_input_files(self):
        command_line_options = ['the_project',
                                'tests/test-files/dotFparser/continuation.f', 'tests/test-files/dotFparser/filelist.f']
        options = ProjectOptions(command_line_options)
        self.assertEqual(options.input_format, 'dotf')

    def test_parser_nonexistent_single_input_file(self):
        command_line_options = ['the_project',
                                'notexist.f']
        with self.assertRaises(SystemExit) as context:
            options = ProjectOptions(command_line_options)
        self.assertEqual('1', str(context.exception))  # exit code 1 from argparse error handling

    def test_parser_nonexistent_multiple_input_files(self):
        command_line_options = ['the_project',
                                'continuation.f', 'tests/test-files/dotFparser/filelist.f']
        with self.assertRaises(SystemExit) as context:
            options = ProjectOptions(command_line_options)
        self.assertEqual('1', str(context.exception))  # exit code 1 from argparse error handling

    def test_parser_mixed_input_types(self):
        command_line_options = ['the_project',
                                'tests/test-files/tree/compilation_order.csv', 'tests/test-files/dotFparser/filelist.f']
        with self.assertRaises(SystemExit) as context:
            options = ProjectOptions(command_line_options)
        self.assertEqual('2', str(context.exception))  # exit code 2 from argparse error handling

    def test_parser_cant_create_destination_folder(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv',
                                '--destination', 'phoo/bahr']
        with self.assertRaises(SystemExit) as context:
            options = ProjectOptions(command_line_options)
        print(f'*ERROR* {context.exception}')
        self.assertEqual('1', str(context.exception))  # exit code 1 from argparse error handling

    def test_parser_do_create_destination_folder(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv', '-d', 'phoobahr']
        options = ProjectOptions(command_line_options)
        destination_folder = pathlib.Path('phoobahr')
        self.assertTrue(destination_folder.is_dir())
        destination_folder.rmdir()

    # def test_parser_parse_file(self):
    #     command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
    #     options = ProjectOptions(command_line_options)
    #     options.parse_args(command_line_options)
    #     project_name, input_file, dest_folder, project_entries = options.parse_input_file(CsvParser.parse_file)
    #     self.assertEqual(project_name, 'the_project')
    #     self.assertEqual(input_file, 'tests/test-files/tree/compilation_order.csv')
    #     self.assertEqual(dest_folder, pathlib.Path.cwd().absolute())
    #     self.assertTrue(isinstance(project_entries, dict))
    #
    # def test_parser_parse_list(self):
    #     command_line_options = ['the_project', 'tests/test-files/tutorial/clock_generator.vhd,tests/test-files/tutorial/dut.vhd']
    #     args_parser = ProjectOptions()
    #     args_parser.parse_args(command_line_options)
    #     project_name, input_file, dest_folder, project_entries = args_parser.parse_input_file(None)
    #     self.assertEqual(project_name, 'the_project')
    #     self.assertTrue(input_file is None)
    #     self.assertEqual(dest_folder, pathlib.Path.cwd().absolute())
    #     self.assertTrue(isinstance(project_entries, dict))


if __name__ == '__main__':
    unittest.main()
