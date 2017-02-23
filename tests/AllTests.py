# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from LibraryMappingFileCreatorTest import LibraryMappingFileCreatorTest
from ProjectFileCreatorTest import ProjectFileCreatorTest
from SettingsFileWriterTest import SettingsFileWriterTest
from SigasiProjectCreatorTest import SigasiProjectCreatorTest
from ConvertCsvFileToLinksTest import ConvertCsvFileToLinksTest
from ConvertCsvFileToTreeTest import ConvertCsvFileToTreeTest
from CreateSigasiProjectFromListOfFilesTest import CreateSigasiProjectFromListOfFilesTest


class AllTestsRunner(unittest.TextTestRunner):
    suites = []
    test_classes = [LibraryMappingFileCreatorTest, ProjectFileCreatorTest, SettingsFileWriterTest,
                    SigasiProjectCreatorTest, ConvertCsvFileToLinksTest, ConvertCsvFileToTreeTest,
                    CreateSigasiProjectFromListOfFilesTest]

    def __init__(self):
        super(AllTestsRunner, self).__init__(verbosity=3)
        for test_class in self.test_classes:
            self.suites.append(unittest.TestLoader().loadTestsFromTestCase(test_class))
        all_tests = unittest.TestSuite(self.suites)
        self.run(all_tests)
