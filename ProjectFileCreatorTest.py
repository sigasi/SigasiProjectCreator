# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from SigasiProjectCreator import ProjectFileCreator
from string import Template

test_template = Template('''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
\t<name>tutorial</name>
\t<comment></comment>
\t<projects>
${project_references}	</projects>
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
\t\t<link>
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
${extra_links}\t</linkedResources>
</projectDescription>''')


class MyTestCase(unittest.TestCase):
    def test_tutorial_project(self):
        creator = ProjectFileCreator('tutorial')
        self.assertEqual(test_template.substitute(extra_links="", project_references=""), str(creator))

    def test_one_link(self):
        creator = ProjectFileCreator('tutorial')
        creator.add_link("test.vhd", "foobar/test.vhd")
        extra_links = '''\t\t<link>
\t\t\t<name>test.vhd</name>
\t\t\t<type>1</type>
\t\t\t<location>foobar/test.vhd</location>
\t\t</link>
'''
        expected = test_template.substitute(extra_links=extra_links, project_references="")
        self.assertEqual(expected, str(creator))

    def test_one_project_reference(self):
        creator = ProjectFileCreator('tutorial')
        creator.add_project_reference('other_tutorial')
        project_reference = '''\t\t<project>other_tutorial</project>\n'''

        expected = test_template.substitute(extra_links="", project_references=project_reference)
        self.assertEqual(expected, str(creator))


if __name__ == '__main__':
    unittest.main()
