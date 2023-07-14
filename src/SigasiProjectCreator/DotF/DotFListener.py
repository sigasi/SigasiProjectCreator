# Generated from DotF.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .DotFParser import DotFParser
else:
    from DotFParser import DotFParser

# This class defines a complete listener for a parse tree produced by DotFParser.
class DotFListener(ParseTreeListener):

    # Enter a parse tree produced by DotFParser#cmd_options.
    def enterCmd_options(self, ctx:DotFParser.Cmd_optionsContext):
        pass

    # Exit a parse tree produced by DotFParser#cmd_options.
    def exitCmd_options(self, ctx:DotFParser.Cmd_optionsContext):
        pass


    # Enter a parse tree produced by DotFParser#cmd_option.
    def enterCmd_option(self, ctx:DotFParser.Cmd_optionContext):
        pass

    # Exit a parse tree produced by DotFParser#cmd_option.
    def exitCmd_option(self, ctx:DotFParser.Cmd_optionContext):
        pass


    # Enter a parse tree produced by DotFParser#plus_option.
    def enterPlus_option(self, ctx:DotFParser.Plus_optionContext):
        pass

    # Exit a parse tree produced by DotFParser#plus_option.
    def exitPlus_option(self, ctx:DotFParser.Plus_optionContext):
        pass


    # Enter a parse tree produced by DotFParser#plus_option_arg.
    def enterPlus_option_arg(self, ctx:DotFParser.Plus_option_argContext):
        pass

    # Exit a parse tree produced by DotFParser#plus_option_arg.
    def exitPlus_option_arg(self, ctx:DotFParser.Plus_option_argContext):
        pass


    # Enter a parse tree produced by DotFParser#dash_option.
    def enterDash_option(self, ctx:DotFParser.Dash_optionContext):
        pass

    # Exit a parse tree produced by DotFParser#dash_option.
    def exitDash_option(self, ctx:DotFParser.Dash_optionContext):
        pass


    # Enter a parse tree produced by DotFParser#filename.
    def enterFilename(self, ctx:DotFParser.FilenameContext):
        pass

    # Exit a parse tree produced by DotFParser#filename.
    def exitFilename(self, ctx:DotFParser.FilenameContext):
        pass


    # Enter a parse tree produced by DotFParser#continuation.
    def enterContinuation(self, ctx:DotFParser.ContinuationContext):
        pass

    # Exit a parse tree produced by DotFParser#continuation.
    def exitContinuation(self, ctx:DotFParser.ContinuationContext):
        pass


    # Enter a parse tree produced by DotFParser#filecont.
    def enterFilecont(self, ctx:DotFParser.FilecontContext):
        pass

    # Exit a parse tree produced by DotFParser#filecont.
    def exitFilecont(self, ctx:DotFParser.FilecontContext):
        pass



del DotFParser