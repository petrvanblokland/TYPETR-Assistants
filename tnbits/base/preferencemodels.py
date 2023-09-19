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
#    preferencemodels.py
#
from tnbits.base.c import *
from tnbits.bites.proof.preferencemodel import preferenceModel as proofModel
from tnbits.bites.qatool.preferencemodel import preferenceModel as qaModel
from tnbits.bites.tctool.preferencemodel import preferenceModel as tcModel

"""Default model of the central set of preference values model for a tool. The
preferences values dictionary is stored in RoboFont's preferences, under the
tool ID. If it does'nt exist, it will be initialized using the default model
dictionary. The one below offers default behavior. Tools can define their own
preference model dictionary."""

DEFAULT_MODEL = dict(windowPosSize=dict(label=u'Window size',
            sort=110, type=PREFTYPE_RECT, default=(0, 0, 0, 0), allowMultiple=False),
    )

MODELS = {}

'''
Dimensioneer doesn't have a window on it's own. Use the DisplayItems tools to
set the preferences. Label in RF preferences. Sort key is to define the
automatic ordering of groups of parameters.
'''

dimensioneerModel = dict(
    drawOn=dict(label=u'Draw on', sort=0, type=PREFTYPE_BOOL, default=True),
    drawInactiveWindows=dict(label=u'Draw inactive windows', sort=5,
        type=PREFTYPE_BOOL, default=True),
    drawSelectedPoints=dict(label=u'Draw selected points', sort=8,
        type=PREFTYPE_BOOL, default=True),
    drawXDimensions=dict(label=u'Draw X dimensions', sort=10,
        type=PREFTYPE_BOOL, default=True),
    drawYDimensions=dict(label=u'Draw Y dimensions', sort=20,
        type=PREFTYPE_BOOL, default=True),
    drawOvershoots=dict(label=u'Draw Y overhoots', sort=25,
        type=PREFTYPE_BOOL, default=True),
    drawComponentTransform=dict(label=u'Draw component transform', sort=30,
        type=PREFTYPE_BOOL, default=True), # Use stem color for the lines
    drawDiagonals=dict(label=u'Draw diagonal dimensions', sort=36,
        type=PREFTYPE_BOOL, default=True),
    diagonalColor=dict(label=u'Diagonal color', sort=40,
        type=PREFTYPE_COLOR, default=(.4, .4, .8, .8)),
    drawComponentDimensions=dict(label=u'Draw component dimensions',
        sort=50, type=PREFTYPE_BOOL, default=True),
    gridColor=dict(label=u'Grid color', sort=70, type=PREFTYPE_COLOR,
        default=(.2, .2, .2, .8)),
    stemColor=dict(label=u'Stem color', sort=72, type=PREFTYPE_COLOR,
        default=(.2, .2, .2, .8)),
    maxStems=dict(label=u'Max showing stems', sort=80, type=PREFTYPE_INT,
        default=40),
    maxBars=dict(label=u'Max showing bars', sort=80, type=PREFTYPE_INT,
        default=20),
    metricsColor=dict(label=u'Metrics color', sort=90,
        type=PREFTYPE_COLOR, default=(.2, .2, .8, .8)),
    counterColor=dict(label=u'Counter color', sort=100,
        type=PREFTYPE_COLOR, default=(.8, .2, .2, .8)),
    endWidth=dict(label=u'Line end width', sort=200, type=PREFTYPE_INT,
        default=3), # Marker size on dimension line endings.
    strokeWidthValue=dict(label=u'Line thickness', sort=210,
        type=PREFTYPE_INT, default=0.5), # Line thickness
    textSize=dict(label=u'Text size', sort=230, type=PREFTYPE_INT,
        default=9), # Text size of value labels,
)

MODELS['Dimensioneer'] = dimensioneerModel
MODELS['Proof'] = proofModel
MODELS['QualityAssurance'] = qaModel
MODELS['TextCenter'] = tcModel

def getModel(appName, defaultPos=None):
    if appName in MODELS:
        return MODELS[appName]
    else:
        return DEFAULT_MODEL


def getSortedPreferences(model):
    """Answers the list name+preference, sorted by the preference['sort']
    value. Allow duplicate sort values. If the sort key is missing in the
    preference, they set it to default 0."""
    preferences = model.items()

    def getSortKey(pair):
        k, v = pair
        return (v.get("sort", 0), k)

    list(preferences).sort(key=getSortKey)
    return preferences
