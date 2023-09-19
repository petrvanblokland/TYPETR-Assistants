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
#    base.py
#

from tnbits.tools.basetool import BaseTool

class Base(BaseTool):
    """
    Base class for proof tool.
    """
    C = BaseTool.C # Inherit the reference to Constants
    TOOLID = 'tnConverter'
    NAME = u'Converter'
    CATEGORY = C.CATEGORY_ANALYZE

    DEFAULTKEY = "com.typenetwork.renderer"

    # We're adding family name to tool identifier before opening so we can have
    # exactly one tool for each family.
    ALLOWMULTIPLE = False
    USEFLOATINGWINDOW = False

    VERSION = 1.0

    VIEWWIDTH = BaseTool.VIEWWIDTH # Take default tool width
    VIEWHEIGHT = 600
    VIEWMINSIZE = (VIEWWIDTH, 400)
    VIEWMAXSIZE = (800, 1000)

    TOOLOBSERVERS = (
        # Callback, eventName
        ('fontDidClose', C.EVENT_FONTDIDCLOSE),
        ('fontDidOpen', C.EVENT_FONTDIDOPEN),
        ('fontWillOpen', C.EVENT_FONTWILLOPEN),
    )

    PREFERENCE_MODEL = dict(
        # Label in RF preferences. Sort key is to define the automatic ordering of groups of parameters.
        useFloatingWindow=dict(label=u'Tool as floating window', sort=200, type=C.PREFTYPE_BOOL, default=USEFLOATINGWINDOW ),
        windowPosSize=dict(label=u'Window size', sort=210, type=C.PREFTYPE_RECT, default=(100, 100, VIEWWIDTH, VIEWHEIGHT)),
        setRFColorOnChange=dict(label=u'Set RoboFont color on interpolation', sort=190, type=C.PREFTYPE_BOOL, default=False),
    )
