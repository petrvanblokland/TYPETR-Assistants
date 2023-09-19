# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     dict2memetalk.py
#
#    http://www.dabeaz.com/ply/ply.html#ply_nn6
#
from tnbits.toolbox.storage.adict import ADict
from basememe import BaseMemeTool

class Dict2MemeTalk(BaseMemeTool):
    """The Dict2MemeTalk compiles a dictionary with meme information into a meme source.
    It does the reverse of the MemeTalk2Dict class."""

    def compile(self, d):
        if isinstance(d, (ADict, dict)):
            hook = 'compile_%s' % (d.get(self.TYPE))
            return getattr(self, hook)(d)
        elif isinstance(d, (list, tuple)):
            elements = []
            for element in d:
                elements.append(self.compile(element))
            return ' '.join(elements)
        elif isinstance(d, str):
            return d
        return repr(d)

    def compile_meme(self, d):
        instructions = []
        for name, dimension in sorted(d.items()):
            if name == 'type':
                continue
            instructions.append('%s: %s' % (name, self.compile(dimension)))
        return ';\n'.join(instructions)

    def compile_aspect(self, d):
        aspects = []
        name = d.get(self.ATTR_NAME)
        if name is not None:
            aspects.append(name)
        for attribute in d.get(self.ATTR_ATTRIBUTES, []):
            aspects.append('.' + attribute)
        if self.ATTR_SELECTOR in d:
            aspects.append('[%s]' % self.compile(d[self.ATTR_SELECTOR]))
        if self.ATTR_PIXEL in d:
            aspects.append('!%s' % self.compile(d[self.ATTR_PIXEL]))
        if self.ATTR_CONSTRUCTOR in d:
            aspects.append(' { %s }' % self.compile(d[self.ATTR_CONSTRUCTOR]))
        return ''.join(aspects)

    def compile_group(self, d):
        aspects = []
        for aspect in d[self.ATTR_ASPECTS]:
            aspects.append(self.compile(aspect))
        return '( %s )' % ' '.join(aspects)

    def compile_glyph(self, d):
        """Compiling the glyph. Note that we don't make a real distinction between the attributes
        and extension of glyph names. The idea is that either /three.sup exists as a glyph in the style,
        or it is calling a function that actually generates the three superior glyph."""
        parameters = ['/'+d[self.ATTR_NAME]]
        for attribute in d.get(self.ATTR_ATTRIBUTES, []):
            parameters.append('.' + attribute)
        if self.ATTR_POSITION in d:
            parameters.append('@%s' % self.compile(d[self.ATTR_POSITION]))
        if self.ATTR_CONSTRUCTOR in d:
            parameters.append(' { %s }' % self.compile(d[self.ATTR_CONSTRUCTOR]))
        return ''.join(parameters)

    def compile_position(self, d):
        name = d.get(self.ATTR_NAME)
        dimensions = d.get(self.ATTR_DIMENSIONS)
        if name is not None and dimensions is not None:
            constructors = []
            for key, dimension in dimensions.items():
                constructors.append('%s: %s' % (key, self.compile(dimension)))
            return '@%s { %s }' % (name, '; '.join(constructors))
        return ''

    def compile_expression(self, d):
        return '%s %s %s' % (self.compile(d[self.ATTR_EXPRESSION1]), d[self.ATTR_OPERATOR], self.compile(d[self.ATTR_EXPRESSION2]))

# Cache the parser.
dict2MemeTalk = Dict2MemeTalk()
