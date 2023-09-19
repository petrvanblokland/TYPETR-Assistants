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
#    controller.py
#

import traceback
from AppKit import (NSBundle, NSImageNameAdvanced,
        NSImageNameFolderSmart, NSImageNameFontPanel)
from vanilla import SearchBox, SplitView, Button

from tnbits.base.constants.tool import *
from tnbits.base.console import Console
from tnbits.base.tools import *
from tnbits.base.scroll import ScrollGroup
from tnbits.base.controller import BaseController
from tnbits.vanillas.dialogs.dropdowndialog import DropDownDialog
from tnbits.bites.qatool.actions import Actions
from tnbits.bites.qatool.buttons import Buttons
from tnbits.bites.qatool.constants import *
from tnbits.bites.qatool.exception import QAException
from tnbits.bites.qatool.side import *
from tnbits.bites.qatool.stylesheet import QAStyleSheet
from tnbits.bites.qatool.transformer import *
from tnbits.qualityassurance.qamessage import headerMessage, getTitle
import tnbits.qualityassurance

class Controller(BaseController):
    """Implements internal logic between different parts of the QA tool."""

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self.selectedStyleIDs = None
        self.referenceID = None
        self.setOTSPath()
        self.setPreferences()
        self.console = Console(self)
        self.buttons = Buttons(self)
        self.tool.w.buttons = self.buttons.getView()
        self.actions = Actions(self, self.mode)
        self.tool.w.actions = self.actions.getView()
        self.styleSheet = QAStyleSheet(self)

        # TODO: use tool.set()
        padding = 4
        TOP = 24
        self.searchBox = SearchBox((2*SIDE + padding, 24, -padding, 16),
                callback=self.searchBoxCallback, sizeStyle="mini")
        self.tool.set('searchBox', self.searchBox)

        self.side = Side(self)
        nsview = self.side.getNSView()
        self.tool.set('side', ScrollGroup(nsview, (0, 0, 2* SIDE, -24)))
        self.console = Console(self)
        d0 = dict(identifier="styleSheet", view=self.styleSheet.getView())
        d1 = dict(identifier="console", view=self.console.getView())
        descriptors = [d0, d1]
        self.splitView = SplitView((2*SIDE, topMenu, -0, -24), descriptors,
                isVertical=False)
        self.tool.set('splitView', self.splitView)

        x = 0
        y = -20
        buttonWidth = 80
        b = Button((x, y, buttonWidth, 16), 'Core', sizeStyle='mini',
                callback=self.selectCore)
        self.tool.set('doSelectCore', b)
        b = Button((x + buttonWidth + padding, y, buttonWidth, 16), 'None',
                sizeStyle='mini', callback=self.selectNone)
        self.tool.set('doSelectNone', b)

    def update(self):
        self.styleSheet.update()

    def close(self):
        pass

    '''
    def getToolbarItems(self):
        items = [
            {"itemIdentifier": "qualityAssurance",
             "label": "QA",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.qualityAssuranceCallback},
            {"itemIdentifier": "sort",
             "label": "Sort",
             "imagePath": None,
             "imageNamed": NSImageNameFolderSmart,
             "callback": self.sortFamilyCallback},
        ]

        return items
    '''

    def textCenterCallback(self, sender):
        from tnbits.bites.tctool.tool import TextCenterTool
        openTool(TextCenterTool, self.family)

    def proofCallback(self, sender):
        from tnbits.bites.proof.tool import ProofTool
        openTool(ProofTool, self.family)

    def openStyleCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()
        self.editStyleKeys(styleKeys)

    def openFamilyCallback(self, sender):
        self.openFamily()

    def searchBoxCallback(self, sender):
        searchString = sender.get()
        self.styleSheet.update(searchString=searchString)

    def designSpaceCallback(self, sender):
        i = sender.get()
        names = self.getDesignSpaceNames()
        name = names[i]
        self.setDesignSpace(name)
        self.update()

    def runQualityAssurance(self):
        """Calls functions in the `tnbits.qualityassurance` module and collects
        the resulting messages to be displayed in the console."""
        selectedIDs = self.styleSheet.getSelectedIDs()
        stylesDict = self.getStylesDict(selectedIDs)
        self.update()
        self.console.clearLines()
        messages = []
        self.console.message(headerMessage('Quality Assurance', 1))
        m = []
        keys = stylesDict.keys()
        hasRef = False

        # Styles report.

        for k in keys:
            if len(keys) > 1 and k == self.referenceID:
                msg = u' • %s (*)\n' % k
                m.append((msg, 'highlight'))
                hasRef = True
            else:
                msg = u' • %s\n' % k
                m.append((msg, 'plaintext'))

        for msg, lineType in m:
            self.console.message(msg, lineType=lineType)

        if hasRef:
            self.console.message('\n(*) reference style\n', lineType='highlight')

        # Calls all QA functions for selected categories.
        for category in categoryOrder:
            m = []
            found = []
            fs = allFunctions[category]

            if self.isSelectedCategory(category):
                # Get the module.

                for functionName in fs:
                    # Gets the function from the module.
                    referenceID = None
                    f = getattr(tnbits.qualityassurance, functionName)

                    if self.referenceID in stylesDict.keys():
                        referenceID = self.referenceID

                    mm = self.runQAFunction(f, category, functionName, referenceID, stylesDict)

                    if mm:
                        m.extend(mm)
                        found.append(getTitle(functionName))

                if m:
                    title = getTitle(category)
                    summary = 'Results for %s.\n' % ', '.join(found)
                    messages.append(headerMessage(title, 2))
                    messages.append(summary)
                    messages.extend(m)

        for m in messages:
            self.console.message(m)

        self.actions.setEnabled(True)

    def runQAFunction(self, f, category, functionName, referenceID, stylesDict):
        """Passes right parameters to function based on name. QA functions are
        called with a styles dictionary, a reference ID when needed and
        optional keyword arguments."""
        if not self.isSelectedFunction(category, functionName):
            return []

        args = self.getFunctionArguments(stylesDict, functionName)
        args['referenceID'] = referenceID
        return f(stylesDict, **args)

    # Saving.

    def getCategory(self, function):
        category = None

        for c, f in allFunctions.items():
            for name in f:
                if name == function:
                    category = c
                    break

        return category

    def savePreferences(self, sender=None):
        """Some of the preferences were changed in the UI. Save the values in
        RoboFont."""
        view = self.tool.getWindow()
        t = sender.getTitle()
        parts = t.split(' ')
        value = self.getCheckFlag(sender)

        # Reverse lookup of function name.
        # NOTE: this fails when function names are identical for different
        # categories, would be better if attribute name could be derived as
        # assigned to view.
        if len(parts) == 1:
            function = parts[0].lower()
        else:
            p = [parts[0].lower()]
            for part in parts[1:]:
                p.append(upperFirst(part))
            function = ''.join(p)

        category = self.getCategory(function)
        flagName = getFlagName(category, function)
        self.setFlag(flagName, value)

    def setFlag(self, flagName, value):
        setattr(self, flagName, value)
        self.tool.setPreference(flagName, value)

    def selectAll(self, sender):
        self.setCheckboxesTo(True)

    def selectNone(self, sender):
        self.setCheckboxesTo(False)

    def selectCore(self, sender):
        self.setCoreCheckboxes()

    # Callbacks.

    def selectionCallback(self, sender):
        """Enables buttons depending selection."""
        '''
        view = self.buttons.getView()
        view.qualityAssurance.enable(len(sender.getSelection()))

        if self.mode == 'tool':
            view = self.actions.getView()
            view.openStyle.enable(len(sender.getSelection()))
        '''
        pass

    def saveCallback(self, sender):
        # TODO: custom name.
        self.console.save(fileName='qa.txt')

    def clearCallback(self, sender):
        self.console.clear()
        self.actions.setEnabled(False)

    def qualityAssuranceCallback(self, sender):
        # TODO: move to Buttons class.
        self.selectedStyleIDs = self.styleSheet.getSelectedIDs()

        if len(self.selectedStyleIDs) > 1 and \
                self.hasComparativeChecked() and \
                not self.referenceID in self.selectedStyleIDs:

            styleIDs = self.styleSheet.getAllIDs()
            dropDown = DropDownDialog(self, 'Reference Style', styleIDs,
                    self.confirmSetReferenceCallback, width=450)
            dropDown.open('Please select the reference style')
        elif len(self.selectedStyleIDs) > 0:
            self.qualityAssurance()

    def confirmSetReferenceCallback(self, referenceID):
        self.setReferenceID(referenceID)
        self.qualityAssurance()

    def qualityAssurance(self):
        """Gets styles after selection and runs them through the quality
        assurance functions."""
        self.console.clearLines()
        self.tool.progressOpen()

        try:
            self.runQualityAssurance()
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            self.console.setStackTrace(msg)

        self.console.setLines()
        self.tool.progressClose()

    def setPreferences(self):
        """Initializes global variables at tool or application startup."""
        # Loads all preferences.
        params = self.getPreferenceParams()

        for p in params:
            self.tool.setDefaultPreference(self, p)

    def preferencesChanged(self):
        self.side.update()

    # Family & style.

    def setFamily(self, family):
        """Initializes selected family at startup based on folder contents."""
        self.family = family
        self.setTitle(family)
        self.setDesignSpace(ANY)
        names = self.getDesignSpaceNames()
        view = self.buttons.getView()
        view.designSpaces.setItems(names)
        view.designSpaces.set(0)
        self.styleSheet.set()

    def sortFamilyCallback(self, sender):
        self.family.sort(verbose=True)
        self.styleSheet.update()
        log = getLog()
        log.set()

    def getStylesDict(self, styleIDs):
        """NOTE: Splitting approaches for now, should be moved to tnbits model."""
        stylesDict = {}

        # Collects styles in a dictonary.
        # TODO: add progress bar, opens all fonts so will be slow.
        # TODO: reverse;
        # for key in styleIDs:
        # if key in family.styleKeys
        #
        for key in self.family.getStyleKeys():
            if key[1] in styleIDs:
                styleID = key[1]
                style = self.family.getStyle(key)
                stylesDict[styleID] = style

        return stylesDict

    # Functions.

    def getFunctionArguments(self, styleID, functionName):
        """Collects optional arguments from constants and returns
        them in a dictionary."""
        d = {}

        if functionName in functionArgs:
            attrs = functionArgs[functionName]

            if isinstance(attrs, list):
                d['attrs'] = attrs
            elif isinstance(attrs, dict):
                for key, value in attrs.items():
                    d[key] = value

        return d

    # Preferences.

    def getPreferenceParams(self):
        params = []

        for category, fs in allFunctions.items():
            for function in fs:
                param = getFlagName(category, function)
                params.append(param)

        return params

    # Checkboxes.

    def getCheckbox(self, category, function):
        """Gets the checkbox value from side."""
        attr = getFlagName(category, function)
        group = self.side.getGroup(category)
        return getattr(group, attr)

    def setCheckboxesTo(self, value):
        """Sets all checkboxes belonging to category - function pair to True
        or False."""
        for category, fs in allFunctions.items():
            for function in fs:
                self.setCheckboxTo(category, function, value)

    def setCoreCheckboxes(self):
        """Sets all checkboxes belonging to category - function pair to True
        or False."""
        for category, fs in allFunctions.items():
            for function in fs:
                if function in coreFunctions:
                    value = True
                else:
                    value = False

                self.setCheckboxTo(category, function, value)

    def setCheckboxTo(self, category, function, value):
        """Sets a single checkbox belonging to category - function pair to
        True or False."""
        checkbox = self.getCheckbox(category, function)
        checkbox.set(value)
        flagName = getFlagName(category, function)
        self.setFlag(flagName, value)

    def hasComparativeChecked(self):
        for function in referenceFunctions:
            category = self.getCategory(function)
            checkbox = self.getCheckbox(category, function)
            if checkbox.get() == 1:
                return True
        return False

    def getCheckFlag(self, sender):
        v = sender.get()
        if v == 1:
            return True
        elif v == 0:
            return False
        else:
            raise QAException('invalid checkbox value for %s' % sender)

    # GUI.

    def setReferenceID(self, referenceID):
        self.referenceID = referenceID
        view = self.buttons.getView()
        view.referenceLabel.set(self.getReferenceLabel())

    def isSelectedFunction(self, category, functionName):
        """Checks if flag for function is selected.

        TODO: move to separate menu class.
        """
        flagName = getFlagName(category, functionName)
        flag = getattr(self, flagName)

        if flag is True:
            return True

        return False

    def isSelectedCategory(self, category):
        """Checks if any of the flags for this category are set.
        TODO: move to separate menu class.
        """
        functions = allFunctions[category]

        for functionName in functions:
            flagName = getFlagName(category, functionName)
            flag = getattr(self, flagName)

            if flag is True:
                return True

        return False

    def getReferenceLabel(self):
        if self.referenceID is None:
            r = '-'
        else:
            r = self.referenceID

        return getAttributedString('Reference: %s' % r)

    def setOTSPath(self):
        """Sets path to OTS, depending on mode.
        """
        import tnbits

        if self.mode == 'tool':
            path = tnbits.__path__[0]
            ots_path = path + '/contributions/ot-sanitise'
        elif self.mode == 'app':
            ots_path = NSBundle.mainBundle().resourcePath() + '/ot-sanitise'

        functionArgs['sanitiser'] = {'ots_path': ots_path}
