#!/usr/local/bin/python3

# Jack compiler constants

# Token types
T_KEYWORD       = 0     # keyword e.g. 'class', 'false' etc
T_SYM           = 1     # symbol e.g. '{', '}' etc
T_NUM           = 2     # number e.g. '123' - from 0 to 32767
T_STR           = 3     # string e.g. "hello"
T_ID            = 4     # identifier e.g. 'name', 'id_42'
T_ERROR         = 5     # error in file

# Keywords for token type T_KEYWORD
KW_CLASS        = 'class'
KW_METHOD       = 'method'
KW_FUNCTION     = 'function'
KW_CONSTRUCTOR  = 'constructor'
KW_INT          = 'int'
KW_BOOLEAN      = 'boolean'
KW_CHAR         = 'char'
KW_VOID         = 'void'
KW_VAR          = 'var'
KW_STATIC       = 'static'
KW_FIELD        = 'field'
KW_LET          = 'let'
KW_DO           = 'do'
KW_IF           = 'if'
KW_ELSE         = 'else'
KW_WHILE        = 'while'
KW_RETURN       = 'return'
KW_TRUE         = 'true'
KW_FALSE        = 'false'
KW_NULL         = 'null'
KW_THIS         = 'this'
KW_NONE         = ''

keywords = [KW_CLASS, KW_METHOD, KW_FUNCTION, KW_CONSTRUCTOR, KW_INT, KW_BOOLEAN,
            KW_CHAR, KW_VOID, KW_VAR, KW_STATIC, KW_FIELD, KW_LET, KW_DO, KW_IF,
            KW_ELSE, KW_WHILE, KW_RETURN, KW_TRUE, KW_FALSE, KW_NULL, KW_THIS]

# # Tokens for sample output
tokens = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier']

#Symbols for token type T_SYM
symbols = '{}()[].,;+-*/&|<>=~'

""""Arithmetic command (Add/Sub/Neg/Eq/Gt/Lt/And/Or/Not)"""
arithmetic_symbols = {'+': 'add', '-': 'sub', '&': 'and',\
                    '|': 'or', '<': 'lt', '>': 'gt', '=': 'eq'}

unary_symbols = {'-': 'neg', '~': 'not'}

#Symbol kinds for class and subroutine (Static/Field/Var/Arg)
SK_STATIC = 0 
SK_FIELD = 1
SK_ARG = 2 
SK_VAR = 3

#Segments 
segments = {SK_STATIC: 'static', SK_FIELD: 'this', SK_ARG: 'argument', SK_VAR: 'local', None: 'ERR'}
