# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    preferencemodel.py
#

from tnbits.base.c import *
from tnbits.base.samples import *
from tnbits.bites.proof.constants import *

preferenceModel = dict(
    #customFontSize=dict(label='customFontSize', default=''),
    templateID=dict(label='Template ID', type=PREFTYPE_LIST,
        default='PageWide', values=TEMPLATES_ORDER),
    templateName=dict(label='Template Name', default='Page Wide',
        type=PREFTYPE_LIST, values=TEMPLATES_NAMES_ORDER),
    paperSize=dict(label='Paper Size', type=PREFTYPE_LIST, default='A4',
        values=PAPERORDER),
    sampleName=dict(label='Sample', type=PREFTYPE_LIST, default='Basic Latin',
        values=SAMPLENAMES),
    fontSize=dict(label='fontSize', type=PREFTYPE_LIST,
        default=FONTSIZE_DEFAULT, values=FONTSIZES),
    fontSizeProgression=dict(label='fontSizeProgression', type=PREFTYPE_LIST,
        default=FONTSIZE_PROGRESSION_DEFAULT, values=FONTSIZES),
    minFontSize=dict(label='minFontSize', type=PREFTYPE_LIST,
        default=FONTSIZE_PROGRESSION_DEFAULT, values=FONTSIZES),
    leading=dict(label='leading', type=PREFTYPE_LIST, default=LEADING_DEFAULT,
        values=LEADINGS),
    align=dict(label='Align', type=PREFTYPE_RADIO, default=0, values=ALIGNMENT_VALUES),
    paperPortrait=dict(label='Portrait', default=False, type=PREFTYPE_BOOL),
    showGlyphSpace=dict(label='showGlyphSpace', default=False,
        type=PREFTYPE_BOOL),
    showKernValues=dict(label='showKernValues', default=False,
        type=PREFTYPE_BOOL),
    withKerning=dict(label='withKerning', default=False, type=PREFTYPE_BOOL),
    withAutoFit=dict(label='withAutoFit', default=False, type=PREFTYPE_BOOL),
    showMarginValues=dict(label='showMarginValues', default=False,
        type=PREFTYPE_BOOL),
    showNames=dict(label='showNames', default=False, type=PREFTYPE_BOOL),
    showMissing=dict(label='showMissing', default=False, type=PREFTYPE_BOOL),
    doNewlines=dict(label='doNewlines', default=False, type=PREFTYPE_BOOL),
    compileText=dict(label='compileText', default=False, type=PREFTYPE_BOOL),
    doOnePage=dict(label='doOnePage', default=False, type=PREFTYPE_BOOL),
    repeatLastGlyph=dict(label='repeatLastGlyph', default=False,
        type=PREFTYPE_BOOL),
    openProof=dict(label='openProof', default=False, type=PREFTYPE_BOOL),
    sortGlyphs=dict(label='sortGlyphs', default=False, type=PREFTYPE_BOOL),
    showDrawWindow=dict(label='showDrawWindow', default=True,
        type=PREFTYPE_BOOL),
    pageAlign=dict(label='pageAlign', default=0,
        type=PREFTYPE_INT),
    sampleTextPath=dict(label='sampleTextPath', default='',
        type=PREFTYPE_LABEL),
)

