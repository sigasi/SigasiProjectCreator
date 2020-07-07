#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from SigasiProjectCreator import CsvParser
from SigasiProjectCreator import ConverterHelper


def main():
    ConverterHelper.parse_and_create_project(CsvParser.usage, CsvParser.parse_file)


if __name__ == '__main__':
    main()
