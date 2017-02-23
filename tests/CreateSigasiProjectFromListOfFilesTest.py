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
import src.createSigasiProjectFromListOfFiles as sigasiProjectCreator


class CreateSigasiProjectFromListOfFilesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_path = os.getcwd()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        os.chdir(self.old_path)

    def test_main(self):
        wd = os.path.dirname(os.path.realpath(__file__))
        list_dir = os.path.join(wd, "test-files/list")
        # Be sure to cd back to the original dir later on
        os.chdir(self.temp_dir)
        files = ["testbench.vhd", "dut.vhd", "clock_generator.vhd", "foo/foo.vhd"]
        file_paths = [os.path.join(wd, "tutorial" + f) for f in files]
        sys.argv = [sys.argv[0], "list"]
        for path in file_paths:
            sys.argv.append(path)
        sigasiProjectCreator.main()
        result = filecmp.dircmp(list_dir, self.temp_dir)
        self.assertTrue(not result.report())
