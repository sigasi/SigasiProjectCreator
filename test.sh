#!/bin/bash
export PYTHONPATH=`pwd`/src:`pwd`/src/SigasiProjectCreator/DotF
pytest --cov-report html --cov=src
