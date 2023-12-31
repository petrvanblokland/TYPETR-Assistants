# -*- coding: UTF-8 -*-
#
#    FontData mines data in a font..
#
# 
class FontData:
    def __init__(self, f):
        """Build X-ref data from the from. Don't store the font itself, as it may be close by the calling application."""
        self.path = f.path
        # Fins all glyphs that use this glyph as component
        self.base = {} # Key is glyphName. Value is list of component.baseGlyph names
        # Find all diacritics and match them with the referring glyphs.
        self.diacritics = {} # Key is diacritics name. Value is list of glyph names that use this diacritic as component.
        # All glyphs that are in the same cloud of diacritics (affected by the position of the same anchor)
        self.diacriticsCloud = {} # Key is glyhName
        # All glyphs usage of anchors
        self.glyphAnchors = {} # Key is glyphName, Value is dict of ancbhor.name --> (x, y).
        self.anchors = {} # Key is anchor name. Value is list of glyphs that use this anchor
        # Unicode --> Glyph name
        self.unicodes = {} # Key is unicode (if it exists). Value is glyph name.
        for g in f:
            self.base[g.name] = [] # These glyphs have components refering to g.
            if g.name.endswith('cmb') or g.name.endswith('comb'):
                if g.unicode and g.name not in self.diacritics: # Only for real floating diacritics that have a unicode
                    self.diacritics[g.name] = []
        for g in f:
            self.base[g.name] = bb = []
            for component in g.components:
                bb.append(component.baseGlyph)
                if component.baseGlyph in self.diacritics: # Only for real diacritics (that have a unicode)
                    self.diacritics[component.baseGlyph].append(g.name)
                    
            # glyphName --> dict of anchors
            self.glyphAnchors[g.name] = aa = {}
            for a in g.anchors:
                aa[a.name] = a.x, a.y
                # anchorName --> List of glyph that are using it
                if a.name not in self.anchors:
                    self.anchors[a.name] = []
                self.anchors[a.name].append(g.name)
            if g.unicode:
                self.unicodes[g.unicode] = g.name
            
