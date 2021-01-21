-makelib ies_lib/vendor_vip -sv \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_axi4streampc.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_axi4pc.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/xil_common_vip_pkg.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_pkg.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_pkg.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi4stream_vip_if.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/axi_vip_if.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/clk_vip_if.sv" \
  "D:/Vendor/Tool/2018.2/data/vendor_vip/hdl/rst_vip_if.sv" \
-endlib
-makelib ies_lib/defaultlib -sv \
  "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
  "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv" \
  "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies_lib/xpm \
  "D:/Vendor/Tool/2018.2/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
