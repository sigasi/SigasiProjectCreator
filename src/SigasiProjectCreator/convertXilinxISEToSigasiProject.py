#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import xml.etree.ElementTree as eT

from SigasiProjectCreator import ConverterHelper

usage = """usage: %prog project-name Xilinx-file [destination]

destination is the current directory by default
example: %prog MyProjectName project.xise
"""


def parse_xilinx_file(xilinx_file):
    entries = dict()
    tree = eT.parse(xilinx_file)
    root = tree.getroot()
    schema = '{http://www.xilinx.com/XMLSchema}'

    for f in root.findall('*/' + schema + 'file'):
        if schema + 'type' in f.attrib:
            schema_type = f.attrib[schema + 'type']
            if schema_type == 'FILE_VHDL':
                name = f.attrib[schema + 'name']
                lib = f.find(schema + 'library')
                library = lib.attrib[schema + 'name'] if (lib is not None) else "work"
                entries[name] = library

    return entries


def main():
    ConverterHelper.parse_and_create_project(usage, parse_xilinx_file)


if __name__ == '__main__':
    main()
