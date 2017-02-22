# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from src.SettingsFileWriter import write
import shutil
import os
import random
import string


class SettingsFileWriterTest(unittest.TestCase):
    prefix = ".SIGASI_DONT_USE_THIS_NAME"

    def tearDown(self):
        if self.path is not None:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
            else:
                os.remove(self.path)

    def test_simple_write(self):
        self.path = self.get_random_file_name()
        content = "some content"
        write(".", self.path, content)
        self.assertCorrect(self.path, content)

    def test_xml_write(self):
        self.path = self.prefix + ".xml"
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
        try:
            self.path = self.prefix + "/" + self.prefix
            content = "some content"
            self.assertTrue(not os.path.exists(self.prefix))
            os.makedirs(self.prefix)
            self.assertTrue(os.path.isdir(self.prefix))
            write(".", self.path, content)
            self.assertCorrect(self.path, content)
        finally:
            # Teardown
            shutil.rmtree(self.prefix)
            self.path = None

    def assertCorrect(self, path, content):
        self.assertTrue(os.path.isfile(path))
        with open(path, 'rb') as f:
            read = f.read(content.__len__())
            self.assertEqual(content, read)

    def get_random_file_name(self):
        return self.prefix + ''.join(random.choice(string.ascii_lowercase))
