SigasiProjectCreator [![Coverage Status](https://coveralls.io/repos/github/sigasi/SigasiProjectCreator/badge.svg?branch=master)](https://coveralls.io/github/sigasi/SigasiProjectCreator?branch=verilog_support) [![Build Status](https://travis-ci.org/sigasi/SigasiProjectCreator.svg?branch=master)](https://travis-ci.org/sigasi/SigasiProjectCreator)
====================

This project offers Python classes that make it easy to generate a
Sigasi Project from your own project specifications.  The
`src/SigasiProjectCreator/Creator.py` file has four classes that you
can use to create the project file and the corresponding Library
configuration files. In most cases you will need the
`SigasiProjectCreator` class.

This repository also contains a few example scripts that create
`.project` and `.library_mapping.xml` files and the `.settings` folder
from various inputs (csv-file, list). See test-files for example
input.

See the [Project setup manual](https://insights.sigasi.com/manual/projectsetup/) for multiple ways to set up a project.

Documented examples:
* [Converting a Quartus project to a Sigasi Studio project](https://insights.sigasi.com/tech/importing-quartus-project-sigasi/)
* [Generating a Sigasi project from a Vivado project](https://insights.sigasi.com/tech/generating-sigasi-project-vivado-project/)

Run `test.sh` to run the tests.
Files containing tests have to end in `Test`.

The project and all tests run under Python 3. Support for `.f` files
requires settings to support the Antlr parser. Other input file
formats don't require Antlr support.

You may need to add the `src` directory to your `PYTHONPATH` environment, e.g.

* Linux/bash: `export PYTHONPATH=/home/mydir/SigasiProjectCreator/src`
* Windows: `set PYTHONPATH=C:\work\SigasiProjectCreator\src`

### Setup

Make sure that required Python packages are installed:

`python -m pip install -r requirements.txt`

### Usage

Run `python` with the script for the project file conversion that you want to make. Scripts are available to create a Sigasi Studio project from:

* **CSV file**: `convertCsvFileToLinks.py` or `convertCsvFileToTree.py`
* **HDP**: `convertHdpProjectToSigasiProject.py`
* **Xilinx ISE**: `convertXilinxISEToSigasiProject.py`
* **List of files**: `createSigasiProjectFromListOfFiles.py`
* **`.f` file**: `convertDotFtoSigasiProject.py [--layout=default|simulator] <project_name> <dot_f_file.f> [<project_folder>]`

With `.f` files, the default project layout references all files in place. The project folder must contain all HDL files in the project.
An alternative *simulator-like* layout uses a folder per library, which contain links to the HDL files. In that case, the project folder must be an empty folder.

In some cases, a CSV (Comma Separated Value) file must be created with
the third party tool, after which the CSV file can be converted to a
Sigasi Studio project:

* **Quartus to CSV**: `convertQuartusProjectToCsv.tcl`
* **Vivado to CSV**: `convertVivadoProjectToCsv.tcl`
