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
#    axisdialog.py
#
from AppKit import NSNumberFormatter
from vanilla import Sheet, TextBox, Button, EditText
from tnbits.base.constants.tool import *
from tnbits.base.transformer import *

class AxisDialog(object):
    """Dialog to add an axis to the designspace."""
    # TODO: check if values are consistent: min <= default <= max

    fields = ('tag', 'name', 'minValue', 'defaultValue', 'maxValue')

    def __init__(self, parent, callback, cancelCallback):
        """
        parent: window calling up the dialog
        title: dialog title
        callback: parent function to be called after selection.
        """
        self.values = {}

        for f in self.fields:
            self.values[f] = None

        self.parent = parent
        self.title = 'Add Axis'
        self.callback = callback
        self.cancelCallback = cancelCallback
        self.width = (len(self.fields) * (PADDING + BUTTON_WIDTH)) + PADDING
        self.height = 6*UNIT + 7*PADDING
        dialogSize = (self.width, self.height)
        w = parent.getController().tool.getWindow()
        self.window = Sheet(dialogSize, w, minSize=dialogSize,
                maxSize=dialogSize)
        self.setButtons()
        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)
        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        self.window.okay.enable(False)
        self.window.open()

    # Callbacks.

    def okay(self, sender):
        self.callback(self.values)
        self.close(sender)

    def close(self, sender):
        if self.window is not None:
            self.window.close()
        self.cancelCallback()

    def tagEditCallback(self, sender):
        #TODO: check if tag exists and show error.
        self.values['tag'] = sender.get()
        self.isOkay()

    def nameEditCallback(self, sender):
        #TODO: check if name exists and show warning.
        self.values['name'] = sender.get()
        self.isOkay()

    def minValueEditCallback(self, sender):
        self.values['minValue'] = sender.get()
        self.isOkay()

    def defaultValueEditCallback(self, sender):
        self.values['defaultValue'] = sender.get()
        self.isOkay()

    def maxValueEditCallback(self, sender):
        self.values['maxValue'] = sender.get()
        self.isOkay()

    def isOkay(self):
        for field in self.fields:
            v = self.values[field]
            if v is None:
                self.window.okay.enable(False)
                return
            elif isinstance(v, str):
                if not v:
                    self.window.okay.enable(False)
                    return
                if field in ('minValue', 'defaultValue', 'maxValue'):
                    try:
                        float(v)
                    except:
                        self.window.okay.enable(False)
                        return

        self.window.okay.enable(True)

    # Set.

    def setButtons(self):
        x = PADDING
        w = BUTTON_WIDTH
        h = 2*UNIT

        for field in self.fields:
            y = PADDING
            pos = (x, y, w, h)
            tb = TextBox(pos, field)
            setattr(self.window, field, tb)
            y = 2*PADDING + 2*UNIT
            pos = (x, y, w, h)
            cb = getattr(self, '%sEditCallback' %  field)
            placeholder = self.getPlaceholder(field)
            #formatter = self.getFormatter(field)
            formatter = None
            et = EditText(pos, callback=cb, formatter=formatter, placeholder=placeholder)
            setattr(self.window, '%sEdit' % field, et)
            x += BUTTON_WIDTH + PADDING

    # Get.

    def getValues(self, sender):
        pass

    def getFormatter(self, field):
        if field in ('minValue', 'maxValue', 'defaultValue'):
            f = NSNumberFormatter.alloc().init()
            f.setPartialStringValidationEnabled_(True)
            return f

    def getPlaceholder(self, field):
        if field == 'minValue':
            return '-1'
        elif field == 'defaultValue':
            return '0'
        elif field == 'maxValue':
            return '1'
