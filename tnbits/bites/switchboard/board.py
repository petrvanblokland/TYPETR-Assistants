
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
#    board.py
#

from AppKit import NSColor
from vanilla import (Group, SegmentedButton, ColorWell, CheckBox, EditText,
        RadioGroup, PopUpButton)
from tnbits.base.c import *
from tnbits.base.samples import *
from tnbits.base.constants.tool import *
from tnbits.base.text import *
from tnbits.base.views import *
from tnbits.base.view import View
from tnbits.bites.proof.constants import *
from tnbits.base.preferencemodels import *
from vanilla import Group
from tnbits.toolbox.transformer import TX

LINE = BUTTON_HEIGHT

class Board(View):
    """Adds buttons to a group view."""

    def __init__(self, controller, preferencesDict):
        padding = 10
        self.controller = controller
        self.preferencesDict = preferencesDict
        self.view = Group((0, 0, -0, -0))
        self.groups = {}
        self.currentToolName = None

        titles = []

        for k in preferencesDict.keys():
            titles.append(dict(title=k))

        b = SegmentedButton((10, 10, -1, 20), titles, callback=self.segSelection)
        b.set(0)
        self.view.preferencesDictKeys = b

        nsView = self.view.getNSView()
        nsView.setFrame_(((0, 0), (-0, -0)))

        for i, preferences in enumerate(preferencesDict.values()):
            group = Group((padding, padding, -padding, -0))
            self.buildPref(preferences, group, padding)
            if i == 0:
                self.currentToolName = preferences.toolName
            if i >= 1:
                self.hide(group)

    def getController(self):
        return self.controller

    def getView(self):
        return self.view

    def getNSView(self):
        return self.view.getNSView()

    def segSelection(self, sender):
        i = int(sender.get())
        self.currentToolName = self.controller.prefOrder[i]

        for n, g in self.groups.items():
            if n == self.currentToolName:
                self.show(g)
            else:
                self.hide(g)

    def hide(self, g):
        g.getNSView().setHidden_(True)

    def show(self, g):
        g.getNSView().setHidden_(False)

    def buildPref(self, preferences, group, padding):
        cx = 0
        cy = 20 + LINE
        CW = BUTTON_WIDTH
        setattr(self.view, preferences.toolName, group)
        self.groups[preferences.toolName] = group

        for name, preferenceModel in getSortedPreferences(preferences.model):
            label = preferenceModel.get('label')
            pType = preferenceModel.get('type')
            print(label)

            if label is None or pType is None:
                continue

            control = None
            controlLabel = None
            value = preferences.getPreference(name, default=preferenceModel['default'])

            if pType == PREFTYPE_COLOR:
                if len(value) == 3:
                    r, g, b = value
                    t = 1
                else:
                    r, g, b, t = value

                aLabel = getAttributedString(label)
                preferenceColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, t)
                control = ColorWell((cx, cy, BUTTON_WIDTH, LINE), color=preferenceColor,
                        callback=self.preferenceChangedCallback)
                controlLabel = TextBox((BUTTON_WIDTH + 2, cy, -2, LINE), aLabel)
                cy += LINE

            elif pType == PREFTYPE_BOOL:
                aLabel = getAttributedString(label)
                control = CheckBox((cx, cy, -2, LINE), aLabel, value=value,
                        callback=self.preferenceChangedCallback)
                cy += LINE

            elif pType in (PREFTYPE_INT, PREFTYPE_FLOAT):
                control = EditText((cx, cy, CW, LINE), text='%s' % value,
                        callback=self.preferenceChangedCallback)
                aLabel = getAttributedString(label)
                controlLabel = TextBox((cx + CW+2, cy+2, -2, LINE), aLabel)
                cy += LINE

            elif pType == PREFTYPE_RECT:
                aLabel = getAttributedString(label)
                setattr(group, 'tLabel_%s' % name, TextBox((cx, cy, -2, LINE),
                    aLabel))
                cy += LINE

                # 4 input boxes for x, y, w, h. Output is done here, because >
                # 1 field.
                for n in range(4):
                    setattr(group, 'tControl%d_%s' % (n, name), EditText((n*(cx+CW+2), cy, CW, 16),
                        text='%s' % value[n], callback=self.preferenceChangedCallback))
                cy += LINE

            elif pType == PREFTYPE_SIZE:
                aLabel = getAttributedString(label)
                setattr(group, 'tLabel_%s' % name, TextBox((cx, cy, -2, 0),
                    aLabel))
                cy += LINE
                # 2 input boxes for w, h. Output is done here, because > 1
                # field.
                for n in range(2):
                    setattr(group, 'tControl%d_%s' % (n, name), EditText(cx+(n*(CW+2), cy, CW, 16),
                        text='%s' % value[n], callback=self.preferenceChangedCallback))
                cy += LINE

            elif pType == PREFTYPE_LABEL:
                # Just show the value, cannot be changed.
                aLabel = getAttributedString('%s: %s' % (label, value))
                setattr(group, 'tLabel_%s' % name, TextBox((cx, cy, -2, 0),
                    aLabel))
                cy += LINE

            elif pType == PREFTYPE_RADIO:
                # Radio button. Needs value attribute to be defined with list
                # of labels.
                aLabel = getAttributedString(label)
                setattr(group, 'tLabel_%s' % name, TextBox((cx, cy,
                    BUTTON_WIDTH, BUTTON_HEIGHT), aLabel))
                values = preferenceModel.get('values')
                # values as attr strings.
                rg = RadioGroup((cx + BUTTON_WIDTH, cy, 2*BUTTON_WIDTH,
                    BUTTON_HEIGHT), values, isVertical=False)
                setattr(group, 'tControl_%s' % name, rg)
                rg.set(value)

                cy += LINE

            elif pType == PREFTYPE_LIST:
                # Popup list with single value select
                aLabel = getAttributedString(label)

                setattr(group, 'tLabel_%s' % name, TextBox((cx, cy, BUTTON_WIDTH, BUTTON_HEIGHT), aLabel))
                p = PopUpButton((cx + BUTTON_WIDTH, cy, 2*BUTTON_WIDTH,
                    BUTTON_HEIGHT), preferenceModel['values'],
                    sizeStyle='small')
                setattr(group, 'tControl0_%s' % name, p)

                if value in preferenceModel['values']:
                    p.setItem(value)

                cy += LINE

            if controlLabel is not None:
                setattr(group, 'tLabel_%s' % name, controlLabel)

            if control is not None:
                setattr(group, 'tControl0_%s' % name, control)

            if cy >= 500:
                cx = 2 * CW
                cy = 20 + LINE


    def preferenceChangedCallback(self, sender):
        """Gets all values of the current group when a preference has changed
        and stores them into the RoboFont preference area.

        FIXME: more efficient to update the correct single value each time.
        """
        group = self.groups[self.currentToolName]
        preferences = self.preferencesDict[self.currentToolName]
        self.updatePreferences(group, preferences, preferences.model)
        self.updateTool(group, preferences)

    def updatePreferences(self, group, preferences, model):
        for name, preference in model.items():
            pType = preference['type']

            if pType == PREFTYPE_COLOR:
                color = getattr(group, 'tControl0_%s' % name).get()
                r = color.redComponent()
                g = color.greenComponent()
                b = color.blueComponent()
                a = color.alphaComponent()
                preferences.setPreference(name, (r, g, b, a))

            elif pType == PREFTYPE_BOOL:
                attr = getattr(group, 'tControl0_%s' % name)
                preferences.setPreference(name, attr.get())

            elif pType == PREFTYPE_INT:
                value = TX.asIntOrNone(getattr(group, 'tControl0_%s' % name).get())
                if value is not None:
                    preferences.setPreference(name, value)

            elif pType == PREFTYPE_RECT:
                rect = list(preferences.getPreference(name, (0, 0, 0, 0)))

                for n in range(4):
                    # 4 input boxes for x, y, w, h.
                    value = TX.asIntOrNone(getattr(group, 'tControl%d_%s' % (n, name)).get())

                    if value is not None:
                        rect[n] = value

                preferences.setPreference(name, rect)

            elif type == PREFTYPE_SIZE:
                size = list(preferences.getPreference(name, (0, 0)))
                for n in range(2): # 2 input boxes for w, h.
                    value = TX.asIntOrNone(getattr(group, 'tControl%d_%s' % (n, name)).get())
                    if value is not None:
                        rect[n] = value
                preferences.setPreference(name, size)

            elif type == PREFTYPE_LIST:
                # Single name from button popup list selection
                preferences.setPreference(name, getattr(group, 'tControl0_%s' % name).getItem())

        if hasattr(preferences, 'standAlone') and preferences.standAlone is True:
            preferences.writePreferences()

    def updateTool(self, group, preferences):
        """Updates active tool preferences and calls the preferencesChanged()
        function to reload the values in the GUI."""
        from tnbits.base.tools import TOOLS
        from tnbits.tools.basetool import TOOLS as BASETOOLS
        group = self.groups[self.currentToolName]
        toolID = 'tn%s' % self.currentToolName
        tool = None
        toolType = None

        for key, value in TOOLS.items():
            if key.startswith(toolID):
                tool = value
                toolType = 'Tool'

        for key, value in BASETOOLS.items():
            if key.startswith(toolID):
                tool = value
                toolType = 'BaseTool'

        # Check if tool is active.

        if tool is not None:
            # Run through the preference model and get the values of the group
            # UI controls, then store the (new) values to the preferences.
            if toolType == 'Tool':
                self.updatePreferences(group, tool.preferences, preferences.model)
            elif toolType == 'BaseTool':
                self.updatePreferences(group, tool, tool.PREFERENCE_MODEL)

            tool.preferencesChanged()
