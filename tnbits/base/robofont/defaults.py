# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    defaults.py
#
#   Mirrors default functions so we can use them outside RoboFont, i.e. in a
#   standalone application.

from AppKit import NSBundle, NSColor, NSUserDefaults

_bundle = NSBundle.mainBundle()
appName = _bundle.infoDictionary().get("CFBundleDisplayName", "RoboFont")
internalAppName = appName.lower()
doodleLibIdentifier = u"com.typemytype.%s" % internalAppName

def getDefault(key, defaultValue=None, defaultClass=None):
    defaultsFromFile = NSUserDefaults.standardUserDefaults()
    value = defaultsFromFile.get(key, defaultValue)

    if defaultClass is not None:
        return defaultClass(value)

    return value

def getDefaultColor(key, alpha=True, defaultValue=None):
    color = getDefault(key, defaultValue)

    if isinstance(color, NSColor):
        return color

    if color is None:
        return None

    r, g, b, a = color

    if not alpha:
        a = 1

    return NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
