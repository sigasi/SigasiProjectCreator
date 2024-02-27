"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""

import pathlib

from SigasiProjectCreator import abort_if_false
from dataclasses import dataclass

project_file_parsers = {}


@dataclass
class ProjectFileParserResult:
    library_mapping: dict[pathlib.Path, str]
    verilog_includes: set[str]
    verilog_defines: list[str]


def project_file_parser(key):
    def register(cls):
        if isinstance(key, list):
            for my_key in key:
                project_file_parsers[my_key] = cls
        else:
            project_file_parsers[key] = cls
        return cls

    return register


@project_file_parser('filelist')
class ProjectFileParser:
    """file list"""

    def __init__(self):
        pass

    def parse_file(self, filename, options):
        # Default parser is no parser: the filename(s) are the HDL files
        library_mapping = {pathlib.Path(entry).absolute().resolve(): options.work_lib
                           for entry in filename}
        return ProjectFileParserResult(library_mapping, None, None)


def get_parser_for_type(input_type) -> ProjectFileParser:
    abort_if_false(input_type in project_file_parsers.keys(), f'Invalid input type: {input_type}')
    return project_file_parsers[input_type]
