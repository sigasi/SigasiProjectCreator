"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import sys

from SigasiProjectCreator.ProjectCreator import get_project_creator
from SigasiProjectCreator.ProjectOptions import ProjectOptions


def main(args):
    get_project_creator(ProjectOptions(args)).create_project()


if __name__ == '__main__':
    main(sys.argv[1:])
