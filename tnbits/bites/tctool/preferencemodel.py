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
from tnbits.bites.tctool.constants import *

# Parameters that should be in the preferences dictionary, including default values.

p = dict()

d = dict(default=True, label='Show Kerning', type=PREFTYPE_BOOL)
p['_showKerning'] = d

d = dict(default=False, label='_showMetrics', type=PREFTYPE_BOOL)
p['_showMetrics'] = d

d = dict(default=True, label='_showMarkers', type=PREFTYPE_BOOL)
p['_showMarkers'] = d

d = dict(default=True, label='_showFollow', type=PREFTYPE_BOOL)
p['_showFollow'] = d

d = dict(default=True, label='_showRepeat', type=PREFTYPE_BOOL)
p['_showRepeat'] = d

d = dict(default=False, label='_showMargins', type=PREFTYPE_BOOL)
p['_showMargins'] = d

d = dict(default=False, label='_showNumbers', type=PREFTYPE_BOOL)
p['_showNumbers'] = d

d = dict(default=False, label='_showGrid', type=PREFTYPE_BOOL)
p['_showGrid'] = d

d = dict(default=False, label='_showComponents', type=PREFTYPE_BOOL)
p['_showComponents'] = d

d = dict(default=False, label='_showAnchors', type=PREFTYPE_BOOL)
p['_showAnchors'] = d

d = dict(default=False, label='_showMeasures', type=PREFTYPE_BOOL)
p['_showMeasures'] = d

d = dict(default=True, label='_showGroupGlyphs', type=PREFTYPE_BOOL)
p['_showGroupGlyphs'] = d

d = dict(default=True, label='_compareGroupMargins', type=PREFTYPE_BOOL)
p['_compareGroupMargins'] = d

d = dict(default=True, label='_showMarkColors', type=PREFTYPE_BOOL)
p['_showMarkColors'] = d

d = dict(default=False, label='_showMissingGlyphs', type=PREFTYPE_BOOL)
p['_showMissingGlyphs'] = d

d = dict(default=False, label='_showEmptyGlyphs', type=PREFTYPE_BOOL)
p['_showEmptyGlyphs'] = d

d = dict(default=True, label='_doRound', type=PREFTYPE_BOOL)
p['_doRound'] = d

d = dict(default=False, label='_overlayRelated', type=PREFTYPE_BOOL)
p['_overlayRelated'] = d

d = dict(default=EDIT_MODES[SPACING], label='_editMode', type=PREFTYPE_RADIO,
        values=list(EDIT_MODES.values()))
p['_editMode'] = d

d = dict(default=1.2, label='_leading', type=PREFTYPE_FLOAT)
p['_leading'] = d

d = dict(default=PPEM_DEFAULT, label='_ppem', type=PREFTYPE_INT)
p['_ppem'] = d

d = dict(default=0, label='_sample', type=PREFTYPE_INT)
p['_sample'] = d

d = dict(default=0, label='_page', type=PREFTYPE_INT)
p['_page'] = d

d = dict(default=4, label='_stepSize', type=PREFTYPE_INT)
p['_stepSize'] = d

d = dict(default=MAX_GLYPHS, label='_maxGlyphs', type=PREFTYPE_INT)
p['_maxGlyphs'] = d

d = dict(default=TAB_WIDTH, label='_tabWidth', type=PREFTYPE_INT)
p['_tabWidth'] = d

d = dict(default=STROKE_WIDTH, label='_strokeWidth', type=PREFTYPE_FLOAT)
p['_strokeWidth'] = d

d = dict(default=KEY_INTERVAL, label='_keyInterval', type=PREFTYPE_FLOAT)
p['_keyInterval'] = d

d = dict(default=0, label='_colorScheme', type=PREFTYPE_RADIO,
        values=list(COLORSCHEMES.keys()))
p['_colorScheme'] = d


preferenceModel = p
