# Generated from C:/Users/Wim Meeus/git/SigasiProjectCreator/src/SigasiProjectCreator/DotF\DotF.g4 by ANTLR 4.9.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("Z\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\7\2\24\n\2\f\2\16\2\27\13\2\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\7\3\"\n\3\f\3\16\3%\13\3\3")
        buf.write("\3\3\3\3\3\3\3\7\3+\n\3\f\3\16\3.\13\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3;\n\3\3\4\3\4\3\5\3\5")
        buf.write("\3\6\3\6\3\7\6\7D\n\7\r\7\16\7E\3\7\3\7\6\7J\n\7\r\7\16")
        buf.write("\7K\3\7\5\7O\n\7\3\b\3\b\5\bS\n\b\3\b\3\b\3\t\3\t\3\t")
        buf.write("\3\t\2\2\n\2\4\6\b\n\f\16\20\2\3\4\2\3\3\7\7\2^\2\25\3")
        buf.write("\2\2\2\4:\3\2\2\2\6<\3\2\2\2\b>\3\2\2\2\n@\3\2\2\2\fN")
        buf.write("\3\2\2\2\16P\3\2\2\2\20V\3\2\2\2\22\24\5\4\3\2\23\22\3")
        buf.write("\2\2\2\24\27\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2\26\3")
        buf.write("\3\2\2\2\27\25\3\2\2\2\30\31\5\f\7\2\31\32\7\13\2\2\32")
        buf.write(";\3\2\2\2\33\34\5\f\7\2\34\35\5\20\t\2\35\36\5\4\3\2\36")
        buf.write(";\3\2\2\2\37#\5\6\4\2 \"\5\b\5\2! \3\2\2\2\"%\3\2\2\2")
        buf.write("#!\3\2\2\2#$\3\2\2\2$&\3\2\2\2%#\3\2\2\2&\'\7\13\2\2\'")
        buf.write(";\3\2\2\2(,\5\6\4\2)+\5\b\5\2*)\3\2\2\2+.\3\2\2\2,*\3")
        buf.write("\2\2\2,-\3\2\2\2-/\3\2\2\2.,\3\2\2\2/\60\5\16\b\2\60\61")
        buf.write("\5\4\3\2\61;\3\2\2\2\62\63\5\n\6\2\63\64\7\13\2\2\64;")
        buf.write("\3\2\2\2\65\66\5\n\6\2\66\67\5\16\b\2\678\5\4\3\28;\3")
        buf.write("\2\2\29;\7\13\2\2:\30\3\2\2\2:\33\3\2\2\2:\37\3\2\2\2")
        buf.write(":(\3\2\2\2:\62\3\2\2\2:\65\3\2\2\2:9\3\2\2\2;\5\3\2\2")
        buf.write("\2<=\7\5\2\2=\7\3\2\2\2>?\7\5\2\2?\t\3\2\2\2@A\7\6\2\2")
        buf.write("A\13\3\2\2\2BD\7\7\2\2CB\3\2\2\2DE\3\2\2\2EC\3\2\2\2E")
        buf.write("F\3\2\2\2FO\3\2\2\2GI\7\r\2\2HJ\t\2\2\2IH\3\2\2\2JK\3")
        buf.write("\2\2\2KI\3\2\2\2KL\3\2\2\2LM\3\2\2\2MO\7\r\2\2NC\3\2\2")
        buf.write("\2NG\3\2\2\2O\r\3\2\2\2PR\7\4\2\2QS\7\n\2\2RQ\3\2\2\2")
        buf.write("RS\3\2\2\2ST\3\2\2\2TU\7\13\2\2U\17\3\2\2\2VW\7\b\2\2")
        buf.write("WX\7\13\2\2X\21\3\2\2\2\n\25#,:EKNR")
        return buf.getvalue()


class DotFParser ( Parser ):

    grammarFileName = "DotF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'\\'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "PLUS_OPTION", 
                      "DASH_OPTION", "FILEPATH_CHAR", "CONT", "LT", "WS", 
                      "NL", "ESC", "DQ", "C_COMMENT", "CC_COMMENT", "SH_COMMENT", 
                      "EX_COMMENT" ]

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
    T__1=2
    PLUS_OPTION=3
    DASH_OPTION=4
    FILEPATH_CHAR=5
    CONT=6
    LT=7
    WS=8
    NL=9
    ESC=10
    DQ=11
    C_COMMENT=12
    CC_COMMENT=13
    SH_COMMENT=14
    EX_COMMENT=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.1")
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
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DotFParser.PLUS_OPTION) | (1 << DotFParser.DASH_OPTION) | (1 << DotFParser.FILEPATH_CHAR) | (1 << DotFParser.NL) | (1 << DotFParser.DQ))) != 0):
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

        def filename(self):
            return self.getTypedRuleContext(DotFParser.FilenameContext,0)


        def NL(self):
            return self.getToken(DotFParser.NL, 0)

        def filecont(self):
            return self.getTypedRuleContext(DotFParser.FilecontContext,0)


        def cmd_option(self):
            return self.getTypedRuleContext(DotFParser.Cmd_optionContext,0)


        def plus_option(self):
            return self.getTypedRuleContext(DotFParser.Plus_optionContext,0)


        def plus_option_arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DotFParser.Plus_option_argContext)
            else:
                return self.getTypedRuleContext(DotFParser.Plus_option_argContext,i)


        def continuation(self):
            return self.getTypedRuleContext(DotFParser.ContinuationContext,0)


        def dash_option(self):
            return self.getTypedRuleContext(DotFParser.Dash_optionContext,0)


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
        self._la = 0 # Token type
        try:
            self.state = 56
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 22
                self.filename()
                self.state = 23
                self.match(DotFParser.NL)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 25
                self.filename()
                self.state = 26
                self.filecont()
                self.state = 27
                self.cmd_option()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 29
                self.plus_option()
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DotFParser.PLUS_OPTION:
                    self.state = 30
                    self.plus_option_arg()
                    self.state = 35
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 36
                self.match(DotFParser.NL)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 38
                self.plus_option()
                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DotFParser.PLUS_OPTION:
                    self.state = 39
                    self.plus_option_arg()
                    self.state = 44
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 45
                self.continuation()
                self.state = 46
                self.cmd_option()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 48
                self.dash_option()
                self.state = 49
                self.match(DotFParser.NL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 51
                self.dash_option()
                self.state = 52
                self.continuation()
                self.state = 53
                self.cmd_option()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 55
                self.match(DotFParser.NL)
                pass


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
            self.state = 58
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
            self.state = 60
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
            self.state = 62
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

        def FILEPATH_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(DotFParser.FILEPATH_CHAR)
            else:
                return self.getToken(DotFParser.FILEPATH_CHAR, i)

        def DQ(self, i:int=None):
            if i is None:
                return self.getTokens(DotFParser.DQ)
            else:
                return self.getToken(DotFParser.DQ, i)

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
            self.state = 76
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DotFParser.FILEPATH_CHAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 65 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 64
                    self.match(DotFParser.FILEPATH_CHAR)
                    self.state = 67 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==DotFParser.FILEPATH_CHAR):
                        break

                pass
            elif token in [DotFParser.DQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.match(DotFParser.DQ)
                self.state = 71 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 70
                    _la = self._input.LA(1)
                    if not(_la==DotFParser.T__0 or _la==DotFParser.FILEPATH_CHAR):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 73 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==DotFParser.T__0 or _la==DotFParser.FILEPATH_CHAR):
                        break

                self.state = 75
                self.match(DotFParser.DQ)
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
            self.state = 78
            self.match(DotFParser.T__1)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DotFParser.WS:
                self.state = 79
                self.match(DotFParser.WS)


            self.state = 82
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
            self.state = 84
            self.match(DotFParser.CONT)
            self.state = 85
            self.match(DotFParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





