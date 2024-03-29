# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from SigasiProjectCreator import VhdlVersion, VerilogVersion
from SigasiProjectCreator.SigasiProject import ProjectFileCreator, project_location_path
from string import Template

test_template = Template('''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
\t<name>tutorial</name>
\t<comment></comment>
\t<projects>
${project_references}\t</projects>
\t<buildSpec>
\t\t<buildCommand>
\t\t\t<name>org.eclipse.xtext.ui.shared.xtextBuilder</name>
\t\t\t<arguments>
\t\t\t</arguments>
\t\t</buildCommand>
\t</buildSpec>
\t<natures>
${natures}\t\t<nature>org.eclipse.xtext.ui.shared.xtextNature</nature>
\t</natures>
\t<linkedResources>
${vhdl_links}${extra_links}\t</linkedResources>
</projectDescription>
''')

vhdl_linked_resources = '''\t\t<link>
\t\t\t<name>Common Libraries</name>
\t\t\t<type>2</type>
\t\t\t<locationURI>virtual:/virtual</locationURI>
\t\t</link>
\t\t<link>
\t\t\t<name>Common Libraries/IEEE</name>
\t\t\t<type>2</type>
\t\t\t<locationURI>sigasiresource:/vhdl/93/IEEE</locationURI>
\t\t</link>
\t\t<link>
\t\t\t<name>Common Libraries/IEEE Synopsys</name>
\t\t\t<type>2</type>
\t\t\t<locationURI>sigasiresource:/vhdl/93/IEEE%20Synopsys</locationURI>
\t\t</link>
\t\t<link>
\t\t\t<name>Common Libraries/STD</name>
\t\t\t<type>2</type>
\t\t\t<locationURI>sigasiresource:/vhdl/93/STD</locationURI>
\t\t</link>
'''

link_template = Template('''\t\t<link>
\t\t\t<name>${name}</name>
\t\t\t<type>${file_type}</type>
\t\t\t<location>${location}</location>
\t\t</link>
''')


vhdl_nature = "\t\t<nature>com.sigasi.hdt.vhdl.ui.vhdlNature</nature>\n"
verilog_nature = "\t\t<nature>com.sigasi.hdt.verilog.ui.verilogNature</nature>\n"


# Every function called test_* will be tested
class ProjectFileCreatorTest(unittest.TestCase):
    # No teardown needed, a new creator is created every instance
    def setUp(self):
        self.creator = ProjectFileCreator('tutorial')

    def test_tutorial_project(self):
        # Vhdl nature is the default
        self.creator.set_languages(VhdlVersion.NINETY_THREE, None)
        self.assertEqual(test_template.substitute(extra_links="", project_references="", natures=vhdl_nature,
                                                  vhdl_links = vhdl_linked_resources), str(self.creator))

    def check_links(self, links, natures):
        extra_links = ""
        for link in links:
            location = "foobar/" + link
            self.creator.add_link(link, location)
            extra_links += link_template.substitute(name=link, file_type=1, location=location)
        if vhdl_nature in natures:
            linked_resources = vhdl_linked_resources
        else:
            linked_resources = ''
        expected = test_template.substitute(extra_links=extra_links, project_references="", natures=natures,
                                            vhdl_links=linked_resources)
        self.assertEqual(expected, str(self.creator))

    def test_one_verilog_link(self):
        self.creator.set_languages(None, VerilogVersion.TWENTY_O_FIVE)
        self.check_links(["test.sv"], verilog_nature)

    def test_one_vhdl_link(self):
        self.creator.set_languages(VhdlVersion.NINETY_THREE, None)
        self.check_links(["test.vhdl"], vhdl_nature)

    def test_mixed_links(self):
        self.creator.set_languages(VhdlVersion.NINETY_THREE, VerilogVersion.TWENTY_O_FIVE)
        self.check_links(["test.vhdl", "test.sv"], verilog_nature + vhdl_nature)

    @unittest.skip  # project reference is obsolete
    def test_one_project_reference(self):
        self.creator.add_project_reference('other_tutorial')
        project_reference = '''\t\t<project>other_tutorial</project>\n'''

        expected = test_template.substitute(extra_links="", project_references=project_reference, natures=vhdl_nature)
        self.assertEqual(expected, str(self.creator))

    def test_project_location_path(self):
        self.assertEqual(project_location_path('/absolute/path'), '/absolute/path')
        self.assertEqual(project_location_path('local/relative/path'), 'local/relative/path')
        self.assertEqual(project_location_path('../relative/path'), 'PARENT-1-PROJECT_LOC/relative/path')
        self.assertEqual(project_location_path('../../../../relative/path'), 'PARENT-4-PROJECT_LOC/relative/path')
