import pathlib

project_file_parsers = {}


def project_file_parser(key):
    def register(cls):
        project_file_parsers[key] = cls
        return cls

    return register


@project_file_parser('filelist')
class ProjectFileParser:
    """file list"""
    def __init__(self):
        self.library_mapping = dict()
        self.verilog_includes = set()
        self.verilog_defines = []

    def parse_file(self, filename, options):
        # Default parser is no parser: the filename(s) are the HDL files
        self.library_mapping = {pathlib.Path(entry).absolute().resolve(): self.options.worklib
                                for entry in filename}
        return self


def get_parser_for_type(input_type) -> ProjectFileParser:
    assert input_type in project_file_parsers.keys(), f'Invalid input type: {input_type}'
    return project_file_parsers[input_type]
