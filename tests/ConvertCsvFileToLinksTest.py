# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest
import sys
import tempfile
import shutil
import os
import filecmp
import SigasiProjectCreator.convertCsvFileToLinks as csvConverter


class ConvertCsvFileToLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_main(self):
        wd = os.path.dirname(os.path.realpath(__file__))
        links_dir = os.path.join(wd, "test-files/links")
        csv_file = os.path.join(links_dir, "compilation_order.csv")
        sys.argv = [sys.argv[0], "tutorial", csv_file, links_dir]
        csvConverter.main()
        result = filecmp.dircmp(links_dir, self.temp_dir)
        self.assertTrue(not result.report())
