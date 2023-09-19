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
#    groupswindow.py
#

from vanilla import Window, TextBox, SplitView, Group, EditText
from tnbits.base.constants.tool import *
from tnbits.base.view import View
from tnbits.base.views import *
from tnbits.base.windows import setBackgroundColor
from tnbits.base.constants.tool import *
from tnbits.bites.tctool.constants import *
from tnbits.bites.tctool.spreadsheetview import SpreadsheetView
from tnbits.bites.tctool.status import Status

class GroupsWindow():

    NAME = 'Groups'

    def __init__(self, controller):
        self.controller = controller
        self.currentGroupName = None
        self._isOpen = False

    def build(self):
        TOP = 6*UNIT
        BOTTOM = -3*UNIT
        self.w = Window((450, 800), "Groups Window", closable=True,
                minSize=(40, 30), maxSize=(450, 1200))
        setBackgroundColor(self.w)
        self.w.info = TextBox((MARGIN, 0, -0, TOP), '')
        self.groupsText = Group((0, 0, -0, -0))
        self.groupsText.info = TextBox((MARGIN, 0, -0, 20), '')
        self.groupsText.editor = EditText((0, 20, -0, -0), '',
                callback=self.groupsTextCallback, continuous=False)

        self.spreadsheetView = SpreadsheetView(self)
        pane0 = dict(identifier="spreadsheet", view=self.spreadsheetView.getView(), size=350)
        pane1 = dict(identifier="edit", view=self.groupsText)

        posSize = (0, TOP, -0, BOTTOM)
        self.splitView = SplitView(posSize, [pane0, pane1], isVertical=False)
        self.status = Status(self)
        self.w.splitView = self.splitView
        self.w.status = self.status.getView()

    def getWindow(self):
        return self.w

    def getSpreadsheetView(self):
        return self.spreadsheetView

    # Window.

    def open(self):
        self.build()
        self.bind()
        self.w.open()
        self._isOpen = True

    def closeCallback(self, sender):
        """Close callback after pressing close button in the title bar."""
        self.terminate()

    def close(self):
        if self.w is not None:
            self.w.close()

    def show(self):
        if self._isOpen is False:
            self.open()

        self.w.show()

    def terminate(self):
        """Finalizes window close."""
        self._isOpen = False
        self.unbind()
        self.w = None

    def bind(self):
        self.w.bind('close', self.closeCallback)

    def unbind(self):
        if self.w is not None:
            self.w.unbind('close', self.closeCallback)

    def setTitle(self, styleName):
        if not self._isOpen:
            return

        t = '%s - %s' % (styleName, self.NAME)
        self.w.setTitle(t)

    # Groups.

    def setInfo(self, msg1, msg2, msg3):
        if not self._isOpen:
            return

        s1 = getAttributedString('%s -- %s' % (msg1, msg2))
        s2 = getAttributedString(msg3)
        self.w.info.set(s2)
        self.status.set(s1)

    def groupsTextCallback(self, sender):
        t = sender.get().strip()
        glyphNames = t.split(' ')
        if self.currentGroupName and glyphNames and len(glyphNames) > 0:
            glyphNames = self.controller.setGroupGlyphs(self.currentGroupName, glyphNames)
            self.groupsText.editor.set(' '.join(glyphNames))

    def clicked(self, left=True):
        style = self.controller.style
        l = self.controller.getSelectedGroup()
        r = self.controller.getSelectedGroup(left=False)
        lgn = self.controller._selectedLeftGroupName
        rgn = self.controller._selectedRightGroupName

        if left and l:
            s = getAttributedString(lgn)
            self.groupsText.info.set(s)
            self.groupsText.editor.set(' '.join(l))
            self.currentGroupName = lgn
        elif not left and r:
            s = getAttributedString(rgn)
            self.groupsText.info.set(s)
            self.groupsText.editor.set(' '.join(r))
            self.currentGroupName = rgn
