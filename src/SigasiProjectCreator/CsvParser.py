# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import csv

usage = """usage: %prog project-name csv-file [destination]

destination is the current directory by default
example: %prog MyProjectName filelist.csv
"""


def parse_file(csv_file):
    entries = dict()
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            if row:
                library = row[0].strip()
                path = row[1].strip()
                entries[path] = library
    return entries
