# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import csv
import pathlib

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
                path = pathlib.Path(row[1].strip()).absolute().resolve()
                if path in entries:
                    if isinstance(entries[path], list):
                        entries[path].append(library)
                    else:
                        entries[path] = [entries[path], library]
                else:
                    entries[path] = library
    return entries
