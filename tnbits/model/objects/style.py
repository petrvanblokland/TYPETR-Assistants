# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    style.py
#
import os
import traceback

from defcon.objects.base import BaseObject
from defcon.objects.uniData import UnicodeData
from fontTools.pens.cocoaPen import CocoaPen
from tnbits.canvas.bezierpath import CanvasBezierPath

from tnbits.model.objects.glyph import Glyph
from tnbits.model.storage.basestorage import getStorage
from tnbits.model.storage.ufostorage import UFOStorage
from tnbits.model.storage.otfstorage import OTFStorage
from tnbits.toolbox.transformer import TX
from fontTools.varLib.models import normalizeLocation
from tnbits.variations.varmath import *

#TODO: move global functions to module __init__.
# Static functions to be used on styles.

def nakedStyle(style):
    try:
        return style.naked()
        print('return style.naked() for style %d' % id(style))
    except AttributeError:
        return style

def setDirty(style, flag=True):
    """Set the naked style to the dirty flag. Default is True."""
    nakedStyle(style).dirty=flag

def getStyleKey(style):
    """Tries to determine the unique key for this style as tuple from
    (familyPath, fileName)"""
    #style = nakedStyle(style) # Make sure we didn't get a wrapper style.

    try:
        if style.path is not None:
            # In case of a RoboFont UFO font that has a valid path.
            # Tuple of format (familyPath, fileName)
            return TX.path2StyleKey(style.path)
    except AttributeError as e:
        print('Error in getStyleKey(): Cannot determine style key -- %s' % e)
        raise(e)


    '''
    No other way left than just answer the Python ID of the naked font/style.
    Must be converted to a real path (by saving the font) if the family saved
    the info pack.
    '''
    #return '', id(style)

def isItalic(styleKey):
    _, styleName = styleKey
    if '_Italic' in styleName:
        return True
    return False

def getItalicStyleKey(styleKey):
    """Answers the styleKey of the italic, matching style. If style key is
    already italic, then answer None.

    The principle of the style name is based on simply adding "_Italic". If
    other types of italic naming are standard, then this function needs to be
    extended. Note that it is not checked if the style really exists in the
    family or if it is already open."""
    familyPath, styleName = styleKey

    if not '_Italic' in styleName:
        parts = styleName.split('.')
        n = parts[-2] + '_Italic'
        name = '.'.join(parts[:-2]) + n + '.' + parts[-1]
        return familyPath, name # Construct new style key

    return None

def getRomanStyleKey(styleKey):
    """Answers the styleKey of the roman, matching style. If style key is
    already roman, then answer None.

    The principle of the style name is based on simply removing "_Italic". If
    other types of italic naming are standard, then this function needs to be
    extended. Note that it is not checked if the style really exists in the
    family or if it is already open."""
    familyPath, styleName = styleKey

    if '_Italic' in styleName:
        return familyPath, styleName.replace('_Italic', '')

    return None

def verifyStyleKey(styleKey):
    """Answers if styleKey appear to be valid format
    (familyPath, styleId)"""
    if not isinstance(styleKey, tuple) or len(styleKey) != 2:
        return False

    familyPath, styleId = styleKey

    # It's really the styleKey for an open file. Check if the file exists.
    if familyPath and isinstance(styleId, str):
        stylePath = TX.path2FamilyDir(familyPath) + '/' + styleId
        a1 = os.path.exists(familyPath)
        a2 = os.path.exists(stylePath)
        # Does it exist as file?
        return os.path.exists(familyPath) and os.path.exists(stylePath)

    # Special type of StyleKey e.g. ('', 12345567), if style is temp without
    # family or filepath.
    if not familyPath and TX.isInt(styleId):
        return True
    return False # Not a valid styleKey

def newGlyph(style, glyphName):
    """Answers a new glyph if it does not exist. Otherwise just answer the
    existing glyph."""
    if glyphName in style:
        return style.newGlyph(glyphName)
    return style[glyphName]

def getStyleName(style):
    return (style.info.familyName or 'Untitled') + '-' + (style.info.styleName or 'NoStyle')

def updateModificationTime(style):
    """Set the modification time of the style to the current date/time."""
    if style.path:
        os.utime(style.path, None)

def clearLayers(style):
    """Removes all layers from all glyphs."""
    style = nakedStyle(style)
    layerNames = set()

    for g in style:
        layerNames = layerNames.union(set(g.layers.keys()))

    for layerName in layerNames:
        if layerName != 'foreground':
            style.removeLayer(layerName)

#--------------------------------------------------------------------------------
#   V A R I A T I O N S

VARIATION_AXIS_KEY = 'tnTools.variationAxes'
VARIATION_DELTA_KEY = 'tnTools.deltaLocations'

#   Axis

def getAxes(style):
    """Answers the axis dictionary from style. Creates an empty dictionary
    entry if it does not exist."""
    return style.axes

def getActiveAxisNames(style):
    """Answers the list with axes names that are referenced to by one or more
    deltaLocations."""
    activeAxisNames = set()
    axes = getAxes(style)

    for glyphLocation in getDeltaLocations(style).values():
        for axisName, axis in glyphLocation['axisLocations'].items():
            if axis['enabled']:
                activeAxisNames.add(axisName)
    return activeAxisNames

def getAxis(style, tag):
    """Answers the axis with the tag. Raise a error if the axis does not
    exist. Makes sure that the axis contains all valid fields. Repairs
    otherwise."""
    axes = getAxes(style)
    assert tag in axes
    return validatedAxis(tag, axes[tag])

def newAxis(style, tag=None, axis=None):
    axes = getAxes(style)

    if tag is None or tag in axes:
        uniqueIndex = 0 # Use in case name is not unique.
        newTag = tag
        while newTag is None or newTag in axes:
            newTag = '?%03d' % uniqueIndex
            uniqueIndex += 1
        tag = newTag
    axes[tag] = validatedAxis(tag, axis) # Validate axis info. Create new if axis is None.
    return axis

def deleteAxis(style, tag):
    axes = getAxes(style)
    assert tag in axes
    del axes[tag]

def renameAxis(style, oldTag, newTag):
    """Rename the axis and update all reference to this axis in DeltaLocations."""
    axes = getAxes(style)
    assert oldTag != newTag and oldTag in axes and not newTag in axes
    axes[newTag] = validatedAxis(oldTag, axes[oldTag])
    del axes[oldTag]
    # Now also run through all DeltaLocation entries, to change the axis name there.
    for deltaLocation in getDeltaLocations(style).values():
        axisLocations = deltaLocation['axisLocations']
        if oldTag in axisLocations: # If this deltaLocation refers oldName, then update.
            axisLocations[newTag] = axisLocations[oldTag]
            axisLocations[newTag]['tag'] = newTag
            del axisLocations[oldTag]

def validatedAxis(tag, axis=None):
    """Check the validity of axis, and do repairs otherwise. Return the axis
    for convenience of the caller.

    dict(enabled=True, name=name, tag='????', description='', minValue=0,
        maxValue=1000, defaultValue=0)
    """
    assert isinstance(tag, str) and len(tag) == 4
    if axis is None:
        axis = {}
    axis['tag'] = tag
    if not 'enabled' in axis:
        axis['enabled'] = True
    # Name can be anything, but must exist.
    if not 'name' in axis:
        axis['name'] = 'Untitled'
    if not 'description' in axis:
        axis['description'] = ''
    if not isinstance(axis.get('minValue'), (int, float)):
        axis['minValue'] = 0
    if not isinstance(axis.get('defaultValue'), (int, float)):
        axis['defaultValue'] = 0
    if not isinstance(axis.get('maxValue'), (int, float)):
        axis['maxValue'] = 1000
    return axis

#   DeltaLocation

def getDeltaLocations(style):
    """Answers the style.lib dictionary with all DeltaLocations dictionaries."""
    if not VARIATION_DELTA_KEY in style.lib:
        # Key is unique DeltaLocation name, value is DeltaLocation dict.
        style.lib[VARIATION_DELTA_KEY] = {}
    return style.lib[VARIATION_DELTA_KEY]

def getDeltaLocation(style,  name):
    """Answers the deltaLocation with the name. Raise a error if the axis does
    not exist. Make sure that the deltaLocation contains all valid fields.
    Repair otherwise."""
    deltaLocations = getDeltaLocations(style)
    assert name in deltaLocations
    return validatedDeltaLocation(style, name, deltaLocations[name])

def newDeltaLocation(style, name, deltaLocation=None, neutral=False):
    deltaLocations = getDeltaLocations(style)

    if name in deltaLocations:
        uniqueIndex = 0 # Use in case name is not unique.
        newName = name
        while newName in deltaLocations:
            newName = '%s%d' % (name, uniqueIndex)
            uniqueIndex += 1
        name = newName
    # If not supplied, creates an empty default delta location. Note, that
    # there should be at least one axis. Ininitializes new if deltaLocation is
    # None.
    deltaLocations[name] = deltaLocation = validatedDeltaLocation(style, name, deltaLocation, neutral)
    return deltaLocation

def deleteDeltaLocation(style, name):
    deltaLocations = getDeltaLocations(style)
    assert name in deltaLocations
    del deltaLocations[name]

def renameDeltaLocation(style, oldName, newName):
    deltaLocations = getDeltaLocations(style)
    assert oldName != newName and oldName in deltaLocations and not newName in deltaLocations
    deltaLocations[newName] = validatedDeltaLocation(style, newName, deltaLocations[oldName])
    del deltaLocations[oldName]

def validatedDeltaLocation(style, name, deltaLocation, neutral=None):
    if deltaLocation is None:
        deltaLocation = dict(neutral=neutral or False, name=name)
    if neutral is not None:
        deltaLocation['neutral'] = neutral or False
    if not 'name' in deltaLocation or deltaLocation['name'] != name:
        deltaLocation['name'] = name
    if not 'axisLocations' in deltaLocation:
        # Format of axisLocations:
        # dict(tag='wght', value=500)
        # Optional: dict(tag='wght', minValue=0, value=500, maxValue=1000)
        deltaLocation['axisLocations'] = {}

    # Make sure that all referenced axes do exist
    axes = getAxes(style)

    for tag in deltaLocation['axisLocations'].keys():
        if not tag in axes:
            del deltaLocation['axisLocations'][tag]
    return deltaLocation

def getNeutralDeltaLocation(style):
    """Answers the first deltaLocation in the list that has the “neutral” flag
    set. There should only be one in a valid design space. If there are more,
    then answer first."""
    for deltaLocation in getDeltaLocations(style).values():
        if deltaLocation.get('neutral'):
            return deltaLocation
    return None # First one found or None

def setNeutralDeltaLocation(style, deltaNeutralName):
    """Clear the neutral flag in all deltaLocations that have a different name.
    Set the neutral flag for deltaName. Answers the neutral deltaLocation if
    found.  Otherwise answer None."""
    neutralDeltaLocation = None
    for deltaLocName, deltaLocation in getDeltaLocations(style).items():
        if deltaLocation['name'] == deltaNeutralName:
            deltaLocation['neutral'] = True
            neutralDeltaLocation = deltaLocation
        else:
            deltaLocation['neutral'] = False
    return neutralDeltaLocation

#   AxisLocation

def getAxisLocations(deltaLocation):
    """Answers the axisLocations dict from the deltaLocation. Repair if it
    missing."""
    if not 'axisLocation' in deltaLocation:
        deltaLocation['axisLocation'] = {}
    return deltaLocation['axisLocation']

def getAxisLocation(deltaLocation, tag):
    axisLocations = getAxisLocations(deltaLocation)
    assert tag in axisLocations
    return axisLocations[tag]

def deleteAxisLocation(deltaLocation, tag):
    axisLocations = getAxisLocations(deltaLocation)
    assert tag in deltaLocation['axisLocations']
    del deltaLocation['axisLocations'][tag]

def setAxisLocation(deltaLocation, tag, value, minValue=None, maxValue=None):
    axisLocations = getAxisLocations(deltaLocation)
    #assert ((minValue or 0) <= (maxValue or 1000))
    #print((minValue or 0) , (maxValue or 1000))
    axisLocations[tag] = axisLocation = dict(tag=tag, value=value)

    # Optional min/max to support Skia "Q-effect", otherwise delete entries.
    # If missing, the minValue and maxValue of axis is used.
    if minValue is not None:
        axisLocation['minValue'] = min(minValue, maxValue or 1000)

    if maxValue is not None:
        axisLocation['maxValue'] = max(minValue or 0, maxValue)

    return axisLocation

#-------------------------------------------------------------------------------
#   G L Y P H

def copyGlyph(srcGlyph, dstStyle, create=True, copyLayers=True, dstName=None,
        copyComponents=True):
    """Copies the srcGlyph into the dstStyle, under the same name. If the
    glyph already exists, then clear the canvas, and draw the srcGlyph. If the
    boolean flag create is set and the dstStyle does not contain a glyph with
    the same name, then create a new glyph. If there is a dstGlyph available,
    answer it. Otherwise answers None."""
    if dstName is None:
        dstName = srcGlyph.name

    assert not (nakedStyle(srcGlyph.font) == nakedStyle(dstStyle) and dstName is None) # Copy onto srcGlyph.

    if not dstName in dstStyle:
        if create:
            dstStyle.newGlyph(dstName)
            dstGlyph = dstStyle[dstName] # Get the newly created glyph.
        else:
            return None
    else:
        dstGlyph = dstStyle[dstName]
        dstGlyph.clear() # Start building on clean canvas, if it already exists.

    if srcGlyph is not None:
        dstGlyph.width = srcGlyph.width
        srcGlyph.drawPoints(dstGlyph.getPointPen()) # Copy Points
        dstGlyph.note = srcGlyph.note
        dstGlyph.lib.clear()
        dstGlyph.lib.update(srcGlyph.lib)

        # If there are components in the glyph, then copy them too if flag is
        # True and srcStyle is not dstStyle.
        srcStyle = dstGlyph.getParent()

        if copyComponents and srcStyle is not dstStyle:
            for component in srcGlyph.components:
                if component.baseGlyph in srcStyle and not component.baseGlyph in dstStyle:
                    copyGlyph(srcStyle[component.baseGlyph], dstStyle, dstName=dstName)

    # TODO Copy of layers does not work this way.
    if 0 and copyLayers:
        dstGlyph.layers = {}
        for layerName, layerGlyph in srcGlyph.layers.items():
            dstGlyph.layers[layerName] = layerGlyph

    return dstGlyph # Answers dstStyle for convenience of the caller.


#   F L I G H T  P A T H

LIBKEY_FLIGHTPATH = 'com.typenetwork.FlightPath'

def getStyleLib(style):
    if style.lib is None:
        style.lib = {}
    return style.lib

def setStyleFlightPath(style, flightPath):
    """Sets the flight path of the style. The value is stored in
    font.lib['com.typenetwork.FlightPath']. Answers the flight path for
    convenience of the caller."""
    styleLib = getStyleLib(style)  # Get the main style.lib.
    styleLib[LIBKEY_FLIGHTPATH] = flightPath
    return flightPath

def getStyleFlightPath(style):
    """Answers the flight path dictionary of the style. Answer None if it does
    not exist."""
    styleLib = getStyleLib(style)  # Get the main style.lib.
    return styleLib.get(LIBKEY_FLIGHTPATH)

#   G U I D E S

def makeGuide(style, guideName, x=None, y=None):
    """Make the named guide at the indicate position. Add the vertical
    position to the name."""
    if x is None:
        x = -200 # Position left of possilble Dumensioneer lines.
    if y is None:
        y = 0
    guide = nakedStyle(style).createGuide()
    guide.name = '%s (%d)' % (guideName, y)  # Show y-value as part of the name.
    guide.x = x
    guide.y = y
    return guide # Answer guide instance for convenience of the caller.

def clearGuides(style, names=None):
    """Removes all global guides from the style. Note that this mostly makes
    sense if the guides are re-generated by a script."""
    for guide in style.guides:
        if names is None or guide.name in names:
            style.removeGuide(guide)

# Classes.

class Info(object):
    """Info storage in a style."""
    pass

class Style(BaseObject):
    """Standard API, should be compatible with Defcon Font and DoodleFont.
    Loads binary data into the appropriate storage type and unpacks the
    necessary data.

    NOTE: can be used as the glyphSet that is passed to path drawing pens.

    FIXME: errors looping over Unicode data.
    FIXME: iteration doesn't match Font:

    for g in style:
        ...

    returns glyphName strings, not Glyph objects.

    style.info.familyName
    style.info.styleName
    getStyleName(style) gives 'CusterRE-Regular'

    style.info.capHeight

    >>> from tnTestFonts import getFontPath
    >>> styleName = "CusterRE-RegularS2.ttf"
    >>> path = getFontPath(styleName)
    >>> style = Style(path)
    >>> print(getStyleName(style), style.info.unitsPerEm, style.info.capHeight)
    CusterRE-Regular 512 384
    >>> style.info.capHeight = 390
    >>> style.info.capHeight
    390
    >>> print(style.lib.keys())
    []
    >>> ###style.save()

    """

    def __init__(self, data, parent=None):
        """Loads font into storage and reads glyph data and metadata.

        TODO:
        - self.setAttributesFromPack(self.storage.getDimensionsPack())
        = self.setAttributesFromPack(self.storage.getBoundariesPack())
        """
        self.storage = getStorage(data)
        self.info = self.fromPack(self.storage.readInfoPack(), Info())
        self.lib = self.fromPack(self.storage.readLibPack(), {})

        # Loads glyphs from storage.
        self._glyphNames = set(self.storage.getGlyphNames())
        self._loadedGlyphs = {}

        for glyphName in self._glyphNames:
            self.get(glyphName)

        self.features = self.storage.readFeaturesPack() # self.fromPack(.., {})
        self.kerning, self.groups = self.storage.readKerningPack() # self.fromPack(.., {})
        self.unicodeData = UnicodeData()
        cmap = self.storage.readCharacterMapping()

        if cmap:
            self.unicodeData.update(cmap)

        try:
            # TODO: check if actually var font before doing this.
            self.axes = self.storage.readAxesPack()
            location = getDefaultLocation(self.axes)
            self.setLocation(location)
        except Exception as e:
            print(traceback.format_exc())

    #   self.id
    def _get_id(self):
        if self.path:
            return self.path # Unique style data path or record id.
        return id(self)

    id = property(_get_id)

    #   self.path
    def _get_path(self):
        return self.storage.path

    path = property(_get_path)

    def fromPack(self, pack, data):
        """Fills the self.info attribute instance with data from the storage
        info pack."""
        for key in pack:
            try:
                setattr(data, key, pack[key])
            except Exception as e:
                print('Style.fromPack(): Cannot set attribute:')
                print(e)
                print(traceback.format_exc())

        return data

    def toPack(self, data):
        return {}

    def setAttributesFromPack(self, pack):
        for key in pack:
            setattr(self, key, pack[key])

    def showUI(self):
        """Open a font window on this style in an editor that fits best. For
        now we'll open this style with the new Editor2."""
        # FIXME: should style have UI functions at all?
        pass
        #from tnTools._dev.Editor2 import Editor
        #Editor.open(style=self)

    def setLocation(self, location):
        self.rawLocation = location
        self.location = normalizeLocation(location, self.axes)

    def save(self):
        """Saves self into the storage. If the glyphs are loaded, saves the
        data back into the storage, otherwise ignores them. Note that there
        seems to be a difference between RF style save and naked style save,
        e.g. not updating the modification date. So, we'll do that separately
        here. Also the dirty flag is not sure to be reliable, so we ignore
        testing it."""
        self.storage.writeInfoPack(self.toPack(self.info))
        self.storage.writeLibPack(self.toPack(self.lib))
        self.storage.save()
        #for glyph in self._loadedGlyphs.values():
        #    glyph.save()

    def __len__(self):
        return len(self._glyphNames)

    def keys(self):
        return self._glyphNames

    def __contains__(self, glyphName):
        return glyphName in self._glyphNames

    def __iter__(self):
        return iter(self._loadedGlyphs)

    '''
    # Defcon Font style iterator. gives:
    # TypeError: 'set' object does not support indexing

    def __iter__(self):
        names = self.keys()

        while names:
            name = names[0]
            yield self[name]
            names = names[1:]
    '''

    def __getitem__(self, glyphName):
        """Tries to fetch a FloqModel glyph from cache, else loads a new one.
        """
        glyph = self._loadedGlyphs.get(glyphName)

        if glyph is None:
            glyphPack = self.storage.readGlyphPack(glyphName)

            try:
                # Reads glyph data from storage.
                glyph = Glyph(glyphName, glyphPack=glyphPack, parent=self)
                self._loadedGlyphs[glyphName] = glyph
            except Exception as e:
                print('Error while loading glyph %s' % glyphName)
                print(e)
                print(traceback.format_exc())
                # FIXME: not printing because of speed, should be caught and
                # collected before output.
                return
        return glyph

    def __setitem__(self, glyphName, glyphPack):
        if isinstance(glyphPack, Glyph):
            # Make sure to get the latest?
            glyphPack = glyphPack.parent.storage.readGlyphPack(glyphPack.name)

        glyph = Glyph(glyphName, glyphPack, parent=self)
        self._loadedGlyphs[glyphName] = glyph

    def getVarWidth(self, glyphName):
        return self.storage.getVarWidth(glyphName, self.location)

    def getVarOutline(self, glyphName):
        u"""Draws variation outline based using location."""
        if isinstance(self.storage, OTFStorage):
            # TODO: cache paths for specific locations.
            path = CanvasBezierPath(glyphSet=self)
            path = self.storage.getRepresentation(glyphName, self.location, path)
            return path._path
        else:
            print('getVarOutline(): to be implemented for %s' % type(self.storage))
            #raise ToBeImplementedError
        '''
        elif isinstance(self.storage, UFOStorage):
            # TODO: RFont now?
            # TODO: connect UFO to design space, mutator, etc. For now just
            # draw outline.
            # TODO: cache paths.
            pen = CocoaPen(glyphSet=self)
            glyph = self[glyphName]
            glyph.draw(pen)
            return pen.path
        '''

    def get(self, glyphName):
        try:
            return self[glyphName]
        except KeyError:
            print('Error finding glyph with name %s' % glyphName)
            return None

    def newGlyph(self, glyphName):
        return self[glyphName]

def _docTests():
    r"""
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("CusterRE-RegularS2.ttf")
        >>> s = Style(path)
        >>> len(s)
        248
        >>> g = s["a"]
        >>> len(g)
        2
        >>> for c in g:
        ...   len(c)
        46
        12
        >>> contour = g[0]
        >>> contour[0]
        P(x224 y36 #0 onCurve)
        >>> contour.getContext(0)
        [P(x229 y18 #45 offCurve), P(x224 y36 #0 onCurve), P(x206 y18 #1 offCurve)]
        >>> p_2, p_1, p, p1, p2 = g.contours[0].getContext(0, 2)
        >>> p
        P(x224 y36 #0 onCurve)
        >>> g.width
        320
        >>> g.unicodes
        [97]
        >>> g.unicode
        97
        >>> path = getFontPath("Condor-Regular.ufo")
        >>> s = Style(path)
        >>> s.unitsPerEm
        1000
        >>> s.ascender
        750
        >>> s.panose
    """

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
