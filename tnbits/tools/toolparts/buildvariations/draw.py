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
#    draw.py
#
from AppKit import NSColor, NSAttributedString, NSMakeRect
from tnbits.model.objects.style import getStyleKey

class Draw(object):

    COLORS = []
    for cv in ( # See also Proof tool.
        (0.75, 0, 0), (0, 0.75, 0), (0, 0, 0.75), (0.75, 0.75, 0), (0.75, 0, 0.75),
        (0, 0.75, 0.75), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0),
        (0.5, 0, 0.5), (0, 0.5, 0.5), (0.25, 0, 0.75), (0, 0.25, 0.75),
        (0.75, 0, 0.25), (0.25, 0.25, 0.75), (0.25, 0.75, 0.25), (0.75, 0.25, 0.25),
    ):
        COLORS.append(NSColor.colorWithCalibratedRed_green_blue_alpha_(cv[0], cv[1], cv[2], 1))
    GRAY_COLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.5, 0.5, 0.5, 1)

    def draw(self, info):
        """Draw the relation between the masters in the family for this glyph, for all of the constellations
        that the master is part of."""
        glyph = info['glyph']
        if glyph is None:
            return # Ignore if we have a non-existing glyph.
        if not glyph.name in self._errorItems:
            return # Ignore if we don't have errors about this glyph.
        view = self.getView()
        if not self._family or not view.drawPointRelations.get():
            return
        style = glyph.font
        if style.path is None:
            return # Ignore new untitled styles.

        glyphName = glyph.name
        errorItem = self._errorItems[glyphName] # Get the error item with additional information.
        scale = info['scale']
        styleKey = getStyleKey(style)
        for mIndex, masterKey in enumerate(self._masterKeys):
            self.GRAY_COLOR.set() # Set color as default for current font.
            if masterKey != styleKey: # Don't draw current glyph.
                master = self._family.getStyle(masterKey)
                if glyphName in master:
                    path = master[glyphName].getRepresentation('defconAppKit.NSBezierPath')
                    self.COLORS[mIndex].set()  # Set the color for this master if not current.
                    path.setLineWidth_(0.75 / scale)
                    path.stroke()
            # Depending on the type of error, we'll add additional info to the glyph drawing.
            if errorItem.errorType == errorItem.POINTCOUNT:
                pass
            elif errorItem.errorType == errorItem.POINTTYPE:
                pass
            elif errorItem.errorType == errorItem.POINTSMOOTHNESS:
                pass
            elif errorItem.errorType == errorItem.CONTOURCOUNT:
                pass
            elif errorItem.errorType == errorItem.CONTOURDIRECTION:
                pass
            elif errorItem.errorType == errorItem.COMPONENTCOUNT:
                pass
            elif errorItem.errorType == errorItem.DIFFERENTCOMPONENTBASE:
                # Show the difference in base glyph name in relation to the masters.
                self.drawDifferentComponentBase(errorItem)
            elif errorItem.errorType == errorItem.MISSINGMASTERGLYPH:
                pass
            elif errorItem.errorType == errorItem.NOMASTERS:
                pass
            else:
                pass
                #raise KeyError('Unknown interpolation error type: "%s"' % errorItem.errorType)

    def drawDifferentComponentBase(self, errorItem):
        print(errorItem.errorType)
        """
        self.drawString(u'Component base')
        label = '%d  %d' % (p.x, p.y)
        nsString = self._stringLabels.get('c' + label)  # Test on cached string label
        if nsString is None:
            self._stringLabels['c' + label] = nsString = NSAttributedString.alloc().initWithString_attributes_(
                label, self.attributesCoordinate)  # Double space to position.
        width, height = nsString.size()
        nsString.drawInRect_(NSMakeRect(p.x - width / 2, p.y + ms3_2, width, height))
        """
