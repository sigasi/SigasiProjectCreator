# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from string import Template
import os

class ProjectFileCreator():
    """A Project File Creator helps you to easily create a Sigasi Project file.

    You can specify the VHDL version (93,2002 or 2008) in the constructor.

    You can add linked resources to your project by calling the add_link method.
    To create the .project file, simply call str() of your ProjectFileCreator instance.

    Typical example:
        creator = ProjectFileCreator(project_name)
        creator.add_link("test.vhd", "/home/heeckhau/shared/test.vhd")
        creator.write("/home/heeckhau/test/")

    """

    __LINK_TEMPLATE = Template(
'''\t\t<link>
\t\t\t<name>$name</name>
\t\t\t<type>$link_type</type>
\t\t\t<locationURI>$location</locationURI>
\t\t</link>
''')

    __PROJECT_FILE_TEMPLATE = Template(
'''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
\t<name>${project_name}</name>
\t<comment></comment>
\t<projects>
\t</projects>
\t<buildSpec>
\t\t<buildCommand>
\t\t\t<name>org.eclipse.xtext.ui.shared.xtextBuilder</name>
\t\t\t<arguments>
\t\t\t</arguments>
\t\t</buildCommand>
\t</buildSpec>
\t<natures>
\t\t<nature>com.sigasi.hdt.vhdl.ui.vhdlNature</nature>
\t\t<nature>org.eclipse.xtext.ui.shared.xtextNature</nature>
\t</natures>
\t<linkedResources>
${links}\t</linkedResources>
</projectDescription>''')

    __DEFAULT_LINKS=[
        ["Common Libraries",Template("virtual:/virtual")],
        ["Common Libraries/IEEE",Template("sigasiresource:/vhdl/${version}/IEEE")],
        ["Common Libraries/IEEE Synopsys",Template("sigasiresource:/vhdl/${version}/IEEE%20Synopsys")],
        ["Common Libraries/STD",Template("sigasiresource:/vhdl/${version}/STD")],
    ]

    def __init__(self, project_name, version=93):
        if version not in {93, 2002, 2008}:
             raise ValueError('Only 93, 2002 and 2008 are allowed as VHDL version number')
        self.__project_name = project_name
        self.__version = version
        self.__links = []
        self.__add_default_links()

    def __add_default_links(self):
        for name, template in self.__DEFAULT_LINKS:
            self.add_link(name, template.substitute(version=self.__version), 2)

    def __str__(self):
        links = ""
        for [name, location, link_type] in self.__links:
            links += self.__LINK_TEMPLATE.substitute(
                    name=name,
                    link_type=link_type,
                    location=location)
        return self.__PROJECT_FILE_TEMPLATE.substitute(
            project_name = self.__project_name,
            links=links
        )

    def add_link(self, name, location, link_type=1):
        if link_type not in {1, 2}:
             raise ValueError('Only types 1 and 2 are allowed. 1 is file, 2 is folder')
        self.__links.append([name, location, link_type])

    def write(self, destination):
        project_file = os.path.join(destination, ".project")
        with open(project_file, 'wb') as f:
            f.write(str(self))