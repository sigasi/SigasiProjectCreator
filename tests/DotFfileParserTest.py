import os.path
import pathlib
import unittest

import pytest

from SigasiProjectCreator.DotF.DotFfileParser import parse_file
from SigasiProjectCreator.ProjectOptions import ProjectOptions


class DotFfileParserTest(unittest.TestCase):
    def setUp(self):
        command_line_options = ['the_project', 'tests/test-files/tree/compilation_order.csv']
        self.options = ProjectOptions(command_line_options)

    def test_basic(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/test1.f"
        result = parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('../bench/verilog/stainlesssteel/ram_d1.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/ram_d2.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/ram_dp.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/ram_p2.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/ram_sp.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/glbl.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/m_debug.sv').absolute().resolve(): 'work',
            pathlib.Path('../bench/verilog/stainlesssteel/m_testbench.sv').absolute().resolve(): 'work',
            pathlib.Path('../rtl/verilog/soc/m_soc.sv').absolute().resolve(): 'work',
            pathlib.Path('../rtl/verilog/soc/m_io_cell.sv').absolute().resolve(): 'work'
        }
        expected_includes = {
            pathlib.Path('../rtl/verilog/pkg').absolute().resolve(),
            pathlib.Path('../bench/verilog/stainlesssteel').absolute().resolve()
        }
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_continuation(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/continuation.f"
        result = parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_axi4streampc.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_axi4pc.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/xil_common_vip_pkg.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_pkg.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_pkg.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_if.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_if.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/clk_vip_if.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/rst_vip_if.sv"): 'vendor_vip',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv"): 'defaultlib',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv"): 'defaultlib',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv"): 'defaultlib',
            pathlib.Path("D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_VCOMP.vhd"): 'xpm'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_filelist(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/filelist.f"
        result = parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_conv.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_lite_conv.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_r_conv.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_w_conv.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b_downsizer.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_decerr_slave.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_simple_fifo.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wrap_cmd.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_incr_cmd.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wr_cmd_fsm.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_rd_cmd_fsm.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_cmd_translator.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_b_channel.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_r_channel.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_aw_channel.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_ar_channel.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s.v').absolute().resolve(): 'work',
            pathlib.Path('ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_some_protocol_converter.v').absolute().resolve(): 'work',
            pathlib.Path('bd/design_1/ip/design_1_auto_pc_0/sim/design_1_auto_pc_0.v').absolute().resolve(): 'work',
            pathlib.Path('bd/design_1/hdl/design_1.vhd').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/glbl.v').absolute().resolve(): 'work'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_variable(self):
        self.maxDiff = None
        input_file = pathlib.Path("tests/test-files/dotFparser/variable.f")
        result = parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('${FUBAR_HOME}/src/fubar_pkg.sv'): 'work',
            pathlib.Path('tests/test-files/dotFparser/vw_wd_g2u_if.sv').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/vw_wd_g2u_test.sv').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/vw_wd_g2u_top.sv').absolute().resolve(): 'work',
        }
        expected_includes = {pathlib.Path('$FUBAR_HOME/src')}
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_wildcard(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/wildcard.f"
        result = parse_file(input_file, self.options)
        expected_library_mapping = {
            pathlib.Path('tests/test-files/dotFparser/../tutorial/clock_generator.vhd').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/../tutorial/dut.vhd').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/../tutorial/testbench.vhd').absolute().resolve(): 'work',
            pathlib.Path('/absolute/path/synthesis/image_average.v'): 'work',
            pathlib.Path('tests/test-files/dotFparser/../tb/tb_image.vhd').absolute().resolve(): 'work',
            pathlib.Path('tests/test-files/dotFparser/../../rtl/image_ram.vhd').absolute().resolve(): 'work'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')


if __name__ == '__main__':
    unittest.main()
