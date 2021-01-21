import unittest
from SigasiProjectCreator.DotF.parseFile import parse_dotf

class test_parseFile(unittest.TestCase):
    
    def test_basic(self):
        result = parse_dotf("tests/test-files/dotFparser/test1.f")
        expected = [
        ['+incdir', '+../../../../rtl/verilog/pkg/'],
        ['+incdir', '+../../../../bench/verilog/stainlesssteel/'],
        '../../../../bench/verilog/stainlesssteel/ram_d1.sv',
        '../../../../bench/verilog/stainlesssteel/ram_d2.sv',
        '../../../../bench/verilog/stainlesssteel/ram_dp.sv',
        '../../../../bench/verilog/stainlesssteel/ram_p2.sv',
        '../../../../bench/verilog/stainlesssteel/ram_sp.sv',
        '../../../../bench/verilog/stainlesssteel/glbl.sv',
        '../../../../bench/verilog/stainlesssteel/m_debug.sv',
        '../../../../bench/verilog/stainlesssteel/m_testbench.sv',
        '../../../../rtl/verilog/soc/m_soc.sv',
        '../../../../rtl/verilog/soc/m_io_cell.sv']
        self.assertListEqual(result, expected)

    def test_continuation(self):
        result = parse_dotf("tests/test-files/dotFparser/continuation.f")
        expected = [
            ['-makelib ies_lib/vendor_vip -sv', "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_axi4streampc.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_axi4pc.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/xil_common_vip_pkg.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_pkg.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_pkg.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_if.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_if.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/clk_vip_if.sv", "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/rst_vip_if.sv", '-endlib'],
            ['-makelib ies_lib/defaultlib -sv',  "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv", "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv", "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv", '-endlib'],
            ['-makelib ies_lib/xpm', "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_VCOMP.vhd", '-endlib' ]
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_filelist(self):
        result = parse_dotf("tests/test-files/dotFparser/filelist.f")
        expected = [
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_conv.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_lite_conv.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_r_conv.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_w_conv.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b_downsizer.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_decerr_slave.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_simple_fifo.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wrap_cmd.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_incr_cmd.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_wr_cmd_fsm.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_rd_cmd_fsm.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_cmd_translator.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_b_channel.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_r_channel.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_aw_channel.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s_ar_channel.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b2s.v',
            '../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_some_protocol_converter.v',
            '../../../bd/design_1/ip/design_1_auto_pc_0/sim/design_1_auto_pc_0.v',
            '../../../bd/design_1/hdl/design_1.vhd',
            'glbl.v'
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_variable(self):
        result = parse_dotf("tests/test-files/dotFparser/variable.f")
        expected = [
            ['+incdir', '+$FUBAR_HOME/src'],
            '${FUBAR_HOME}/src/fubar_pkg.sv',
            'vw_wd_g2u_if.sv',
            'vw_wd_g2u_test.sv',
            'vw_wd_g2u_top.sv',
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_wildcard(self):
        result = parse_dotf("tests/test-files/dotFparser/wildcard.f")
        expected = [
            '-smartorder -work work -V93 -top tb_image -gui -access +rw -maxdelays -sdf_cmd_file ./sdf_cmd.cmd',
            '/usr/eda/dk/vendor/tech/verilog/*.v',
            '../../synthesis/image_average.v',
            '../tb/tb_image.vhd',
            '../../rtl/image_ram.vhd'
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()