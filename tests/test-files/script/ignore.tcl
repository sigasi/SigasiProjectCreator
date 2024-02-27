vcom foo.vhd
global result
set result [string cat $result "SIGASI IGNORE args args\n"]
vlog foo.sv
