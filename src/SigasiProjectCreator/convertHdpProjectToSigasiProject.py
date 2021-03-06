#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from configparser import ConfigParser

from SigasiProjectCreator import ConverterHelper

usage = """usage: %prog project-name hdp-file [destination]

destination is the current directory by default
example: %prog MyProjectName myproject.hdp
"""


def parse_hdp_file(hdp_file):
    config = ConfigParser()
    config.read(hdp_file)
    entries = config.items("hdl")
    return {lib: path for path, lib in entries}


def main():
    ConverterHelper.parse_and_create_project(usage, parse_hdp_file)


if __name__ == '__main__':
    main()
