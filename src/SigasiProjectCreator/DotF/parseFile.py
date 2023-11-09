import sys

from antlr4 import *

from .DotFLexer import DotFLexer
from .DotFListener import DotFListener
from .DotFParser import DotFParser


class DotFextractListener(DotFListener):
    options = []
    addtolast = False

    def add_to_options(self, option):
        if self.addtolast and self.options.__len__() > 0:
            if isinstance(self.options[-1], list):
                self.options[-1].append(option)
            else:
                tmplist = [self.options[-1], option]
                self.options[-1] = tmplist
        else:
            self.options.append(option)
        self.addtolast = False

    def reset(self):
        self.options = []
        self.addtolast = False

    def enterFilename(self, ctx: DotFParser.FilenameContext):
        self.add_to_options(ctx.getText().rstrip().strip('"'))
        self.addtolast = False

    def enterDash_option(self, ctx: DotFParser.Dash_optionContext):
        self.add_to_options(ctx.getText().rstrip())
        self.addtolast = False

    def enterPlus_option(self, ctx: DotFParser.Plus_optionContext):
        self.add_to_options(ctx.getText().rstrip())
        self.addtolast = False

    def enterPlus_option_arg(self, ctx: DotFParser.Plus_optionContext):
        self.addtolast = True
        self.add_to_options(ctx.getText().rstrip())
        self.addtolast = False

    def enterContinuation(self, ctx: DotFParser.ContinuationContext):
        self.addtolast = True

    def enterFilecont(self, ctx: DotFParser.FilecontContext):
        self.addtolast = True


def parse_dotf(filename):
    print(f'\nParsing file: {filename}')
    input_stream = FileStream(filename)
    lexer = DotFLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DotFParser(stream)
    tree = parser.cmd_options()
    extractor = DotFextractListener()
    extractor.options = []
    walker = ParseTreeWalker()
    walker.walk(extractor, tree)
    return extractor.options


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parse_dotf(sys.argv[1])
    else:
        parse_dotf("../../../dotF/testfiles/test1.f")
