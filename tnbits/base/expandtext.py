# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    expandtext.py
#

# Static functions to expand glyph sets based on glyphs present in the style.

from tnbits.base.groups import *
from tnbits.base.samples import (RE_GLYPHNAMES, ALL_GLYPHS_TAG,
        ALL_BASE_GLYPHS_TAG, CAPS_ON_ALL_BASE_GLYPHS_TAG,
        LC_ON_ALL_BASE_GLYPHS_TAG, SMALL_CAPS_TAG, SORTED_KERNING_TAG,
        FIGURE_SETS, TN_FIGURES, TN_PRIMARY, SUPS_SINF,
        SUPS_SINF_NUMR_DNOM_SETS,)
from tnbits.base.constants.samples import (TN_UC, TN_LC, SS_CURRENCY,
        SS_FIGURESMATH, SS_FIGURES_MC)

REPLACEMENTS = {'ldot': 'ldot/l', 'Ldot': 'Ldot/L'}
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWERS = 'abcdefghijklmnopqrstuvwxyz'

def expandText(style, t, xgroups):
    """Splits up text in separate pages based on maxGlyphs."""

    # Expand wild cards, such as ALL_GLYPHS.
    # Additions: also add to check in function setSample()
    if t == ALL_GLYPHS_TAG:
        t = expandAll(style, t)
    elif t == ALL_BASE_GLYPHS_TAG:
        t = expandAllBase(style, t)
    elif t == CAPS_ON_ALL_BASE_GLYPHS_TAG:
        t = expandAllCapsXLC(style, t)
    elif t == LC_ON_ALL_BASE_GLYPHS_TAG:
        t = expandLowerCaseXBase(style, t)
    elif t == SMALL_CAPS_TAG:
        t = expandSmallCaps(style, t)
    elif t == SUPS_SINF_NUMR_DNOM_SETS:
        t = expandSupsSinfNumrDnomSets(style, t)
    elif t == FIGURE_SETS:
        t = expandFigureSets(style, t)
    elif t == SORTED_KERNING_TAG:
        t = expandSortedKerning(style, t, xgroups)

    return t

def expandAll(style, t):
    """Dynamically expands with the sorted glyph set of the current
    style."""
    glyphNames = _getAllGlyphNames(style)
    return t.replace(ALL_GLYPHS_TAG, '/' + '/'.join(glyphNames))

def expandAllBase(style, t):
    """Dynamically expands with all sorted glyphs that don't have an extension.
    The extension should be address by feature selection and by groups."""
    glyphNames = _getAllBaseGlyphNames(style)
    return t.replace(ALL_BASE_GLYPHS_TAG, '/' + '/'.join(glyphNames))

def expandAllCapsXLC(style, t):
    """Dynamically expand with all sorted glyphs that don't have an extension.
    The extension should be addressed by feature selection and by groups."""
    glyphNames = _getCapsXAllBaseGlyphNames(style)
    return t.replace(CAPS_ON_ALL_BASE_GLYPHS_TAG, '/' + '/'.join(glyphNames))


def expandLowerCaseXBase(style, t):
    """Dynamically expands with all sorted glyphs that don't have an extension.
    The extension should be addressed by feature selection and by groups."""
    glyphNames = _getLowercaseXAllBaseGlyphNames(style)
    return t.replace(LC_ON_ALL_BASE_GLYPHS_TAG, '/' + '/'.join(glyphNames))

def expandSmallCaps(style, t):
    """Dynamically expands with the sorted list of smallcaps in the current
    style."""
    smallCaps = _getSmallCapsGlyphNames(style)
    return t.replace(SMALL_CAPS_TAG, '/' + '/'.join(smallCaps))

def expandSupsSinfNumrDnomSets(style, t):
    """Dynamically expand superiors and inferiors into kerning permutation."""
    # FIXME: does this work?
    glyphSetString = []
    for ext in ('sinf', 'sups', 'numr', 'dnom'):
        for glyphName1 in SUPS_SINF:
            glyphNameExt1 = glyphName1 + '.' + ext
            if glyphNameExt1 in style:
                for glyphName2 in SUPS_SINF:
                    glyphNameExt2 = glyphName2 + '.' + ext
                    if glyphNameExt2 in style:
                        glyphSetString.append('/'+glyphNameExt1)
                        glyphSetString.append('/'+glyphNameExt2)

    return t.replace(SUPS_SINF_NUMR_DNOM_SETS, ''.join(glyphSetString))

def expandFigureSets(style, t):
    figureSetString = []
    figureSets = {} # Key is type of extension
    # Find extensions that have a figure glyph, then combine with other glyphs for kerning

    for glyphName1 in _getAllGlyphNames(style):
        nameParts = glyphName1.split('.')
        figureName = nameParts[0]
        if not figureName in TN_FIGURES:
            continue

        if len(nameParts) > 1:
            extension = '.'.join(nameParts[1:])
            if 'tab' in extension: 
                continue
        else:
            extension = None
        if not extension in figureSets:
            figureSets[extension] = []

    for extension in figureSets.keys():
        for glyphName in TN_UC + TN_LC + SS_CURRENCY + SS_FIGURESMATH + SS_FIGURES_MC:
            for figureName in TN_FIGURES:
                if extension is not None:
                    figureName += '.' + extension
                if glyphName in style:
                    figureSetString.append('/%s/%s/%s' % (figureName, glyphName, figureName))
                if extension is not None:
                    glyphName += '.' + extension
                    if glyphName in style:
                        figureSetString.append('/%s/%s/%s' % (figureName, glyphName, figureName))
    
    return t.replace(FIGURE_SETS, ''.join(figureSetString))

def expandSortedKerning(style, t, xgroups):
    # TODO: move to tx.
    kerningSample = []
    k = {}
    kerning = style.kerning

    for nameL, nameR in kerning.keys():
        # Test if there are still group names in the kerning. Then get the
        # value from the We expanded, so we can skip them.
        kerning = getGroupKerning(style, nameL, nameR, xgroups)

        if not kerning:
            continue

        if not kerning in k:
            k[kerning] = []

        if nameL in style: 
            # Direct glyph name.
            namesL = [nameL]
        elif nameL in style.groups:
            namesL = style.groups[nameL]
        else:
            namesL = []

        if nameR in style: 
            # Direct glyph name.
            namesR = [nameR]
        elif nameR in style.groups:
            namesR = style.groups[nameR]
        else:
            namesR = []

        for n1 in namesL:
            for n2 in namesR:
                k[kerning].append('/space/%s/%s' % (n1, n2))

    # Negative values first.
    for _, pairs in sorted(k.items()): 
        kerningSample += sorted(pairs)

    return t.replace(SORTED_KERNING_TAG, ''.join(kerningSample))

def _getAllGlyphNames(style):
    """Answers the sorted list with glyph names of the selected style.
    Anwers the RoboFont sort order if it is available and the sorted
    style.keys() otherwise."""
    glyphNames = []

    if style is not None:
        glyphNames = style.lib.get("public.glyphOrder", [])

        if not glyphNames:
            glyphNames = sorted(style.keys())

    return glyphNames

def _getAllBaseGlyphNames(style):
    """Answers the sorted list with glyph names of the selected style that
    don't have an extension. Anwers the RoboFont sort order if it is
    available and the sorted style.keys() otherwise."""
    replacements = REPLACEMENTS
    baseGlyphNames = []

    for glyphName in _getAllGlyphNames(style):
        if not '.' in glyphName and not glyphName.endswith('cmb'):
            glyphName = replacements.get(glyphName, glyphName)
            baseGlyphNames.append(glyphName)

    return baseGlyphNames

def _getCapsXAllBaseGlyphNames(style):
    """Answers the sorted list with glyph names of the selected style that
    don't have an extension. Anwers the RoboFont sort order if it is available
    and the sorted style.keys() otherwise."""
    replacements = REPLACEMENTS
    capXBaseGlyphNames = []

    for capName in CAPS:
        for glyphName in _getAllGlyphNames(style):
            if not '.' in glyphName and not '_tab' in glyphName and \
                    not glyphName.endswith('cmb'):
                glyphName = replacements.get(glyphName, glyphName)
                capXBaseGlyphNames.append(capName + '/' + glyphName)

    return capXBaseGlyphNames

def _getLowercaseXAllBaseGlyphNames(style):
    """Answers the sorted list with glyph names of the selected style that
    don't have an extension. Anwers the RF sort order if it is available and
    the sorted style.keys() otherwise."""
    lcXBaseGlyphNames = []

    for capName in LOWERS:
        for glyphName in _getAllGlyphNames(style):
            if not '.' in glyphName and not '_tab' in glyphName and \
                    not glyphName.endswith('cmb'):
                lcXBaseGlyphNames.append(capName + '/' + glyphName)

    return lcXBaseGlyphNames

def _getSmallCapsGlyphNames(style):
    smallCaps = []

    for glyphName in _getAllGlyphNames(style):
        if '.sc' in glyphName:
            smallCaps.append(glyphName)

    return smallCaps
