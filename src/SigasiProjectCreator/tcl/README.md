# Creating a sigasi project from a TCL script

Oftentimes, TCL scripts are used to compile a design e.g. for simulation or synthesis. The "script" input format is
meant to **use those existing scripts to create a Sigasi project**. As scripts may call other scripts or programs,
or they may contain control flow commands (loops, conditionals, function calls...), it is not obvious to just extract
project information by parsing the scripts. **SigasiProjectCreator will therefore execute the script(s)** and extract
the information from the execution. Compilation commands in the script, e.g. `vcom` and `vlog`, are overridden to
pass the information from their command line to SigasiProjectCreator. Other commands, e.g. for setting up and starting
a simulation, are ignored as they are not relevant to project creation.

SigasiProjectCreator can create a Sigasi project from TCL scripts with `vcom`/`vlog` commands. Note that
Modelsim/Questasim's `.do` files are in fact TCL scripts. SigasiProjectCreator contains the necessary overrides to
extract project information from `vcom`/`vlog`. A typical command line would look like this:

`python3 createSigasiProject.py <project> <inputfile.tcl> [--format tcl] [--tcl-ignore <command_to_ignore>] [--tcl-command <command_to_execute>] [<other options>]`

* If your file extension is not `.tcl` (but e.g. `.do`), use `--format tcl` to specify the TCL format
* The script may contain TCL commands which are not needed for importing the project in Sigasi Studio, e.g. commands to add waveforms or run a simulation. Most commands that are irrelevant to project creation are already ignored. To ensure the import does not miss anything, it will fail if it encounters unknown commands. Add those that can safely be ignored with `--tcl-ignore`.
* Some TCL scripts just run the compile commands, other scripts define a function to run the compilation, and leave it up to the user to call the function. In the latter case, use `--tcl-command <command>` to run the command after sourcing the script.
