# -*- coding: UTF-8 -*-
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
        self.fixedMarginWidthPatterns = {
            0: ('cmb|', 'comb|', 'comb-cy|', '.component'), # "|" matches pattern on end of name"
            self.tabWidth: ('.tab|', '.tnum|')
    }
