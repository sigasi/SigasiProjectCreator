# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2013 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from optparse import OptionParser
import os


class ArgsAndFileParser:
    def __init__(self, usage):
        self.parser = OptionParser(usage=usage)

    def parse_args(self, args_len, optional_dir=False):
        (options, args) = self.parser.parse_args()

        if len(args) < args_len:
            self.parser.error("incorrect number of arguments")
        if optional_dir:
            self.check_next_arg_is_dir(args, args_len)
        return args

    def check_next_arg_is_dir(self, args, args_len):
        if len(args) > args_len and not os.path.isdir(args[args_len]):
            self.parser.error("destination has to be a folder")

    def parse_args_and_file(self, parse_file):
        args = self.parse_args(2, True)
        project_name = args[0]
        input_file = args[1]
        destination = args[2] if len(args) > 2 else os.getcwd()
        entries = parse_file(input_file)
        return project_name, input_file, destination, entries
