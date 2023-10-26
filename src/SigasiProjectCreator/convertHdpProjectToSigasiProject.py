#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from configparser import ConfigParser


def parse_hdp_file(hdp_file, options=None):
    config = ConfigParser()
    config.read(hdp_file)
    entries = config.items("hdl")
    return {lib: path for path, lib in entries}  # TODO HUH? isn't that the other way around?
