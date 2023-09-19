from mutatorMath.objects.mutator import buildMutator
from mutatorMath.objects.location import Location
from fontMath.mathGlyph import MathGlyph
from tnbits.tools.toolparts.buildvariations.designspacemodel import DesignSpaceBase

class UFODesignSpace(DesignSpaceBase):
    """
    masters = [
        dict(font=FontObject, location=LocationObject),
        ...
    ]
    """

    def __init__(self, axes, masters):
        self.axes = axes
        self.masters = masters

    def _getInstanceGlyph(self, glyphName, location, masters):
        from defcon.objects.glyph import Glyph
        targetGlyph = Glyph() # TODO temp
        items = []

        for item in masters:
            locationObject = item['location']
            fontObject = item['font']
            ###glyphName = item['glyphName']
            if not glyphName in fontObject:
                continue
            glyphObject = MathGlyph(fontObject[glyphName])
            items.append((locationObject, glyphObject))

        bias, m = buildMutator(items)
        instanceObject = m.makeInstance(location)
        instanceGlyph = instanceObject.extractGlyph(targetGlyph)
        return instanceGlyph

    def getOutline(self, glyphName, location, penFactory):
        pen = penFactory(None)
        location = Location(location)
        masters = self.masters
        instanceGlyph = self._getInstanceGlyph(glyphName, location, masters)
        instanceGlyph.draw(pen)
        centerPoint = (instanceGlyph.width / 2, 250) # TODO y pos
        size = 750 # TODO size should be capHeight?

        return pen, centerPoint, size

    def getGlyphName(self, charCode):
        # TODO
        # FIXME if the glyph ".notdef" doesn't exist, it breaks...
        from fontTools.agl import UV2AGL
        glyphName = UV2AGL.get(charCode) or ".notdef"
        return glyphName
