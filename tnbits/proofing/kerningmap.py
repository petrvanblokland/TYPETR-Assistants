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
#    kerningmap.py
#

from drawBot import newPage, saveImage, newDrawing, save, restore, translate, \
        rotate, fill, stroke, scale, rect, fontSize, text, pdfImage
from tnbits.vanillas.dialogs.warningdialog import WarningDialog
from tnbits.proofing.base import Base

class KerningMap(Base):
    """
    Draws the selected glyph set in a kerning map.
    """

    name = "Kerning Map"

    def build(self, styleKeys):
        """Draw black square kerning matrix per style. Red dot is negative
        kerning, green dot is positive kerning. The layout ignores the
        selected glyph set."""
        self.sampleName = None
        return self.draw(styleKeys)

    def draw(self, styleKeys):
        """
        """
        w, h, margin = self.getPaperSize()
        extraBottomMargin = 13
        width = w - 2 * margin
        height = h - 2 * margin - extraBottomMargin
        glyphNameMargin = 40
        labelFontSize = 3.5
        labelMargin = 3
        fSize = 16 # Size in case of drawing pairs.

        if len(styleKeys) < 1:
            dialog = WarningDialog()
            dialog.openWarningDialog('Please select at least one style.')
            return

        newDrawing()
        flatKernings = self.getFlatKernings(styleKeys)
        left, right = self.splitKerningPairs(flatKernings)


        for styleKey in styleKeys:
            newPage(w, h)
            self.drawDebug()
            # self.tool.progressUpdate(title='Draw kerning map', text='Opening %s' % styleId)
            style = self.family.getStyle(styleKey)
            self.drawHeader([styleKey])
            self.drawFooter()

            hScale = float(width) / (len(right) * 3 + glyphNameMargin)
            vScale = float(height) / (len(left) * 3 + glyphNameMargin)
            save()
            translate(margin, margin + extraBottomMargin)
            s = min(hScale, vScale)
            scale(s)

            # Initializes canvas as black square.
            fill(0)
            rect(0, 0, len(right) * 3, len(left) * 3)
            stroke(None)

            for y, glyphName1 in enumerate(left):
                for x, glyphName2 in enumerate(right):
                    pair = glyphName1, glyphName2

                    if pair in flatKernings[styleKey]:
                        # Calculates the kerning color and draw the color rect.
                        value = flatKernings[styleKey][pair]

                        if value < 0:
                            fill(-value/16, 0, 0) # 15/100
                        elif value > 0:
                            fill(0, value/16, 0)
                        else:
                            fill(0)
                        rect(x*3, y*3, 2, 2)

                # Draws the glyph names as labels on the side.
                fill(0.3)
                fontSize(labelFontSize)
                text(glyphName1, (len(right)*3+labelMargin, y*3))

            # Rotates the glyph names at the top.
            translate(0, len(left)*3)
            rotate(90)
            fill(0.3)
            fontSize(labelFontSize)

            for y, glyphName2 in enumerate(right):
                text(glyphName2, (labelMargin, -3 -y*3))
            restore()

        path = self.getPath(styleKeys, size=fSize)
        saveImage(path)
        pdf = pdfImage()
        self.pdfs.append(pdf)
        return [path]

