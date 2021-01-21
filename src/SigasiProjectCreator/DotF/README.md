This directory contains an Antlr4 parser for `.f` files.

`.f` files contain command line options for (EDA) tools. As tools have
different sets of options, the content of `.f` files are tool (and tool
vendor) dependent. In their simplest form, a `.f` file contains a list
of input files, one per line. `.f` files may also contain tool options
starting with dash (`-`) or plus (`+`).

So far, the .f to Sigasi Studio project tool supports:

* input files (mapped to library work)
* `+incdir+...` (Verilog includes, added to Verilog preferences)
* `+define+...` (Verilog defines, added to Verilog preferences)
* `-makelib <libname> ... -endlib` with input files on separate lines between `makelib` and `endlib`, with continuation characters (mapped to the library <`libname`>, or the part of `libname` after the last slash `/` if it contains any)
* `-f <filename>` to include another `.f` file
* environment variables in input files and include paths (which get expanded if they are defined)
* VHDL, (System)Verilog and mixed language projects

The grammar of `.f` files is in `DotF.g4` and is written in [Antlr
4](https://www.antlr.org/). The other files are generated from it with
the Antlr Tool. If you want to change the grammar, edit `DotF.g4` and
re-generate the python code:

* Download the Antlr4 jar from the Antlr website.
* Make sure that a compatible version of Java is available on your system.
* Run `java -jar /usr/local/lib/antlr-4.9.1-complete.jar DotF.g4`
