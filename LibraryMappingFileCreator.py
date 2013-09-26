# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from string import Template
import os

class LibraryMappingFileCreator:
    """A Library Mapping File Creator helps you to easily create a Sigasi Library Mapping file.

    You can add library mappings by calling the add_mapping method.
    To create the .library_mapping file content, simply call str() of your LibraryMappingFileCreator instance.

    Typical example:
        creator = ProjectFileCreator(project_name)
        creator.add_link("test.vhd", /home/heeckhau/shared/test.vhd")
        return str(creator)

    """
    __LIBRARIES_TEMPLATE = Template(
        '''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
$mappings</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
''')

    __MAPPING_TEMPLATE = Template('''  <Mappings Location="$path" Library="$library"/>
''')

    __DEFAULT_MAPPINGS = {
        "Common Libraries/IEEE":"ieee",
        "Common Libraries/IEEE Synopsys":"ieee",
        "Common Libraries":"not mapped",
        "Common Libraries/STD":"std"
    }

    def __init__(self):
        self.__entries = dict()
        self.__add_default_mappings()

    def __add_default_mappings(self):
        for path, library in self.__DEFAULT_MAPPINGS.iteritems():
            self.add_mapping(path, library)

    def __str__(self):
        mappings = ""
        for (path, library) in sorted(self.__entries.items()):
            mappings += self.__MAPPING_TEMPLATE.substitute(
                    path=path,
                    library=library)
        return self.__LIBRARIES_TEMPLATE.substitute(mappings=mappings)

    def add_mapping(self, path, library):
        self.__entries[path] = library

    def write(self, destination):
        libray_mapping_file = os.path.join(destination, ".library_mapping.xml")
        with open(libray_mapping_file, 'wb') as f:
            f.write(str(self))