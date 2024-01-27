# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#
class SimilaritySpacer:

    TAB_WIDTH = 650 # Default tab width.

    def __init__(self, f=None, tabWidth=None):
        """Calculate all values, patterns and similarity caching to guess margins for individual glyphs.
        For reasons of validity, the font itself is not stored in the spacer instance.
        The spacer can be initialize with a font later."""
        
        if f is not None:
            # Initialize the Similarity cache here.
            pass

        self.tabWidth = tabWidth or TAB_WIDTH
        # Generic fixed spacing patterns

        self.fixedLeftMarginPatterns = { # Key is margin, value is list of glyph names
            0:  ('enclosingkeycapcomb',)
        }
        self.fixedRightMarginPatterns = { # Key is right margin, value is list of glyph names
            0:  ('enclosingkeycapcomb',)
        }
        self.fixedWidthPatterns = {
            0: ('cmb|', 'comb|', 'comb-cy|', '.component'), # "|" matches pattern on end of name"
            self.tabWidth: ('.tab|', '.tnum|')
    }

    def getLeftMargin(self, g):
        """Try different strategies to find the width of the glyph:
        - Search by patterns.
        - Similarity check
        """
        for lm, patterns in self.fixedLeftMarginPatterns.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if (pattern.endswith('|') and g.name.endswith(pattern[:-1])) or pattern in g.name:
                    return lm
        # Could not find a valid left margin guess for this glyph.
        return None

    def getRightMargin(self, g):
        """Try different strategies to find the width of the glyph:
        - Search by patterns.
        - Similarity check
        """
        for rm, patterns in self.fixedRightMarginPatterns.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if (pattern.endswith('|') and g.name.endswith(pattern[:-1])) or pattern in g.name:
                    return rm
        # Could not find a valid right margin guess for this glyph.
        return None

    def getWidth(self, g):
        """Try different strategies to find the width of the glyph:
        - Search by patterns.
        - Similarity check
        """
        for width, patterns in self.fixedMarginWidthPatterns.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if (pattern.endswith('|') and g.name.endswith(pattern[:-1])) or pattern in g.name:
                    return width
        # Could not find a valid width guess for this glyph.
        return None

