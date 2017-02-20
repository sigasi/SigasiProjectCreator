# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

import unittest

from SigasiProjectCreator import LibraryMappingFileCreator


class LibraryMappingFileCreatorTest(unittest.TestCase):
    def test_empty_file(self):
        creator = LibraryMappingFileCreator()
        expected = '''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
  <Mappings Location="Common Libraries" Library="not mapped"/>
  <Mappings Location="Common Libraries/IEEE" Library="ieee"/>
  <Mappings Location="Common Libraries/IEEE Synopsys" Library="ieee"/>
  <Mappings Location="Common Libraries/STD" Library="std"/>
</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
'''
        self.assertEqual(str(creator), expected)

    def test_simple_mapping(self):
        creator = LibraryMappingFileCreator()
        expected = '''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
  <Mappings Location="" Library="not mapped"/>
  <Mappings Location="Common Libraries" Library="not mapped"/>
  <Mappings Location="Common Libraries/IEEE" Library="ieee"/>
  <Mappings Location="Common Libraries/IEEE Synopsys" Library="ieee"/>
  <Mappings Location="Common Libraries/STD" Library="std"/>
  <Mappings Location="test.vhd" Library="work"/>
</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
'''
        creator.add_mapping("test.vhd", "work")
        creator.add_mapping("", "not mapped")
        self.assertEqual(str(creator), expected)

    def test_duplicate_mapping(self):
        creator = LibraryMappingFileCreator()
        expected = '''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
  <Mappings Location="Common Libraries" Library="not mapped"/>
  <Mappings Location="Common Libraries/IEEE" Library="ieee"/>
  <Mappings Location="Common Libraries/IEEE Synopsys" Library="ieee"/>
  <Mappings Location="Common Libraries/STD" Library="std"/>
  <Mappings Location="test.vhd" Library="work"/>
</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
'''
        creator.add_mapping("test.vhd", "test")
        creator.add_mapping("test.vhd", "work")
        self.assertEqual(str(creator), expected)

if __name__ == '__main__':
    unittest.main()
