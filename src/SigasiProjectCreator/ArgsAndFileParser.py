# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import argparse


class ArgsAndFileParser:
    options = None

    def __init__(self, usage):
        self.parser = argparse.ArgumentParser(prog='SigasiProjectCreator')
        self.parser.add_argument('project_name', help='project name', required=True)
        self.parser.add_argument('input_file', help='input file', required=True)
        self.parser.add_argument('destination_folder', help='root folder of created project', type=pathlib.Path)
        self.parser.add_argument('-l', '--layout', action='store', dest='layout',
                                 choices=['default', 'simulator'], default='default',
                                 help='Project layout: default (in place) or simulator (one folder per library with linked files)')

    def parse_args(self):
        args = self.parser.parse_args()
        if not os.path.isfile(args.input_file):
            self.parser.error("Incorrect number of arguments: given input file does not exist")
        if args.destination_folder is not None:
            if not args.destination_folder.is_dir():
                self.parser.error("destination folder has to be a folder")
        return args

    def parse_args_and_file(self, parse_file):
        args = self.parse_args()
        ArgsAndFileParser.options = args
        destination = args.destination_folder if args.destination_folder is not None else os.getcwd()
        entries = parse_file(args.input_file)
        return args.project_name, args.input_file, destination, entries

    @staticmethod
    def get_layout_option():
        return ArgsAndFileParser.options.layout
