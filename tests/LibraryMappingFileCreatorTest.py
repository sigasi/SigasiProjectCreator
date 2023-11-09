# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from SigasiProjectCreator import VhdlVersion, VerilogVersion
from SigasiProjectCreator.SigasiProject import LibraryMappingFileCreator
from string import Template


mapping_template = Template('  <Mappings Location="${loc}" Library="${lib}"/>\n')

mappings_template = Template('''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
  <Mappings Location="" Library="not mapped"/>
  <Mappings Location="Common Libraries" Library="not mapped"/>
  <Mappings Location="Common Libraries/IEEE" Library="ieee"/>
  <Mappings Location="Common Libraries/IEEE Synopsys" Library="ieee"/>
  <Mappings Location="Common Libraries/STD" Library="std"/>
${after}</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
''')


class LibraryMappingFileCreatorTest(unittest.TestCase):
    def setUp(self):
        self.creator = LibraryMappingFileCreator()

    def test_empty_file(self):
        expected = mappings_template
        self.creator.set_languages(VhdlVersion.TWENTY_O_EIGHT, None)
        self.assertEqual(expected.substitute(after=""), str(self.creator))

    def test_simple_mapping(self):
        loc = "test.vhd"
        lib = "work"
        after = mapping_template.substitute(loc=loc, lib=lib)
        expected = mappings_template.substitute(after=after)

        self.creator.add_mapping(loc, lib)
        self.creator.add_mapping("", "not mapped")
        self.creator.set_languages(VhdlVersion.TWENTY_O_EIGHT, VerilogVersion.TWENTY_O_FIVE)
        self.assertEqual(expected, str(self.creator))

    def test_duplicate_mapping(self):
        loc = "test.vhd"
        lib = "work"
        after = mapping_template.substitute(loc=loc, lib=lib)
        expected = mappings_template.substitute(after=after)

        self.creator.add_mapping(loc, "test")
        self.creator.add_mapping(loc, lib)
        self.creator.set_languages(VhdlVersion.TWENTY_O_EIGHT, None)
        self.assertEqual(expected, str(self.creator))
