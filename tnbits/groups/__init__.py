# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     __init__.py
#
#     Operations on kerning and spacing groups.

from tnbits.base.constants.groups import *
from tnbits.toolbox.fontparts.groups import GroupsTX
from fontTools.misc.arrayTools import unionRect
import logging

logger = logging.getLogger(__name__)

def _findGroupBaseGlyph(groupName):
    for pattern in ('SPC_L_', 'MMK_L_', 'SPC_R_', 'MMK_R_', 'public.kern1.',
            'public.kern2.'):
        if pattern in groupName:
            return groupName.split(pattern)[-1].replace('_', '.')

def getSpaceOrKerningGroupNames(style, glyphName, groups):
    """Either returns spacing group or kerning group if spacing group doesn't
    exist, for both left and right groups. To be used in a spacing context."""
    leftName = getSpaceGroupName(style, glyphName, groups, LEFT)
    rightName = getSpaceGroupName(style, glyphName, groups, RIGHT)
    return leftName, rightName

# Kerning.

def changeKerning(style, previousGlyphName, glyphName, stepX, groups, stepY=0,
        round2Step=True):
    """Changes kerning value for a glyphs pair. Ignores vertical kerning for
    now (needs to be set in GPOS)."""
    if not stepX:
        return False

    if previousGlyphName is not None:
        # Makes group names for glyphs. Can be None if pair does not exist as
        # group of glyph names.
        k = getGroupKerning(style, previousGlyphName, glyphName, groups)

        # Sets the kerning as group name if is can be found for the glyph
        # names. Otherwise set a single glyph name in the pair. Set to new
        # rounded value.
        if round2Step:
            s = int((k - k % stepX + stepX) / stepX) * stepX
        else:
            s = int(k + stepX)

        _setGroupKerning(style, previousGlyphName, glyphName, s, groups,
                round2Step=round2Step)

    return True

def fixKerningGroups(style):
    for groupName in style.groups.keys():
        pass

def getKernGroupNames(style, glyphName, groups):
    g2lg, g2rg, _, _ = groups
    groupL = None
    groupR = None

    if not GroupsTX.isRightKernGroup(glyphName) and \
            glyphName in g2lg[style.path]:
        groupL = g2lg[style.path][glyphName][0]

    if not GroupsTX.isLeftKernGroup(glyphName) and \
            glyphName in g2rg[style.path]:
        groupR = g2rg[style.path][glyphName][0]

    return groupL, groupR

def getGroupKerning(style, nameL, nameR, groups):
    """Gets value from group kerning or direct kerning if groups are missing.
    Answers the kerning best fitting the (nameL, nameR) pair. If one or both
    are glyph names then try the group they are part of for left or right.
    Otherwise try by their plain name. Test if there are single glyph kerning
    pairs, overwriting the group. Answers zero if the kerning pair (glyph names
    or group name) does not exist."""
    g2lg, g2rg, _, _ = groups
    groupL = nameL
    groupR = nameR

    if not GroupsTX.isLeftKernGroup(nameL):
        if nameL in g2lg[style.path]:
            groupL = g2lg[style.path][nameL][0]

    if not GroupsTX.isRightKernGroup(nameR):
        if nameR in g2rg[style.path]:
            groupR = g2rg[style.path][nameR][0]

    # Test for None, wich RF2 doesn't accept in kerning pairs.
    if not None in (nameL, nameR) and (nameL, nameR) in style.kerning:
        return style.kerning[(nameL, nameR)]

    if not None in (groupL, nameR) and (groupL, nameR) in style.kerning:
        return style.kerning[(groupL, nameR)]

    if not None in (nameL, groupR) and (nameL, groupR) in style.kerning:
        return style.kerning[(nameL, groupR)]

    if not None in (groupL, groupR) and (groupL, groupR) in style.kerning:
        return style.kerning[(groupL, groupR)]

    return 0

def _setGroupKerning(style, nameL, nameR, k, groups, round2Step=True):
    """Sets the kerning corresponding to the (nameL, nameR) pair.

    - If either nameL, nameR, or both are glyph names, look up the kerning pair.
    If one of the two combinations exists, we're dealing with an overwriting
    kerning pair.
    - Else we change the group value.
    """
    g2lg, g2rg, _, _ = groups
    groupL = nameL
    groupR = nameR

    if not GroupsTX.isLeftKernGroup(nameL):
        if nameL in g2lg[style.path]:
            groupL = g2lg[style.path][nameL][0]

    if not GroupsTX.isRightKernGroup(nameR):
        if nameR in g2rg[style.path]:
            groupR = g2rg[style.path][nameR][0]

    # Test for None, RoboFont doesn't accept None values in kerning pairs.

    if not None in (nameL, nameR) and (nameL, nameR) in style.kerning:
        _setKerning(style, (nameL, nameR), k, round2Step=round2Step)
    elif not None in (groupL, nameR) and (groupL, nameR) in style.kerning:
        _setKerning(style, (groupL, nameR), k, round2Step=round2Step)
    elif not None in (nameL, groupR) and (nameL, groupR) in style.kerning:
        _setKerning(style, (nameL, groupR), k, round2Step=round2Step)
    elif not None in (groupL, groupR):
        _setKerning(style, (groupL, groupR), k, round2Step=round2Step)

def _setKerning(style, pair, k, round2Step=True):
    """Sets the kerning if value != 0. Otherwise deletes the pair if it
    exists."""
    if k:
        style.kerning[pair] = k
        logger.info('Set kerning to %s for pair (%s, %s)' % (k, pair[0], pair[1]))
    elif pair in style.kerning:
        logger.info('No kerning for pair (%s, %s), removing it.' % pair)
        del style.kerning[pair]

# Spacing.

def getSpaceGroupName(style, glyphName, groups, mode):
    """Either returns spacing group or kerning group if spacing group doesn't
    exist, for left or right group.

    If there is a @SPC_L_ space group for this glyph it overwrites the @MMK_L_
    if it exists. Note that the groups are made for kerning, so for spacing we
    swap left and right groups."""
    if mode == LEFT:
        # Get any group named @SPC_<LR>_<glyphName>
        _, groupName = getSpaceGroupNames(style, glyphName, groups)
    else:
        groupName, _ = getSpaceGroupNames(style, glyphName, groups)

    # No space group, try a kern group.
    if not groupName:
        if mode == LEFT:
            _, groupName = getKernGroupNames(style, glyphName, groups)
        else:
            groupName, _ = getKernGroupNames(style, glyphName, groups)

    return groupName

def getSpaceGroupNames(style, glyphName, groups):
    _, _, g2lsg, g2rsg = groups
    groupL = None
    groupR = None

    if not GroupsTX.isLeftSpaceGroup(glyphName) and \
            glyphName in g2lsg[style.path]:
        groupL = g2lsg[style.path][glyphName][0]

    if not GroupsTX.isRightSpaceGroup(glyphName) and \
            glyphName in g2rsg[style.path]:
        groupR = g2rsg[style.path][glyphName][0]

    return groupL, groupR

def changeSpacing(style, glyphName, stepX, mode, groups, stepY=0,
        round2Step=True):
    """Changes the spacing of all glyphs in the group by stepX. Adjusts the
    width and optionally the position of the glyph.

    TODO? Make sure that total width never gets negative.
    TODO: check for multiple references / recursion.
    TODO: process stepY.
    """
    assert glyphName in style
    moved = set()
    glyph = style[glyphName]

    # If there are no contours or components, for example with space, then set
    # the glyph.width. Rounding to step size first.
    # TODO: check group behaviour.
    if glyph.leftMargin is None:
        glyph.width = _roundMargin2Step(glyph.width, stepX)
        moved.add(glyphName)

    groupName, group = _getGroup(style, glyph, groups, mode)
    groupBaseGlyph = _getGroupBaseGlyph(style, glyph, groupName)

    if not groupBaseGlyph:
        logger.error('Couldn\'t find base glyph for group %s' % groupName)
        return

    groupGlyphs = _getGroupGlyphs(style, groupBaseGlyph, group)
    marginBase = getMargin(groupBaseGlyph, mode)
    newMargin = _getNewMargin(groupBaseGlyph, mode, stepX, round2Step=round2Step)
    _setEqualSpacing(style, groupBaseGlyph, groups, mode, round2Step=round2Step)
    diffs = _getGroupDiffs(newMargin, groupGlyphs, mode)
    _moveGroup(groupGlyphs, diffs, mode, moved)
    logger.info("Set margin to %s for glyphs %s in group %s" % (newMargin, ', '.join(moved), groupName))

def fixSpacingGroups(style):
    fixed = []

    for groupName, group in style.groups.items():
        for glyphName in group:
            if not glyphName in style:
                fixed.append((glyphName, groupName))
                removeGlyphFromGroup(groupName, glyphName, style)

    return fixed

def removeGlyphFromGroup(groupName, glyphName, style):
    glyphNames = list(style.groups[groupName])
    glyphNames.remove(glyphName)
    style.groups[groupName] = glyphNames
    return glyphNames

def isLocked(glyph):
    if glyph.lib.get(EXTKEY_LOCK):
        return True
    return False

def toggleLock(glyph):
    glyph.lib[EXTKEY_LOCK] = not glyph.lib.get(EXTKEY_LOCK)

def setExtWidths(style, width, subExt):
    assert style
    glyphNames = []
    diffs = {}

    for glyphName in style.keys():
        if '.' in glyphName:
            parts = glyphName.split('.')
            ext = parts[-1]

            if subExt in ext:
                glyphNames.append(glyphName)

    for glyphName in glyphNames:
        glyph = style[glyphName]
        if glyph.width != width:
            glyph.width = width
            print('Set %s width to %s' %  (glyphName, width))

def _getGroupGlyphs(style, groupBaseGlyph, group):
    """Adds glyphs belonging to a group to a dictionary."""
    groupGlyphs = {}

    # Loads non-base group glyphs.
    for glyphName in group:
        #if glyphName == groupBaseGlyph.name:
        #    continue
        if not glyphName in style:
            continue

        glyph = style[glyphName]
        groupGlyphs[glyphName] = glyph

    return groupGlyphs

def _moveGroup(groupGlyphs, diffs, mode, moved):
    """Moves entire groups by precalculated offsets in diffs."""

    if mode == LEFT:
        for glyphName, glyph in groupGlyphs.items():
            diff = diffs[glyphName]

            if diff != 0:
                _moveGroupContours(glyph, diff, moved)

        for glyphName, glyph in groupGlyphs.items():
            diff = diffs[glyphName]

            if diff != 0:
                _moveGroupComponents(glyph, diff, moved)

    for glyphName, glyph in groupGlyphs.items():
        diff = diffs[glyphName]

        if diff != 0:
            glyph.width += diff

            # Not actually moved, but needed for log.
            if glyphName  not in moved:
                moved.add(glyphName)

def _moveGroupContours(glyph, diff, moved):
    """Moves non-base group glyph contours if not done already."""
    if glyph.contours:
        for contour in glyph.contours:
            contour.move((diff, 0))
    if glyph.anchors:
        for anchor in glyph.anchors:
            anchor.move((diff, 0))

    glyph.update()
    moved.add(glyph.name)

def _moveGroupComponents(glyph, diff, moved):
    """Moves all components except group base glyph."""
    if glyph.components:
        for component in glyph.components:
            # NOTE: component base glyph is a reference to the original
            # glyph, not the group base glyph.
            if component.baseGlyph not in moved:
                t = list(component.transformation)
                t[-2] += diff
                component.transformation = t

def equalizeSpacing(style, glyphName, groups, round2Step=True):
    """Sets all spacing to same value of base glyph.
    """
    assert glyphName in style
    glyph = style[glyphName]
    _setEqualSpacing(style, glyph, groups, LEFT, round2Step=round2Step)
    _setEqualSpacing(style, glyph, groups, RIGHT, round2Step=round2Step)

def _getGroupDiffs(value, groupGlyphs, mode):
    """Compares glyph margins against a value, usually a base margin, and
    stores the difference in a dictionary."""
    diffs = {}

    for glyphName, glyph in groupGlyphs.items():
        marginGlyph = getMargin(glyph, mode)
        # Moves by difference between the group base glyph margin and current
        # glyph margin.
        diff = value - marginGlyph
        diffs[glyphName] = diff

    return diffs

def _setEqualSpacing(style, glyph, groups, mode, round2Step=True):
    """Makes all group glyph margins the same as base glyph."""
    groupName, group = _getGroup(style, glyph, groups, mode)
    groupBaseGlyph = _getGroupBaseGlyph(style, glyph, groupName)
    groupGlyphs = _getGroupGlyphs(style, groupBaseGlyph, group)

    # TODO: optionally round to step.
    marginBase = getMargin(groupBaseGlyph, mode)
    diffs = _getGroupDiffs(marginBase, groupGlyphs, mode)
    moved = set()
    _moveGroup(groupGlyphs, diffs, mode, moved)
    if len(moved) > 0:
        logger.info("Equalized spacing for %s, moved %s" % (groupName, ', '.join(moved)))

# Group base glyph.

def getGroupBaseGlyphName(groupName):
    groupBaseGlyphName = _findGroupBaseGlyph(groupName)

    if groupBaseGlyphName is None:
        #TODO: add to message log.
        msg = 'Base glyph name is missing for group %s.' % groupName
        print(msg)

    return groupBaseGlyphName

def _getGroupBaseGlyph(style, glyph, groupName):
    """If there is a group, returns it's base glyph, else reutrns glyph."""
    if groupName:
        groupBaseGlyphName = getGroupBaseGlyphName(groupName)

        if not groupBaseGlyphName in style:
            #TODO: add to message log.
            msg = 'No base glyph "%s".' % groupBaseGlyphName
            print(msg)
            return

        return style[groupBaseGlyphName]

    else:
        return glyph

def _getGroup(style, glyph, groups, mode):
    groupName = getSpaceGroupName(style, glyph.name, groups, mode)

    if not groupName in style.groups.keys():
        # If the group does not exist, or there is no group for this glyph then
        # make a temporary one so we can set the spacing as if there was a group.
        group = set([glyph.name])
    else:
        group = set(style.groups[groupName])

    return groupName, group

def getMargin(glyph, mode):
    """
    Getting margin values directly from bounds.
    """
    bounds = _getContourComponentBounds(glyph)

    if mode == LEFT:
        if glyph.leftMargin is None:
            return
        return int(round(bounds[0]))
    else:
        if glyph.rightMargin is None:
            return
        return int(round(glyph.width - bounds[2]))

def _getContourComponentBounds(glyph):
    bounds = None
    subObjects = [contour for contour in glyph]
    subObjects += [component for component in glyph.components]

    for subObject in subObjects:
        b = getattr(subObject, 'bounds')
        if b is not None:
            if bounds is None:
                bounds = b
            else:
                bounds = unionRect(bounds, b)

    return bounds


def _getNewMargin(groupBaseGlyph, mode, step, round2Step=True):
    oldMargin = getMargin(groupBaseGlyph, mode)

    if round2Step:
        newMargin = _roundMargin2Step(oldMargin, step)
    else:
        newMargin = oldMargin + step

    return newMargin

def _setMargin(glyph, margin, mode):
    """Sets the margin of glyph. If glyph has a base glyph and components, then
    take that as margin reference. Otherwise just use margin. Don't update the
    glyph, just answer if it changed."""

    if mode == LEFT:
        oldMargin = glyph.leftMargin
        glyph.leftMargin = margin
        newMargin = glyph.leftMargin
    else:
        oldMargin = glyph.rightMargin
        glyph.rightMargin = margin
        newMargin = glyph.rightMargin

    diff = newMargin - oldMargin
    #print('Set %s margin for glyph %s from %s to %s, diff is %s' % (mode.lower(), glyph.name, oldMargin, newMargin, diff))
    return diff

def _moveBy(glyph, diff, mode):
    """Sets the margin of glyph. If glyph has a base glyph and components, then
    take that as margin reference. Otherwise just use margin. Don't update the
    glyph, just answer if it changed."""
    glyph.move((diff, 0))
    glyph.width += diff
    #print('Moved %s by %s for glyph %s' % (mode.lower(), diff, glyph.name))

# Helper functions.

def _roundMargin2Step(margin, step):
    """Rounding takes place in the direction of the step."""
    return int(margin / step) * step + step

# Make.

def g(groups, name, group):
    groups[name] = sorted(set(group))

def makeGroups(style, groupsDict):
    groups = style.groups
    groups.clear()

    for key, value in groupsDict.items():
        g(groups, key, value)

def makeRomanGroups(style):
    makeGroups(style, DEFAULTGROUPS_ROMAN)

def makeItalicGroups(style):
    makeGroups(style, DEFAULTGROUPS_ITALIC)

# QA.

def checkGlyphs(masters):
    for path, master in masters.items():
        changed = False
        if master.path == regular.path:
            continue
        for g in regular:
            if not g.name in master:
                report('Glyphs: Regular "%s" missing in %s' % (g.name, master.info.styleName))
                if FIX:
                    master[g.name] = g
                    changed = True
        for g in master:
            if not g.name in regular:
                report('Glyphs: %s "%s" missing in Regular' % (master.info.styleName, name))
                if FIX:
                    regular[g.name] = g
                    changed = True
        if changed:
            master.update()

def checkGroups(masters):
    for path, master in masters.items():
        changed = False

        if master.path == regular.path:
            continue

        for name, group in regular.groups.items():
            if not name in master.groups:
                report('Groups: Regular "%s" missing in %s' % (name, master.info.styleName))
                if FIX:
                    master.groups[name] = group
                    changed = True

        for name, group in master.groups.items():
            if not name in regular.groups:
                report('Groups: %s "%s" missing in Regular' % (master.info.styleName, name))
                if FIX:
                    regular.groups[name] = group
                    regular.update()
                continue

            if sorted(regular.groups[name]) != sorted(group):
                diff1 = set(regular.groups[name]).difference(set(group))
                diff2 = set(group).difference(set(regular.groups[name]))
                report('Groups: Regular "%s" %s difference group %s %s' % (name, sorted(diff1), master.info.styleName, sorted(diff2)))
                # How to fix?
        if changed:
            master.update()

def checkKerning(masters):
    for path, master in masters.items():
        changed = False

        if master.path == regular.path:
            continue

        for pair, kerning in regular.kerning.items():
            if not pair in master.kerning:
                report('Kerning: Regular "%s-->%s" missing in %s' % (pair, kerning, master.info.styleName))
                if FIX:
                    master.kerning[pair] = 0
                    changed = True

        for pair, kerning in master.kerning.items():
            if not pair in regular.kerning:
                report('Kerning: %s "%s-->%s" missing in Regular' % (master.info.styleName, pair, kerning))
                if FIX:
                    regular.kerning[pair] = 0
                    regular.update()
        if changed:
            master.update()
