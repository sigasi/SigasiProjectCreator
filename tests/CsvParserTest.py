import pathlib
import unittest

from SigasiProjectCreator.CsvParser import CsvParser
from SigasiProjectCreator.ProjectOptions import ProjectOptions


class CsvParserTest(unittest.TestCase):
    def test_extended_csv(self):
        input_file = 'tests/test-files/csv/extended.csv'
        command_line_options = ['the_project', input_file]
        self.options = ProjectOptions(command_line_options)
        result = CsvParser().parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('foo/bar.vhd').absolute().resolve(): ['test1'],
            pathlib.Path('bahr/define.sv').absolute().resolve(): ['define'],
            pathlib.Path('clock_generator.vhd').absolute().resolve(): ['test2'],
            pathlib.Path('dut.vhd').absolute().resolve(): ['test2'],
            pathlib.Path('testbench.vhd').absolute().resolve(): ['test1'],
            pathlib.Path('include.vhd').absolute().resolve(): ['include']
        }
        expected_includes = {
            pathlib.Path('includes').absolute().resolve()
        }
        expected_defines = ['SIGASI=true']
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.verilog_includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.verilog_defines, expected_defines, 'Defines list mismatch')

    def test_multimap_csv(self):
        self.maxDiff = None
        input_file = 'tests/test-files/csv/multimap.csv'
        command_line_options = ['the_project', input_file]
        self.options = ProjectOptions(command_line_options)
        result = CsvParser().parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('foo/bar.vhd').absolute().resolve(): ['test1'],
            pathlib.Path('clock_generator.vhd').absolute().resolve(): ['test2', 'test1', 'test7'],
            pathlib.Path('dut.vhd').absolute().resolve(): ['test2', 'test3'],
            pathlib.Path('testbench.vhd').absolute().resolve(): ['test1']
        }
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.verilog_includes, set(), 'Includes list mismatch')
        self.assertListEqual(result.verilog_defines, [], 'Defines list mismatch')

    def test_invalid_library_name(self):
        self.maxDiff = None
        input_file = 'tests/test-files/csv/invalid_lib.csv'
        command_line_options = ['the_project', input_file]
        self.options = ProjectOptions(command_line_options)
        with self.assertRaises(SystemExit) as context:
            result = CsvParser().parse_file(input_file, self.options)
        self.assertEqual('5', str(context.exception))  # exit code 5 from abort_if_false


if __name__ == '__main__':
    unittest.main()
