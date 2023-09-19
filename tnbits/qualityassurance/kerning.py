# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     kerning.py
#

import unicodedata
import traceback
from tnbits.toolbox.font import FontTX
from tnbits.model.toolbox.kerning.buildgroups import explodeKerning
from tnbits.qualityassurance.qamessage import addHeader
from tnbits.errors.floqerror import FloqError
import collections
from tnbits.base.future import chr

def showFlattenedGroups(stylesDict, **kwargs):
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        pairs0, usedGroups, groupsNotUsed, exceptions = explodeKerning(style.kerning, style.groups)
        pairs1 = FontTX.kerning.getFlattenedPairs(style.kerning, style.groups)

        # Enable to show in reporter, slow for larger group sets.
        #for key, value in pairs1.items():
        #    m.append('%s: %s' % (key, value))
        k0 = pairs0.keys()
        k1 = pairs1.keys()

        intersection = list(set(k0).intersection(k1))
        diff0 = list(set(k0).difference(intersection))
        diff1 = list(set(k1).difference(intersection))
        m.append('pairs0: %s' % len(pairs0))
        m.append('diff0: %s' % diff0)
        m.append('pairs1: %s' % len(pairs1))
        m.append('diff1: %s' % diff1)

        # Compare values.
        for key in intersection:
            if pairs0[key] != pairs1[key]:
                m.append('Values for  %s do not match: %d != %d' % (key, pairs0[key], pairs1[key]))

        addHeader("Show Flattened Groups", styleId, m, messages)

    return messages

def flattenWithExceptions(stylesDict, **kwargs):
    fix = False
    messages = []
    flatKernings = {}

    for styleId, style in stylesDict.items():
        m = []

        for pair, value in style.kerning.items():
            left, right = pair
            new = False

            # Right is a group, find left group for left.
            if right in style.groups.keys():
                for group, glyphs in style.groups.items():
                    if len(group) > 5 and group[5] == 'L':
                        if left in glyphs:
                            msg = "Glyph to group exception for pair: %s, value: %d" % (pair, value)
                            m.append(msg)
                            new = True

                            if fix is True:
                                del style.kerning[pair]

                            for char in style.groups[right]:
                                    newpair = (left, char)
                                    msg = 'New pair: %s, value: %d' % (newpair, value)
                                    m.append(msg)
                                    flatKernings[newpair] = value

                                    if fix is True:
                                        del style.kerning[pair]
                                        style.kerning[newpair] = value

            # Left is a group.
            if left in style.groups.keys():
                for group, glyphs in style.groups.items():
                    if len(group) > 5 and group[5] == 'R':
                        if right in glyphs:
                            msg = 'group to glyph exception for pair: %s, value: %d' % (pair, value)
                            m.append(msg)
                            new = True

                            if fix is True:
                                del style.kerning[pair]

                            for char in style.groups[left]:
                                    newpair = (char, right)
                                    style.kerning[newpair] = value
                                    msg = 'New pair: %s, value: %d' % (newpair, value)
                                    m.append(msg)

                                    if fix is True:
                                        style.kerning[newpair] = value

            # Add pairs with no groups.
            if new is False:
                flatKernings[pair] = value

        m.append('Number of flat kernings: %d' % len(flatKernings))
        addHeader("Flatten With Exceptions", styleId, m, messages)

    return messages

def countTotalKerns(stylesDict, **kwargs):
    """Counts UFO classes, estimated exploded pairs, fontlab classes. Checks if
    OpenType feature exists."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        flKerningClasses = []
        ufoKerningClasses = []
        fOtKernExists = False
        kernDict = style.kerning.items()
        m.append('Kerning pairs: %d' % len(kernDict))

        for groupName, groupGlyphs in style.groups.items():
            if groupName[0] == '_':
                flKerningClasses.append(groupName)

            if FontTX.groups.isKernGroup(groupName):
                ufoKerningClasses.append(groupName)

        try:
            if 'feature kern' in style.features.text:
                fOtKernExists = True
        except Exception as e:
            print('Cannot find features:', style.features)

        m.append('UFO kerning classes: %d' % len(ufoKerningClasses))

        pairs = None
        # FIXME: doubles the amount, should length kerning be added?
        #estimatedKerningPairs = len(kernDict) + len(getExpandedKerning(style))
        try:
            pairs, _, _, _ = explodeKerning(style.kerning, style.groups)
        except FloqError as e:
            m.append(('Problem running explodeKerning() on %s: %s' % (styleId, e), 'error'))
            print(traceback.format_exc())

        if pairs:
            m.append('Estimated exploded kerning pairs: %d' % len(pairs))

        m.append('FL kerning classes: %d' % len(flKerningClasses))
        m.append('OpenType {kern} feature: %s' % fOtKernExists)
        addHeader("Count Total Kerns", styleId, m, messages)

    return messages

def questionablePairs(stylesDict, attrs=None, fix=False, **kwargs):
    """
    ...
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        troublesomes = []
        alphabetics = []

        for t in attrs:
            troublesomes.append(t)

        for glyphName in style.keys():
            g = style[glyphName]

            if g.unicodes:
                u = g.unicodes[0]
                if unicodedata.category(chr(u)) in ['Ll', 'Lu'] and g.name not in ['florin']:
                    alphabetics.append(g.name)

        # loop through all kerning groups and find those involving alphabetics.
        for groupName, groupGlyphs in FontTX.groups.getKernGroups(style.groups).items():
            isAlphabetic = False
            isTroublesome = True

            for groupGlyph in groupGlyphs:
                if groupGlyph in alphabetics:
                    isAlphabetic = True

                if groupGlyph not in troublesomes:
                    isTroublesome = False

            if isAlphabetic:
                alphabetics.append(groupName)

            if isTroublesome:
                troublesomes.append(groupName)

        pairsToCheck = []

        # Loop through all pairs and find one in troublesomes and the other in
        # alphabetics.
        for p, v in style.kerning.items():
            l, r = p
            if (l in troublesomes and r in alphabetics) or (r in troublesomes and l in alphabetics):
                pairsToCheck.append(p)

        for l, r in pairsToCheck:
            glyphl = l

            if FontTX.groups.isGroup(l):
                glyphl = style.groups[l][0]

            glyphr = r

            if FontTX.groups.isGroup(r):
                glyphr = style.groups[r][0]

            msg = '/%s/%s' % (glyphl, glyphr)
            m.append((msg, 'error'))

        if fix:
            for pair in pairsToCheck:
                style.kerning.remove(pair)

        if len(m) == 0:
            m.append('Didn\'t find any questionable pairs.')

        addHeader("Questionable Pairs", styleId, m, messages)

    return messages

def glyphsWithNoKerns(stylesDict, **kwargs):
    """Gives an idea of how many glyphs are not associated with a kerning pair.
    This explodes the kerning, so groups are not a factor. Right kerns and left
    kerns are counted together.

    TODO: compare getFlattenedPairs() to explodeKerning().

    fk, _, _, _ = explodeKerning(style.kerning, style.groups)
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        fk = FontTX.kerning.getFlattenedPairs(style.kerning, style.groups)
        kernTracker = {}
        kernValueTracker = {}

        for glyphName in sorted(style.keys()):
            kernTracker[glyphName] = 0
            kernValueTracker[glyphName] = 0

        for pair, value in fk.items():
            l, r = pair

            if l in kernTracker:
                kernTracker[l] += 1
                kernValueTracker[l] += abs(value)

            if r in kernTracker:
                kernTracker[r] += 1
                kernValueTracker[r] += abs(value)

        for glyphName in sorted(style.keys()):
            if kernTracker[glyphName] == 0:
                m.append(glyphName)

        addHeader("No Kerns", styleId, m, messages)

    return messages

'''
NOTE: EXAMPLE CODE, check if these situations are handled.
# Valid only if glyph /V and glyph /A exist in f
f.kerning[('V', 'A')]

# Valid only if glyph /A exists in f and group /@Agroup exists in f.groups
f.kerning['V', '@Agroup']
f.kerning['@Agroup', 'V']

# Valid only if group is used in f.kerning or in a GSUB.
f.groups['@Agroup']

# Only valid if /Agrave, etc. exist in f
f.groups['@Agroup']  #containing ['A', 'Agrave', 'Aacute', ...]
'''

def missingGlyphsInGroups(stylesDict, **kwargs):
    """Checks if a glyph name mentioned in a group actually exists in the
    font."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        # Actual groups.

        for groupName, group in style.groups.items():
            for name in group:
                if name not in style.keys():
                    msg = 'Glyph %s mentioned in group %s does not exist in font.' % (name, groupName)
                    m.append((msg, 'error'))

        # Glyphs mentioned in kerning pairs.

        for pair in style.kerning.keys():
            name1, name2 = pair

            for name in pair:
                if not FontTX.groups.isKernGroup(name) and not name in style:
                    p = '(%s, %s), %s not in style.' % (pair[0], pair[1], name)
                    m.append((p, 'error'))

        addHeader("Missing Glyphs in Groups", styleId, m, messages)

    return messages

def sameGlyphInMultipleGroups(stylesDict, **kwargs):
    """Checks if a glyph name occurs in several groups, which is undesirable
    because it can cause unpredictable results."""
    messages = []
    left = {}
    right = {}

    for styleId, style in stylesDict.items():
        m = []

        for group in style.groups.keys():
            if FontTX.groups.isKernGroup(group):
                l = FontTX.groups.isLeftKernGroup(group)
                r = FontTX.groups.isRightKernGroup(group)

                for glyph in style.groups[group]:
                    if l:
                        if not glyph in left:
                            left[glyph] = []
                        left[glyph].append(group)
                    elif r:
                        if not glyph in right:
                            right[glyph] = []
                        right[glyph].append(group)

        for glyph, groups in left.items():
            if len(groups) > 1:
                msg = '%s in multiple groups: %s' % (glyph, ', '.join(groups))
                m.append((msg, 'error'))

        for glyph, groups in right.items():
            if len(groups) > 1:
                msg = '%s in multiple groups: %s' % (glyph, ', '.join(groups))
                m.append((msg, 'error'))

        addHeader("Same Glyph in Multiple Groups", styleId, m, messages)

    return messages

def missingGroups(stylesDict, **kwargs):
    """Checks if a group name used in kerning exists."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for pair in style.kerning.keys():
            for name in pair:
                if FontTX.groups.isKernGroup(name) and name not in style.groups:
                    msg = '%s in kerning pair %s does not exist as a group' % (name, pair)
                    m.append((msg, 'error'))

        addHeader("Missing Kern Group", styleId, m, messages)

    return messages

def duplicateGlyphsInGroups(stylesDict, **kwargs):
    """Finds duplicate glyph names in groups."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for groupName, group in style.groups.items():
            duplicates = [item for item, count in collections.Counter(group).items() if count > 1]

            if len(duplicates) > 0:
                msg = 'Found duplicate items %s in group %s' % (', '.join(duplicates), groupName)
                m.append((msg, 'error'))

        addHeader("Duplicate Glyphs in Groups", styleId, m, messages)

    return messages

def glyphInGroupAndSeparate(stylesDict, **kwargs):
    """
    In a kerning pair, what about right to left direction?
    What about recursive groups?
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        reverse = {}

        for pair in style.kerning.keys():
            l, r = pair

            if r not in reverse:
                reverse[r] = []

            reverse[r].append(l)

        for key, values in reverse.items():
            if len(values) > 1:
                for value in values:
                    if FontTX.groups.isKernGroup(value):
                        if value in style.groups:
                            group = style.groups[value]

                            for g in group:
                                if g in values:
                                    msg = 'Both in group %s and separate: %s, kerning to %s' % (value, g, key)
                                    m.append((msg, 'error'))

        addHeader("Glyph in Group and Separate", styleId, m, messages)

    return messages

def emptyGroups(stylesDict, **kwargs):
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for groupName, group in style.groups.items():
            if len(group) == 0:
                msg = 'Empty group %s' % groupName
                m.append((msg, 'warning'))

        addHeader("Empty Groups", styleId, m, messages)

    return messages

def zeroValueKerning(stylesDict, **kwargs):
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for pair, value in style.kerning.items():
            if value == 0:
                msg = 'Zero-value kerning pair (%s, %s)' % (pair[0], pair[1])
                m.append((msg, 'warning'))

        addHeader("Zero Value Kerning", styleId, m, messages)

    return messages

def spacingDiff(referenceKeys, referenceStyle, style):
    """
    Width & bearings difference.
    """
    messages = []
    m = []

    for glyphName in referenceKeys:
        if not glyphName in referenceStyle or not glyphName in style:
            continue

        mm = []
        msg = glyphName
        m.append(msg)
        w1 = referenceStyle[glyphName].width
        w2 = style[glyphName].width
        lsb1 = referenceStyle[glyphName].leftMargin
        lsb2 = style[glyphName].leftMargin
        rsb1 = referenceStyle[glyphName].rightMargin
        rsb2 = style[glyphName].rightMargin

        if w1 != w2:
            msg = 'setwidth difference: %s, %s' % (w1, w2)
            mm.append(msg)

        if lsb1 != lsb2:
            msg = 'LSB difference: %s, %s' % (lsb1, lsb2)
            mm.append(msg)

        if rsb1 != rsb2:
            msg = 'RSB difference: %s, %s' % (rsb1, rsb2)
            mm.append(msg)

        if len(mm) > 0:
            m.append(mm)

    messages.append('SPACING DIFF:')
    messages.append(m)
    return messages

def glyphDiff(referenceName, referenceStyle, referenceSet, styleId, style):
    """
    """
    messages = []
    m = []
    styleKeys = style.keys()
    glyphSet = set(styleKeys)
    messages.append('GLYPH DIFF:')
    #m.append('In "%s", but not "%s":' %(referenceName, styleId))
    diff = sorted(list(referenceSet - glyphSet))
    messages.append(diff)
    #messages.append('t%s' % ', '.join(diff))
    return messages

def unicodeDiff(referenceUnicodeSet, styleUnicodeSet):
    messages = []
    messages.append('UNICODE DIFF:')
    diff1 = list(referenceUnicodeSet - styleUnicodeSet)
    diff2 = list(styleUnicodeSet - referenceUnicodeSet)

    if len(diff1) == 0:
        messages.append('No Unicode difference')
    else:
        msg = 'In "%s", but not "%s":' %(referenceName, styleId)
        unicodeListMessage(sorted(diff1))

    if len(diff2) == 0:
        messages.append('No Unicode difference')
    else:
        msg = 'In "%s", but not "%s":' %(styleId, referenceName)
        unicodeListMessage(sorted(diff2))

    return messages

def diff(referenceKernings, styleId, styleKernings):
    kernThreshold = 6
    messages = []
    messages.append('KERNING DIFF:')

    for referencePair, value in sorted(referenceKernings.items()):
        m = []
        stylePair = styleKernings.get(referencePair)

        if stylePair is None:
            msg = '[%s, %s] missing.' % (referencePair[0], referencePair[1])
            m.append((msg, 'error'))
        elif abs(stylePair - value) > kernThreshold:
            msg = 'Pair (%s, %s) has a different value: %s, %s' % (referencePair[0], referencePair[1], value, stylePair)
            m.append((msg, 'error'))
        messages.append(m)

    return messages

def duplexing(referenceName, stylesDict):
    """Compiles sets and compares various differences: spacing, glyph sets,
    unicode, kerning.

    NOTE: This is a lesser used attribute, applied in situations where type has
    variable inking, for example in newspapers.

    TODO: move to correct category class.
    """
    if len(stylesDict) == 1:
        []

    messages = []
    referenceStyle = stylesDict[referenceName]
    referenceKeys = sorted(referenceStyle.keys())
    referenceSet = set(referenceKeys)
    referenceUnicodeSet = set(referenceStyle.unicodeData.keys())
    referenceKernings = FontTX.kerning.getFlattenedPairs(referenceStyle.kerning,
            referenceStyle.groups)

    for styleId, style in stylesDict.items():

        # Skip the reference style.
        if styleId == referenceName:
            continue

        styleUnicodeSet = set(referenceStyle.unicodeData.keys())
        styleKernings = FontTX.kerning.getFlattenedPairs(style.kerning,
            style.groups)

        m = spacingDiff(referenceKeys, referenceStyle, style)
        messages.extend(m)
        m = glyphDiff(referenceName, referenceStyle, referenceSet, styleId, style)
        messages.extend(m)
        m = unicodeDiff(referenceUnicodeSet, styleUnicodeSet)
        messages.extend(m)
        m = diff(referenceKernings, styleId, styleKernings)
        messages.extend(m)

    msg = 'Against %s (%d glyphs)' % (styleId, len(style))
    return [msg, messages]
