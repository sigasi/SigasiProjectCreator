#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from configparser import ConfigParser

from SigasiProjectCreator.ProjectFileParser import ProjectFileParser, project_file_parser, ProjectFileParserResult


@project_file_parser('hdp')
class HdpParser(ProjectFileParser):
    """HDP project"""
    def __init__(self):
        super().__init__()

    def parse_file(self, hdp_file, options=None):
        config = ConfigParser()
        config.read(hdp_file)
        entries = config.items("hdl")
        library_mapping = {lib: path for path, lib in entries}  # TODO HUH? isn't that the other way around?
        return ProjectFileParserResult(library_mapping, None, None)
