"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
from SigasiProjectCreator import ProjectCreator
from SigasiProjectCreator.ProjectOptions import ProjectOptions


def main():
    project_options = ProjectOptions()
    ProjectCreator(project_options).create_project()


if __name__ == '__main__':
    main()
