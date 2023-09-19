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
#     explore.py
#


from drawBot import *
import numpy

def histogram(data):
    """TODO: should visualize data as a histogram."""
    pass

def cluster(data):
    """TODO: should cluster data using unsupervised learning."""
    pass

def scatter(data):
    """TODO: should create scatter plots, for example sorted size versus pair,
    kerning versus spacing, etc."""
    pass

def splitKerningPairs(kerning):
    """Splits kerning pairs into sorted sets of left and right glyph names."""
    left = set()
    right = set()
    left.update([l for l in kerning[:, 0]])
    right.update([r for r in kerning[:, 1]])
    left = sorted(left, reverse=True)
    right = sorted(right)
    return left, right

def exploreKerning(data):
    """Draws version of kerning map for TrueType fonts."""
    messages = []

    if data is None:
        return

    for path in data:
        kerning = data[path]['kerning']
        if kerning is None:
            continue

        left, right = splitKerningPairs(kerning)
        w, h, margin = 800, 600, 10
        width = w - 2 * margin
        height = h - 2 * margin
        glyphNameMargin = 40
        labelFontSize = 3.5
        labelMargin = 3
        zoom = 3
        hScale = float(width) / (len(right) * zoom + glyphNameMargin)
        vScale = float(height) / (len(left) * zoom + glyphNameMargin)

        newDrawing()
        newPage(w, h)
        save()
        translate(margin, margin)
        s = min(hScale, vScale)
        scale(s)
        #fill(None)
        #stroke(0)
        #rect(0, 0, len(right) * 3, len(left) * 3)
        kerningDict = {}
        minValue = 0.0
        maxValue = 0.0
        squareSize = 3

        # Dumps pairs as a dictionary for fast lookup.
        for row in kerning:
            l, r, value = row
            value = int(value)
            pair = (l, r)
            kerningDict[pair] = value

            if value < minValue:
                minValue = float(value)
            elif value > maxValue:
                maxValue = float(value)

        # Loops over rows and columns.
        for i, glyphName1 in enumerate(left):
            y = i * zoom

            for j, glyphName2 in enumerate(right):
                x = j * zoom
                stroke(0.75)
                strokeWidth(0.2)
                line((x, 0), (x, height - glyphNameMargin))
                #line((x, margin), (x, height - glyphNameMargin))
                stroke(None)
                pair = glyphName1, glyphName2

                if pair in kerningDict:
                    # Calculates the kerning color and draw the color rect.
                    value = kerningDict[pair]

                    if value < 0:
                        percentage = value / (minValue / 100)
                        g = b = (percentage / 100)
                        fill(1, g, b)
                    elif value > 0:
                        percentage = value / (maxValue / 100)
                        r = b = (percentage / 100)
                        fill(r, 1, b)

                    rect(x, y, squareSize, squareSize)

            # Draws the left hand names.
            fill(0.5, 0.5, 0)
            fontSize(labelFontSize)
            text(glyphName1, (len(right) * zoom + labelMargin, y))

        # Rotates the glyph names at the top.
        translate(0, len(left) * zoom)
        rotate(90)
        fill(0, 0.5, 0.5)
        fontSize(labelFontSize)

        # Draws right hand names.
        for j, glyphName2 in enumerate(right):
            y = j * zoom
            stroke(0.75)
            strokeWidth(0.2)
            line((y, 0), (y, width - glyphNameMargin))
            stroke(None)
            text(glyphName2, (labelMargin, -3 -j*zoom))

        restore()
        familyName = data[path]['familyName']
        familyDir = data[path]['familyDir']
        styleName = data[path]['styleName']
        fileName = '%s/kerningMap-%s-%s.pdf' % (familyDir, familyName, styleName)
        saveImage(fileName)
        print('saved %s' % fileName)
