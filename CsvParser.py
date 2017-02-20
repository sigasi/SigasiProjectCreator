# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from optparse import OptionParser
import csv
import os


usage = """usage: %prog project-name csv-file [destination]

destination is the current directory by default
example: %prog test-proj filelist.csv
"""


def parse_csv_file(csv_file):
    entries = dict()
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            library = row[0].strip()
            path = row[1].strip()
            entries[path] = library
    return entries


def parse_csv_args():
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("incorrect number of arguments")
    elif len(args) > 2 and not os.path.isdir(args[2]):
        parser.error("destination has to be a folder")
    return args


def parse_csv_args_and_file():
    args = parse_csv_args()
    project_name = args[0]
    csv_file = args[1]
    destination = args[2] if len(args) > 2 else os.getcwd()
    entries = parse_csv_file(csv_file)
    return project_name, destination, entries
