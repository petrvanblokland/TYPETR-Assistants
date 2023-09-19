#!/usr/bin/python
import unittest
import random
from defcon.objects.glyph import Glyph
from defcon.objects.anchor import Anchor
from tnbits.tools.toolparts.buildvariations.fixinterpolations import \
    checkUnicodes, fixUnicodes, checkContourCount, checkContourLength, checkAnchorCount


class FixInterpolationsTest(unittest.TestCase):
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_fixUnicodes(self):
        glyph = Glyph()
        glyph.unicodes = [65]
        otherGlyphs = []
        for u in [65, 65, 66]:
            otherGlyph = Glyph()
            otherGlyph.unicodes = [u]
            otherGlyphs.append(otherGlyph)
        self.assertFalse(checkUnicodes(glyph, otherGlyphs))
        fixUnicodes(glyph, otherGlyphs)
        self.assertTrue(checkUnicodes(glyph, otherGlyphs))

    def test_checkContourCount(self):
        glyph = Glyph()
        pointPen = glyph.getPointPen()
        pointPen.beginPath()
        pointPen.addPoint((0, 0))
        pointPen.addPoint((50, 0))
        pointPen.addPoint((50, 500))
        pointPen.addPoint((0, 500))
        pointPen.endPath()

        otherGlyph1 = Glyph()
        otherGlyph2 = Glyph()

        self.assertFalse(checkContourCount(glyph, [otherGlyph1, otherGlyph2]))

        pointPen1 = otherGlyph1.getPointPen()
        pointPen1.beginPath()
        pointPen1.addPoint((0, 0))
        pointPen1.endPath()

        pointPen2 = otherGlyph2.getPointPen()
        pointPen2.beginPath()
        pointPen2.addPoint((0, 0))
        pointPen2.endPath()

        self.assertTrue(checkContourCount(glyph, [otherGlyph1, otherGlyph2]))

    def test_checkContourLength(self):
        glyph = Glyph()
        pointPen = glyph.getPointPen()
        pointPen.beginPath()
        pointPen.addPoint((0, 0))
        pointPen.addPoint((100, 0))
        pointPen.endPath()
        pointPen.beginPath()
        pointPen.addPoint((0, 0))
        pointPen.endPath()

        otherGlyph1 = Glyph()
        pointPen1 = otherGlyph1.getPointPen()
        pointPen1.beginPath()
        pointPen1.addPoint((0, 0))
        pointPen1.addPoint((200, 0))
        pointPen1.endPath()
        pointPen1.beginPath()
        pointPen1.addPoint((0, 0))
        pointPen1.endPath()

        otherGlyph2 = Glyph()
        pointPen2 = otherGlyph2.getPointPen()
        pointPen2.beginPath()
        pointPen2.addPoint((0, 0))
        pointPen2.endPath()
        pointPen2.beginPath()
        pointPen2.addPoint((0, 0))
        pointPen2.endPath()

        self.assertFalse(checkContourLength(glyph, [otherGlyph1, otherGlyph2]))

        otherGlyph2 = Glyph()
        pointPen2 = otherGlyph2.getPointPen()
        pointPen2.beginPath()
        pointPen2.addPoint((0, 0))
        pointPen2.addPoint((300, 0))
        pointPen2.endPath()
        pointPen2.beginPath()
        pointPen2.addPoint((0, 0))
        pointPen2.endPath()

        self.assertTrue(checkContourLength(glyph, [otherGlyph1, otherGlyph2]))

    def test_checkAnchorCount(self):
        glyph = Glyph()
        for i in range(3):
            anchor = Anchor()
            anchor.x = random.randint(0, 500)
            anchor.y = random.randint(0, 1000)
            anchor.name = str(i)
            glyph.appendAnchor(anchor)

        otherGlyph1 = Glyph()
        for i in range(3):
            anchor = Anchor()
            anchor.x = random.randint(0, 500)
            anchor.y = random.randint(0, 1000)
            anchor.name = str(i)
            otherGlyph1.appendAnchor(anchor)

        otherGlyph2 = Glyph()
        for i in range(4):
            anchor = Anchor()
            anchor.x = random.randint(0, 500)
            anchor.y = random.randint(0, 1000)
            anchor.name = str(i)
            otherGlyph2.appendAnchor(anchor)

        self.assertFalse(checkAnchorCount(glyph, [otherGlyph1, otherGlyph2]))

        # anchor is last Anchor added, remove it to get the same count
        otherGlyph2.removeAnchor(anchor)

        self.assertTrue(checkAnchorCount(glyph, [otherGlyph1, otherGlyph2]))

if __name__ == "__main__":
    unittest.main()
