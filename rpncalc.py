#   
#   Draft RPN Calculator
#   For assignment 1.1, language structure class
#   an implementation of the PLY - python lex & yacc modules
#
#
#

import ply.lex as lex
import ply.yacc as yacc
from pystack import Stack

# required list of token names
tokens = (
    'NUMBER',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'LPAREN',
    'RPAREN',
    'SIN',
    'COS',
    'TAN',
    'VARIABLE'      # possible addition
)

# regex rules
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_POWER     = r'\^'     # consider allowing both ^ and ** operators
# maybe use reserved words for sin cos tan
# 4/18 seems to be working with this format plus invalid char ignore
t_SIN       = r'[Ss][Ii][Nn]'
t_COS       = r'[Cc][Oo][Ss]'
t_TAN       = r'[Tt][Aa][Nn]'
# this is for a normal calculator
# for RPN white space must be tracked
# as configured now it creates separate tokens when spaces are found
# between numbers
t_ignore    = ' \t'     # ignore tabs and spaces

def t_FLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+'
    # r'[+-]?[0-9]+(\.[0-9]+)?'     # this regex makes all nums floats
    t.value = float(t.value)
    return t
    
def t_NUMBER(t):
    r'\d+'              # regex for 1 or more digits
    t.value = int(t.value) 
    return t

# detects line breaks to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# error handling rule for invalid chars
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# build lexer
lexer = lex.lex()

data = ''' 35 + 48 33 22 11 - 33 sin 12 / 55.55 '''
lexer.input(data)


# lexer.token() goes through the tokens in order

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

zz = Stack()
zz.push(5)
print(zz.top())