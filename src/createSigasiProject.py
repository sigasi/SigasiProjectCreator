"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import sys

from SigasiProjectCreator.ProjectCreator import get_project_creator
from SigasiProjectCreator.ProjectOptions import ProjectOptions
from SigasiProjectCreator import CsvParser
from SigasiProjectCreator.DotF import DotFfileParser
from SigasiProjectCreator.HdpProjectParser import HdpParser
from SigasiProjectCreator.XilinxProjectParser import XilinxProjectParser
from SigasiProjectCreator.tcl import ScriptImporter


def main(args):
    get_project_creator(ProjectOptions(args)).create_project()


if __name__ == '__main__':
    main(sys.argv[1:])
