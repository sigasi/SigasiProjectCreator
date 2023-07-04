# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import argparse
import pathlib


class ArgsAndFileParser:
    options = None

    def __init__(self, usage):
        self.parser = argparse.ArgumentParser(prog='SigasiProjectCreator')
        self.parser.add_argument('project_name', help='Project name')
        self.parser.add_argument('input_file', help='Input file or comma-separated list of input files')
        self.parser.add_argument('destination_folder', help='Root folder of created project', type=pathlib.Path,
                                 nargs='?')
        self.parser.add_argument('-l', '--layout', action='store', dest='layout',
                                 choices=['default', 'simulator'], default='default',
                                 help='Project layout: default (in place) or simulator (one folder per library with linked files)')
        self.parser.add_argument('--uvm', help='Add UVM to the project, using UVM from the given install path',
                                 dest='uvm', type=pathlib.Path)
        self.parser.add_argument('--use-uvm-home', help='Add UVM to the project. Sigasi Studio will use the UVM_HOME environment variable to find your UVM installation',
                                 dest='uvmhome', action='store_true')
        self.parser.add_argument('--uvmlib', help='Library in which to compile the UVM package (default `work`)',
                                 dest='uvmlib', default='work')

    def parse_args(self):
        args = self.parser.parse_args()
        if not os.path.isfile(args.input_file):
            self.parser.error('Input file does not exist')
        if args.destination_folder is not None:
            if not args.destination_folder.is_dir():
                self.parser.error('destination folder has to be a folder')
        if args.uvmhome:
            if args.uvm is not None:
                self.parser.error('Conflicting options --uvm and --use-uvm-home used')
            args.uvm = 'ENV-UVM_HOME'
        elif args.uvm is not None:
            if not os.path.isdir(args.uvm):
                self.parser.error(f'UVM home \'{args.uvm}\' must be a folder')
            if not os.path.isfile(os.path.join(args.uvm, 'src/uvm_macros.svh')):
                self.parser.error(f'Could not find uvm_macros.svh in \'{args.uvm}/src\'')
            if not os.path.isfile(os.path.join(args.uvm, 'src/uvm_pkg.sv')):
                self.parser.error(f'Could not find uvm_pkg.sv in \'{args.uvm}/src\'')
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

    @staticmethod
    def get_uvm_option():
        return ArgsAndFileParser.options.uvm, ArgsAndFileParser.options.uvmlib
