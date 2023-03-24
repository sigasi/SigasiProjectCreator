#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os

from SigasiProjectCreator.Creator import SigasiProjectCreator
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser
from SigasiProjectCreator import CsvParser
from SigasiProjectCreator import VhdlVersion


def get_file_name(entry):
    (folder, filename) = os.path.split(os.path.abspath(entry))
    return filename


def main():
    parser = ArgsAndFileParser(CsvParser.usage)
    (project_name, _, destination, entries) = parser.parse_args_and_file(CsvParser.parse_file)

    creator = SigasiProjectCreator(project_name, VhdlVersion.NINETY_THREE)

    for path, library in entries.items():
        file_name = get_file_name(path)
        link_type = os.path.isdir(path)
        creator.add_link(file_name, os.path.abspath(path), link_type)
        creator.add_mapping(file_name, library)

    creator.write(destination, force_vunit=True)


if __name__ == '__main__':
    main()
