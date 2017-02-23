# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from src.SettingsFileWriter import write
import shutil
import os
import tempfile


class SettingsFileWriterTest(unittest.TestCase):
    prefix = ".SIGASI_DONT_USE_THIS_NAME"

    def tearDown(self):
        if self.path is not None:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
            elif os.path.isfile(self.path):
                os.remove(self.path)

    def test_simple_write(self):
        self.path = tempfile.mktemp()
        content = "some content"
        write(".", self.path, content)
        self.assertCorrect(self.path, content)

    def test_xml_write(self):
        self.path = tempfile.mktemp(suffix=".xml")
        content = "<node>test</node>\n<node>test2</node>\n"
        write(".", self.path, content)
        self.assertCorrect(self.path, content)

    @unittest.expectedFailure
    def test_non_existent_parent_write(self):
        self.path = self.prefix + "/" + self.prefix
        content = "some content"
        try:
            write(".", self.path, content)
        except IOError:
            self.path = None
            raise AssertionError("Path doesn't exist")

    def test_existent_parent_write(self):
        tempdir = None
        try:
            tempdir = tempfile.mkdtemp()
            self.path = tempfile.mktemp(dir=tempdir)
            content = "some content"
            write(".", self.path, content)
            self.assertCorrect(self.path, content)
        finally:
            # Teardown
            if tempdir is not None:
                shutil.rmtree(tempdir)
            self.path = None

    def assertCorrect(self, path, content):
        self.assertTrue(os.path.isfile(path))
        with open(path, 'rb') as f:
            read = f.read(content.__len__())
            self.assertEqual(content, read)
