#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""

import os
from SigasiProjectCreator import SigasiProjectCreator
import CsvParser as cP


def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.abspath(entry))
    return filename


def main():
    (project_name, destination, entries) = cP.parse_csv_args_and_file()

    creator = SigasiProjectCreator(project_name, 93)

    for path, library in entries.iteritems():
        file_name = get_file_name(path)
        link_type = 2 if os.path.isdir(path) else 1
        creator.add_link(file_name, os.path.abspath(path), link_type)
        creator.add_mapping(file_name, library)

    creator.write(destination)

if __name__ == '__main__':
    main()
