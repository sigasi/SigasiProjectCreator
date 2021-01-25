"""
    :copyright: (c) 2008-2021 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from SigasiProjectCreator import ConverterHelper
from SigasiProjectCreator.DotF import DotFfileParser


def main():
    ConverterHelper.parse_and_create_project(DotFfileParser.usage, DotFfileParser.parse_file)


if __name__ == '__main__':
    main()
