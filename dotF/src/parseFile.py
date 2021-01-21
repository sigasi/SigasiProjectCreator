import sys
import os
from antlr4 import *
from DotFLexer import DotFLexer
from DotFParser import DotFParser
from DotFListener import DotFListener
from pip._vendor.requests.api import options

 
class DotFextractListener(DotFListener):
    options = []
    addtolast = False

    def reset(self):
        self.options = []
        self.addtolast = False

    def enterFilename(self, ctx:DotFParser.FilenameContext):
        print("file: " + ctx.getText().rstrip())
        if self.addtolast and self.options.__len__() > 0:
            self.options[-1] += ' ' + ctx.getText().rstrip().strip('"')
        else:
            self.options.append(ctx.getText().rstrip().strip('"'))
        self.addtolast = False
        
    def enterDash_option(self, ctx:DotFParser.Dash_optionContext):
        print("dash: " + ctx.getText().rstrip())
        if self.addtolast and self.options.__len__() > 0:
            self.options[-1] += ' ' + ctx.getText().rstrip()
        else:
            self.options.append(ctx.getText().rstrip())
        self.addtolast = False
        
    def enterPlus_option(self, ctx:DotFParser.Plus_optionContext):
        print("plus: " + ctx.getText().rstrip())
        if self.addtolast and self.options.__len__() > 0:
            self.options[-1] += ' ' + ctx.getText().rstrip()
        else:
            self.options.append(ctx.getText().rstrip())
        self.addtolast = False
    
    def enterContinuation(self, ctx:DotFParser.ContinuationContext):
        print("+/- : add to previous")
        self.addtolast = True
        
    def enterFilecont(self, ctx:DotFParser.FilecontContext):
        print("file: add to previous")
        self.addtolast = True

 
def parse_dotf(filename):
    print('\nParsing file: ' + filename)
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
    if len(sys.argv) > 2:
        parse_dotf(sys.argv[1])
    else:
        parse_dotf("../testfiles/test1.f")
