#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import os
import xml.etree.ElementTree as ET

from SigasiProjectCreator import SigasiProjectCreator

def parse_slickEdit_file(slickEdit_file):
    entries = []
    tree = ET.parse(slickEdit_file)
    root = tree.getroot()

    for f in root.findall('Files'):
        process_children(f, entries)
    return entries

def process_children(element, entries):
    for c in element._children:
        if c.tag == 'Folder':
            process_children(c, entries)
        else:
            process_file(c, entries)

def process_folder(folder_element, entries):
    children = []
    process_children(folder_element, children)
#     entries.append({'type':'folder', 'name':folder_element.attrib.get('Name'), 'children':children})

def process_file(file_element, entries):
    entries.append({'type':'file', 'path':file_element.attrib.get('N')})
    
def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.abspath(entry))
    return filename

def main():
    usage = """usage: %prog project-name slick_edit_file [destination]
    
destination is the current directory by default
example: %prog MyProjectName project.vpj
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len (args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    slickEdit_file = args[1]

    destination = os.getcwd()
    if len (args) > 2:
        destination = args[2]
        if not os.path.isdir(destination):
            parser.error("destination has to be a folder")

    entries = parse_slickEdit_file(slickEdit_file)

    sigasProjectFileCreator = SigasiProjectCreator(project_name)
    sigasProjectFileCreator.add_mapping("", "work")
    
    for entry in entries:
        path = entry.get('path')
        sigasProjectFileCreator.add_link(get_file_name(path), path, 1)
        
    sigasProjectFileCreator.write(destination)

if __name__ == '__main__':
    main()
