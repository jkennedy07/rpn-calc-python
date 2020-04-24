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
    'POWER',        # not required
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
                        # exponents are not required functionality
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

# testing data
data = ''' 35 + 48 33 22 -11 - 33 sin 12 / 55.55 '''
lexer.input(data)


rpnStack = Stack()




# lexer.token() goes through the tokens in order
# this loop prints everything in the lexer
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

### PARSING ###


# postfix might not require precedence rules


# parse grammar rules go here
# t[0] is the result, t[1] is the first argument, etc.

### Below taken from sample calc #############
##############################################

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)










##############################################


# build parser
# parser = yacc.yacc()

# RPN evaluation function






"""
def RPN(stack, tok):
    if (tok.type() == ('NUMBER' | 'FLOAT')):
        stack.push(tok)
    elif tok.type() == 
 """













# main function loop
""" while True:
    print("Reverse Polish Notation Calculator (type \"help\" for more information)")
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s) """