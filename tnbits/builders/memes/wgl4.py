# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     wgl4.py
#

from math import sqrt
from tnbits.analyzers.analyzermanager import analyzerManager

def roundP(px, py):
    return round(px), round(py)

def rect(pen, x, y, w, h):
    pen.moveTo(roundP(x, y))
    pen.lineTo(roundP(x, y+h))
    pen.lineTo(roundP(x+w, y+h))
    pen.lineTo(roundP(x+w, y))
    pen.closePath()

def rrect(pen, x, y, w, h):
    # Reverse rectangle (for counters)
    pen.moveTo(roundP(x, y))
    pen.lineTo(roundP(x+w, y))
    pen.lineTo(roundP(x+w, y+h))
    pen.lineTo(roundP(x, y+h))
    pen.closePath()

class Memes(object):

    # TODO: Should be normalized to em size.
    MARGIN_SMALL = 32
    MARGIN_MEDIUM = 64
    OPTICAL = 16
    OVERSHOOT = 24

    def __init__(self):
        self.marginSmall = self.MARGIN_SMALL
        self.marginMedium = self.MARGIN_MEDIUM
        self.optical = self.OPTICAL
        self.overshoot = self.OVERSHOOT

    def getBarWidth(self, style):
        """Get the bar with of hyphen, endash, macro, etc."""
        sa = analyzerManager.getStyleAnalyzer(style=style)
        for c in ('hyphen', 'endash', 'emdash', 'macron'):
            if c in style:
                _, y1, _, y2 = sa[c].boundings
                if y1 is not None and y2 is not None:
                    return abs(y2 - y1)
        return None

    #   Arrows

    def meme_arrowleft(self, glyph, pen):
        """Build left arrow."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh  - bar)*0.3
        my = xh/2  +  self.optical
        indent = 0.8 # Indent factor of arrowHead
        length = style.info.capHeight

        pen.moveTo(roundP(0, my))
        pen.lineTo(roundP(arrowHead, my + arrowHead))
        pen.lineTo(roundP(arrowHead*indent, my + bar2))
        pen.lineTo(roundP(length, my + bar2))
        pen.lineTo(roundP(length, my - bar2))
        pen.lineTo(roundP(arrowHead*indent, my - bar2))
        pen.lineTo(roundP(arrowHead, my - arrowHead))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_arrowright(self, glyph, pen):
        """Build right arrow."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh   -  bar)*0.3
        my = xh/2  +  self.optical
        indent = 0.8
        length = style.info.capHeight

        pen.moveTo(roundP(0, my - bar2))
        pen.lineTo(roundP(0, my + bar2))
        pen.lineTo(roundP(length - arrowHead*indent, my + bar2))
        pen.lineTo(roundP(length - arrowHead, my + arrowHead))
        pen.lineTo(roundP(length, my))
        pen.lineTo(roundP(length - arrowHead, my - arrowHead))
        pen.lineTo(roundP(length - arrowHead*indent, my - bar2))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_arrowup(self, glyph, pen):
        """Build up arrow."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh   -  bar)*0.3
        indent = 0.8 # Indent factor of arrowHead
        length = style.info.capHeight

        pen.moveTo(roundP( - bar2, 0))
        pen.lineTo(roundP( - bar2, length - arrowHead*indent))
        pen.lineTo(roundP( - arrowHead, length - arrowHead))
        pen.lineTo(roundP(0, length))
        pen.lineTo(roundP(arrowHead, length - arrowHead))
        pen.lineTo(roundP(arrowHead, length - arrowHead))
        pen.lineTo(roundP(bar2, length - arrowHead*indent))
        pen.lineTo(roundP(bar2, 0))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_arrowdown(self, glyph, pen):
        """Build down arrow."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh  - bar)*0.3
        my = xh/2  +  self.optical
        indent = 0.8 # Indent factor of arrowHead
        length = style.info.capHeight

        pen.moveTo(roundP(0, 0))
        pen.lineTo(roundP( - arrowHead, arrowHead))
        pen.lineTo(roundP( - bar2, arrowHead*indent))
        pen.lineTo(roundP( - bar2, length))
        pen.lineTo(roundP(bar2, length))
        pen.lineTo(roundP(bar2, arrowHead*indent))
        pen.lineTo(roundP(arrowHead, arrowHead))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_arrowboth(self, glyph, pen):
        """Build left - right."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh  - bar)*0.3
        my = xh/2  +  self.optical
        indent = 0.8 # Indent factor of arrowHead
        length = style.info.capHeight

        pen.moveTo(roundP(arrowHead, my - arrowHead))
        pen.lineTo(roundP(0, my))
        pen.lineTo(roundP(arrowHead, my + arrowHead))
        pen.lineTo(roundP(arrowHead*indent, my + bar2))
        pen.lineTo(roundP(length - arrowHead*indent, my + bar2))
        pen.lineTo(roundP(length - arrowHead, my + arrowHead))
        pen.lineTo(roundP(length, my))
        pen.lineTo(roundP(length - arrowHead, my - arrowHead))
        pen.lineTo(roundP(length - arrowHead*indent, my - bar2))
        pen.lineTo(roundP(arrowHead*indent, my - bar2))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_arrowupdn(self, glyph, pen):
        """Build arrow up - down."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        bar2 = bar/2
        arrowHead = bar + (xh  - bar)*0.3
        indent = 0.8 # Indent factor of arrowHead
        length = style.info.capHeight

        pen.moveTo(roundP(0, 0))
        pen.lineTo(roundP( - arrowHead, arrowHead))
        pen.lineTo(roundP( - bar2, arrowHead * indent))
        pen.lineTo(roundP( - bar2, length - arrowHead * indent))
        pen.lineTo(roundP( - arrowHead, length - arrowHead))
        pen.lineTo(roundP(0, length))
        pen.lineTo(roundP(arrowHead, length - arrowHead))
        pen.lineTo(roundP(arrowHead, length - arrowHead))
        pen.lineTo(roundP(bar2, length - arrowHead * indent))
        pen.lineTo(roundP(bar2, arrowHead * indent))
        pen.lineTo(roundP(arrowHead, arrowHead))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    #   Boxes

    def meme_fullblock(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        descender = style.info.descender
        rect(pen, 0, descender, em, em)
        glyph.leftMargin = glyph.rightMargin = 0

    def meme_dnhalfblock(self, glyph, pen):
        # 0x2584
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        descender = style.info.descender
        rect(pen, 0, descender, em, em/2)
        glyph.leftMargin = glyph.rightMargin = 0

    def meme_lefthalfblock(self, glyph, pen):
        # 0x258C
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        descender = style.info.descender
        rect(pen, 0, descender, em/2, em)
        glyph.leftMargin = glyph.rightMargin = 0


    def meme_blacksmallsquare(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        h = style.info.xHeight
        my = h/2 + self.optical
        rect(pen, 0, my-h/8, h/4, h/4)
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    def meme_blacksquare(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        h = style.info.xHeight
        my = h/2 + self.optical
        rect(pen, 0, my-h/4, h/2, h/2)
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    def meme_whitesquare(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        h = style.info.xHeight
        my = h/2 + self.optical
        rect(pen, -bar, my-h/4-bar, h/2+2*bar, h/2+2*bar)
        rrect(pen, 0, my-h/4, h/2, h/2)
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    def meme_whitesmallsquare(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        h = style.info.xHeight
        my = h/2 + self.optical
        rect(pen, -bar, my-h/8-bar, h/4+2*bar, h/4+2*bar)
        rrect(pen, 0, my-h/8, h/4, h/4)
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    def meme_blackuppointingtriangle(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        h = style.info.capHeight + self.overshoot
        w = h*2/sqrt(3)
        pen.moveTo(roundP(0, 0))
        pen.lineTo(roundP(w, 0))
        pen.lineTo(roundP(w/2, h))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    def meme_blackdownpointingtriangle(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        h = style.info.capHeight
        w = (h+self.overshoot)*2/sqrt(3)
        pen.moveTo(roundP(0, h))
        pen.lineTo(roundP(w, h))
        pen.lineTo(roundP(w/2, -self.overshoot))
        pen.closePath()
        glyph.leftMargin = glyph.rightMargin = self.marginSmall

    #   Graphic boxes (Light)

    def meme_lightvertbxd(self, glyph, pen):
        # Unicode 0x2502
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em)
        glyph.width = em

    def meme_lightverthorzbxd(self, glyph, pen):
        # Unicode 0x253C
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em, bar2)
        glyph.width = em

    def meme_lightvertleftbxd(self, glyph, pen):
        # Unicode 0x2524
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lightvertrightbxd(self, glyph, pen):
        # Unicode 0x251C
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em)
        rect(pen, em/2, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lightuprightbxd(self, glyph, pen):
        # Unicode 0x2514
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender+em/2-bar2/2, bar2, em/2+bar2/2)
        rect(pen, em/2, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lightupleftbxd(self, glyph, pen):
        # Unicode 0x2518
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender+em/2, bar2, em/2+bar2/2)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em/2+bar2/2, bar2)
        glyph.width = em

    def meme_lightuphorzbxd(self, glyph, pen):
        # Unicode 0x2534
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender+em/2-bar2/2, bar2, em/2+bar2/2)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em, bar2)
        glyph.width = em

    def meme_lightdnleftbxd(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em/2+bar2/2)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lighthorzbxd(self, glyph, pen):
        # Unicode 0x2500
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, 0, style.info.descender+em/2-bar2/2, em, bar2)
        glyph.width = em

    def meme_lightdnrightbxd(self, glyph, pen):
        # Unicode 0x250C
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em/2+bar2/2)
        rect(pen, em/2, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lightdnlefttbxd(self, glyph, pen):
        # Unicode 0x2510
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender, bar2, em/2+bar2/2)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em/2, bar2)
        glyph.width = em

    def meme_lightdnhorzbxd(self, glyph, pen):
        # Unicode 0x2510
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar2 = self.getBarWidth(style)/2 # Make it light
        rect(pen, em/2-bar2/2, style.info.descender-bar2/2, bar2, em/2+bar2/2)
        rect(pen, 0, style.info.descender+em/2-bar2/2, em, bar2)
        glyph.width = em

    # Graphic boxes (doubles)

    def meme_dblhorzbxd(self, glyph, pen):
        # Unicode 0x2550
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar = self.getBarWidth(style)
        rect(pen, 0, style.info.descender+em/2+bar*3/2, em, bar)
        rect(pen, 0, style.info.descender+em/2-bar/2, em, bar)
        glyph.width = em

    def meme_dblvertbxd(self, glyph, pen):
        # Unicode 0x02551
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar = self.getBarWidth(style)
        rect(pen, em/2-bar/2, style.info.descender, bar, em)
        rect(pen, em/2+bar*3/2, style.info.descender, bar, em)
        glyph.width = em

    def meme_dbldnhorzbxd(self, glyph, pen):
        # Unicode 0x2566
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar = self.getBarWidth(style)
        rect(pen, 0, style.info.descender+em/2+bar*3/2, em, bar)
        rect(pen, 0, style.info.descender+em/2-bar/2, em/2-bar/2, bar)
        rect(pen, em/2+bar/2, style.info.descender+em/2-bar/2, em/2-bar/2, bar)
        rect(pen, em/2-bar*3/2, style.info.descender, bar, em/2-bar/2)
        rect(pen, em/2+bar/2, style.info.descender, bar, em/2-bar/2)
        glyph.width = em

    def meme_dbldnleftbxd(self, glyph, pen):
        # Unicode 0x2566
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar = self.getBarWidth(style)
        rect(pen, 0, style.info.descender+em/2+bar*3/2, em/2+bar*3/2, bar)
        rect(pen, 0, style.info.descender+em/2-bar/2, em/2-bar/2, bar)
        rect(pen, em/2-bar*3/2, style.info.descender, bar, em/2-bar/2)
        rect(pen, em/2+bar/2, style.info.descender, bar, em/2+bar*3/2)
        glyph.width = em

    def meme_dbldnrightbxd(self, glyph, pen):
        # Unicode 0x2554
        glyph.clear()
        style = glyph.font
        em = style.info.unitsPerEm
        bar = self.getBarWidth(style)
        rect(pen, em/2-bar*3/2, style.info.descender+em/2+bar*3/2, em/2+bar*3/2, bar)
        rect(pen, em/2+bar/2, style.info.descender+em/2-bar/2, em/2-bar/2, bar)
        rect(pen, em/2-bar*3/2, style.info.descender, bar, em/2+bar*3/2)
        rect(pen, em/2+bar/2, style.info.descender, bar, em/2+bar/2)
        glyph.width = em


    #   Greek

    def meme_anoteleia(self, glyph, pen):
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        bar2 = bar/2
        xh = style.info.xHeight
        my = xh/2 + self.optical
        rect(pen, -bar2, my+bar2, bar, bar)
        glyph.leftMargin = glyph.rightMargin = self.marginSmall
        glyph.unicode = 0x0387

    #   Math

    def meme_equal(self, glyph, pen):
        """Build equal sign."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        my = xh/2 + self.optical
        length = style.info.capHeight * 0.75
        rect(pen, 0, my - 1.5*bar, length, bar)
        rect(pen, 0, my + bar/2, length, bar)

        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_minus(self, glyph, pen):
        """Build equal sign."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        my = xh/2 + self.optical
        length = style.info.capHeight * 0.75
        rect(pen, 0, my - bar/2, length, bar)
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_equivalence(self, glyph, pen):
        """Build equal sign."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        my = xh/2 + self.optical
        length = style.info.capHeight * 0.75
        rect(pen, 0, my - bar/2, length, bar)
        rect(pen, 0, my - 2*bar, length, bar)
        rect(pen, 0, my + 2*bar, length, bar)
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_minus(self, glyph, pen):
        """Build equal sign."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        my = xh/2 + self.optical
        length = style.info.capHeight * 0.75
        rect(pen, 0, my - bar, length, bar)
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    def meme_plus(self, glyph, pen):
        """Build equal sign."""
        glyph.clear()
        style = glyph.font
        bar = self.getBarWidth(style)
        xh = style.info.xHeight
        my = xh/2 + self.optical
        length = style.info.capHeight * 0.75
        rect(pen, -bar/2, my - length/2, length, bar)
        rect(pen, 0, my - bar, length, bar)
        glyph.leftMargin = glyph.rightMargin = self.marginMedium

    #   S C A L E R

    def meme_scScaler(self, glyph, pen):
        """Scale the glyph from another source. e.g. SmallCaps."""
        print('SC-SCALER', glyph.name)

