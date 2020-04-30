#   
#   Draft RPN Calculator
#   For assignment 1.1, language structure class
#   an implementation of the PLY - python lex & yacc modules
#
#
#

import math
import ply.lex as lex
import ply.yacc as yacc
from pystack import Stack

########################
###### lexer ###########
########################

# basic parameters


tokens = (
    'NUMBER',
    'FLOAT',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',        # not required
    'LPAREN',
    'RPAREN',
    'SIN',
    'COS',
    'TAN'      
)

# regex rules
t_EQUALS    = r'\='
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
def t_SIN(t):
    r'[Ss][Ii][Nn]'
    t.value = 'SIN'
    return t

def t_COS(t):
    r'[Cc][Oo][Ss]'
    t.value = 'COS'
    return t

def t_TAN(t):
    r'[Tt][Aa][Nn]'
    t.value = 'TAN'
    return t

# this is for a normal calculator
# for RPN white space must be tracked (fixed)
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
data = ''' 3 11 + 5 Sin'''
lexer.input(data)


rpnStack = Stack()




# lexer.token() goes through the tokens in order
# this loop prints everything in the lexer

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)



#########################
###### PARSING ##########
#########################

# postfix might not require precedence rules

# parse grammar rules go here
# t[0] is the result, t[1] is the first argument, etc.

names = { }

# left means left associative operators
# right means the opposite, as in unary minus
# the list runs from low to high priority
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )


def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_binop(t):
    '''expression : expression expression PLUS
                  | expression expression MINUS
                  | expression expression TIMES
                  | expression expression DIVIDE'''
    if t[3] == '+'  : t[0] = t[1] + t[2]
    elif t[3] == '-': t[0] = t[1] - t[2]
    elif t[3] == '*': t[0] = t[1] * t[2]
    elif t[3] == '/': t[0] = t[1] / t[2]

def p_expression_trig(t):
    '''expression : expression SIN
                  | expression COS
                  | expression TAN'''
    if t[2] == 'SIN' : t[0] = math.sin(t[1])
    elif t[2] == 'COS' : t[0] = math.cos(t[1])
    elif t[2] == 'TAN' : t[0] = math.tan(t[1])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    '''expression : NUMBER
                  | FLOAT'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


# build parser
parser = yacc.yacc()


# RPN evaluation function?
# probably not needed as yacc will use stack and recursion
# internally to evaluate complex inputs

"""
def RPN(stack, tok):
    if (tok.type() == ('NUMBER' | 'FLOAT')):
        stack.push(tok)
    elif tok.type() == 
 """



# main function loop
while True:
    print("Reverse Polish Notation Calculator (type \'tips\' for information, or ctrl+Z to exit)")
    try:
        s = input(' --> ')   # Use raw_input on Python 2
        if (s == 'tips'):
            print("here are tips")
            continue
        #print(data)
        #s = data
    except EOFError:
        break
    parser.parse(s)
    #break