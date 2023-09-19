# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tx.py
#
#    Proof template transformation functions. Calculates dimensions and sets
#    for the proof tool.

def getXOverlay(x, align, width, glyph, scale):
    """Calculates alignment x-value in case of overlay, else just returns
    x."""
    if align == 0:
        xGlyph = x
    elif align == 1:
        xGlyph = x + ((width - glyph.width) / 2) * scale
    elif align == 2:
        xGlyph = x + (width - glyph.width) * scale

    return xGlyph

def getLineHeight(size, leading):
    return size * leading

def getDescenderHeight(style, size, upem):
    return -(style.info.descender * getScale(size, upem))

def getAscenderHeight(style, size, upem):
    return style.info.ascender * getScale(size, upem)

def getCapHeight(style, size, upem):
    return style.info.capHeight * getScale(size, upem)

def scaledWidth(glyphWidth, scale):
    return glyphWidth * scale

def getGlyphWidth(glyphName, size, style):
    """Gets glyph width width in pixel size."""
    glyph = style[glyphName]
    return glyph.width * getScale(size, style.info.unitsPerEm)

def getMaxGlyphWidth(glyphName, sizes, styles, prevGlyphName, flatKernings):
    """Returns the largest width of a glyph across styles."""
    # FIXME: disabling kerning for now.
    maxWidth = 0

    for styleKey, style in styles.items():
        if not glyphName in style:
            continue

        size = sizes[styleKey]
        w = getGlyphWidth(glyphName, size, style)

        '''
        if flatKernings:
            flatKerning = flatKernings[styleKey]

            if prevGlyphName is not None and flatKerning is not None :
                pair = prevGlyphName, glyphName
                if pair in flatKerning:
                    kerning = flatKerning[pair] * getScale(size, upem)
                    w += kerning
        '''

        if w > maxWidth:
            maxWidth = w

    return maxWidth

def getScale(size, upem):
    """Vector size to screen size factor."""
    return size / float(upem)

def getScaledY(y, descenderHeight, margin):
    return h - ((y + descenderHeight - margin) + margin)

def getGlyphPageSets(glyphNames, styles, sizes, pageWidth,
        pageHeight, flatKernings, lineHeight):
    """Returns set of glyphs so each can be fitted on a single page. Assumes
    result must have same order as glyphNames."""
    totalWidth = 0
    totalHeight = lineHeight
    kerning = 0
    prevGlyphName = None
    glyphSets = []
    glyphSet = []

    # Loop through glyphs.
    for glyphName in glyphNames:

        # Calculates the maximum width of a glyph across all styles. Doesn't
        # handle the glyph if it's missing in one of them.
        maxWidth = getMaxGlyphWidth(glyphName, sizes, styles, prevGlyphName,
                flatKernings)

        if maxWidth is None:
            continue

        # This set will cause an overflow on the current line, extend current
        # set or start a new one if page is full.
        if totalWidth + maxWidth >= pageWidth:
            if totalHeight + lineHeight > pageHeight:
                glyphSets.append(glyphSet)
                glyphSet = [glyphName]
                totalHeight = lineHeight
            else:
                totalHeight += lineHeight
                glyphSet.append(glyphName)

            # Recalculate maximum width without kerning.
            prevGlyphName = None
            maxWidth = getMaxGlyphWidth(glyphName, sizes, styles, prevGlyphName, flatKernings)
            totalWidth = maxWidth
        else:
            totalWidth += maxWidth
            glyphSet.append(glyphName)
            prevGlyphName = glyphName

    # Add the remainder.
    if len(glyphSet) > 0:
        glyphSets.append(glyphSet)

    return glyphSets

def getGlyphLineSets(glyphNames, styles, sizes, pageWidth,
        flatKernings):
    """Returns set of glyphs so each can be fitted on a single line. Splits up
    glyphs into sets by calculating the total set width for all styles
    simultaneously, where the total width for each set is smaller than
    `pageWidth`. Assumes result must have same order as glyphNames."""
    #TODO: keep track of kerning.
    totalWidth = 0
    kerning = 0
    prevGlyphName = None
    glyphSets = []
    glyphSet = []
    maxWidths = {}

    # Loop through glyphs.
    for glyphName in glyphNames:
        #  - Calculates the maximum width of a glyph across all styles.
        # - Takes largest width if some are missing.
        # - Doesn't handle the glyph if it's missing in one of them.
        maxWidth = getMaxGlyphWidth(glyphName, sizes, styles, prevGlyphName,
                flatKernings)

        if maxWidth == 0:
            continue

        maxWidths[glyphName] = maxWidth

        # This set will cause an overflow on the current line, flushes to
        # `glyphSets` to start a new set.
        if totalWidth + maxWidth >= pageWidth:
            glyphSets.append(glyphSet)
            glyphSet = [glyphName]
            prevGlyphName = None
            # Recalculates maximum width without kerning.
            maxWidth = getMaxGlyphWidth(glyphName, sizes, styles,
                    prevGlyphName, flatKernings)
            totalWidth = maxWidth
            maxWidths[glyphName] = maxWidth
        else:
            totalWidth += maxWidth
            glyphSet.append(glyphName)
            prevGlyphName = glyphName

    # Add the remainder.
    if len(glyphSet) > 0:
        glyphSets.append(glyphSet)

    return glyphSets, maxWidths
