#   
#   Draft RPN Calculator
#   For assignment 1.1, language structure class
#   an implementation of the PLY - python lex & yacc modules
#
#
#


#  Sample input:
#  3.141 ( 2 3 +) (1.571 sin) * *
#  ~= 15.708



import math
import ply.lex as lex
import ply.yacc as yacc

########################
###### lexer ###########
########################

# basic parameters


tokens = (
    'INT',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER', 
    'SQRT',     
    'SIN',
    'COS',
    'TAN'     
)

# regex rules
t_ignore    = ' \t()\n='     # ignore tabs and spaces

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_POWER     = r'\^' 

def t_SQRT(t):
    r'[Ss][Qq][Rr][Tt]'
    t.value = 'SQRT'
    return t

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

def t_FLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+'
    # r'[+-]?[0-9]+(\.[0-9]+)?'     # this regex makes all nums floats
    t.value = float(t.value)
    return t
    
def t_INT(t):
    r'\d+'              # regex for 1 or more digits
    t.value = int(t.value) 
    return t

# error handling rule for invalid chars
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# build lexer
lexer = lex.lex()

# testing data
data = ''' 3 11 + 5 Sin'''
lexer.input(data)

# lexer.token() goes through the tokens in order when called
# this loop prints everything in the lexer to the console for testing
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)


#########################
###### PARSING ##########
#########################

# left means left associative operators
# right means the opposite, as in unary minus
# the list runs from low to high priority
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# t[0] is the result, t[1] is the first argument, etc.
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
                  | expression expression DIVIDE
                  | expression expression POWER'''
    if t[3] == '+'  : t[0] = t[1] + t[2]
    elif t[3] == '-': t[0] = t[1] - t[2]
    elif t[3] == '*': t[0] = t[1] * t[2]
    elif t[3] == '/': t[0] = t[1] / t[2]
    elif t[3] == '^': t[0] = t[1] ** t[2]

def p_expression_sqrt(t):
    '''expression : expression SQRT'''
    if t[2] == 'SQRT' : t[0] = math.sqrt(t[1])

def p_expression_trig(t):
    '''expression : expression SIN
                  | expression COS
                  | expression TAN'''
    if t[2] == 'SIN' : t[0] = math.sin(t[1])
    elif t[2] == 'COS' : t[0] = math.cos(t[1])
    elif t[2] == 'TAN' : t[0] = math.tan(t[1])

def p_expression_number(t):
    '''expression : INT
                  | FLOAT'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

# build parser
parser = yacc.yacc()

# main function loop
while True:
    print("Reverse Polish Notation Calculator (type \'tips\' for information, or ctrl+Z to exit)")
    try:
        s = input(' --> ')   # Use raw_input on Python 2
        if (s == 'tips'):
            print("This program does calculations in Reverse Polish Notation, also called postfix.")
            print("Operations are binary or unary. This calculator is capable of performing")
            print("add, subtract, multiply, divide, and the basic trig functions sin, cos, and tan.")
            print("Exponents take the form: x y ^ ---> x^y. For square root use \'sqrt\'")
            print("The calculator ignores parentheses, but you may use them for clarity.\n")
            continue
    except EOFError:
        break
    parser.parse(s)