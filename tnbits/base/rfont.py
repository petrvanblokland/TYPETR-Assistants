# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    rfont.py

# FIXME: test RFont.
#

def getRoboFontFont(style):
    """Answers the corresponding RoboFont wrapper font for this style. The
    assumption is that the RF font and style share the same naked font
    instance. Style can be another wrapper or a naked instance. This does the
    reverse of nakedStyle(f)"""
    # TODO: Should not be here? Move to RF BaseTool.
    from mojo.roboFont import AllFonts

    for font in AllFonts():
        if font and font.path == style.path:
            return font

    return None

def closeStyle(style):
    font = getRoboFontFont(style)

    if font is not None:
        font.close()

def updateStyle(style):
    """If the parent style of glyph is an open RoboFont font, then broadcast
    the update."""
    # TODO: Should not be here? Move to RF BaseTool.
    font = getRoboFontFont(style)

    if font is not None:
        print('Updating RF style %s, ID is %d' % (style.path, id(style)))
        font.update()

def style2Front(style):
    """Make style the front window and set to current font."""
    # TODO: Should not be here? Move to RF BaseTool.
    font = getRoboFontFont(style)

    if font is not None:
        font.document().getMainWindow().getNSWindow().makeKeyAndOrderFront_(None)

def updateRoboFont(self, style):
    """Update the style in RoboFont, if it is open."""
    roboFontFont = getRoboFontFont(style)

    if roboFontFont is not None:
        roboFontFont.update()

def updateRoboFontGlyph(self, style, glyphName, layerName=None):
    """Update the RoboFont glyph, if it exists."""
    roboFontFont = getRoboFontFont(style)

    if roboFontFont is not None and glyphName in roboFontFont:
        glyph = roboFontFont[glyphName]

        if layerName is not None:
            glyph = glyph.getLayer(layerName)
        if glyph is not None:
            glyph.update()

def saveRoboFont(self, style):
    """Save the style in RoboFont, if it is open, to avoid confusion of
    "saving by external application". """
    roboFontFont = getRoboFontFont(style)

    if roboFontFont is not None: # It is open in RoboFont. Let RF do the saving.
        roboFontFont.save()
    else: # Otherwise save the style directly.
        style.save()

@classmethod
def openRoboFontGlyphWindow(cls, style, glyphName):
    from mojo.UI import OpenGlyphWindow
    font = getRoboFontFont(style)

    if font is None:
        from fontParts.nonelab import RFont
        font = RFont(naked=style)
    if glyphName in font:
        return OpenGlyphWindow(font[glyphName])
    return None
