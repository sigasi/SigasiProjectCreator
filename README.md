SigasiProjectCreator [![Coverage Status](https://coveralls.io/repos/github/sigasi/SigasiProjectCreator/badge.svg?branch=master)](https://coveralls.io/github/sigasi/SigasiProjectCreator?branch=verilog_support) [![Build Status](https://travis-ci.org/sigasi/SigasiProjectCreator.svg?branch=master)](https://travis-ci.org/sigasi/SigasiProjectCreator)
====================

This project offers Python classes that make it easy to generate a
Sigasi Project from your project specifications.

On one hand, you can use `createSigasiProject.py` (in folder `src`) to
create a Sigasi Studio project from various input formats. We'll
discuss the use of `createSigasiProject.py` below. SigasiProjectCreator
is meant to work *out of the box* in a broad range of use cases, but
some changes may be needed for your design or working environment.

On the other hand, the `src/SigasiProjectCreator/SigasiProject.py` file
offers classes which you can use in a custom script to create a Sigasi
Studio project from your (e.g. in-house) project description. Each
class in `SigasiProject.py` corresponds with one praticular
configuration files (`.project`, `.library_mapping.xml` and
`.settings/...`). In most cases, you will need the top level
`SigasiProject` class, which encompasses the classes for individual
configuration files.

See the [Project setup manual](https://insights.sigasi.com/manual/projectsetup/) for multiple ways to set up a project.

Documented examples:
* [Converting a Quartus project to a Sigasi Studio project](https://insights.sigasi.com/tech/importing-quartus-project-sigasi/)
* [Generating a Sigasi project from a Vivado project](https://insights.sigasi.com/tech/generating-sigasi-project-vivado-project/)

Run `test.sh` to run the unit tests.
Files containing tests have to end in `Test`.

The project and all tests run under Python 3.9 and above.
Support for `.f` files requires settings to support the Antlr parser.
Other input file formats don't require Antlr support.

You may need to add the `src` directory to your `PYTHONPATH` environment, e.g.

* Linux/bash: `export PYTHONPATH=/home/mydir/SigasiProjectCreator/src`
* Windows: `set PYTHONPATH=C:\work\SigasiProjectCreator\src`

### Setup

Make sure that the required Python packages are installed:

`python -m pip install -r requirements.txt`

### Using createSigasiProject.py to create a Sigasi Studio project

Starting with version 2.0.0, SigasiProjectCreator has a single
top-level script which supports all input formats and project options. The meaning of most options is obvious. We'll discuss some of the options below.

```
$ python src/createSigasiProject.py -h
usage: SigasiProjectCreator [-h] [-d DESTINATION_FOLDER]
                            [-l {in-place,simulator,linked-files-flat,linked-files-tree,linked-folders}]
                            [--uvm UVM] [--use-uvm-home] [--uvmlib UVMLIB]
                            [--format {filelist,csv,dotf,hdp,xise,tcl}]
                            [--mapping {file,folder}] [--enable-vhdl]
                            [--vhdl-version {93,2002,2008,2019}]
                            [--enable-verilog] [--verilog-as-sv]
                            [--enable-vunit] [-w WORKLIB]
                            [--skip-check-exists] [--encoding ENCODING] [-f]
                            [--rel-path [REL_PATH_ROOT ...]] [-v]
                            [--tcl-command TCL_COMMAND] [--tcl-ignore [TCL_IGNORE ...]]
                            [--tcl-exec TCL_EXEC] [--tcl-no-wrapper]
                            project_name input_file [input_file ...]

positional arguments:
  project_name          Project name
  input_file            Input file or comma-separated list of input files

options:
  -h, --help            show this help message and exit
  -d DESTINATION_FOLDER, --destination DESTINATION_FOLDER
                        Root folder of created project
  -l {in-place,simulator,linked-files-flat,linked-files-tree,linked-folders}, --layout {in-place,simulator,linked-files-flat,linked-files-tree,linked-folders}
                        Any of the following layouts: in-place (default),
                        simulator (one folder per library with linked files),
                        linked-files-flat (one folder with links to all
                        files), linked-files-tree (virtual folders like the
                        source tree, with links to files), linked-folders (mix
                        of virtual and linked folders)
  --uvm UVM             Add UVM to the project, using UVM from the given
                        install path
  --use-uvm-home        Add UVM to the project. Sigasi Studio will use the
                        UVM_HOME environment variable to find your UVM
                        installation
  --uvmlib UVMLIB       Library in which to compile the UVM package (default:
                        the library set with `--work`, or `work`)
  --format {filelist,csv,dotf,hdp,xise,tcl}
                        Force input format (ignore file extension): filelist
                        (file list), csv (CSV file), dotf (.f file), hdp (HDP
                        project), xise (Xilinx ISE project), tcl (TCL script)
  --mapping {file,folder}
                        Library mapping style: `folder` = map folders where
                        possible, `file` = map individual files (default).
                        Option `folder` requires that files are actually
                        available. Only relevant with `default`, `linked-
                        files-tree` and `linked-folders` project layouts
  --enable-vhdl         Force VHDL support (regardless of VHDL file presence)
  --vhdl-version {93,2002,2008,2019}
                        Set VHDL version (default VHDL-2008)
  --enable-verilog      Force (System)Verilog support (regardless of
                        (System)Verilog file presence)
  --verilog-as-sv       Treat .v files as SystemVerilog
  --enable-vunit        Enable VUnit support
  -w WORKLIB, --work WORKLIB
                        Main HDL library name (default `work`)
  --skip-check-exists   Skip checking whether files and folders exist
  --encoding ENCODING   Set unicode character encoding (default: UTF-8)
  -f, --force           Overwrite existing project files
  --rel-path [REL_PATH_ROOT ...]
                        Use relative paths for links to files in this folder
                        and its sub-folders
  -v, --verbose         Verbose output
  --tcl-command TCL_COMMAND
                        Command to run after sourcing input TCL scripts
  --tcl-ignore [TCL_IGNORE ...]
                        TCL commands to ignore during input script execution
  --tcl-exec TCL_EXEC   TCL interpreter path and command line options (internal TCL interpreter if unspecified)
  --tcl-no-wrapper      Don't use the internal TCL wrapper
```

Option `-l` / `--layout` determines the layout of the project.
* By default, the *in place* layout is used. Files are referenced from their actual place on the filesystem. In this case, all project files must be in the project root folder (see `-d`/`--destination`).
* In the *linked-files-flat* layout, the Sigasi Studio project will look like a single folder with links to all design files.
* In the *simulator* layout, the Sigasi Studio project has one folder for each library. These folders are populated with links to the design files. This looks similar to the library view of a simulator.
* In the *linked-files-tree* layout, the Sigasi Studio project mimics the file structure of your project with linked folders and links to design files.
* The *linked-folders* layout is similar to linked-files-tree, except that the links point to folders rather than files.

Option `--mapping` determines how design files are mapped to folders.
* By default, `file` mapping is used, which means the design files are mapped to libraries one by one. As a consequence, HDL files which are not needed for the project are automatically excluded from compilation. However, when adding a file to the design, you'll need to explicitly include it in the project.
* Alternatively, `folder` mapping maps entire folders to a HDL library. Exceptions are handled in the project creator, e.g. if files need to be either excluded from compilation, or if a folder contains files from multiple libraries.

Note that in the `simulator` layout, `folder` mapping is always used, whereas in the `linked-files-flat` layout, `file` mapping is used.

Option `--rel-path` tells SigasiProjectCreator to use relative paths for files in the 
given folder or any of its subfolders. You can use `--rel-path` multiple times.

In some cases, a CSV (Comma Separated Value) file can be created with
the third-party tool, after which the CSV file can be converted to a
Sigasi Studio project:

* **Quartus to CSV**: `convertQuartusProjectToCsv.tcl`
* **Vivado to CSV**: `convertVivadoProjectToCsv.tcl`

# Creating a sigasi project from a TCL script
Creating a sigasi project from a script is discussed [here](src/SigasiProjectCreator/tcl/README.md). Note that this is an advanced project creation method that may require some scripting/programming skills to set up.