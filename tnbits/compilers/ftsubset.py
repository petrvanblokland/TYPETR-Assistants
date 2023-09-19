"""Simple front end to the fontTools subsetter.

Supports TTF, OTF, WOFF, possibly even WOFF2.

- subsetFont(fontFile, outFile, charset, options=None, **kwargs)
- charsetByName(charsetName)
"""

import codecs
import logging
from fontTools.subset import Options, Subsetter, load_font, save_font
from fontTools import configLogger


__all__ = ["charsetByName", "subsetFont"]


def charsetByName(charsetName):
    """Given a name for a character set, return a set of unicode values
    (integers). The character set names are how they are supported by Python's
    unicode encoding/decoding infrastructure, so most common code pages
    and character sets are covered:
    https://docs.python.org/2/library/codecs.html#standard-encodings
    """
    ci = codecs.lookup(charsetName)
    unicodes = set()
    for i in range(256):
        try:
            char, length = ci.decode(chr(i))
        except UnicodeDecodeError:
            pass
        else:
            unicodes.add(ord(char))
    return unicodes


def subsetFont(fontFile, outFile, charset, options=None, **kwargs):
    """Subset the font at fontFile and save it at outFile. `charset` is
    the set of characters to retain, and any dependencies. It should be
    a sequence of unicode values (integers).
    """
    if options is None:
        options = Options()
        options.layout_features = ["*"]  # keep all features

    for key, value in kwargs.items():
        if not hasattr(options, key):
            raise TypeError("unknown Options attribute %r" % key)
        setattr(options, key, value)

    configLogger(level=logging.INFO if options.verbose else logging.WARNING)

    subsetter = Subsetter(options=options)

    glyphs = []
    gids = []
    unicodes = charset

    font = load_font(fontFile, options)

    subsetter.populate(glyphs=glyphs, unicodes=unicodes)
    subsetter.subset(font)

    save_font(font, outFile, options)


if __name__ == "__main__":
    import tnTestFonts
    fontFile = tnTestFonts.getFontPath("Condor-Bold.otf")
    outFile = fontFile + '.subset'
    charset = charsetByName("latin1") | charsetByName("macroman")
    subsetFont(fontFile, outFile, charset, verbose=False)
