from glyphNameFormatter.data import name2unicode_AGD, unicode2name_AGD
from instructions import INSTRUCTIONS, ANCHOR_POS

SERIALIZE_DATA = {
    'width': 0,
    'anchors': [],
    'lib': {},
    'unicodes': [],
    'components': [],
    'name': '',
    'contours': [],
}

ACCENT_PLACEHOLDER = SERIALIZE_DATA
ACCENT_PLACEHOLDER['contours'] = [{'points': [{'y': -10, 'x': -110, 'smooth': False, 'segmentType': u'line'}, {'y': -10, 'x': -90, 'smooth': False, 'segmentType': u'line'}, {'y': 10, 'x': -90, 'smooth': False, 'segmentType': u'line'}, {'y': 10, 'x': -110, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': -10, 'x': 90, 'smooth': False, 'segmentType': u'line'}, {'y': -10, 'x': 110, 'smooth': False, 'segmentType': u'line'}, {'y': 10, 'x': 110, 'smooth': False, 'segmentType': u'line'}, {'y': 10, 'x': 90, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': 60, 'x': -80, 'smooth': False, 'segmentType': u'line'}, {'y': 60, 'x': -60, 'smooth': False, 'segmentType': u'line'}, {'y': 80, 'x': -60, 'smooth': False, 'segmentType': u'line'}, {'y': 80, 'x': -80, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': -80, 'x': 60, 'smooth': False, 'segmentType': u'line'}, {'y': -80, 'x': 80, 'smooth': False, 'segmentType': u'line'}, {'y': -60, 'x': 80, 'smooth': False, 'segmentType': u'line'}, {'y': -60, 'x': 60, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': 90, 'x': -10, 'smooth': False, 'segmentType': u'line'}, {'y': 90, 'x': 10, 'smooth': False, 'segmentType': u'line'}, {'y': 110, 'x': 10, 'smooth': False, 'segmentType': u'line'}, {'y': 110, 'x': -10, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': -110, 'x': -10, 'smooth': False, 'segmentType': u'line'}, {'y': -110, 'x': 10, 'smooth': False, 'segmentType': u'line'}, {'y': -90, 'x': 10, 'smooth': False, 'segmentType': u'line'}, {'y': -90, 'x': -10, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': 60, 'x': 60, 'smooth': False, 'segmentType': u'line'}, {'y': 60, 'x': 80, 'smooth': False, 'segmentType': u'line'}, {'y': 80, 'x': 80, 'smooth': False, 'segmentType': u'line'}, {'y': 80, 'x': 60, 'smooth': False, 'segmentType': u'line'}]}, {'points': [{'y': -80, 'x': -80, 'smooth': False, 'segmentType': u'line'}, {'y': -80, 'x': -60, 'smooth': False, 'segmentType': u'line'}, {'y': -60, 'x': -60, 'smooth': False, 'segmentType': u'line'}, {'y': -60, 'x': -80, 'smooth': False, 'segmentType': u'line'}]}]

import math
def italicizedPoint(d, angle):
    x, y = d
    if angle == 0:
        return (x, y)
    else:
        return (x - math.tan(math.radians(angle))*y, y)

class AccentBuilder(object):
    def __init__(self):
        self.font = CurrentFont()
        self._capSuffix = "uc"
        self._capOffset = -50

        self.instructions = INSTRUCTIONS

    def getAnchor(self, glyph, anchorName):
        for anchor in glyph.anchors:
            if anchorName == anchor.name:
                return anchor
        return None

    def getBasesComposites(self):
        basesComposites = {}
        for glyphName, instruction in self.instructions.items():
            items = instruction.split("+")
            base = items[0]
            if base not in basesComposites:
                basesComposites[base] = set()
            basesComposites[base].add(glyphName)
        return basesComposites

    def getBasesCompositesWithExtensions(self, basesComposites):
        font = self.font
        for glyph in font:
            glyphName = glyph.name
            split = glyphName.split(".")
            baseName = split[0]
            extensions = split[1:]
            if extensions and baseName in basesComposites:
                # copy base set
                basesComposites[glyphName] = basesComposites[baseName]
        return basesComposites

    def getCompositeSet(self):
        pass
        # TODO get all glyph names that are in constructions
        # TODO get all glyph names with extensions and add them to the list if their base name is in constructions. E.g. we have Aacute.sc in the font already, let's udate it.
        # TODO also get all glyph names with extensions and construct composites if they are in BASE_SET. e.g. A.sc exist, we need to build all accents for it. Greedy? We need a set for this, like getBasesComposites in _dev/AccentBuilder
        # TODO get optional flight path
        # construct dict of key (glyphName) value (instruction)

    def autoUnicode(self, glyph):
        # TODO autoUnicode preference flag? but outside of this function
        # TODO if GN and not AGD
        uni = name2unicode_AGD.get(glyph.name)
        if uni:
            glyph.unicode = uni

    def buildBasePlaceholder(self, base, d, angle=0):
        w, h = d
        font = self.font
        baseGlyph = font.newGlyph(base)
        baseGlyph.width = w
        pen = baseGlyph.getPen()
        pen.moveTo(italicizedPoint((0, 0), angle))
        pen.lineTo(italicizedPoint((w, 0), angle))
        pen.lineTo(italicizedPoint((w, h), angle))
        pen.lineTo(italicizedPoint((0, h), angle))
        pen.closePath()

    def buildAccentPlaceholder(self, accentName, posY, angle):
        font = self.font
        accentGlyph = font.newGlyph(accentName)

        placeholder = ACCENT_PLACEHOLDER
        placeholder['name'] = accentName
        accentGlyph.naked().deserialize(placeholder)

        if posY == "top":
            accentGlyph.move(italicizedPoint((0, font.info.capHeight), angle))
        elif posY == "bottom":
            accentGlyph.move(italicizedPoint((0, font.info.descender), angle))
        else: # center
            accentGlyph.move(italicizedPoint((0, font.info.xHeight), angle))

    def buildComposite(self, glyphName, instruction, analyzeOnly=False):
        # TODO italic offset
        font = self.font
        angle = font.info.italicAngle or 0

        extensions = glyphName.split(".")[1:]
        items = instruction.split("+")
        base = items[0]

        if base[0].isupper():
            isupper = True
        else:
            isupper = False

        if extensions:
            ext =  ".".join(extensions)
            base += "."+ext

        if base not in font:
            w = 500
            if isupper:
                h = font.info.capHeight
            else:
                h = font.info.xHeight
            self.buildBasePlaceholder(base, (w, h), angle)
        baseGlyph = font[base]

        newGlyph = font.newGlyph(glyphName)
        newGlyph.appendComponent(base)
        newGlyph.width = font[base].width
        self.autoUnicode(newGlyph)

        for i in items[1:]:
            accentName, anchorName = i.split("@")
            _anchorName = "_"+anchorName
            posX, posY = ANCHOR_POS.get(anchorName) or (None, None)

            if extensions:
                accentNameExt = accentName+"."+ext
                if accentNameExt in font:
                    accentName = accentNameExt

            # TODO what if capSuffix is "" (None)
            if isupper:
                accentNameCap = accentName+"."+self._capSuffix
                if accentNameCap in font:
                    accentName = accentNameCap

            if accentName not in font:
                self.buildAccentPlaceholder(accentName, posY, angle)

            accentGlyph = font[accentName]
            self.autoUnicode(accentGlyph)

            anchor = self.getAnchor(baseGlyph, anchorName)
            if not anchor:
                if posX == "left":
                    x = 0
                elif posX == "right":
                    x = baseGlyph.width
                else: # center
                    x = baseGlyph.width/2
                if posY == "top":
                    if isupper:
                        y = font.info.capHeight
                    else:
                        y = font.info.xHeight
                elif posY == "bottom":
                    y = 0 # baseline
                else: # center
                    pass # TODO ? let's catch error for now
                x, y = italicizedPoint((x, y), angle)
                baseGlyph.appendAnchor(anchorName, (x, y))
                anchor = self.getAnchor(baseGlyph, anchorName)

            _anchor = self.getAnchor(accentGlyph, _anchorName)
            if not _anchor:
                x = 0 # because cmb width is 0
                if posY == "top":
                    y = font.info.xHeight
                elif posY == "bottom":
                    y = 0 # baseline
                else: # center
                    pass # TODO ? let's catch error for now
                x, y = italicizedPoint((x, y), angle)
                accentGlyph.appendAnchor(_anchorName, (x, y))
                _anchor = self.getAnchor(accentGlyph, _anchorName)

            x, y = anchor.x, anchor.y
            _x, _y = _anchor.x, _anchor.y

            dx = x - _x
            dy = y - _y

            if isupper:
                dy += self._capOffset

            newGlyph.appendComponent(accentName, offset=(dx, dy))


builder = AccentBuilder()
builder.buildComposite("Uhorndotbelow", "U+horncmb@horn+dotbelowcmb@bottom", False)
builder.buildComposite("Acircumflex", "A+circumflexcmb@top", False)
builder.buildComposite("lcaron", "l+caroncmb.vert@caron.vert", False)
builder.buildComposite("Eacute.sc", "E+acutecmb@top", False)
builder.buildComposite("aacute", "a+acutecmb@top", False)
