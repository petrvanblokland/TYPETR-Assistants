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
#    side.py
#
from vanilla import Group, Button, PopUpButton, CheckBox, SegmentedButton
from tnbits.bites.assembly.constants import *
from tnbits.base.constants.tool import *
from tnbits.base.constants.colors import *
from tnbits.base.text import *
from tnbits.base.views import *
from tnbits.base.view import View

class Side(View):
    # TODO: set size to size of parent view if smaller, or to max size if larger.

    indent = 80
    height = 500

    def __init__(self, controller):
        """Interface to set parameters passed to FontMake."""
        # TODO: dynamic resize of view frame.
        self.controller = controller
        self.view = Group((0, 0, SIDE, self.height))
        nsView = self.view.getNSView()
        nsView.setFrame_(((0, 0), (SIDE, self.height)))
        nsView.setFlipped_(True)
        self.build()

    def build(self):
        line = BUTTON_HEIGHT + PADDING
        x = PADDING
        y = self.height - line
        w = SIDE - 2*PADDING
        h = BUTTON_HEIGHT
        s = 'small'

        pos = (x, y, w, h)
        y = addTitle(self.view, pos, 'Design Space', inverse=True)
        y -= line


        pos = (x, y, w, h)
        self.view.selectDesignSpace = PopUpButton(pos, [], sizeStyle=s,
                callback=self.controller.setDesignSpaceCallback)
        y -= line

        pos = (x, y, w, h)
        self.view.addRemove = SegmentedButton(pos, segmentDescriptions=PLUSMIN,
                selectionStyle="momentary", callback=self.addRemoveCallback)

        x1 = 60
        w1 = w - x1
        self.view.importDesignSpace = Button((x1, y, w1, h), 'Import', sizeStyle=s,
                callback=self.controller.importCallback)

        y -= 2*line
        y = addTitle(self.view, (x, y, w, h), 'XML', inverse=True)
        y -= line

        title = getAttributedString('Show Numbers')
        self.view.showNumbers = CheckBox((x, y, w, h), title, sizeStyle=s,
                value=True, callback=self.controller.showNumbersCallback)


        y-= line
        y = addTitle(self.view, (x, y, w, h), 'options', inverse=True)
        y -= line

        for k, v in options.items():
            value = self.getOptionValue(k, v)
            title = self.getOptionTitle(k)
            title = getAttributedString(title)

            cb = CheckBox((x, y, w, h), title, sizeStyle=s, value=value,
                    callback=self.setOptionsCheck)
            setattr(self.view, k, cb)
            y-= line

        self.view.setDefaultsButton = Button((x, y, w, h), 'Set to Defaults', sizeStyle=s,
                callback=self.setDefaultsCallback)
        y-= line

        '''
        y = addTitle(self.view, (x, y, w, h), 'run', inverse=True)
        y -= line
        t1 = getAttributedString('from Designspace')
        t2 = getAttributedString('from UFOs')
        cb = RadioGroup((x, y, w, 2*h), [t1, t2], sizeStyle=s,
                callback=self.setRun)
        cb.set(self.controller._runFrom)
        y-= 2*h + PADDING
        setattr(self.view, 'run', cb)
        y-= line
        y = addTitle(self.view, (x, y, w, h), 'outputs', inverse=True)
        y -= line

        for k in outputs_order:
            v = outputs[k]
            v = getAttributedString(v)
            value = getattr(self.controller, '_' + k)
            cb = CheckBox((x, y, w, h), v, sizeStyle=s, value=value,
                    callback=self.setOutputsCheck)

            setattr(self.view, k, cb)
            y-= line
        '''


    # Views.

    def getView(self):
        return self.view

    def getNSView(self):
        return self.view.getNSView()

    def show(self, doShow=True):
        hidden = not doShow
        self.view.getNSView().setHidden_(hidden)

    #

    def getController(self):
        return self.controller

    def getOptionTitle(self, key):
        return key.replace('_', ' ').title()

    def getOptionValue(self, key, default):
        value = getattr(self.controller, '_' + key)

        if value is None:
            value = default
            setattr(self.controller, '_' + key, default)
            self.controller.tool.setPreference(key, value)

        return value

    def setOutputsCheck(self, sender):
        """Sets fontmake output types."""
        t = sender.getTitle()
        # FIXME: reconnect.

        '''
        for k, v in outputs.items():
            if v == t:
                value = sender.get()
                setattr(self.controller, '_' + k, value)
                self.controller.tool.setPreference(k, value)
                break
        '''

    def setOptionsCheck(self, sender):
        """Sets fontmake run argument values."""
        t = sender.getTitle()
        t = t.replace(' ', '_').lower()

        for k, v in options.items():
            if k == t:
                value = sender.get()
                setattr(self.controller, '_' + t, value)
                self.controller.tool.setPreference(k, value)
                break

    def setDefaultsCallback(self, sender):
        for k, v in options.items():
            setattr(self.controller, '_' + k, v)
            self.controller.tool.setPreference(k, v)
            cb = getattr(self.view, k)
            cb.set(v)

    def addRemoveCallback(self, sender):
        if sender.get() == 0:
            self.controller.openAddDesignSpace()
        elif sender.get() == 1:
            self.controller.removeDesignSpace()

    def setRun(self, sender):
        self.controller._runFrom = int(sender.get())
        self.controller.tool.setPreference('runFrom', self.controller._runFrom)

    def getView(self):
        return self.view
