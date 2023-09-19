# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     postscriptglyphparser.py
#
#     http://www.dabeaz.com/ply/ply.html#ply_nn6
#
#===========================================================================


class PostscriptGlyphParser(object):
    """Parser for points from postscript glyph source program."""

tokens = (
    'NUMBER', 'MINUS', 'HSTEM', 'VSTEM', 'RMOVETO', 'RRCURVETO', 'HLINETO',
    'VHCURVETO', 'HVCURVETO', 'HHCURVETO', 'VLINETO', 'VVCURVETO', 'RCURVELINE',
)

instructions = []

# Tokens

#t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_MINUS = r'-'
t_HSTEM = r'hstem'
t_VSTEM = r'vstem'
t_RMOVETO = r'rmoveto'
t_RRCURVETO = r'rrcurveto'
t_HLINETO = r'hlineto'
t_HVCURVETO = r'hvcurveto'
t_HHCURVETO = r'hhcurveto'
t_VVCURVETO = r'vvcurveto'
t_VHCURVETO = r'vhcurveto'
t_VLINETO = r'vlineto'
t_RCURVELINE = r'rcurveline'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t\r\n"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

def p_statement_expr(t):
    '''statement : instruction statement
               | instruction'''
    instructions.append(t[1])

def p_number_minus(t):
    'number : MINUS NUMBER'
    t[0] = -t[2]

def p_number_number(t):
    'number : NUMBER'
    t[0] = t[1]

def p_instruction_name(t):
    '''instruction : number number number number number number number number number number number number number number number number number number RRCURVETO
                  | number number number number number number number number number number number number number number number number number number number number RCURVELINE
                  | number number number number number VHCURVETO
                  | number number number number number HVCURVETO
                  | number number number number number HHCURVETO
                  | number number number number number VVCURVETO
                  | number number HSTEM
                  | number number VSTEM
                  | number number RMOVETO
                  | number number HLINETO
                  | number number VLINETO
                  | number HLINETO
                  | number VLINETO
    '''
    if len(t) == 3:
        t[0] = ((t[1],), t[2])
    elif len(t) == 4:
        t[0] = (t[1], t[2]), t[3]
    elif len(t) == 7:
        t[0] = t[1:6], t[6]
    elif len(t) == 20:
        t[0] = t[1:19], t[19]
    elif len(t) == 22:
        t[0] = (t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10],
               t[11], t[12], t[13], t[14], t[15], t[16], t[17], t[18], t[19], t[20]), t[21]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

examples = (
    """   643 100 hstem
          435 111 vstem
          648 605 rmoveto
          -39 -61 -67 -68 -96 -76 -28 26 -14 12 -33 27 74 63 45 49 50 66 rrcurveto
          299 hlineto
          48 34 -2 -4 32 hvcurveto
          113 vlineto
          -5 -33 -35 -2 -49 hhcurveto
          -290 26 hlineto
          26 2 24 4 22 vhcurveto
          -123 hlineto
          4 -22 2 -24 -27 vvcurveto
          -25 -269 vlineto
          -49 -36 2 5 -33 hvcurveto
          -113 vlineto
          4 33 34 2 47 hhcurveto
          240 hlineto
          -29 -40 -25 -29 -35 -31 -13 -11 0 0 -7 -7 -25 18 -15 11 -43 28 -84 -63 rcurveline
    """,
)
"""
          92 -60 77 -60 60 -59 -91 -54 -90 -38 -114 -34 31 -34 19 -27 19 -37 122 44 91 43 88 55 102 64 100 85 70 84 24 29 0 0 4 4 13 14 0 0 6 7 rrcurveto
          32 -92 rmoveto
          -32 -49 -42 -45 -72 -63 -158 -139 -176 -86 -240 -56 26 -33 16 -29 18 -42 152 49 54 20 76 36 60 29 56 33 62 42 34 -34 13 -12 25 -21 76 -61 67 -39 100 -44 rrcurveto
          16 37 20 33 29 38 -142 52 -53 30 -96 88 73 59 61 60 72 81 rrcurveto
          endchar
""",

for index, example in enumerate(examples):
    yacc.parse(example) #@UndefinedVariable

instructions.reverse()
for instruction in instructions:
    print(instruction)
