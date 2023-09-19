from tnbits.model import model
from defcon.objects.font import Font
from fontmake.font_project import FontProject
from fontTools.varLib import build
from mutatorMath.ufo.document import DesignSpaceDocumentWriter
import os

# FIXME axis defaultValue for Bitcount???

STANDARD_AXIS_MAP = {
        'weight':  ('wght', 'Weight'),
        'width':   ('wdth', 'Width'),
        'slant':   ('slnt', 'Slant'),
        'optical': ('opsz', 'Optical Size'),
        'custom':  ('xxxx', 'Custom'),
    }

def writeDesignSpaceDocument(designSpace, fileName):

    # this removes interpolations axes not in designSpace axes
    for key in designSpace.interpolations.keys():
        for axis in designSpace.interpolations[key].keys():
            if axis not in designSpace.axes.keys():
                del designSpace.interpolations[key][axis]

    designSpaceDocument = DesignSpaceDocumentWriter(fileName)
    family = designSpace.parent

    # TODO clean up

    sources = {}
    for styleKey in designSpace.getMasterKeys():
        style = family.getStyle(styleKey)
        path = style.path
        familyName = style.info.familyName
        styleName = style.info.styleName
        name = "%s-%s" % (familyName, styleName)
        location = designSpace.interpolations.get(styleKey) or {}
        source = dict(path=path, name=name, location=location, familyName=familyName, styleName=styleName)
        sources[path] = source

    if designSpace.origin: # TODO this is repetitive
        # copy lib, groups, info and features
        styleId = designSpace.origin
        styleKey = (family.familyID, styleId)
        style = family.getStyle(styleKey)
        path = style.path
        familyName = style.info.familyName
        styleName = style.info.styleName
        name = "%s-%s" % (familyName, styleName)
        location = designSpace.interpolations.get(styleKey) or {}
        source = dict(path=path, name=name, location=location, familyName=familyName, styleName=styleName,
                      copyLib=1, copyGroups=1, copyInfo=1, copyFeatures=1)
        sources[path] = source

    instances = sources # include origin and masters in instances

    for styleKey in designSpace.getInstanceKeys():
        #familyID, styleId = instanceKey
        style = family.getStyle(styleKey)
        path = style.path
        familyName = style.info.familyName
        styleName = style.info.styleName
        name = "%s-%s" % (familyName, styleName)
        location = designSpace.interpolations.get(styleKey) or {}
        instance = dict(name=name, location=location, familyName=familyName, styleName=styleName, fileName=path)
        instances[path] = instance

    # TODO repetitive
    for source in sources.values():
        path = source.get("path")
        name = source.get("name")
        location = source.get("location")
        copyLib = source.get("copyLib") or False
        copyGroups = source.get("copyGroups") or False
        copyInfo = source.get("copyInfo") or False
        copyFeatures = source.get("copyFeatures") or False
        muteKerning = source.get("muteKerning") or False
        muteInfo = source.get("muteInfo") or False
        mutedGlyphNames = source.get("mutedGlyphNames") or None
        familyName = source.get("familyName") or None
        styleName = source.get("styleName") or None
        designSpaceDocument.addSource(path, name, location,
            copyLib=copyLib, copyGroups=copyGroups, copyInfo=copyInfo, copyFeatures=copyFeatures, muteKerning=muteKerning, muteInfo=muteInfo, mutedGlyphNames=mutedGlyphNames, familyName=familyName, styleName=styleName)

    for instance in instances.values():
        name = instance.get("name")
        location = instance.get("location")
        familyName = instance.get("familyName")
        styleName = instance.get("styleName")
        fileName = instance.get("fileName")
        postScriptFontName = instance.get("postScriptFontName") or None
        styleMapFamilyName = instance.get("styleMapFamilyName") or None
        styleMapStyleName = instance.get("styleMapStyleName") or None
        designSpaceDocument.startInstance(name=name, location=location, familyName=familyName, styleName=styleName, fileName=fileName, postScriptFontName=postScriptFontName, styleMapFamilyName=styleMapFamilyName, styleMapStyleName=styleMapStyleName)
        designSpaceDocument.writeInfo()
        designSpaceDocument.writeKerning()
        designSpaceDocument.endInstance()

    designSpaceDocument.save()


def makeInterpolatableTTF(ufos, reverse=False):
    project = FontProject()
    project.build_interpolatable_ttfs(ufos, reverse_direction=reverse, conversion_error=None, use_production_names=False)

def buildVariationFont(familyFile, glyphSubset=None, masterSubset=None): #TODO  what should I work with, family object, familyFile, designSpace?

    familyFile = os.path.abspath(familyFile)
    family = model.openFamily(path=familyFile)

    variation_name = family.name + '-GX'
    variation_filename = variation_name+".ttf"

    designSpaceNames = family.designSpaces.keys()
    designSpace = family.getDesignSpace(designSpaceNames[0]) # only first for now TODO

    if masterSubset:
        for styleKey in family.getStyleKeys():
            styleId = styleKey[1]
            if styleId not in masterSubset:
                print('ignoring', styleId)
                designSpace.asIgnore(styleKey)

    origin = designSpace.origin
    if not origin:
        print('FamilyError: %s origin is not set' % designSpace.name)
        return

    #familyDir = os.path.dirname(designSpace.familyID)
    #variationDir = os.path.join(familyDir, 'variations')
    #subsetDir = os.path.join(variationDir, 'subsets')
    subsetDir = 'subsets'

    if not os.path.exists(subsetDir) and glyphSubset:
        os.makedirs(subsetDir)

    designSpaceName = '%s-%s.designspace' % (family.name, designSpace.name)
    #designSpaceFileName = os.path.join(variationDir, designSpaceName)
    designSpaceFileName = designSpaceName

    writeDesignSpaceDocument(designSpace, designSpaceFileName)

    masters = designSpace.getMasters()

    if glyphSubset:
        subsets = []
        for master in masters:
            subset = Font()
            for glyphName in glyphSubset:
                if glyphName in master:
                    glyph = master[glyphName]
                    subset.insertGlyph(glyph)
                else:
                    print('SubsetError: %s not in %s' % (glyphName, master))
                    return

            subset.info.familyName = master.info.familyName
            subset.info.styleName = master.info.styleName

            subset.info.unitsPerEm = master.info.unitsPerEm
            subset.info.ascender = master.info.ascender
            subset.info.descender = master.info.descender
            subset.info.xHeight = master.info.xHeight
            subset.info.capHeight = master.info.capHeight

            subset.glyphOrder = glyphSubset

            # TODO
            # temp kerning pair to have a GPOS table
            g = glyphSubset[0]
            subset.kerning[(g, g)] = 0

            subsetFileName = "Subset-%s-%s.ufo" % (subset.info.familyName, subset.info.styleName)
            subsetPath = os.path.join(subsetDir, subsetFileName)
            subset.save(subsetPath)

            subsets.append(subset)
        ufos = subsets
    else:
        ufos = masters

    makeInterpolatableTTF(ufos)

    axes = designSpace.getAxes()
    axisMap = {}
    for axisName, axis in axes.items():
        axisTag = axis.get("axis") or axisName
        axisMap[axisName] = (axisTag, axisName)
    if not axisMap:
        axisMap = STANDARD_AXIS_MAP
    print(axisMap)

    master_finder = lambda s: os.path.join('master_ttf_interpolatable', os.path.basename(s)).replace('.ufo', '.ttf')

    gx, model, master_ttfs = build(designSpaceFileName, master_finder, axisMap=axisMap)
    print("Saving variation font", variation_filename)
    gx.save(variation_filename)
