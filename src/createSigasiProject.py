"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from SigasiProjectCreator import ConverterHelper
from SigasiProjectCreator.ProjectOptions import ProjectOptions


def main():
    parser = ProjectOptions()
    parser.parse_args()
    ConverterHelper.parse_and_create_project()


if __name__ == '__main__':
    main()
