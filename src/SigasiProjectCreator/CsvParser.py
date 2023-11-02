# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import csv
import pathlib

from SigasiProjectCreator.ProjectFileParser import ProjectFileParser, project_file_parser


@project_file_parser('csv')
class CsvParser(ProjectFileParser):
    """CSV file"""
    def __init__(self):
        super().__init__()

    def parse_file(self, csv_file, options=None):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True)
            for row in reader:
                if row:
                    library = row[0].strip()
                    path = pathlib.Path(row[1].strip()).absolute().resolve()
                    if path in self.library_mapping:
                        if isinstance(self.library_mapping[path], list):
                            self.library_mapping[path].append(library)
                        else:
                            self.library_mapping[path] = [self.library_mapping[path], library]
                    else:
                        self.library_mapping[path] = library
        return self
