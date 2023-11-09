# Generated from DotF.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,52,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,5,0,18,8,0,10,0,12,0,21,9,0,1,1,1,1,3,1,25,8,1,1,1,
        1,1,3,1,29,8,1,1,1,1,1,3,1,33,8,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,
        5,1,6,1,6,3,6,45,8,6,1,6,1,6,1,7,1,7,1,7,1,7,0,0,8,0,2,4,6,8,10,
        12,14,0,1,1,0,6,7,50,0,19,1,0,0,0,2,32,1,0,0,0,4,34,1,0,0,0,6,36,
        1,0,0,0,8,38,1,0,0,0,10,40,1,0,0,0,12,42,1,0,0,0,14,48,1,0,0,0,16,
        18,3,2,1,0,17,16,1,0,0,0,18,21,1,0,0,0,19,17,1,0,0,0,19,20,1,0,0,
        0,20,1,1,0,0,0,21,19,1,0,0,0,22,24,3,4,2,0,23,25,3,6,3,0,24,23,1,
        0,0,0,24,25,1,0,0,0,25,33,1,0,0,0,26,28,3,8,4,0,27,29,3,10,5,0,28,
        27,1,0,0,0,28,29,1,0,0,0,29,33,1,0,0,0,30,33,3,10,5,0,31,33,5,11,
        0,0,32,22,1,0,0,0,32,26,1,0,0,0,32,30,1,0,0,0,32,31,1,0,0,0,33,3,
        1,0,0,0,34,35,5,2,0,0,35,5,1,0,0,0,36,37,5,2,0,0,37,7,1,0,0,0,38,
        39,5,3,0,0,39,9,1,0,0,0,40,41,7,0,0,0,41,11,1,0,0,0,42,44,5,1,0,
        0,43,45,5,10,0,0,44,43,1,0,0,0,44,45,1,0,0,0,45,46,1,0,0,0,46,47,
        5,11,0,0,47,13,1,0,0,0,48,49,5,8,0,0,49,50,5,11,0,0,50,15,1,0,0,
        0,5,19,24,28,32,44
    ]

class DotFParser ( Parser ):

    grammarFileName = "DotF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\\'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "PLUS_OPTION", "DASH_OPTION", 
                      "C_COMMENT", "CC_COMMENT", "FILEPATH", "QUOTED_FILEPATH", 
                      "CONT", "LT", "WS", "NL", "ESC", "SH_COMMENT", "EX_COMMENT" ]

    RULE_cmd_options = 0
    RULE_cmd_option = 1
    RULE_plus_option = 2
    RULE_plus_option_arg = 3
    RULE_dash_option = 4
    RULE_filename = 5
    RULE_continuation = 6
    RULE_filecont = 7

    ruleNames =  [ "cmd_options", "cmd_option", "plus_option", "plus_option_arg", 
                   "dash_option", "filename", "continuation", "filecont" ]

    EOF = Token.EOF
    T__0=1
    PLUS_OPTION=2
    DASH_OPTION=3
    C_COMMENT=4
    CC_COMMENT=5
    FILEPATH=6
    QUOTED_FILEPATH=7
    CONT=8
    LT=9
    WS=10
    NL=11
    ESC=12
    SH_COMMENT=13
    EX_COMMENT=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Cmd_optionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def cmd_option(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DotFParser.Cmd_optionContext)
            else:
                return self.getTypedRuleContext(DotFParser.Cmd_optionContext,i)


        def getRuleIndex(self):
            return DotFParser.RULE_cmd_options

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmd_options" ):
                listener.enterCmd_options(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmd_options" ):
                listener.exitCmd_options(self)




    def cmd_options(self):

        localctx = DotFParser.Cmd_optionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cmd_options)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2252) != 0):
                self.state = 16
                self.cmd_option()
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cmd_optionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def plus_option(self):
            return self.getTypedRuleContext(DotFParser.Plus_optionContext,0)


        def plus_option_arg(self):
            return self.getTypedRuleContext(DotFParser.Plus_option_argContext,0)


        def dash_option(self):
            return self.getTypedRuleContext(DotFParser.Dash_optionContext,0)


        def filename(self):
            return self.getTypedRuleContext(DotFParser.FilenameContext,0)


        def NL(self):
            return self.getToken(DotFParser.NL, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_cmd_option

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmd_option" ):
                listener.enterCmd_option(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmd_option" ):
                listener.exitCmd_option(self)




    def cmd_option(self):

        localctx = DotFParser.Cmd_optionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_cmd_option)
        try:
            self.state = 32
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 22
                self.plus_option()
                self.state = 24
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 23
                    self.plus_option_arg()


                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 26
                self.dash_option()
                self.state = 28
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 27
                    self.filename()


                pass
            elif token in [6, 7]:
                self.enterOuterAlt(localctx, 3)
                self.state = 30
                self.filename()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 4)
                self.state = 31
                self.match(DotFParser.NL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Plus_optionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS_OPTION(self):
            return self.getToken(DotFParser.PLUS_OPTION, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_plus_option

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlus_option" ):
                listener.enterPlus_option(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlus_option" ):
                listener.exitPlus_option(self)




    def plus_option(self):

        localctx = DotFParser.Plus_optionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_plus_option)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(DotFParser.PLUS_OPTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Plus_option_argContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS_OPTION(self):
            return self.getToken(DotFParser.PLUS_OPTION, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_plus_option_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlus_option_arg" ):
                listener.enterPlus_option_arg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlus_option_arg" ):
                listener.exitPlus_option_arg(self)




    def plus_option_arg(self):

        localctx = DotFParser.Plus_option_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_plus_option_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(DotFParser.PLUS_OPTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dash_optionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DASH_OPTION(self):
            return self.getToken(DotFParser.DASH_OPTION, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_dash_option

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDash_option" ):
                listener.enterDash_option(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDash_option" ):
                listener.exitDash_option(self)




    def dash_option(self):

        localctx = DotFParser.Dash_optionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_dash_option)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(DotFParser.DASH_OPTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FilenameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILEPATH(self):
            return self.getToken(DotFParser.FILEPATH, 0)

        def QUOTED_FILEPATH(self):
            return self.getToken(DotFParser.QUOTED_FILEPATH, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_filename

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilename" ):
                listener.enterFilename(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilename" ):
                listener.exitFilename(self)




    def filename(self):

        localctx = DotFParser.FilenameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_filename)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            _la = self._input.LA(1)
            if not(_la==6 or _la==7):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinuationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NL(self):
            return self.getToken(DotFParser.NL, 0)

        def WS(self):
            return self.getToken(DotFParser.WS, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_continuation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinuation" ):
                listener.enterContinuation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinuation" ):
                listener.exitContinuation(self)




    def continuation(self):

        localctx = DotFParser.ContinuationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_continuation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(DotFParser.T__0)
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 43
                self.match(DotFParser.WS)


            self.state = 46
            self.match(DotFParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FilecontContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONT(self):
            return self.getToken(DotFParser.CONT, 0)

        def NL(self):
            return self.getToken(DotFParser.NL, 0)

        def getRuleIndex(self):
            return DotFParser.RULE_filecont

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilecont" ):
                listener.enterFilecont(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilecont" ):
                listener.exitFilecont(self)




    def filecont(self):

        localctx = DotFParser.FilecontContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_filecont)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(DotFParser.CONT)
            self.state = 49
            self.match(DotFParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





