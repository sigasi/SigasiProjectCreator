#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import csv
import os
from LibraryMappingFileCreator import LibraryMappingFileCreator
from SigasiProjectCreator import ProjectFileCreator

def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.normpath(entry))
    return filename

def write_project_file(project_name, destination, entries, version=93):
    creator = ProjectFileCreator(project_name, version)
    for location in entries.keys():
        file_name=get_file_name(location)
        link_type=2 if os.path.isdir(file_name) else 1
        creator.add_link(file_name, location, link_type)
    creator.write(destination)

def write_library_mapping_file(destination, entries):
    creator = LibraryMappingFileCreator()
    for path, library in entries.iteritems():
        creator.add_mapping(path, library)
    creator.write(destination)

def parse_csv_file(csv_file):
    entries = dict()
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f,skipinitialspace=True)
        for row in reader:
            library = row[0]
            path = row[1]
            entries[path] = library
    return entries

def main():
    usage = """usage: %prog project-name csv-file [destination]

destination is the current directory by default
example: %prog filelist.csv 
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len (args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    csv_file = args[1]

    destination = os.getcwd()
    if len (args) >= 2:
        destination = args[2]
        if not os.path.isdir(destination):
            parser.error("destination has to be a folder")

    entries = parse_csv_file(csv_file)

    write_project_file(project_name, destination, entries)

    write_library_mapping_file(destination, entries)

if __name__ == '__main__':
    main()