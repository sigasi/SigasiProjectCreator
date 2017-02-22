#!/bin/bash
python ProjectFileCreatorTest.py
python LibraryMappingFileCreatorTest.py

echo "expect no changes in test-files folder"
echo "create links project"
python convertCsvFileToLinks.py tutorial test-files/links/compilation_order.csv test-files/links
echo "create tree project"
pushd test-files/tree
python ../../convertCsvFileToTree.py tutorial compilation_order.csv
popd
echo "create project from list"
pushd test-files/list
python ../../createSigasiProjectFromListOfFiles.py list ../tutorial/testbench.vhd ../tutorial/dut.vhd ../tutorial/clock_generator.vhd ../tutorial/foo/foo.vhd
popd

git status
