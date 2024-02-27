# 
#  File Name:         demo_random_2002_mti.do
#  Revision:          2002 VERSION,  revision 1.0
#  
#  Maintainer:        Jim Lewis      email:  jim@synthworks.com 
#  Contributor(s):            
#     Jim Lewis      email:  jim@synthworks.com   
#  
#  Description:
#    ModelSim VHDL-2002 compilation script for 
#    SynthWorks randomization libraries
#    
#  Developed for: 
#        SynthWorks Design Inc. 
#        VHDL Training Classes
#        11898 SW 128th Ave.  Tigard, Or  97223
#        http://www.SynthWorks.com
#  
#  Revision History:
#    Date      Version    Description
#    02/2009:  1.0        Initial revision and First Public Released Version
#  
#  Copyright (c) 2009-2011 by SynthWorks Design Inc.  All rights reserved.
#  
#  Verbatim copies of this source file may be used and 
#  distributed without restriction.   
# 								 
#  This source file is free software; you can redistribute it  
#  and/or modify it under the terms of the ARTISTIC License 
#  as published by The Perl Foundation; either version 2.0 of 
#  the License, or (at your option) any later version. 						 
# 								 
#  This source is distributed in the hope that it will be 	 
#  useful, but WITHOUT ANY WARRANTY; without even the implied  
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 	 
#  PURPOSE. See the Artistic License for details. 							 
# 								 
#  You should have received a copy of the license with this source.
#  If not download it from, 
#     http://www.perlfoundation.org/artistic_license_2_0
#

# declare variables so you can locate 
# the libraries and source files where you like.
echo " "
echo "VHDL-2002 Version"
echo " "

set DIR_SCRIPT "wahoo"
# [file dirname [status file] ] 
if {![file isdirectory $DIR_SCRIPT]} {
  file mkdir $DIR_SCRIPT
}
cd  $DIR_SCRIPT

set DIR_LIB_IEEE_PROPOSED   ${DIR_SCRIPT}/MLIBS
set DIR_SRC_IEEE_PROPOSED   ${DIR_SCRIPT}/..
set DIR_LIB_SYNTHWORKS      ${DIR_SCRIPT}/MLIBS
set DIR_SRC_SYNTHWORKS      ${DIR_SCRIPT}/..
set DIR_LIB_DEMO            ${DIR_SCRIPT}/MLIBS
set DIR_SRC_DEMO            ${DIR_SCRIPT}/..
set NAME_DEMO               "Demo"


# Create IEEE_proposed library and compile standard_additions_c.vhdl into it
# Remove the following if you already have the IEEE_PROPOSED library
if {![file isdirectory $DIR_LIB_IEEE_PROPOSED]} {
  file mkdir $DIR_LIB_IEEE_PROPOSED
}
vlib  ${DIR_LIB_IEEE_PROPOSED}/ieee_proposed
vmap  ieee_proposed  ${DIR_LIB_IEEE_PROPOSED}/ieee_proposed
vcom -2002 -work ieee_proposed ${DIR_SRC_IEEE_PROPOSED}/standard_additions_c.vhdl
vcom -2002 -work ieee_proposed ${DIR_SRC_IEEE_PROPOSED}/standard_textio_additions_c.vhdl


# Create SynthWorks library and compile the randomization packages into it
if {![file isdirectory $DIR_LIB_SYNTHWORKS]} {
  file mkdir $DIR_LIB_SYNTHWORKS
}
vlib  ${DIR_LIB_SYNTHWORKS}/SynthWorks
vmap  SynthWorks  ${DIR_LIB_SYNTHWORKS}/SynthWorks
vcom -2002 -work SynthWorks ${DIR_SRC_SYNTHWORKS}/SortListPkg_int_2002.vhd
vcom -2002 -work SynthWorks ${DIR_SRC_SYNTHWORKS}/RandomBasePkg_2002.vhd
echo "vcom -2002 -work SynthWorks ${DIR_SRC_SYNTHWORKS}/RandomPkg_2002.vhd"
vcom -2002 -work SynthWorks ${DIR_SRC_SYNTHWORKS}/RandomPkg_2002.vhd


# Create Demo library and compile the randomization packages into it
if {![file isdirectory $DIR_LIB_DEMO]} {
  file mkdir $DIR_LIB_DEMO
}
vlib  ${DIR_LIB_DEMO}/$NAME_DEMO
vmap  $NAME_DEMO  ${DIR_LIB_DEMO}/$NAME_DEMO
echo "vcom -2002 -work $NAME_DEMO ${DIR_SRC_DEMO}/Demo_Rand.vhd"
vcom -2002 -work $NAME_DEMO ${DIR_SRC_DEMO}/Demo_Rand.vhd


# run the simulation - no time passes in demo program, so run 1 ns is ok.
vsim ${NAME_DEMO}.demo_rand 
run 
