# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    contours.py
#

# Contants attribute values
POINTTYPE_NONECURVE = None
POINTTYPE_OFFCURVE = 'offCurve'
POINTTYPE_OFFCURVES = (POINTTYPE_NONECURVE, POINTTYPE_OFFCURVE)        # Values of point types as they come from RoboFont
POINTTYPE_QUADRATIC = u'qcurve'
POINTTYPE_BEZIER = u'curve'
POINTTYPE_MOVE = u'move'
POINTTYPE_LINE = u'line'
POINTTYPE_SPACE = u'space'
POINTTYPE_CURVES = (POINTTYPE_QUADRATIC, POINTTYPE_BEZIER)
POINTTYPES = (POINTTYPE_NONECURVE, POINTTYPE_OFFCURVE, POINTTYPE_QUADRATIC,
    POINTTYPE_BEZIER, POINTTYPE_LINE, POINTTYPE_MOVE,
    POINTTYPE_SPACE)

# C O N T O U R

C_CW = PATHDIRECTION_CLOCK = 'CW' # Contour clockwise direction
C_CCW = PATHDIRECTION_COUNTERCLOCK = 'CCW' # Contour counter-clockwise direction

#   A N C H O R

ANCHORTOP = 'top'
ANCHOR_TOP = '_' + ANCHORTOP
ANCHORCENTER = 'center'
ANCHOR_CENTER = '_' + ANCHORCENTER
ANCHORBOTTOM = 'bottom'
ANCHOR_BOTTOM = '_' + ANCHORBOTTOM
# Standardized anchor positions that the analyzer knows what to do with.
ANCHORNAMES = (ANCHORTOP, ANCHORCENTER, ANCHORBOTTOM)
