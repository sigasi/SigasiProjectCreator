#!/bin/sh
python ProjectFileCreatorTest.py
python LibraryMappingFileCreatorTest.py
echo "expect no changes in test-files folder"
python convertToSigasiProject.py tutorial test-files/compilation_order.csv test-files
git status