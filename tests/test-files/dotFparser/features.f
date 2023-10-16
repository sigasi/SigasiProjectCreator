////////////////////////////////////////////////////////////////////////////////
// Comments                                                                   //
////////////////////////////////////////////////////////////////////////////////

-makelib foolib -sv \
  ../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_conv.v
  ../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_b_downsizer.v
-endlib
-makelib ies_lib/b2s -sv \
  ../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/foo_b2s.v
-endlib
../../../ipstatic/some_protocol_converter_v2_1/hdl/verilog/some_protocol_converter_v2_1_some_protocol_converter.v
../../../bd/design_1/ip/design_1_auto_pc_0/$(SIM)/design_1_auto_pc_0.v
../../../bd/design_1/hdl/design_all.vhd

-smartorder -work work -V93 -top tb_image -gui -access +rw -maxdelays -sdf_cmd_file ./sdf_cmd.cmd
glbl.v
/*
 * Block comments
 * More comments
 */

+incdir+../../rtl/$FUBAR_HOME/pkg/

//=============================================================================
// Intermediate comments
//=============================================================================

+incdir+../../bench/verilog/
+incdir+../../verilog/
+incdir+/somelib/verilog/
+define+SIGASI="yes"
+define+FOOOOOOOH
