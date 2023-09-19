# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     memetalk2dict.py
#
#    http://www.dabeaz.com/ply/ply.html#ply_nn6
#

from tnbits.toolbox.transformer import TX
from basememe import BaseMemeTool
import tnbits

DEBUG = False

class MemeTalk2Dict(BaseMemeTool):
    """
    Base class for a lexer/parser that has the rules defined as methods

        >>> m = MemeTalk2Dict()
        >>> m.compile('g: /A')
        {'type': 'meme', 'g': [{'type': 'glyph', 'name': 'A'}]}
        >>> A = '''g: /A;a: @top {x:center; y:top+em//10} @bottom {x:center; y:baseline}'''
        >>> B = '''g: /B;a: @top {x:center; y:top-10}'''
        >>> C = '''g: /C;a: @top {x: center; y: top+em//10} @bottom {x: center; y:baseline.undershoot}'''
        >>> D = '''g: /A;a: @top {x:center; y:top+em//10}'''
        >>> Adieresis = '''g: /Adieresis {/A /dieresis@top}'''
        >>> n = '''g: /n;
        ...     a: @top {x:center; y:top+em//10};
        ...     x: ssb[0]!1 (sstem!1 counter[0] {ssb[0] ssb[1]} sstem!1) rsb[2]!0;
        ...     y: sbaseline.sstem sbasealign.sstem xht!3 xht.overshoot rstem!1
        ... '''
        >>> p = '''g: /p;
        ...     x: ssb[1]!1 (sstem!1 counter[1] {ssb[0] /o.ssb} rstem!1) rsb[2]!0;
        ...     y: sdescentalign basealign.undershoot rstem!1 xht!3 xht.overlap rstem!1
        ... '''
        >>> m.compile(A)
        {'a': [{'type': 'position', 'name': 'top', 'dimensions': {'y': [{'operator': '+', 'e1': {'type': 'aspect', 'name': 'top'}, 'type': 'expression', 'e2': {'operator': '//', 'e1': {'type': 'aspect', 'name': 'em'}, 'type': 'expression', 'e2': 10}}], 'x': [{'type': 'aspect', 'name': 'center'}]}}, {'type': 'position', 'name': 'bottom', 'dimensions': {'y': [{'type': 'aspect', 'name': 'baseline'}], 'x': [{'type': 'aspect', 'name': 'center'}]}}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'A'}]}
        >>> m.compile(B)
        {'a': [{'type': 'position', 'name': 'top', 'dimensions': {'y': [{'type': 'aspect', 'name': 'top'}, {'e': 10, 'type': 'minus'}], 'x': [{'type': 'aspect', 'name': 'center'}]}}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'B'}]}
        >>> m.compile(C)
        {'a': [{'type': 'position', 'name': 'top', 'dimensions': {'y': [{'operator': '+', 'e1': {'type': 'aspect', 'name': 'top'}, 'type': 'expression', 'e2': {'operator': '//', 'e1': {'type': 'aspect', 'name': 'em'}, 'type': 'expression', 'e2': 10}}], 'x': [{'type': 'aspect', 'name': 'center'}]}}, {'type': 'position', 'name': 'bottom', 'dimensions': {'y': [{'attributes': ['undershoot'], 'type': 'aspect', 'name': 'baseline'}], 'x': [{'type': 'aspect', 'name': 'center'}]}}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'C'}]}
        >>> m.compile(D)
        {'a': [{'type': 'position', 'name': 'top', 'dimensions': {'y': [{'operator': '+', 'e1': {'type': 'aspect', 'name': 'top'}, 'type': 'expression', 'e2': {'operator': '//', 'e1': {'type': 'aspect', 'name': 'em'}, 'type': 'expression', 'e2': 10}}], 'x': [{'type': 'aspect', 'name': 'center'}]}}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'A'}]}
        >>> m.compile(Adieresis)
        {'type': 'meme', 'g': [{'type': 'glyph', 'name': 'Adieresis', 'constructor': [{'type': 'glyph', 'name': 'A'}, {'position': 'top', 'type': 'glyph', 'name': 'dieresis'}]}]}
        >>> m.compile(n)
        {'y': [{'attributes': ['sstem'], 'type': 'aspect', 'name': 'sbaseline'}, {'attributes': ['sstem'], 'type': 'aspect', 'name': 'sbasealign'}, {'type': 'aspect', 'name': 'xht', 'pixel': 3}, {'attributes': ['overshoot'], 'type': 'aspect', 'name': 'xht'}, {'type': 'aspect', 'name': 'rstem', 'pixel': 1}], 'a': [{'type': 'position', 'name': 'top', 'dimensions': {'y': [{'operator': '+', 'e1': {'type': 'aspect', 'name': 'top'}, 'type': 'expression', 'e2': {'operator': '//', 'e1': {'type': 'aspect', 'name': 'em'}, 'type': 'expression', 'e2': 10}}], 'x': [{'type': 'aspect', 'name': 'center'}]}}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'n'}], 'x': [{'pixel': 1, 'type': 'aspect', 'name': 'ssb', 'selector': 0}, {'aspects': [{'type': 'aspect', 'name': 'sstem', 'pixel': 1}, {'constructor': [{'type': 'aspect', 'name': 'ssb', 'selector': 0}, {'type': 'aspect', 'name': 'ssb', 'selector': 1}], 'type': 'aspect', 'name': 'counter', 'selector': 0}, {'type': 'aspect', 'name': 'sstem', 'pixel': 1}], 'type': 'group'}, {'pixel': 0, 'type': 'aspect', 'name': 'rsb', 'selector': 2}]}
        >>> m.compile(p)
        {'y': [{'type': 'aspect', 'name': 'sdescentalign'}, {'attributes': ['undershoot'], 'type': 'aspect', 'name': 'basealign'}, {'type': 'aspect', 'name': 'rstem', 'pixel': 1}, {'type': 'aspect', 'name': 'xht', 'pixel': 3}, {'attributes': ['overlap'], 'type': 'aspect', 'name': 'xht'}, {'type': 'aspect', 'name': 'rstem', 'pixel': 1}], 'x': [{'pixel': 1, 'type': 'aspect', 'name': 'ssb', 'selector': 1}, {'aspects': [{'type': 'aspect', 'name': 'sstem', 'pixel': 1}, {'constructor': [{'type': 'aspect', 'name': 'ssb', 'selector': 0}, '/'], 'type': 'aspect', 'name': 'counter', 'selector': 1}, {'type': 'aspect', 'name': 'rstem', 'pixel': 1}], 'type': 'group'}, {'pixel': 0, 'type': 'aspect', 'name': 'rsb', 'selector': 2}], 'type': 'meme', 'g': [{'type': 'glyph', 'name': 'p'}]}
    """
    tokens = ()
    precedence = ()
    # Cache the compiled yacc parser.
    MEMETALK2DICT = None

    def __init__(self, **kw):
        import ply.lex
        import ply.yacc
        import tnbits.toolbox.parsers
        self.names = {}
        self.outputdir = TX.module2Path(tnbits.toolbox.parsers) + '/meme'

        # Build the lexer and parser
        self.lex = ply.lex.lex(module=self, optimize=False, debug=DEBUG, outputdir=self.outputdir)
        self.yacc = ply.yacc.yacc(module=self, optimize=False, debug=DEBUG, outputdir = self.outputdir, write_tables=0)

    @classmethod
    def compile(cls, s):
        if cls.MEMETALK2DICT is None:
            cls.MEMETALK2DICT = MemeTalk2Dict()
        return cls.MEMETALK2DICT.yacc.parse(s or '', debug=DEBUG)

    tokens = (
        'NAME','NUMBER', 'GLYPH', 'PIXEL', 'KEY',
        'POSITION', 'ATTR', 'SEPARATOR',
        'PLUS','MINUS','EXP', 'MULTIPLY','DIVIDE',
        'LPAREN','RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        )

    # Tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EXP = r'\*\*'
    t_MULTIPLY = r'\*'
    t_PIXEL = r'\!'
    t_DIVIDE = r'\/\/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_ATTR = r'\.'
    t_POSITION = r'\@'
    t_GLYPH = r'\/' #  Marker for glyph names
    t_SEPARATOR = r'\;'
    t_KEY = r'\:'
    #t_COMMENT = r'\#[.]*[^\\r\\n'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large", t.value)
            t.value = 0
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','MULTIPLY','DIVIDE'),
        ('left', 'EXP'),
        ('right','UMINUS'),
        )

    def p_meme(self, p):
        '''meme : dimensions
        '''
        p[1][self.ATTR_TYPE] = self.TYPE_MEME # Result is already a dictionary.
        p[0] = p[1]

    def p_dimensions_instruction(self, p):
        'dimensions : dimension'
        # G: aspects
        p[0] = p[1]

    def p_dimensions_divider(self, p):
        'dimensions : dimensions SEPARATOR dimension'
        # G: aspects X: aspects Y: aspects
        for key, dimension in p[1].items():
            p[3][key] = dimension
        p[0] = p[3]

    def p_dimension(self, p):
        'dimension : key statements'
        # G: statement
        p[0] = {p[1]: p[2]} # Key, value

    def p_key(self, p):
        'key : NAME KEY'
        p[0] = p[1]

    def p_statements_statement(self, p):
        'statements : statement'
        p[0] = [p[1]]

    def p_statements_statements(self, p):
        'statements : statements statement'
        p[0] = p[1] + [p[2]] # statement statement statement

    def p_statement_group(self, p):
        'statement : LPAREN statements RPAREN'
        p[0] = dict(type=self.TYPE_GROUP, aspects=p[2])

    def p_statement_aspect(self, p):
        'statement : aspect'
        p[0] = p[1]

    def p_statement_constructor_dimensions(self, p):
        'statement : aspect LBRACE dimensions RBRACE'
        # aspect { x:center; y:top+em//10 }
        p[1][self.ATTR_DIMENSIONS] = p[3] # p[1] Aspect already is a dictionary
        p[0] = p[1]

    def p_statement_constructor_statements(self, p):
        'statement : aspect LBRACE statements RBRACE'
        # aspect { sstem rstem }
        p[1][self.ATTR_CONSTRUCTOR] = p[3] # p[1] Aspect already is a dictionary
        p[0] = p[1]

    def p_statement_expression(self, p):
        'statement : expression'
        p[0] = p[1]

    #   Aspect

    def p_statement_position(self, p):
        'aspect : position'
        p[0] = dict(type=self.TYPE_POSITION, name=p[1])

    def p_aspect_selector(self, p):
        'aspect : selector'
        # sstem
        p[0] = p[1]

    def p_aspect_pixel(self, p):
        'aspect : selector pixel'
        # xht!1
        p[1][self.ATTR_PIXEL] = p[2] # p[1] Aspect already is a dictionary
        p[0] = p[1]

    #   Selectors

    def p_selector_identifier(self, p):
        'selector : identifier'
        # sstem
        p[0] = p[1]

    def p_selector_brackets(self, p):
        'selector : identifier LBRACKET expression RBRACKET'
        # sstem[0]
        p[1][self.ATTR_SELECTOR] = p[3]
        p[0] = p[1]

    #   Identifiers

    def p_identifier_name(self, p):
        'identifier : name'
        # sstem
        p[0] = p[1] # p[1] Name already is a dictionary

    def p_identifier_attributes(self, p):
        'identifier : name attributes'
        # sstem.x
        p[1][self.ATTR_ATTRIBUTES] = p[2] # p[1] Name already is a dictionary
        p[0] = p[1]

    def p_identifier_glyph(self, p):
        'identifier : glyph'
        p[0] = p[1] # p[1] Glyph is a dictionary

    def p_identifier_glyph_attributes(self, p):
        'identifier : glyph attributes'
        # /three.sup
        p[1][self.ATTR_ATTRIBUTES] = p[2]
        p[0] = p[1]

    def p_identifier_position(self, p):
        'identifier : position'
        p[0] = dict(type=self.TYPE_ASPECT, name=p[1])

    #   Glyph

    def p_glyph_name(self, p):
        'glyph : GLYPH name'
        # /Adieresis
        p[2][self.ATTR_TYPE] = self.TYPE_GLYPH
        p[0] = p[2]

    def p_glyph_position(self, p):
        '''glyph : GLYPH name position
        '''
        p[2][self.ATTR_TYPE] = self.TYPE_GLYPH
        p[2][self.ATTR_POSITION] = p[3] # p[1] Position already is a dictionary
        p[0] = p[2]

    def p_glyph_attr(self, p):
        '''glyph : GLYPH name attributes
        '''
        p[2][self.ATTR_TYPE] = self.TYPE_GLYPH
        p[2][self.ATTR_ATTRIBUTES] = p[3] # p[1] Position already is a dictionary
        p[0] = p[1]

    def p_name(self, p):
        'name : NAME'
        p[0] = dict(type=self.TYPE_ASPECT, name=p[1])

    def p_attributes_name(self, p):
        'attributes : ATTR NAME'
        # sstem.x
        p[0] = [p[2]]

    def p_attributes(self, p):
        'attributes : ATTR NAME attributes'
        # /A.analyzer.stems
        p[0] = [p[2]] + p[3]

    def p_expression_name(self, p):
        'expression : name'
        p[0] = p[1]

    def p_expression_arithmetic(self, p):
        '''expression : expression PLUS expression
            | expression MINUS expression
            | expression MULTIPLY expression
            | expression DIVIDE expression
            | expression EXP expression
        '''
        # top + em//2
        p[0] = dict(type=self.TYPE_EXPRESSION, e1=p[1], operator=p[2], e2=p[3])

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = dict(type=self.TYPE_MINUS, e=p[2])

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_pixel(self, p):
        'pixel : PIXEL expression'
        # xht!3  Minimal size in pixels
        p[0] = p[2]

    def p_position(self, p):
        'position : POSITION NAME'
        p[0] = p[2]

    def p_error(self, p):
        if p is not None:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Error: no source")

