import os.path
import unittest
from SigasiProjectCreator.DotF.DotFfileParser import parse_file

class DotFfileParserTest(unittest.TestCase):
    def test_basic(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/test1.f"
        result = parse_file(input_file)
        base_path = os.path.abspath(os.path.join(os.path.dirname(input_file), '../../../..'))
        expected_library_mapping = {
            f'{base_path}/bench/verilog/stainlesssteel/ram_d1.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/ram_d2.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/ram_dp.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/ram_p2.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/ram_sp.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/glbl.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/m_debug.sv': 'work',
            f'{base_path}/bench/verilog/stainlesssteel/m_testbench.sv': 'work',
            f'{base_path}/rtl/verilog/soc/m_soc.sv': 'work',
            f'{base_path}/rtl/verilog/soc/m_io_cell.sv': 'work'
        }
        expected_includes = {
            '../rtl/verilog/pkg',
            '../bench/verilog/stainlesssteel'
        }
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_continuation(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/continuation.f"
        result = parse_file(input_file)
        expected_library_mapping = {
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_axi4streampc.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_axi4pc.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/xil_common_vip_pkg.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_pkg.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_pkg.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_if.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_if.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/clk_vip_if.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/rst_vip_if.sv": 'vendor_vip',
            "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv": 'defaultlib',
            "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv": 'defaultlib',
            "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv": 'defaultlib',
            "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_VCOMP.vhd": 'xpm'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_filelist(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/filelist.f"
        result = parse_file(input_file)
        base_path = os.path.abspath(os.path.join(os.path.dirname(input_file), '../../..'))
        expected_library_mapping = {
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_conv.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_lite_conv.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_r_conv.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_w_conv.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b_downsizer.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_decerr_slave.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_simple_fifo.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wrap_cmd.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_incr_cmd.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wr_cmd_fsm.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_rd_cmd_fsm.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_cmd_translator.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_b_channel.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_r_channel.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_aw_channel.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_ar_channel.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s.v': 'work',
            f'{base_path}/ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_some_protocol_converter.v': 'work',
            f'{base_path}/bd/design_1/ip/design_1_auto_pc_0/sim/design_1_auto_pc_0.v': 'work',
            f'{base_path}/bd/design_1/hdl/design_1.vhd': 'work',
            f'{base_path}/tests/test-files/dotFparser/glbl.v': 'work'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_variable(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/variable.f"
        result = parse_file(input_file)
        base_path = str(os.path.abspath(os.path.join(os.path.dirname(input_file), '.')))
        expected_library_mapping = {
            '${FUBAR_HOME}/src/fubar_pkg.sv': 'work',
            f'{base_path}/vw_wd_g2u_if.sv': 'work',
            f'{base_path}/vw_wd_g2u_test.sv': 'work',
            f'{base_path}/vw_wd_g2u_top.sv': 'work',
        }
        expected_includes = {'$FUBAR_HOME/src'}
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')

    def test_wildcard(self):
        self.maxDiff = None
        input_file = "tests/test-files/dotFparser/wildcard.f"
        base_path1 = str(os.path.abspath(os.path.join(os.path.dirname(input_file), '..')))
        base_path2 = str(os.path.abspath(os.path.join(os.path.dirname(input_file), '../..')))
        result = parse_file(input_file)
        expected_library_mapping = {
            '/usr/eda/dk/vendor/tech/verilog/*.v': 'work',
            f'{base_path2}/synthesis/image_average.v': 'work',
            f'{base_path1}/tb/tb_image.vhd': 'work',
            f'{base_path2}/rtl/image_ram.vhd': 'work'
        }
        expected_includes = set()
        expected_defines = []
        self.assertDictEqual(result.library_mapping, expected_library_mapping, 'Library mapping mismatch')
        self.assertSetEqual(result.includes, expected_includes, 'Includes list mismatch')
        self.assertListEqual(result.defines, expected_defines, 'Defines list mismatch')


if __name__ == '__main__':
    unittest.main()
