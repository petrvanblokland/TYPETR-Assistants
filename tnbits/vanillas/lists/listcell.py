# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     listcell.py
#

import objc
from AppKit import NSButtonCell, NSColor, NSMakeRect, NSInsetRect, NSBezierPath, NSRoundedBezelStyle
from vanilla import CheckBoxListCell

class TnBitsListCell(NSButtonCell):
    """
    Overriding button cell for list.
    """

    def mouseDown_(self, event):
        print('cell', event)

    '''
    def drawWithFrame_inView_(self, frame, view):
        """
        """
        (x, y), (w, h) = frame
        w *= .5
        h *= .5
        cx = x + w
        cy = y + h
        s = w

        if h < w:
            s = h

        frame = NSMakeRect(cx - s, cy - s, s * 2, s * 2)
        r = NSInsetRect(frame, 3, 3)
        path = NSBezierPath.bezierPathWithOvalInRect_(r)
        NSColor.colorWithCalibratedWhite_alpha_(1, .3).set()

        if self.isHighlighted():
            NSColor.colorWithCalibratedWhite_alpha_(0, .3).set()

        path.fill()
        NSColor.blackColor().set()

        if self.isHighlighted():
            NSColor.whiteColor().set()

        path.stroke()

        if self.objectValue() or self.isHighlighted():
            r = NSInsetRect(frame, 6, 6)
            NSBezierPath.bezierPathWithOvalInRect_(r).fill()
    '''

@objc.IBAction
def buttonClick_(self):
    print('button click')

def getListCell():
    """
    """
    cell = CheckBoxListCell.alloc().init()
    #cell.setButtonType_(NSRoundedBezelStyle)
    print(cell, type(cell))
    #s = objc.selector(buttonClick_, signature='v@:')
    #cell.setAction_(s)
    print(cell, cell.target, cell.action)
    #cell.setTarget_(self)
    return cell
