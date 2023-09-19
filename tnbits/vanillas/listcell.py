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
from vanilla import VanillaBaseObject, List
from AppKit import NSView, NSBezierPath, NSTextFieldCell, NSSmallControlSize,\
    NSFont, NSLeftTextAlignment, NSButtonCell, NSRadioButton,\
    NSRightTextAlignment, NSCenterTextAlignment, NSRegularControlSize,\
    NSInsetRect, NSColor, NSAffineTransform, NSLineBreakByTruncatingMiddle
from tnbits.vanillas.iconview import IconNSView

def hideColumn(name, listView, hide=True):
    """Bit of code to hide the column, because this is not in Vanilla. Name
    is the identifier of the column in the list."""
    tableView = listView.getNSTableView()
    index = tableView.columnWithIdentifier_(name)
    column = tableView.tableColumns()[index]
    column.setHidden_(hide)

def SmallTextListCell(editable=False, size=None):
    # Height needs to be set by the parent list, not the cell.
    cell = NSTextFieldCell.alloc().init()

    if size is None:
        size = NSSmallControlSize # NSMiniControlSize
        font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
        cell.setControlSize_(size)
        #cell.setControlSize_(size)
    else:
        font = NSFont.systemFontOfSize_(size)

    cell.setFont_(font)
    cell.setEditable_(editable)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def SmallLeftAlignTextListCell(editable=False, size=None):
    """Alternate options: NSLeftTextAlignment,
    NSRightTextAlignment,NSCenterTextAlignment, NSJustifiedTextAlignment, or
    NSNaturalTextAlignment."""
    cell = SmallTextListCell(editable=editable, size=size)
    cell.setAlignment_(NSLeftTextAlignment)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def LeftAlignTextListCell(editable=False, size=None):
    cell = SmallTextListCell(editable=editable, size=size)
    size = NSRegularControlSize
    cell.setControlSize_(size)
    font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    cell.setFont_(font)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def RightAlignTextListCell(editable=False, size=None):
    cell = SmallTextListCell(editable=editable, size=size)
    size = NSRegularControlSize
    cell.setControlSize_(size)
    cell.setAlignment_(NSRightTextAlignment)
    font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    cell.setFont_(font)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def SmallRightAlignTextListCell(editable=False, size=None):
    cell = SmallTextListCell(editable=editable, size=size)
    cell.setAlignment_(NSRightTextAlignment)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def SmallCenterAlignTextListCell(editable=False, size=None):
    cell = SmallTextListCell(editable=editable, size=size)
    cell.setAlignment_(NSCenterTextAlignment)
    cell.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    return cell

def GlyphCell(glyph=None):
    glyphView = IconNSView((24, 24))
    #glyphView._glyph = glyph
    return glyphView

def RadioButtonListCell(title=None):
    cell = NSButtonCell.alloc().init()
    cell.setButtonType_(NSRadioButton)
    cell.setControlSize_(NSSmallControlSize)
    font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(NSSmallControlSize))
    cell.setFont_(font)

    if title is None:
        title = ""

    cell.setTitle_(title)
    return cell
