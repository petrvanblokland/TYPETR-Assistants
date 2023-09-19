# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    interpolatorbits.py
#
#   Interpolation Mutator stuff. Used by inheriting e.g. Proof and Interpolator tools.
#
#    D E P R E C A T E D
#    Will be removed form BaseTool in the future.
#    Functions will be taken over by BuildVariations tool.


from mutatorMath.objects.mutator import buildMutator
from mutatorMath.objects.location import Location
from fontMath.mathGlyph import MathGlyph
from fontMath.mathInfo import MathInfo
from fontMath.mathKerning import MathKerning

from tnbits.model.objects.glyph import roundPoints, roundComponents, getAvatarGlyphs, nakedGlyph, getComponents,\
    getContours, setAutoStartPoints, isClockWise, closeContour, contourIsOpen, deleteComponent, getComponentBaseOrder
from tnbits.model.objects.style import getStyleKey
from tnbits.model import model

class ErrorItem(object):
    """Defines the behavior of error items, detected by the interpolation
    testing methods. Each of the paramters may be None, except the message. If
    there is a fixMethod defined, this can be called to try to fix the problem.
    If the method is None, there is currently nu automated (reliable) cure for
    the problem."""

    # Types of interpolation errors
    NOMASTERS = 'No Master'
    MISSINGMASTERGLYPH = 'Missing Master Glyph'
    CONTOURCOUNT = 'Contour Count'
    COMPONENTCOUNT = 'Component Count'
    MISSINGCOMPONENTBASE = 'Missing Component Base'
    DIFFERENTCOMPONENTBASE = 'Different Component Base'
    CONTOURCOUNT = 'Contour Count'
    CONTOURDIRECTION = 'Contour Direction'
    POINTCOUNT = 'Point Count'
    POINTTYPE = 'Point Type'
    POINTSMOOTHNESS = 'Point Smoothness'

    def __init__(self, errorType, styleKeys, glyphName, message, fixMethod=None,
                 componentIndex=None, cIndex=None, pIndex=None):
        self.errorType = errorType
        self.styleKeys = styleKeys
        self.glyphName = glyphName
        self.message = message
        self.fixMethod = fixMethod
        self.fixed = False # Flag to indicate if fixMethod has been called. Caller can check on this.
        self.componentIndex = componentIndex # Optional index for relevant component errors
        self.cIndex = cIndex # Optional contour index for relevant contour error
        self.pIndex = pIndex # Optional point index for point errors

    def __le__(self, error):
        return sorted((self.glyphName, error.glyphName))[0] == self.glyphName

    def __ge__(self, error):
        return sorted((self.glyphName, error.glyphName))[0] != self.glyphName

    def __repr__(self):
        s = "%s: %s" % (self.glyphName, self.message)
        if self.fixed:
            s = 'FIXED -- ' + s
        return s

    def fix(self):
        if self.fixMethod is not None:
            self.fixMethod(self)

class InterpolatorBits:
    #   Assumes self.family to be defined.

    def getMutators(self):
        """Answer self._mutators. Initialize it as dictionary if it is still None."""
        if self._mutators is None:
            self._mutators = {}
        return self._mutators

    def clearMutators(self):
        """Clear dictionary with Mutator instances. Key is glyph name. Clear if
        one of the master changes."""
        self._mutators = None

    def setChangedColor(self, glyph):
        """Set the color in RoboFont, as it changed, if the flags are on."""
        if self._setRFColorOnChange:
            glyph.mark = self._colorOnChangedGlyph

    def updateInterpolation(self, c, glyphNames=None, instanceKeys=None, errors=None):
        """Update the interpolation for the given glyphName and the given
        instance and given constellation c. Update the interpolations for all
        instances in the family, if instance is None. Add ErrorItems instances
        to errors list, if defined. This method is also used for updating the
        "open design space" canvas style in Interpolator."""
        if instanceKeys is None:
            instanceKeys = c.getInstanceKeys() # Get all instance keys of opened instances from the constellation.

        masterKeys = c.getMasterKeys() # Get first master in the glyph line and see how the glyph is constructed.

        if masterKeys:
            if glyphNames is not None: # Collect all glyph names from all masters
                glyphNames = set(glyphNames)
            else:
                glyphNames = set()
                for masterKey in masterKeys:
                    master = self.family.getStyle(masterKey)
                    glyphNames = glyphNames.union(set(master.keys()))
            # Now check again if all glyphs are in all masters
            for masterKey in masterKeys:
                master = self.family.getStyle(masterKey)
                for glyphName in sorted(glyphNames.difference(set(master.keys()))):
                    # This glyphName is not in the master, but it is in one of the others.
                    if errors is None:
                        errors = []
                    errors.append(ErrorItem(ErrorItem.MISSINGMASTERGLYPH, [masterKey], glyphName,
                        'Glyph(%s) does not exist in Master(%s)' % (glyphName, master.info.styleName),
                        fixMethod=self.fixMissingGlyph))

            for instanceKey in instanceKeys:
                # InstanceKey can be (familyPath, fileName) but also ('', 5751248016) in case of temp dragging instance.
                # Code handling the instanceKey should be aware that family path can be empty and that fileName can be
                # unique integer number, if the style does not have a path.
                interpolatedGlyphs = set()
                for glyphName in glyphNames:
                    self.updateGlyphInterpolation(c, glyphName, instanceKey, interpolated=interpolatedGlyphs,
                        errors=errors) # Just do one glyph.
                    # No need for now to update the font.info and kerning here.
                instance = self.family.getStyle(instanceKey)
                # If there is a difference, not all glyphs could interpolate rightly. Mark them in the instance.
                # We have to do this after the whole interpolation loop, because there is recursive interpolation
                # for different glyphs necessary.
                instanceKeys = set(instance.keys())
                for glyphName in glyphNames:
                    if glyphName in instanceKeys:
                        if not glyphName in interpolatedGlyphs:
                            instance[glyphName].mark = (1, 0.8, 0.8, 1)
                        else:
                            instance[glyphName].mark = (0.9, 0.9, 1, 1)
                # Remove the instance glyphs that are not in one of the masters
                for glyphName in instanceKeys:
                    if not glyphName in glyphNames:
                        del instance[glyphName]
                updateStyle(instance) # Update RoboFont, in case the font is open

    def updateInfoInterpolation(self, c, instanceKey):
        """Interpolating instance.info from constellation c."""
        # Make sure never to interpolate masters or locked instances.
        instance = c.getStyle(instanceKey)

        # Test if we, for some reason, did not get an instance with the key
        # Make sure never to interpolate masters or locked instances.
        if instance is None or c.isMaster(instanceKey) or c.isLocked(instanceKey):
            return

        infoMutator = self.getInfoMutator(c)

        if infoMutator is not None:
            location = Location()

            for axisName in c.getActiveAxisNames(): # WHY? --> Do all axes here, not just the active/visible
                interpolationValue = c.getStyleInterpolationAxis(instanceKey, axisName)

                if interpolationValue is not None:
                    location[axisName] = interpolationValue

            # Make interpolated info instance.
            infoInstance = infoMutator.makeInstance(location)
            # Write info instance into the style
            instance = c.getStyle(instanceKey)

            if instance is not None: # We can only extract it the instance really exists.
                infoInstance.extractInfo(instance.info)

    def updateKerningInterpolation(self, c, instanceKey):
        """Interpolating instance.kerning from constellation c. """
        instance = c.getStyle(instanceKey)
        # Test if we, for some reason, did not get an instance with the key
        # Make sure never to interpolate masters or locked instances.
        if instance is None or c.isMaster(instanceKey) or c.isLocked(instanceKey):
            return
        kerningMutator = self.getKerningMutator(c)
        if kerningMutator is not None:
            location = Location()
            for axisName in c.getActiveAxisNames(): # WHY? --> Do all axes here, not just the active/visible
                interpolationValue = c.getStyleInterpolationAxis(instanceKey, axisName)
                if interpolationValue is not None:
                    location[axisName] = interpolationValue
            # Make interpolated kerning instance.
            kerningInstance = kerningMutator.makeInstance(location)
            # Write kerning instance into the style
            kerningInstance.extractKerning(instance)

    def updateGlyphInterpolation(self, c, glyphName, instanceKey, interpolated=None, errors=None,
        preflight=False, roundGlyph=True):
        """Interpolate the instance glyph name, according to the existing
        mutators. The master is used as model to find any referenced component,
        because the interpolated glyph may not already exist in the instance.
        The optional "interpolated" attribute is a set that is recursively
        answered, containing all the interpolated glyph names.  This way the
        caller can decide that this method should not be called again if the
        glyph was already done (e.g. with component references of multiple
        glyphs to the same base glyph). Check on instanceKey: never interpolate
        on locked instances or masters.

        Preflight == True will just check on errors without doing actual
        interpolation."""
        instance = c.getStyle(instanceKey)
        # Test if we, for some reason, did not get an instance with the key
        # Make sure never to interpolate masters or locked instances.
        if instance is None or c.isMaster(instanceKey) or c.isLocked(instanceKey):
            return

        if interpolated is None: # Collect the names of glyphs that already are done through components.
            interpolated = set()

        if errors is None:
            errors = []

        # If there are components in the glyph, then recursively call for these
        # separate. Just take one of the masters to check for this, since all
        # references are supposed to be the same.
        foundErrors = False  # Detect if there was an error. Some are not raised by mutator.
        masterKeys = c.getMasterKeys()

        if masterKeys:
            # Pre-check if there are any errors. Better than trying to resolve
            # the error as it happens in the mutator. Try to add a useful error
            # description.
            self.preflightInterpolationGlyph(self.family, glyphName, masterKeys, errors=errors)

        try:
            # Update the mutator design space with the current fonts and axis
            # selection
            mutators = self.getMutators()

            if not glyphName in mutators:  # No cached mutator yet for this glyph. Create it.
                self.updateMutator(c, glyphName)

            location = Location()

            for axisName in c.getActiveAxisNames():  # WHY? --> Do all axes here, not just the active/visible
                interpolationValue = c.getStyleInterpolationAxis(instanceKey, axisName)
                if interpolationValue is not None:
                    location[axisName] = interpolationValue

            # Now get the interpolating glyph. Write the MathGlyph back into the instance.
            interpolatedGlyph = mutators[glyphName].makeInstance(location)
            if not glyphName in instance:
                instance.newGlyph(glyphName)
            glyph = instance[glyphName]
            nakedGlyph(glyph).disableNotifications()
            glyph.clear()
            self.setChangedColor(glyph)
            interpolatedGlyph.extractGlyph(glyph)

            # Get the avatar glyphs (in layers) that need to get the same interpolation.
            avatars = getAvatarGlyphs(glyph)

            # Add the glyphName only if it really got successfully interpolated.
            # Otherwise below is not reached, due to exception.
            interpolated.add(glyphName)
            glyph.width = interpolatedGlyph.width

            # Optionally round the interpolated points and component transformation
            if roundGlyph:
                roundPoints(glyph)
                roundComponents(glyph)
                glyph.width = int(round(glyph.width))
            nakedGlyph(glyph).enableNotifications()
            nakedGlyph(glyph)._destroyBoundsCache()
            nakedGlyph(glyph).dirty = True

        except (IndexError, KeyError):
            errors.append('Mutator interpolation error for glyph "%s"' % glyphName)

        # Answer the set with interpolated glyph names and the list of possible deteted errors,
        # so the called knows what has been done.
        return interpolated, errors

    def preflightInterpolation(self, family, styleKey, errors=None, testSmoothness=False):
        """Check if there is a problem with this interpolation masters of
        styleKey. Try to make a detailed problem description, so the designer
        can solve. A list of found error lines is answered."""
        masters = [] # Storage of master styles.
        # Collect the master keys, the related interpolate with styleKey in any of the constellations.
        masterKeys = family.getMasterKeysOfStyle(styleKey)
        if errors is None:
            errors = [] # Storage of found ErrorItem instances.
        glyphNames = set() # Collect all glyphs of all masters to compare.
        # Keep track of interpolated glyphs, in case of multiple glyphs referring to the same or even circular references.
        checkedGlyphNames = set()

        for masterKey in masterKeys:
            master = family.getStyle(masterKey)
            masters.append(master)
            glyphNames = glyphNames.union(set(master.keys()))
        # Now interpolate for all unique glyphnames in the combined set of masters.
        for glyphName in sorted(glyphNames):
            self.preflightInterpolationGlyph(family, glyphName, masters=masters, errors=errors, testSmoothness=testSmoothness)
        return errors

    def preflightInterpolationGlyph(self, family, glyphName, masterKeys=None, masters=None, errors=None,
        checkedGlyphNames=None, testSmoothness=False):
        assert masterKeys is not None or masters is not None # Make sure at least one of them is defined.
        if errors is None:
            errors = [] # Storage of found ErrorItem instances.
        if masters is None: # In case not defined (e.g if called to interpolate for a single glyph name)
            masters = []  # Collect once, not for every
            for masterKey in masterKeys:
                master = self.family.getStyle(masterKey)
                if master is not None:
                    masters.append(master)
        if checkedGlyphNames is None:
            checkedGlyphNames = set() # Keep track of multiple glyphs referring to the same component base or even circular.
        self._preflightInterpolationGlyph(family, glyphName, masters, errors, checkedGlyphNames,
            testSmoothness=testSmoothness)
        return errors

    def _preflightInterpolationGlyph(self, family, glyphName, masters, errors, checkedGlyphNames, testSmoothness=False):
        if not masters: # Cannot be fixed automatically.
            errors.append(ErrorItem(ErrorItem.NOMASTERS, [], glyphName, 'No valid Master styles defined.'))
            return
        if len(masters) == 1: # Cannot be fixed automatically.
            errors.append(ErrorItem(ErrorItem.NOMASTERS, [], glyphName, 'Cannot interpolate from one Master.'))
            return

        checkedGlyphNames.add(glyphName)

        # Do a precheck to see if all master glyphs have components with valid base glyphs.
        # We make recursive calls and meanwhile interpolate the referenced glyphs (only once).
        for master in masters:
             if master is not None and glyphName in master:
                for component in master[glyphName]._components:
                    if not component.baseGlyph in master:
                        errors.append(ErrorItem(ErrorItem.MISSINGCOMPONENTBASE,
                            [getStyleKey(master)], glyphName,
                            'Component(%s) base does not exist in Master(%s).' % (
                            component.baseGlyph, master.info.styleName),
                            fixMethod=self.fixMissingBaseGlyph))
                    else:
                        # Do a pre-check if referenced glyphs for all masters have contours with the same point structure
                        self._preflightInterpolationGlyph(family, component.baseGlyph, masters, errors, checkedGlyphNames)

        for mIndex, master1 in enumerate(masters):  # Check for the amount contours
            if not glyphName in master1:
                errors.append(ErrorItem(ErrorItem.MISSINGMASTERGLYPH,
                    [getStyleKey(master1)], glyphName,
                    'Glyph does not exist in Master(%s)".' % master1.info.styleName,
                    fixMethod=self.fixMissingGlyph))
                continue
            for master2 in masters[mIndex + 1:]:
                if not glyphName in master2:
                    errors.append(ErrorItem(ErrorItem.MISSINGMASTERGLYPH,
                        [getStyleKey(master2)], glyphName,
                        'Glyph does not exist in Master(%s)".' % master2.info.styleName,
                        fixMethod=self.fixMissingGlyph))
                    break
                mGlyph1 = master1[glyphName]
                mGlyph2 = master2[glyphName]
                # Components
                mComponents1 = getComponents(mGlyph1)
                mComponents2 = getComponents(mGlyph2)
                if len(mComponents1) != len(mComponents2):
                    errors.append(ErrorItem(ErrorItem.COMPONENTCOUNT,
                        [getStyleKey(master1), getStyleKey(master2)], glyphName,
                        'Master(%s) has %d components. Master(%s) has %d components.' % (
                        master1.info.styleName, len(mComponents1), master2.info.styleName,
                        len(mComponents2)),
                        fixMethod=self.fixUnequalComponentCount))
                else:
                    for cIndex, mComponent1 in enumerate(mComponents1):
                        mComponent2 = mComponents2[cIndex]
                        if not mComponent1.baseGlyph in master1:
                            errors.append(ErrorItem(ErrorItem.MISSINGCOMPONENTBASE, [getStyleKey(master1)],
                                glyphName, 'Component(base=%s) does not exist in Master(%s).' % (
                                mComponent1.baseGlyph, master1.info.styleName),
                                fixMethod=self.fixMissingComponentBase, componentIndex=cIndex))
                        if not mComponent2.baseGlyph in master2:
                            errors.append(ErrorItem(ErrorItem.MISSINGCOMPONENTBASE, [getStyleKey(master2)],
                                glyphName, 'Component(base=%s) does not exist in Master(%s).' % (
                                mComponent2.baseGlyph, master2.info.styleName),
                                fixMethod=self.fixMissingComponentBase, componentIndex=cIndex))
                        if mComponent1.baseGlyph != mComponent2.baseGlyph:
                            errors.append(ErrorItem(ErrorItem.DIFFERENTCOMPONENTBASE,
                                [getStyleKey(master1), getStyleKey(master2)], glyphName,
                                'Master(%s) component(%d/reference=%s) not equal to Master(%s) component(%d/reference=%s).' % (
                                    master1.info.styleName, cIndex, mComponent1.baseGlyph, master2.info.styleName,
                                    cIndex, mComponent2.baseGlyph),
                            fixMethod=self.fixUnequalComponentBase, componentIndex=cIndex))
                # Contours
                contours1 = getContours(mGlyph1)
                contours2 = getContours(mGlyph2)
                if len(contours1) != len(contours2):
                    errors.append(ErrorItem(ErrorItem.CONTOURCOUNT,
                        [getStyleKey(master1), getStyleKey(master2)], glyphName,
                        'Master(%s) has %d contours. Master(%s) has %d contours.' % (
                        master1.info.styleName, len(contours1), master2.info.styleName, len(contours2)),
                        fixMethod=self.fixContourCount))
                else:
                    for cIndex, mContour2 in enumerate(contours2):
                        checkedContour = False
                        contour1 = contours1[cIndex]
                        if len(contour1) != len(mContour2):
                            errors.append(ErrorItem(ErrorItem.POINTCOUNT,
                                [getStyleKey(master1), getStyleKey(master2)], glyphName,
                                'Master(%s) contour(%d/length=%d) not equal to Master(%s) contour(%d/length=%d).' % (
                                master1.info.styleName, cIndex, len(contour1), master2.info.styleName, cIndex,
                                len(mContour2)),
                                fixMethod=self.fixContourLength, cIndex=cIndex))
                            break
                        if contour1.clockwise != mContour2.clockwise:
                            errors.append(ErrorItem(ErrorItem.CONTOURDIRECTION,
                                [getStyleKey(master1), getStyleKey(master2)], glyphName,
                                'Master(%s) contour(%d/clockwise=%s) not equal to Master(%s) contour(%d/clockwise=%s).' % (
                                master1.info.styleName, cIndex, contour1.clockwise, master2.info.styleName, cIndex,
                                mContour2.clockwise),
                                fixMethod=self.fixContourDirection, cIndex=cIndex))
                            break
                        # Now we know to gave contours of the same length, we test on the segment types.
                        for pIndex, p1 in enumerate(contour1):
                            p2 = mContour2[pIndex]
                            if p1.segmentType != p2.segmentType:
                                errors.append(ErrorItem(ErrorItem.POINTTYPE,
                                    [getStyleKey(master1), getStyleKey(master2)], glyphName,
                                    'Master(%s) point(%d/%d/type=%s) not equal to Master(%s) point(%d/%d/type=%s).' % (
                                    master1.info.styleName, cIndex, pIndex, p1.segmentType, master2.info.styleName,
                                    cIndex, pIndex, p2.segmentType),
                                    fixMethod=self.fixStartPointOrPointTypes, cIndex=cIndex, pIndex=pIndex))
                                checkedContour = True # Avoid multiple errors on the same contour compare.
                                break
                            if testSmoothness and p1.smooth != p2.smooth:
                                errors.append(ErrorItem(ErrorItem.POINTSMOOTHNESS,
                                    [getStyleKey(master1), getStyleKey(master2)], glyphName,
                                    'Master(%s) point(%d/%d/%s/smooth=%s) not equal to Master(%s) point(%d/%d/%s/smooth=%s).' % (
                                    master1.info.styleName, cIndex, pIndex, p1.segmentType, p1.smooth,
                                    master2.info.styleName, cIndex, pIndex, p2.segmentType, p2.smooth),
                                    fixMethod=self.fixMasterSmoothPoints, cIndex=cIndex, pIndex=pIndex))
                                checkedContour = True  # Avoid multiple errors on the same contour compare.
                                break
                        if checkedContour: # Something wrong with this contour pair, already mentioned in errors.
                            break

    def fixMasterSmoothPoints(self, masters, glyphName):
        """Fix any difference between the masters glyph name for smooth flag
        of their points. (This assumes all outlines to have the same length
        and rotation, start points at the right positions and all points
        interpolating rightly with the same type)."""
        # TODO: correct the smoothness by context first: an on-curve point cannot be smooth if both neighbors are on-curve too.
        # For now: correct all corresponding master points to smooth if one of them is
        pass

    def getInfoMutator(self, c):
        """Answer a MathInfo mutator for the current masters of c."""
        mutator = None # Answer is case there are no axes or no value
        items = []
        activeAxisNames = c.getActiveAxisNames()
        for masterKey in c.getMasterKeys():
            style = c.getStyle(masterKey)
            if style is None:
                continue
            location = None
            axisDict = c.getStyleInterpolations(masterKey)
            for axisName, axisValue in axisDict.items():
                if axisName in activeAxisNames and axisValue is not None:
                    if location is None:
                        location = Location()
                    location[axisName] = axisValue
            if location is not None:
                items.append((location, MathInfo(style.info)))
        if items: # Found any valid master or axis to interpolate?
            try:
                ok, mutator = buildMutator(items)
                if not ok:
                    mutator = None
            except IndexError:
                pass # Ignore this mutator, master info is not matching
        return mutator

    def getKerningMutator(self, c):
        """Answer a MathKerning mutator for the current masters of
        Constellation c."""
        mutator = None # Answer is case there are no axes or no value
        items = []
        activeAxisNames = c.getActiveAxisNames()
        for masterKey in c.getMasterKeys():
            style = c.getStyle(masterKey)
            if style is None:
                continue
            location = None
            axisDict = c.getStyleInterpolations(masterKey)
            for axisName, axisValue in axisDict.items():
                if axisName in activeAxisNames and axisValue is not None:
                    if location is None:
                        location = Location()
                    location[axisName] = axisValue
            if location is not None:
                items.append((location, MathKerning(style.kerning, style.groups)))
        if items: # FOund any valid master or axis to interpolate?
            try:
                ok, mutator = buildMutator(items)
                if not ok:
                    mutator = None
            except IndexError:
                pass # Ignore this mutator, master kerning is not matching
        return mutator

    def updateMutator(self, c, glyphName):
        """Something changed to the axis or master definitions. Construct a
        new Mutator for the current selected glyph. Beware just set the values
        for the selected axes, or else MutatorMath gets confused ("ambigious
        info") and won't do the interpolation."""
        items = []
        # Run through the defined masters to build the mutator.
        activeAxisNames = c.getActiveAxisNames()
        for masterKey in c.getMasterKeys():
            style = self.family.getStyle(masterKey)
            if style is None or not glyphName in style: # This style does not add to this mutator, as the glyph does not exist.
                continue
            glyph = style[glyphName]
            # Note that the glyph may be empty (no contours or components) but we still need to interpolate
            # because we always need the interpolated width. But it needs checking by the caller if there is
            # no data in the interpolated glyph.
            location = None
            axisDict = c.getStyleInterpolations(masterKey)
            for axisName in activeAxisNames:
                if axisName in axisDict:
                    if location is None:
                        location = Location()
                    location[axisName] = axisDict[axisName]
            if location is not None:
                items.append((location, MathGlyph(glyph)))
        if items: # Found any valid master or axis to interpolate?
            try:
                ok, mutator = buildMutator(items)
                self.getMutators()[glyphName] = mutator
            except IndexError:
                pass # Ignore this mutator, master glyphs are not matching.

    #   F I X I N G  E R R O R S

    def fixMissingGlyph(self, errorItem):
        """If the glyph does not exist or it is empty and the source is not
        empty, then make a copy. Also check if the problem exists in the other
        masters, then copy it there too."""
        fixed = False
        glyphName = errorItem.glyphName
        styleKey = errorItem.styleKeys[0] # First one is target.
        family = model.getFamily(styleKey[0])
        masterKeys = family.getMasterKeysOfStyle(styleKey) # No matter in which constellation they are used.
        # Try to find a master that has a glyph with this name to use as source for the missing glyph in other masters.
        sourceMaster = None
        for masterKey in masterKeys:
            master = family.getStyle(masterKey)
            if master is not None and glyphName in master:
                # We found one, take this as source.
                sourceMaster = master
                break
        if sourceMaster is not None: # Only if we found one. Should never happen that we don't
            for masterKey in masterKeys:
                targetStyle = family.getStyle(masterKey)
                if not glyphName in targetStyle: # No need to copy in case it is there, also includes the source master.
                    targetStyle.insertGlyph(sourceMaster[glyphName])
                    targetStyle[glyphName].mark = (1, 0.2, 0.2, 0.4) # Mark that we copied this one. Needs adjustment to master.
                    fixed = True
                    updateStyle(targetStyle)
        errorItem.fixed = fixed
        print(errorItem)

    def fixMissingBaseGlyph(self, errorItem):
        """There are components with base names referring to non-existing
        glyphs. Delete these components."""
        fixed = False
        glyphName = errorItem.glyphName
        for styleKey in errorItem.styleKeys:
            master = model.getStyle(styleKey)
            if master is not None and glyphName in master: # Otherwise ignore, cannot solve that here.
                self._deleteComponentsWithMissingBase(master, glyphName)
                fixed = True # We fixed something.
                updateStyle(master)

        errorItem.fixed = fixed
        print(errorItem)

    def _deleteComponentsWithMissingBase(self, style, glyphName):
        """Delete the component from the glyph, if the referenced base glyph
        is missing in the style. Return the flag if something was fixed."""
        fixed = False
        g = style[glyphName]
        for component in getComponents(g):
            if not component.baseGlyph in style:
                deleteComponent(g, component)
                fixed = True # We changed something
        return fixed

    def fixUnequalComponentCount(self, errorItem):
        """compare the components of the two styles. The copy the difference
        and mark the target glyphs as changed."""
        assert len(errorItem.styleKeys) == 2
        fixed = False
        glyphName = errorItem.glyphName
        master1 = model.getStyle(errorItem.styleKeys[0])
        master2 = model.getStyle(errorItem.styleKeys[1])
        assert glyphName in master1 and glyphName in master2 # Just to make sure. Should never happen here.
        # Make sure all referenced base glyphs exist.
        self._deleteComponentsWithMissingBase(master1, glyphName)
        self._deleteComponentsWithMissingBase(master2, glyphName)
        glyph1 = master1[glyphName]
        glyph2 = master2[glyphName]
        # {glyphBase: (index1, index3, ...), ...} there may be more than one reference to the same base.
        componentBaseOrder1 = getComponentBaseOrder(glyph1)
        componentBaseOrder2 = getComponentBaseOrder(glyph2)
        """
        # Now compare the two, they should match in base names and counts.
        for baseGlyph, cIndices1 in componentBaseOrder1.items():
            if sorted(cIndices1) == sorted(cIndices2): # If they are identical, then there is nothing to fix.
                continue

            cIndices2 = componentBaseOrder2[baseGlyph]
            # If lengths are different, the one has more than the other. Copy the difference.
            if len(cIndices1) != len(cIndices2(2)):
                print('AAAAA', cIndices1,)
            # If the lengths are equal, but the tuples are different, then the order of components is wrong.

            # Now the indices should match.
            if count1 != count2: # Does not match, copy one to the other.

                continue
            # There is a difference. Figure out what to do.
        """
        #self.autoFixGlyphInterpolation(errorItem)
        print(errorItem)

    def fixUnequalComponentBase(self, errorItem):
        print(errorItem)

    def fixContourCount(self, errorItem):
        """Number of contours is different. Try to find matching contours
        (length and position) and then try to figure out which ones to copy to
        the target glyph to make the matching work.  Of course the glyph will
        need adjust after that."""
        #self.autoFixGlyphContours(errorItem)
        print(errorItem)

    def fixContourLength(self, errorItem):
        #self.autoFixGlyphContours(errorItem)
        print(errorItem)

    def fixStartPointOrPointTypes(self, errorItem):
        assert len(errorItem.styleKeys) == 2
        fixed = False
        glyphName = errorItem.glyphName
        master1 = model.getStyle(errorItem.styleKeys[0])
        master2 = model.getStyle(errorItem.styleKeys[1])

        glyph1 = master1[glyphName]
        if glyphName in master2:  # Should never happen here. We cannot fix, otherwise ignore.
            glyph2 = master2[glyphName]
            changed1 = setAutoStartPoints(glyph1)
            changed2 = setAutoStartPoints(glyph2)
            # For now. Later check if this solved (there are exceptions in master-drawings where the results not identical.
            # In that case, try to fix better.
            fixed = changed1 or changed2
            if changed1:
                updateStyle(glyph1.getParent())
            if changed2:
                updateStyle(glyph2.getParent())
        errorItem.fixed = fixed

    def fixContourDirection(self, errorItem):
        # Check if there is mismatch between the sizes of contours. Otherwise reconnect them in order of length and position.
        assert len(errorItem.styleKeys) == 2
        fixed = False
        glyphName = errorItem.glyphName
        master1 = model.getStyle(errorItem.styleKeys[0])
        master2 = model.getStyle(errorItem.styleKeys[1])

        glyph1 = master1[glyphName]
        if glyphName in master2:  # Should never happen here. We cannot fix, otherwise ignore.
            glyph2 = master2[glyphName]
            # Check if there are any open contours. Otherwise close them.
            contours1 = getContours(glyph1)
            contours2 = getContours(glyph2)
            for contours in (contours1, contours2):
                for contour in contours:
                    if contourIsOpen(contour):
                        closeContour(contour)
                        fixed = True # We fixed something
            # Fix directions of the contours.
            for index, contour1 in enumerate(glyph1):
                if index < len(master2[glyphName]): # Assume the same amount of contours. Other ignore here.
                    contour2 = master2[glyphName][index]
                    if isClockWise(contour1) != isClockWise(contour2):
                        contour2.reverse()
                        fixed = True # We fixed something.
        if fixed:
            updateStyle(master2)
        errorItem.fixed = fixed

    def syncContourOrder(self, glyphName, master, referenceMaster):
        """If the glyph exists in both styles, run through the contours and
        see if there is better match possible, considering their length and
        position. This will fix the order better. Still there may be
        incompatible contours, but the matching will be closer to the final
        matching."""
        if not glyphName in master or not glyphName in referenceMaster:
            return False  # Nothing changed.
        glyph = master[glyphName]
        rGlyph = referenceMaster[glyphName]
        contours = {}  # Ordered by their length
        for contour in glyph:
            pass
            # Distance of left-bottom from origin

            # key = '%04d-%10d' % (len(contour), )
            # if not len(contour) in contours:

        pass
