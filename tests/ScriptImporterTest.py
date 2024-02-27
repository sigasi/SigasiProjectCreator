"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from dataclasses import dataclass
import os
import pathlib
import unittest
from SigasiProjectCreator import VhdlVersion

from SigasiProjectCreator.tcl.ScriptImporter import ScriptImporter, ScriptImporterOptions


@dataclass
class OptionsForTest:
    vhdl_version: str
    verbose: bool
    tcl_run_command: str
    work_lib: str
    input_file: str
    input_format: str
    tcl_ignore: list[str]


class TestScriptImporter(unittest.TestCase):
    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)
        self.working_directory = pathlib.Path.cwd()
        self.maxDiff = None

    def setUp(self) -> None:
        os.chdir(self.working_directory)
        return super().setUp()

    def tearDown(self) -> None:
        os.chdir(self.working_directory)
        return super().tearDown()

    def test_constructor(self):
        self.assertEqual(ScriptImporter().parser_line_types.keys(), {'VHDL', 'VLOG'})

    def test_vhdl_line_file_only(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VHDL foo.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vhdl_line(line, options)
        self.assertEqual(line_files, ['foo.vhd'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertIsNone(line_defines)
        self.assertIsNone(line_includes)

    def test_vhdl_line_vhdl_version_2008(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VHDL -v08 foo.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vhdl_line(line, options)
        self.assertEqual(line_files, ['foo.vhd'])
        self.assertIsNone(line_library)
        self.assertEqual(line_version, VhdlVersion.TWENTY_O_EIGHT)
        self.assertIsNone(line_defines)
        self.assertIsNone(line_includes)

    def test_vhdl_line_vhdl_version_2019(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VHDL -2019 foo.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vhdl_line(line, options)
        self.assertEqual(line_files, ['foo.vhd'])
        self.assertIsNone(line_library)
        self.assertEqual(line_version, VhdlVersion.TWENTY_NINETEEN)
        self.assertIsNone(line_defines)
        self.assertIsNone(line_includes)

    def test_vhdl_line_vhdl_library_bar(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VHDL -work bar foo.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vhdl_line(line, options)
        self.assertEqual(line_files, ['foo.vhd'])
        self.assertEqual(line_library, 'bar')
        self.assertIsNone(line_version)
        self.assertIsNone(line_defines)
        self.assertIsNone(line_includes)

    def test_vhdl_line_multi_vhdl_library_bar(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VHDL -brol -foo fooh.vhdl -work bar foo.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vhdl_line(line, options)
        self.assertEqual(line_files, ['fooh.vhdl', 'foo.vhd'])
        self.assertEqual(line_library, 'bar')
        self.assertIsNone(line_version)
        self.assertIsNone(line_defines)
        self.assertIsNone(line_includes)

    def test_vlog_line_file_only(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG foo.v'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['foo.v'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, [])
        self.assertSetEqual(line_includes, set())

    def test_vlog_line_library_bahr(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG -work bahr foo.v'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['foo.v'])
        self.assertEqual(line_library, 'bahr')
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, [])
        self.assertSetEqual(line_includes, set())

    def test_vlog_line_dash_defines(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG -define FOO=aah -define SIGASI=true foo.v'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['foo.v'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, ['FOO=aah', 'SIGASI=true'])
        self.assertSetEqual(line_includes, set())

    def test_vlog_line_plus_defines(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG +define+FOO=bee +define+SIGASI=yes phoo.v'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['phoo.v'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, ['FOO=bee', 'SIGASI=yes'])
        self.assertSetEqual(line_includes, set())

    def test_vlog_line_includes(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG +incdir+/my/path +incdir+../../relative/path foo.v'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['foo.v'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, [])
        self.assertSetEqual(line_includes, set([pathlib.Path('/my/path').absolute().resolve(), pathlib.Path('../../relative/path').absolute().resolve()]))

    def test_vlog_line_multiple_files(self):
        options = ScriptImporterOptions(
            verbose=True,
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_run_command='',
            work_lib='work',
            input_file=''
        )
        my_importer = ScriptImporter()
        line = 'VLOG foo.v -sv -rubbish bahr.sv ignore.vhd'
        line_files, line_library, line_version, line_defines, line_includes = my_importer.parse_vlog_line(line, options)
        self.assertEqual(line_files, ['foo.v', 'bahr.sv'])
        self.assertIsNone(line_library)
        self.assertIsNone(line_version)
        self.assertEqual(line_defines, [])
        self.assertSetEqual(line_includes, set())

    def test_tkinter_1(self):
        options = OptionsForTest(
            input_file='tests/test-files/script/run_sim.tcl',
            input_format='tcl',
            verbose=True,
            tcl_run_command='com',
            work_lib='work',
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_ignore=[],
        )

        my_importer = ScriptImporter()
        result = my_importer.parse_file(options.input_file, options)
        expected_mapping = {
            pathlib.Path('./mem.sv').absolute().resolve(): 'work',
            pathlib.Path('./package.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32_EX.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32_ID.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32_IF.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32_MEM.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32.sv').absolute().resolve(): 'work',
            pathlib.Path('./qrisc32_TB.sv').absolute().resolve(): 'work'
        }
        self.assertEqual(result.library_mapping, expected_mapping)
        self.assertEqual(result.verilog_defines, ['FPV_ON'])
        self.assertEqual(result.verilog_includes, set([pathlib.Path('includes').absolute().resolve()]))

    def test_tkinter_2(self):
        options = OptionsForTest(
            input_file='tests/test-files/script/demo_random_2002_mti.tcl',
            input_format='tcl',
            verbose=True,
            tcl_run_command='',
            work_lib='lib',
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_ignore=[],
        )

        my_importer = ScriptImporter()
        result = my_importer.parse_file(options.input_file, options)
        expected_mapping = {
            pathlib.Path('standard_additions_c.vhdl').absolute().resolve(): 'ieee_proposed',
            pathlib.Path('standard_textio_additions_c.vhdl').absolute().resolve(): 'ieee_proposed',
            pathlib.Path('SortListPkg_int_2002.vhd').absolute().resolve(): 'SynthWorks',
            pathlib.Path('RandomBasePkg_2002.vhd').absolute().resolve(): 'SynthWorks',
            pathlib.Path('RandomPkg_2002.vhd').absolute().resolve(): 'SynthWorks',
            pathlib.Path('Demo_Rand.vhd').absolute().resolve(): 'Demo'
        }
        self.assertEqual(result.library_mapping, expected_mapping)
        self.assertEqual(result.verilog_defines, [])
        self.assertEqual(result.verilog_includes, set())

    def test_tkinter_3(self):
        options = OptionsForTest(
            input_file='tests/test-files/script/osvvm_old.tcl',
            input_format='tcl',
            verbose=False,
            tcl_run_command='',
            work_lib='lib',
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_ignore=['foo'],
        )

        my_importer = ScriptImporter()
        result = my_importer.parse_file(options.input_file, options)
        expected_mapping = {
            pathlib.Path('ResolutionPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('NamePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('NameStorePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('OsvvmGlobalPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('VendorCovApiPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('TranscriptPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('TextUtilPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('AlertLogPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('MessagePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('SortListPkg_int.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('RandomBasePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('RandomPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('RandomProcedurePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('CoveragePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('MemoryPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('ScoreboardGenericPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('ScoreboardPkg_slv.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('ScoreboardPkg_int.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('ResizePkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('TbUtilPkg.vhd').absolute().resolve(): 'osvvm',
            pathlib.Path('OsvvmContext.vhd').absolute().resolve(): 'osvvm'
        }
        self.assertEqual(result.library_mapping, expected_mapping)
        self.assertEqual(result.verilog_defines, [])
        self.assertEqual(result.verilog_includes, set())

    def test_tkinter_4(self):
        options = OptionsForTest(
            input_file='tests/test-files/script/wrapped.tcl',
            input_format='tcl',
            verbose=False,
            tcl_run_command='',
            work_lib='lib',
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_ignore=['foo'],
        )

        my_importer = ScriptImporter()
        result = my_importer.parse_file(options.input_file, options)
        expected_mapping = {
            pathlib.Path('a_file.v').absolute().resolve(): 'asdf'
        }
        self.assertEqual(result.library_mapping, expected_mapping)
        self.assertEqual(result.verilog_defines, [])
        self.assertEqual(result.verilog_includes, set())

    def test_tkinter_5(self):
        options = OptionsForTest(
            input_file='tests/test-files/script/ignore.tcl',
            input_format='tcl',
            verbose=False,
            tcl_run_command='',
            work_lib='lib',
            vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
            tcl_ignore=['foo'],
        )

        my_importer = ScriptImporter()
        with self.assertRaises(SystemExit) as context:
            result = my_importer.parse_file(options.input_file, options)
        self.assertTrue("5" in str(context.exception))  # Exit code 5 on unsupported line in data


if __name__ == '__main__':
    unittest.main()
