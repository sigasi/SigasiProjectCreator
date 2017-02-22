#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import CsvParser
from SigasiProjectCreator import SigasiProjectCreator
from ArgsAndFileParser import ArgsAndFileParser
from VhdlVersion import VhdlVersion


def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.abspath(entry))
    return filename


def main():
    parser = ArgsAndFileParser(CsvParser.usage)
    (project_name, _, destination, entries) = parser.parse_args_and_file(CsvParser.parse_file)

    creator = SigasiProjectCreator(project_name, VhdlVersion.NINETY_THREE)

    for path, library in entries.iteritems():
        file_name = get_file_name(path)
        link_type = os.path.isdir(path)
        creator.add_link(file_name, os.path.abspath(path), link_type)
        creator.add_mapping(file_name, library)

    creator.write(destination)


if __name__ == '__main__':
    main()
