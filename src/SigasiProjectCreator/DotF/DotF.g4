/**
 * Define a grammar for .f (Dot-f) files used in EDA tools
 * These files contain command line options and potentially comments
 */
grammar DotF;

options {
  language=Python3;
}

cmd_options
	: cmd_option*
	;

cmd_option
	: filename NL
	| filename filecont cmd_option
	| plus_option plus_option_arg* NL
	| plus_option plus_option_arg* continuation cmd_option
	| dash_option NL
	| dash_option continuation cmd_option
	| NL
	;

plus_option: PLUS_OPTION;
plus_option_arg: PLUS_OPTION;
dash_option: DASH_OPTION;

PLUS_OPTION
	: '+' ~[+\\\n]+
	;

DASH_OPTION
	: '-' ~[\\\n]+
	;

filename
	: FILEPATH_CHAR+
	| DQ (FILEPATH_CHAR | ':')+ DQ
	;

continuation
	: '\\' WS? NL
	;

filecont: CONT NL;

FILEPATH_CHAR: [a-zA-Z0-9_/\\.${}*] ;

CONT : WS '\\';

LT : [.,?!] ;

WS : [ \t\r]+ -> skip ; // skip spaces, tabs, newlines

NL : [\n] ;

ESC : [\\] ;

DQ : ["] ;

C_COMMENT : '/*' .*? '*/' -> skip ; // skip C style comments
CC_COMMENT : '//' ~[\n]*  -> skip ; // skip C++ style comments
SH_COMMENT : '#'  ~[\n]*  -> skip ; // skip C++ style comments
EX_COMMENT : '!'  ~[\n]*  -> skip ; // skip exclamation mark comments
