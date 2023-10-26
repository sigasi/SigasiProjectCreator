#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import xml.etree.ElementTree as eT
import os


def parse_xilinx_file(xilinx_file, options=None):
    entries = dict()
    tree = eT.parse(xilinx_file)
    root = tree.getroot()
    schema = '{http://www.xilinx.com/XMLSchema}'

    for f in root.findall('*/' + schema + 'file'):
        if schema + 'type' in f.attrib:
            schema_type = f.attrib[schema + 'type']
            if schema_type == 'FILE_VHDL':  # TODO VHDL only?
                name = os.path.realpath(os.path.abspath(f.attrib[schema + 'name']))
                lib = f.find(schema + 'library')
                library = lib.attrib[schema + 'name'] if (lib is not None) else "work"
                entries[name] = library

    return entries
