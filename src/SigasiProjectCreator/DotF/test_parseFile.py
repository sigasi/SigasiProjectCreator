import unittest
from parseFile import parse_dotf

class test_parseFile(unittest.TestCase):
    
    def test_basic(self):
        result = parse_dotf("testfiles/test1.f")
        expected = [
        ['+incdir', '+../../../../rtl/verilog/pkg/'],
        ['+incdir', '+../../../../bench/verilog/baremetal/'],
        '../../../../bench/verilog/baremetal/ram_d1.sv',
        '../../../../bench/verilog/baremetal/ram_d2.sv',
        '../../../../bench/verilog/baremetal/ram_dp.sv',
        '../../../../bench/verilog/baremetal/ram_p2.sv',
        '../../../../bench/verilog/baremetal/ram_sp.sv',
        '../../../../bench/verilog/baremetal/glbl.sv',
        '../../../../bench/verilog/baremetal/msp430_debug.sv',
        '../../../../bench/verilog/baremetal/msp430_testbench.sv',
        '../../../../rtl/verilog/soc/msp430_soc.sv',
        '../../../../rtl/verilog/soc/msp430_io_cell.sv',
        '../../../../rtl/verilog/core/fuse/msp430_and_gate.sv',
        '../../../../rtl/verilog/core/fuse/msp430_clock_gate.sv',
        '../../../../rtl/verilog/core/fuse/msp430_clock_mux.sv',
        '../../../../rtl/verilog/core/fuse/msp430_scan_mux.sv',
        '../../../../rtl/verilog/core/fuse/msp430_sync_cell.sv',
        '../../../../rtl/verilog/core/fuse/msp430_sync_reset.sv',
        '../../../../rtl/verilog/core/fuse/msp430_wakeup_cell.sv',
        '../../../../rtl/verilog/core/omsp/msp430_alu.sv',
        '../../../../rtl/verilog/core/omsp/msp430_dbg_hwbrk.sv',
        '../../../../rtl/verilog/core/omsp/msp430_dbg_i2c.sv',
        '../../../../rtl/verilog/core/omsp/msp430_dbg_uart.sv',
        '../../../../rtl/verilog/core/omsp/msp430_register_file.sv',
        '../../../../rtl/verilog/core/main/msp430_bcm.sv',
        '../../../../rtl/verilog/core/main/msp430_dac.sv',
        '../../../../rtl/verilog/core/main/msp430_dbg.sv',
        '../../../../rtl/verilog/core/main/msp430_execution.sv',
        '../../../../rtl/verilog/core/main/msp430_frontend.sv',
        '../../../../rtl/verilog/core/main/msp430_gpio.sv',
        '../../../../rtl/verilog/core/main/msp430_memory.sv',
        '../../../../rtl/verilog/core/main/msp430_multiplier.sv',
        '../../../../rtl/verilog/core/main/msp430_sfr.sv',
        '../../../../rtl/verilog/core/main/msp430_ta.sv',
        '../../../../rtl/verilog/core/main/msp430_watchdog.sv',
        '../../../../rtl/verilog/core/main/msp430_template08.sv',
        '../../../../rtl/verilog/core/main/msp430_template16.sv',
        '../../../../rtl/verilog/core/main/msp430_uart.sv',
        '../../../../rtl/verilog/pu/msp430_core.sv',
        '../../../../rtl/verilog/pu/msp430_pu0.sv',
        '../../../../rtl/verilog/pu/msp430_pu1.sv']
        self.assertListEqual(result, expected)

    def test_continuation(self):
        result = parse_dotf("testfiles/continuation.f")
        expected = [
            ['-makelib ies_lib/xilinx_vip -sv', "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi4stream_vip_axi4streampc.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi_vip_axi4pc.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/xil_common_vip_pkg.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi4stream_vip_pkg.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi_vip_pkg.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi4stream_vip_if.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/axi_vip_if.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/clk_vip_if.sv", "D:/Xilinx/Vivado/2018.2/data/xilinx_vip/hdl/rst_vip_if.sv", '-endlib'],
            ['-makelib ies_lib/xil_defaultlib -sv',  "D:/Xilinx/Vivado/2018.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv", "D:/Xilinx/Vivado/2018.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv", "D:/Xilinx/Vivado/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv", '-endlib'],
            ['-makelib ies_lib/xpm', "D:/Xilinx/Vivado/2018.2/data/ip/xpm/xpm_VCOMP.vhd", '-endlib' ]
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_filelist(self):
        result = parse_dotf("testfiles/filelist.f")
        expected = [
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_axi3_conv.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_axilite_conv.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_r_axi3_conv.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_w_axi3_conv.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b_downsizer.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_decerr_slave.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_simple_fifo.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_wrap_cmd.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_incr_cmd.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_wr_cmd_fsm.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_rd_cmd_fsm.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_cmd_translator.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_b_channel.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_r_channel.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_aw_channel.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s_ar_channel.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_b2s.v',
            '../../../ipstatic/axi_protocol_converter_v2_1/hdl/verilog/axi_protocol_converter_v2_1_axi_protocol_converter.v',
            '../../../bd/design_1/ip/design_1_auto_pc_0/sim/design_1_auto_pc_0.v',
            '../../../bd/design_1/hdl/design_1.vhd',
            'glbl.v'
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_variable(self):
        result = parse_dotf("testfiles/variable.f")
        expected = [
            ['+incdir', '+$VW_GO2UVM_HOME/src'],
            '${VW_GO2UVM_HOME}/src/vw_go2uvm_pkg.sv',
            'vw_wd_g2u_if.sv',
            'vw_wd_g2u_test.sv',
            'vw_wd_g2u_top.sv',
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

    def test_wildcard(self):
        result = parse_dotf("testfiles/wildcard.f")
        expected = [
            '-smartorder -work work -V93 -top tb_image -gui -access +rw -maxdelays -sdf_cmd_file ./sdf_cmd.cmd',
            '/usr/eda/dk/ibm/cmrf7sf/digital_20111130/verilog/*.v',
            '../../synthesis/image_average.v',
            '../tb/tb_image.vhd',
            '../../rtl/image_ram.vhd'
            ]
        self.maxDiff = None
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()