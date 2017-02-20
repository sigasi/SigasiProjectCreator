# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

from SigasiProjectCreator import ProjectFileCreator
from string import Template

test_template = Template('''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>tutorial</name>
	<comment></comment>
	<projects>
${project_references}	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.xtext.ui.shared.xtextBuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>com.sigasi.hdt.vhdl.ui.vhdlNature</nature>
		<nature>org.eclipse.xtext.ui.shared.xtextNature</nature>
	</natures>
	<linkedResources>
		<link>
			<name>Common Libraries</name>
			<type>2</type>
			<locationURI>virtual:/virtual</locationURI>
		</link>
		<link>
			<name>Common Libraries/IEEE</name>
			<type>2</type>
			<locationURI>sigasiresource:/vhdl/93/IEEE</locationURI>
		</link>
		<link>
			<name>Common Libraries/IEEE Synopsys</name>
			<type>2</type>
			<locationURI>sigasiresource:/vhdl/93/IEEE%20Synopsys</locationURI>
		</link>
		<link>
			<name>Common Libraries/STD</name>
			<type>2</type>
			<locationURI>sigasiresource:/vhdl/93/STD</locationURI>
		</link>
${extra_links}	</linkedResources>
</projectDescription>''')


class MyTestCase(unittest.TestCase):
    def test_tutorial_project(self):
        creator = ProjectFileCreator('tutorial')
        self.assertEqual(test_template.substitute(extra_links="", project_references=""), str(creator))

    def test_one_link(self):
        creator = ProjectFileCreator('tutorial')
        creator.add_link("test.vhd", "foobar/test.vhd")
        extra_links = '''		<link>
			<name>test.vhd</name>
			<type>1</type>
			<location>foobar/test.vhd</location>
		</link>
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
