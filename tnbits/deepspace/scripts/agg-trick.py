#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------

from freetype import *
import numpy as np
from PIL import Image
from tnTestFonts import getFontPath
from tnbits.base.samples import *

def textProgression(text, filename="Vera.ttf", minSize=9, maxSize=16, hinting=(True, True), gamma=1.5, lcd=False, pixelFraction=64, resolution=72):
    """Renders a text progression of a TrueType font using the FreeType
    library."""

    # FIXME: overflow errors when out of bounds, calculate width and height instead.
    W,H,D = 680, 280, 1
    Z = np.zeros((H,W), dtype=np.ubyte)
    face = Face(filename)
    pen = Vector(5 * pixelFraction, (H-10) * pixelFraction)
    flags = FT_LOAD_RENDER
    print(hinting[0], hinting[1])

    # Horizontal & vertical hinting. Horizontal hinting should probably at
    # least be enabled for training purposes.
    if hinting[1]: flags |= FT_LOAD_FORCE_AUTOHINT
    else:          flags |= FT_LOAD_NO_HINTING

    if hinting[0]: hres, hscale = resolution,    1.0
    else:          hres, hscale = resolution*10, 0.1

    if lcd:
        flags |= FT_LOAD_TARGET_LCD
        Z = np.zeros((H,W,3), dtype=np.ubyte)
        set_lcd_filter(FT_LCD_FILTER_DEFAULT)

    # Builds progression.
    for size in range(minSize, maxSize):
        face.set_char_size(size * pixelFraction, 0, hres, resolution)
        matrix = Matrix(int((hscale) * 0x10000), int((0.0) * 0x10000),
                         int((0.0) * 0x10000), int((1.0) * 0x10000))
        previous = 0
        pen.x = 5 * pixelFraction

        # Iterate over glyphs.
        for current in text:
            face.set_transform(matrix, pen)
            face.load_char(current, flags)
            kerning = face.get_kerning(previous, current, FT_KERNING_UNSCALED)
            pen.x += kerning.x
            glyph = face.glyph
            bitmap = glyph.bitmap
            x, y = glyph.bitmap_left, glyph.bitmap_top
            w, h, p = bitmap.width, bitmap.rows, bitmap.pitch
            buff = np.array(bitmap.buffer, dtype=np.ubyte).reshape((h, p))

            if lcd:
                Z[H-y:H-y+h, x:x+w/3].flat |= buff[:,:w].flatten()
            else:
                Z[H-y:H-y+h, x:x+w].flat |= buff[:,:w].flatten()

            # Steps to next position using advance.
            pen.x += glyph.advance.x
            previous = current

        # New line.
        pen.y -= (size+4) * pixelFraction
        print(pen.x / pixelFraction, pen.y / pixelFraction)

    # Gamma correction
    Z = (Z/255.0)**(gamma)
    Z = ((1-Z)*255).astype(np.ubyte)

    if lcd:
        I = Image.fromarray(Z, mode='RGB')
    else:
        I = Image.fromarray(Z, mode='L')

    name = filename.split('.')[0]
    filename = '%s-gamma(%.1f)-hinting(%d,%d)-lcd(%d).png' % (name,gamma,hinting[0],hinting[1],lcd)
    I.save(filename)

if __name__ == '__main__':
    path = getFontPath('Georgia.ttf')
    text = GLYPHSETS['Lorem ipsum']
    QUICK_BROWN_FOX = "A Quick Brown Fox Jumps Over The Lazy Dog 0123456789"
    textProgression(text[0:69], filename=path, minSize=9, maxSize=20, hinting=(False, False), gamma=1.25, lcd=True)
