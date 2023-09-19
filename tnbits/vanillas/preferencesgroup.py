# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     prefereencesGroup.py
#


from AppKit import NSSegmentStyleSmallSquare, NSColor
from vanilla import (CheckBox, SegmentedButton, List, Tabs, Group, TextBox,
        ColorWell, EditText, Button, RadioGroup, PopUpButton)
from tnbits.tools.basetool import BaseTool

class PreferencesGroup():
    C = BaseTool.C # Inherit the reference to Constants

    def __init__(self, tool, pos, callback):
        group = Group(pos)
        group.toolId = tool.getId()
        cy = 4
        CW = 36

        for name, preference in self.getSortedPreferences(tool):
            label = preference.get('label')
            type = preference.get('type')

            if label is not None and type is not None:
                control = None
                controlLabel = None
                value = tool.getPreference(name, default=preference['default'])

                if type == self.C.PREFTYPE_COLOR:
                    if len(value) == 3:
                        r, g, b = value
                        t = 1
                    else:
                        r, g, b, t = value
                    preferenceColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, t)
                    control = ColorWell((0, cy, CW, 20), color=preferenceColor, callback=callback)
                    controlLabel = TextBox((CW+2, cy+4, -2, 12), label, sizeStyle='mini')
                    cy += 22

                elif type == self.C.PREFTYPE_BOOL:
                    control = CheckBox((0, cy, -2, 16), label, sizeStyle='mini', value=value, callback=callback)
                    cy += 18

                elif type in (self.C.PREFTYPE_INT, self.C.PREFTYPE_FLOAT):
                    control = EditText((0, cy, CW, 16), text='%s' % value, sizeStyle='mini', callback=callback)
                    controlLabel = TextBox((CW+2, cy+2, -2, 12), label, sizeStyle='mini')
                    cy += 18

                elif type == self.C.PREFTYPE_RECT:
                    setattr(group, 'tLabel_%s' % name, TextBox((0, cy, -2, 0), label, sizeStyle='mini'))
                    cy += 12
                    for n in range(4): # 4 input boxes for x, y, w, h. Output is done here, because > 1 field.
                        setattr(group, 'tControl%d_%s' % (n, name), EditText((n*(CW+2), cy, CW, 16),
                            text='%s' % value[n], sizeStyle='mini', callback=callback))
                    cy += 18

                elif type == self.C.PREFTYPE_SIZE:
                    setattr(group, 'tLabel_%s' % name, TextBox((0, cy, -2, 0), label, sizeStyle='mini'))
                    cy += 12
                    for n in range(2): # 2 input boxes for w, h. Output is done here, because > 1 field.
                        setattr(group, 'tControl%d_%s' % (n, name), EditText((n*(CW+2), cy, CW, 16),
                            text='%s' % value[n], sizeStyle='mini', callback=callback))
                    cy += 18

                elif type == self.C.PREFTYPE_LABEL: # Just show the value, cannot be changed.
                    setattr(group, 'tLabel_%s' % name, TextBox((0, cy, -2, 0), '%s: %s' % (label, value), sizeStyle='mini'))
                    cy += 12

                elif type == self.C.PREFTYPE_RADIO: # Radio button. Needs value attribute to be defined with list of labels.
                    setattr(group, 'tLabel_%s' % name, TextBox((0, cy, -2, 0), label, sizeStyle='mini'))
                    cy += 12
                    values = preference.get('values') or []
                    setattr(group, 'tControl_%s' % name, RadioGroup((0, cy, -2, 0), values, sizeStyle='mini', isVertical=False))
                    getattr(group, 'tControl_%s' % name).set(preference.get('default') or 0)
                    cy += 18

                elif type == self.C.PREFTYPE_LIST: # Popup list with single value select
                    setattr(group, 'tLabel_%s' % name, TextBox((0, cy, -2, 0), label, sizeStyle='mini'))
                    cy += 12
                    setattr(group, 'tControl0_%s' % name, PopUpButton((0, cy, -12, 16), preference['values'], sizeStyle='mini'))
                    cy += 18
                    if value in preference['values']:
                        getattr(group, 'tControl0_%s' % name, preference['values']).setItem(value)

                if controlLabel is not None:
                    setattr(group, 'tLabel_%s' % name, controlLabel)
                if control is not None:
                    setattr(group, 'tControl0_%s' % name, control)

        self.group = group

    def getSortedPreferences(self, tool):
        """Answers the list name+preference, sorted by the preference['sort']
        value. Allow duplicate sort values. If the sort key is missing in the
        preference, they set it to default 0."""
        preferences = tool.PREFERENCE_MODEL.items()

        def getSortKey(pair):
            k, v = pair
            return (v.get("sort", 0), k)

        list(preferences).sort(key=getSortKey)
        return preferences

    def hide(self):
        self.group.show(False)
