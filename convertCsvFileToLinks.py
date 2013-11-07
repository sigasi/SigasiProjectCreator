#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import os
from SigasiProjectCreator import SigasiProjectCreator
import csv

def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.abspath(entry))
    return filename

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
example: %prog test-proj filelist.csv
"""
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len (args) < 2:
        parser.error("incorrect number of arguments")

    project_name = args[0]
    csv_file = args[1]

    destination = os.getcwd()
    if len (args) > 2:
        destination = args[2]
        if not os.path.isdir(destination):
            parser.error("destination has to be a folder")

    entries = parse_csv_file(csv_file)

    creator = SigasiProjectCreator(project_name, 93)

    for path, library in entries.iteritems():
        file_name=get_file_name(path)
        link_type=2 if os.path.isdir(path) else 1
        creator.add_link(file_name, os.path.abspath(path), link_type)
        creator.add_mapping(file_name, library)

    creator.write(destination)

if __name__ == '__main__':
    main()