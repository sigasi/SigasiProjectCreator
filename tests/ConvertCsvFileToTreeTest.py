# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest
import sys
import tempfile
import shutil
import os
import filecmp
import src.convertCsvFileToTree as csvConverter


class ConvertCsvFileToTreeTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_main(self):
        wd = os.path.dirname(os.path.realpath(__file__))
        tree_dir = os.path.join(wd, "test-files/tree")
        csv_file = os.path.join(tree_dir, "compilation_order.csv")
        sys.argv = [sys.argv[0], "tutorial", csv_file, self.temp_dir]
        csvConverter.main()
        result = filecmp.dircmp(tree_dir, self.temp_dir)
        self.assertTrue(not result.report())
