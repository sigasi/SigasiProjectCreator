SigasiProjectCreator [![Coverage Status](https://coveralls.io/repos/github/sigasi/SigasiProjectCreator/badge.svg?branch=master)](https://coveralls.io/github/sigasi/SigasiProjectCreator?branch=verilog_support) [![Build Status](https://travis-ci.org/sigasi/SigasiProjectCreator.svg?branch=master)](https://travis-ci.org/sigasi/SigasiProjectCreator)
====================

This project offers Python classes that make it easy to generate a Sigasi Project from your own project specifications.
The `src/SigasiProjectCreator/Creator.py` file has four classes that you can use to create the project file and
the corresponding Library configuration files. In most cases you will need the `SigasiProjectCreator` class.

This repository also contains a few example scripts that create `.project` and `.library_mapping.xml` files and the `.settings` folder from various inputs (csv-file, list). See test-files for example input.

See the [Project setup manual](https://insights.sigasi.com/manual/projectsetup/) for multiple ways to setup a project.

Documented examples:
* [Converting a Quartus project to a Sigasi Studio project](https://insights.sigasi.com/tech/importing-quartus-project-sigasi/)
* [Converting a Vivado project to a Sigasi Studio project](https://insights.sigasi.com/tech/importing-quartus-project-sigasi/)

Run `test.sh` to run the tests.
Files containing tests have to end in `Test`.

The project and all tests run under both Python 2 and 3. You may need to add the `src` directory to your `PYTHONPATH` environment, e.g.

* Linux/bash: `export PYTHONPATH=/home/mydir/SigasiProjectCreator/src`
* Windows: `set PYTHONPATH=C:\work\SigasiProjectCreator\src`