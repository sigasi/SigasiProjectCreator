"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from SigasiProjectCreator.ProjectCreator import ProjectCreator
from SigasiProjectCreator.ProjectOptions import ProjectOptions


def main():
    ProjectCreator(ProjectOptions()).create_project()


if __name__ == '__main__':
    main()
