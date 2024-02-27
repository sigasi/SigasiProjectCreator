rename vlog __orig_vlog
proc vlog args {
	tailcall __orig_vlog {*}$args
}

vlog -work asdf a_file.v
