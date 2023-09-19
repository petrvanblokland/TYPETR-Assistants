# methods from interpolatorbits
"""
fixMissingGlyph
fixMissingBaseGlyph
fixUnequalComponentCount
fixUnequalComponentBase
fixContourCount
fixContourLength
fixStartPointOrPointTypes
fixContourDirection
"""

# Assuming origin has the correct structure
# Use the origin to compare with other masters
# (glyph, otherGlyphs)

# THINGS TO CHECK
# glyph
# - missing glyph
# - unicode value
# contours
# - number of contours
# - contour order
# - contour direction
# - start point
# points
# - number of points
# - point type
# components
# - number of components
# - component order
# - component base glyph
# anchors
# - number of anchors
# - anchor names


# These methods should return information about what is wrong.
# E.g. error in anchor count for a glyph, error item could open that glyph and show anchors...

# M InterpolationGlyphError
# V InterpolationErrorView (FixInterpolations)
# C InterpolationValidator

# InterpolationFeatureError?
# InterpolationGroupError?
# InterpolationKerningError?

# TODO idea: VeryStrictPen or something that validates the point structure to be identical. Needed to build interpolatable ttfs
# TODO it would validate origin vs otherGlyphs, and report which are not compatible.

# View

from vanilla import Group, List, Button, CheckBoxListCell, PopUpButton, TextBox
# TODO
# fix selected
# fix all of same type e.g. fix all unicodes
class InterpolationErrorView(Group):

    SELECT_NONE = "None"
    SELECT_ALL = "All"
    SELECT_SAME = "Same"

    SELECT_METHODS = {
        SELECT_NONE: "selectNone",
        SELECT_ALL: "selectAll",
        SELECT_SAME: "selectSame",
    }

    def __init__(self, posSize, font, otherFonts):
        Group.__init__(self, posSize)
        self.font = font
        self.otherFonts = otherFonts
        self.interpolationValidator = InterpolationValidator(font, otherFonts)

        selectActions = [self.SELECT_NONE, self.SELECT_ALL, self.SELECT_SAME]

        self.selectAction = PopUpButton((10, 10, 20, 20), selectActions, callback=self.selectActionCallback)

        errorListColumnDescriptions = [
            dict(title="", key="selected", width=20, cell=CheckBoxListCell()),
            dict(title="Type", key="type", width=100),
            dict(title="Error", key="error")]
        self.errorList = List((0, 40, -0, -40), [], columnDescriptions=errorListColumnDescriptions)
        self.validateButton = Button((10, -30, 80, 20), "Validate", callback=self.validateButtonCallback)
        self.fixButton = Button((-70, -30, 60, 20), "Fix", callback=self.fixButtonCallback)

    def setFonts(self, font, otherFonts):
        self.font = font
        self.otherFonts = otherFonts
        # TODO delete validator and create new one?
        # TODO update errorList

    def setErrorList(self, errors):
        errorList = []
        for error in errors:
            item = dict(selected=False, type=error.type, error=error) # keep the error object, the list will display the error __repr__ (message)
            errorList.append(item)
        self.errorList.set(errorList)

    def validateButtonCallback(self, sender):
        self.interpolationValidator.validateAllGlyphs()
        errors = self.interpolationValidator.glyphErrors
        self.setErrorList(errors)

    def fixButtonCallback(self, sender):
        selectedItems = []
        for item in self.errorList.get():
            if item["selected"]:
                selectedItems.append(item)

        print('will fix:')
        print(selectedItems)

    def selectActionCallback(self, sender):
        item = sender.getItem()
        select = self.SELECT_METHODS.get(item)
        selectMethod = getattr(self, select)
        selectMethod()

    def selectNone(self):
        for item in self.errorList.get():
            item["selected"] = False

    def selectAll(self):
        for item in self.errorList.get():
            item["selected"] = True

    def selectSame(self):
        selection = self.errorList.getSelection()
        if len(selection) != 1:
            return
        index = selection[0]
        errorList = self.errorList.get()
        selected = errorList[index]
        selectedType = selected["type"]

        for item in errorList:
            if item["type"] == selectedType:
                item["selected"] = True


# Model
class InterpolationGlyphError(object):

    def __init__(self, type, message, errorGlyph, glyph=None, fixMethod=None):
        self.type = type
        self.message = message
        self.errorGlyph = errorGlyph
        self.glyph = glyph
        self.fixMethod = fixMethod

    def __repr__(self):
        return self.message

    def fix(self):
        if self.fixMethod is not None:
            self.fixMethod(self)

# TODO test cases for this class
# Controller
class InterpolationValidator(object):
    # test one glyph
    # test all glyph

    def __init__(self, font, otherFonts):
        self.font = font
        self.otherFonts = otherFonts
        self.glyphErrors = []

    def _get_otherGlyphs(self, glyphName):
        otherGlyphs = []
        for otherFont in self.otherFonts:
            if glyphName not in otherFont:
                message = "Glyph error: Glyph %s not in Font %s" % (glyphName, otherFont) # TODO pretty name for font
                #errorItem = InterpolationGlyphError() # TODO is this an InterpolationFontError ?
            else:
                otherGlyph = otherFont[glyphName]
                otherGlyphs.append(otherGlyph)
        return otherGlyphs

    def validateAllGlyphs(self):
        self.glyphErrors = [] # fresh start
        for glyph in self.font:
            otherGlyphs = self._get_otherGlyphs(glyph.name)
            # unicodes
            unicodeErrors = self.validateUnicodes(glyph, otherGlyphs)
            self.glyphErrors += unicodeErrors
            # other validation
            # ...

    def validateUnicodes(self, glyph, otherGlyphs):
        unicodeErrors = []
        for otherGlyph in otherGlyphs:
            if otherGlyph.unicodes != glyph.unicodes:
                type = "Unicode error"
                message = "Glyph %s unicode is %s instead of %s" % (otherGlyph.name, otherGlyph.unicodes, glyph.unicodes)
                item = InterpolationGlyphError(type, message, otherGlyph, glyph=glyph, fixMethod=fixUnicodes)
                unicodeErrors.append(item)
        return unicodeErrors

    # other methods...


#   S A N D B O X   #

def checkUnicodes(glyph, otherGlyphs):
    for otherGlyph in otherGlyphs:
        if otherGlyph.unicodes != glyph.unicodes:
            return False
    return True

def fixUnicodes(glyph, otherGlyphs):
    for otherGlyph in otherGlyphs:
        if otherGlyph.unicodes != glyph.unicodes:
            otherGlyph.unicodes = glyph.unicodes
    return True

def checkContourCount(glyph, otherGlyphs):
    for otherGlyph in otherGlyphs:
        if len(otherGlyph) != len(glyph):
            return False
    return True

# no fix method for contours count

def checkContourLength(glyph, otherGlyphs):
    if not checkContourCount(glyph, otherGlyphs):
        return False
    for otherGlyph in otherGlyphs:
        for i, contour in enumerate(otherGlyph):
            if len(contour) != len(glyph[i]):
                return False
    return True

def fixContourLength(glyphs, otherGlyphs):
    pass
    # try autoContourOrder
    # otherwise fail

def checkAnchorCount(glyph, otherGlyphs):
    for otherGlyph in otherGlyphs:
        if len(otherGlyph.anchors) != len(glyph.anchors):
            return False
    return True

# no fix method for anchors count
