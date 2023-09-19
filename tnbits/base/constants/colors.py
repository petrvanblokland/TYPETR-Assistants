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
#    colors.py
#
from AppKit import NSColor

def getRGBA(r, g, b, a=1.0):
    """Converts RGBA color values to AppKit NSColor objects. RGB values should
    be in range 0-255, alpha between 0.0 and 1.0"""
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    assert 0.0 <= a <= 1.0
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    return NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)

# Preset colors.

blackColor = NSColor.blackColor()
opaqueBlackColor = getRGBA(0, 0, 0, 0.5)
blueColor = NSColor.blueColor()
brownColor = NSColor.brownColor()
clearColor = NSColor.clearColor()
cyanColor = NSColor.cyanColor()
darkGrayColor = getRGBA(80, 80, 80)
darkGreyColor = darkGrayColor
grayColor = NSColor.grayColor()
greyColor = grayColor
grayColor = NSColor.grayColor()
greenColor = NSColor.greenColor()
lightGreenColor = getRGBA(75, 211, 154)
darkGreenColor = getRGBA(41, 120, 37)
lightestGrayColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.98, 0.98, 0.98, 1)
lightestGreyColor = lightestGrayColor
lightGrayColor = NSColor.lightGrayColor()
lightGreyColor = lightGrayColor
magentaColor = NSColor.magentaColor()
orangeColor = NSColor.orangeColor()
lightOrangeColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.98, 0.81, 0.32, 1)
purpleColor = NSColor.purpleColor()
opaquePurpleColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 1, 0.3)
redColor = NSColor.redColor()
opaqueRedColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 0.3)
whiteColor = NSColor.whiteColor()
opaqueWhiteColor = getRGBA(255, 255, 255, 0.5)
yellowColor = NSColor.yellowColor()

# Interface presets.

UIGray = getRGBA(31, 38, 46)
UIOpaqueGray = getRGBA(31, 38, 46, 0.5)
UIOpaqueGrey = UIOpaqueGray
UIGrey = UIGray
UILightGray = getRGBA(100, 121, 146)
UILightGrey = UILightGray
UIBlue = getRGBA(13, 48, 54)
UILightBlue = getRGBA(86, 196, 229)
