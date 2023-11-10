# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import csv
import pathlib
from collections import defaultdict

from SigasiProjectCreator import abort_if_false, is_valid_name
from SigasiProjectCreator.ProjectFileParser import ProjectFileParser, project_file_parser, ProjectFileParserResult


@project_file_parser('csv')
class CsvParser(ProjectFileParser):
    """CSV file"""
    def __init__(self):
        super().__init__()

    def parse_file(self, csv_file, options=None):
        library_mapping = defaultdict(list)
        includes = set()
        defines = []
        with open(csv_file, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True)
            for row in reader:
                if row:
                    library = row[0].strip()
                    if library == '#define':
                        defines.append(row[1].strip())
                    else:
                        path = pathlib.Path(row[1].strip()).absolute().resolve()
                        if library == '#include':
                            includes.add(path)
                        else:
                            abort_if_false(is_valid_name(library), f'Invalid library name: {library}')
                            library_mapping[path].append(library)
        return ProjectFileParserResult(library_mapping, verilog_defines=defines, verilog_includes=includes)
