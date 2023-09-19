#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     obtain.py
#

import traceback
import os
import subprocess
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont
from tnbits.toolbox.transformer import TX
from tnbits.renderer.freetyperenderer import FreetypeRenderer
from tnbits.renderer.bitmap import *
from tnbits.base.samples import *
from tnbits.deepspace.scrub import *

def obtain(path, fontSize=32):
    """
    TODO: do sorting.
    TODO: do clustering of kern values.
    TODO: connect size to GUI
    TODO: connect output path to GUI
    TODO: create font vector
    TODO: normalize
    TODO: save data as hdf5
    TODO: use Subprocess to batch process fonts.
    * Generate glyph bitmaps.
    * Font-as-a-vector
    """
    paths = collectTrueTypes(path)
    messages = []
    data = {}

    for path in paths:
        familyName = TX.path2FamilyName(path)
        styleName = TX.path2StyleName(path)
        familyDir = TX.path2FamilyDir(path)
        msg = 'Scanning %s (%s)\n' % (familyName, styleName)
        messages.append(msg)
        data[path] = {}
        data[path]['familyName'] = familyName
        data[path]['styleName'] = styleName
        data[path]['familyDir'] = familyDir
        bitmaps, messages = getBitmaps(path, messages, fontSize=fontSize)
        data[path]['bitmaps'] = bitmaps
        kerning, messages = getKerning(path, messages)
        data[path]['kerning'] = kerning

    return data, messages

def getSpacingDict(f, messages):
    return messages

def getKerning(path, messages):
    """
    Gets kerning data from a font and converts it to a numpy array for all
    (expanded) pairs. For more information on kerning see:

    * https://en.wikipedia.org/wiki/Kerning
    * https://www.microsoft.com/typography/OTSPEC/KERN.htm

    TODO: implement for OpenType, GPOS needs to be tested ont OTFs.
    TODO: implement for UFO, see explodeKerning() in
    tnbits.model.toolbox.kerning.buildgroups.
    """
    f = TTFont(path, lazy=True)
    vector = None

    if 'kern' in f:
        # TrueType.
        kernTable = f['kern'].kernTables[0].kernTable
        vector = getKerningVector(kernTable)
        messages.append(str(vector))

    if 'gpos' in f:
        gpos = f['gpos']
        msg = 'GPOS: %s, length is %d\n' % (type(gpos), len(gpos))
        messages.append(msg)

    return vector, messages

def getKerningVector(kernTable):
    """
    TODO: match kern values to freetype pixel size.
    """
    array = []

    for key in sorted(kernTable.keys()):
        (left, right) = key
        value = kernTable[key]
        array.append([left, right, value])

    return np.array(array)

def getBitmaps(path, messages, fontSize=32):
    """
    Passes font to Freetype renderer to extract bitmaps at font size.
    """
    bitmaps = {}
    fr = FreetypeRenderer(path, fontSize)
    maxAbove = 0
    maxBelow = 0
    minWidth = None
    maxWidth = 0

    for glyphName, (_, charCode) in fr.glyphsDict.items():

        try:
            fr.loadGlyphByCharCode(charCode)
        except AssertionError as e:
            msg = 'Failed to load glyph %s, %d' % (glyphName, charCode)
            messages.append((msg, 'error'))
            raise

        bitmap = fr.getInvertedBitmap()
        top = fr.bitmapTop
        baseLine = fr.bitmapBaseLine
        left = fr.bitmapLeft
        width = fr.bitmapWidth
        if width == 0:
            continue

        bitmaps[glyphName] = {'bitmap': bitmap, 'baseLine': baseLine,
                'left': left, 'width': width}

        if top > maxAbove:
            maxAbove = top

        if baseLine > maxBelow:
            maxBelow = baseLine

        if minWidth is None or width < minWidth:
            minWidth = width
        elif width > maxWidth:
            maxWidth = width

    msg = 'Number of bitmaps: %d, max above: %d, max below: %d, minWidth: %d, maxWidth: %d\n' % (len(bitmaps), maxAbove, maxBelow, minWidth, maxWidth)
    messages.append(msg)

    bitmaps = normalize(bitmaps, maxAbove, maxBelow, minWidth, maxWidth)
    return bitmaps, messages

def collectTrueTypes(path, maximum=None):
    """Collects all TTF files inside the folder at path."""
    truetypes = []
    i = 0

    for root, dirs, files in os.walk(path):
        for f in files:
            p = root + '/' + f

            if p.lower().endswith('.ttf'):
                truetypes.append(p)
                i += 1

            if maximum is not None and i >= maximum:
                break

        if maximum is not None and i >= maximum:
            break

    return truetypes

if __name__ == '__main__':
    import tnTestFonts
    familyName = 'Gasket'
    styleName = 'Regular'
    path = tnTestFonts.getFontPath('%s-%s.ttf' % (familyName, styleName))
