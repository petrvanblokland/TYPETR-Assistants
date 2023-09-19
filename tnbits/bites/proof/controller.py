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
from AppKit import NSImageNameFolderSmart, NSImageNameAdvanced
from vanilla import Window, SplitView

import os, traceback
from tnbits.base.console import Console
from tnbits.base.constants.tool import *
from tnbits.base.controller import BaseController
from tnbits.base.model import *
from tnbits.base.samples import *
from tnbits.base.scroll import ScrollGroup
from tnbits.base.toolbar import Toolbar
from tnbits.base.tools import *
from tnbits.bites.proof.constants import *
from tnbits.bites.proof.preferencemodel import preferenceModel
from tnbits.bites.proof.side import Side
from tnbits.bites.proof.stylesheet import StyleSheet
from tnbits.bites.proof.variations import Variations
from tnbits.proofing.factory import Factory

# TODO: add DrawBot to tool requirements.
try:
    from drawBot.ui.drawView import DrawView
except Exception:
    print("Could not find a valid installation of the DrawBot library!")
    print("To enable the live DrawView, please install DrawBot")
    print(" - with Mechanic,")
    print(" - install the Python module on your system using pip, easy_install or homebrew,")
    print(" - run the manual setup after downloading the code from")
    print('   https://github.com/typemytype/drawbot.')
    print(' - install the extension in RoboFont:')
    print('   https://github.com/typemytype/drawBotRoboFontExtension')

class Controller(BaseController):
    """Implements internal logic between different parts of proof tool."""

    style = None

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self.currentProof = None # Stores a reference to the latest proof.
        self.proofTraceback = None # TODO: remove once reporter class is used.
        self.fileNames = []
        self.factory = Factory() # Factory for getting the proof template.
        self.setPreferences()

        # GUI.
        #self.toolbar = Toolbar(self, items=self.getToolbarItems())
        self.side = Side(self)
        nsview = self.side.getNSView()
        self.tool.set('side', ScrollGroup(nsview, (0, 0, SIDE, -0)))
        self.styleSheet = StyleSheet(self)
        self.console = Console(self)
        self.variations = Variations(self)

        s0 = dict(identifier="variations", view=self.variations.getView())
        c = dict(identifier="console", view=self.console.getView())
        sv0 = SplitView((0, 0, -0, -0), [s0, c])

        s1 = dict(identifier="styleSheet", view=self.styleSheet.getView())
        sv = dict(identifier="SplitView0", view=sv0)
        splitView = SplitView((SIDE, 0, -0, -0), [s1, sv], isVertical=False)
        self.tool.set('splitView', splitView)
        self.initParameters()
        self.setConsole()
        self.setDrawWindow()

    def setDrawWindow(self):
        self.drawWindow = None

        if self.showDrawWindow:
            self.newDrawWindow()

    def getSampleIndex(self):
        try:
            i = SAMPLENAMES.index(self.sampleName)
        except:
            print(traceback.format_exc())
            print('%s does not exist' % self.sampleName)
            i = 0

        return i

    def newDrawWindow(self):
        self.drawWindow = Window((1200, 800), "Draw Window", closable=False,
                minSize=(40, 30), maxSize=(2000, 1600))
        self.drawWindow.drawView = DrawView((0, 0, -0, -0))
        self.drawWindow.open()

    def showDrawWindowCallback(self, sender):
        i = sender.get()
        self.showDrawWindow = i

        if self.showDrawWindow:
            self.newDrawWindow()
        else:
            self.drawWindow.close()
            self.drawWindow = None

        self.tool.setPreference('showDrawWindow', self.showDrawWindow)

    def close(self):
        if self.drawWindow:
            self.drawWindow.close()
            self.drawWindow = None

    def initParameters(self):
        try:
            g = self.getParameters(self.templateID)
        except Exception as e:
            #  Still on old 'waterfall' value, reset.
            self.tool.setPreference('templateID', 'PageWide')
            self.tool.setPreference('templateName', 'Page Wide')
            self.templateID = TEMPLATES_ORDER[0]
            self.templateName = TEMPLATE_NAMES_ORDER[0]
            return

        if self.templateID in ('TextProgression', 'PageWide', 'Overlay', 'AllMetrics'):
            g.fontSizeEntry.set(self.fontSize)

    def setStyle(self, styleKey):
        self.style = self.family.getStyle(styleKey)
        self.variations.setStyle(self.style)
        self.variations.update()

    def setFamily(self, family):
        """Sets the family after selection. This will reset the Proof caching
        and update the views. Sets the window title from the family name to see
        the difference when multiple Proof windows are open. Loads family in
        styles spreadsheet."""
        if not family:
            print('This is not a valid family!')
            return

        window = self.tool.getWindow()
        self.family = family
        self.setTitle(family)
        self.setDesignSpace(ANY)
        view = self.side.getView()
        names = self.getDesignSpaceNames()
        view.designSpaces.setItems(names)
        view.designSpaces.set(0)
        self.update()

    def closeFamily(self):
        self.family = None
        self.setTitle(None)
        self.update()

    def sortFamilyCallback(self, sender):
        self.family.sort(verbose=True)
        self.styleSheet.update()
        setLog()

    def getToolbarItems(self):
        items = [
            #{"itemIdentifier": "tc",
            # "label": "TC",
            # "imagePath": None,
            # "imageNamed": NSImageNameFolderSmart,
            # "callback": self.textCenterCallback},
            #{"itemIdentifier": "fix",
            # "label": "QA",
            # "imagePath": None,
            # "imageNamed": NSImageNameFolderSmart,
            # "callback": self.qualityAssuranceCallback},
            {"itemIdentifier": "openFamily",
             "label": "Open",
             "imagePath": None,
             "imageNamed": NSImageNameFolderSmart,
             "callback": self.openFamilyCallback},
            {"itemIdentifier": "proof",
             "label": "Proof",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.proofCallback},
        ]

        '''
        if self.mode == 'tool':
            items.append(
                {"itemIdentifier": "openStyle",
                 "label": "Open Style",
                 "imagePath": None,
                 "imageNamed": NSImageNameFontPanel,
                 "callback": self.openStyleCallback})
        '''
        return items

    def textCenterCallback(self, sender):
        from tnbits.bites.tctool.tool import TextCenterTool
        openTool(TextCenterTool, self.family)

    def qualityAssuranceCallback(self, sender):
        from tnbits.bites.qatool.tool import QualityAssuranceTool
        openTool(QualityAssuranceTool, self.family)

    # Preferences.

    def setPreferences(self):
        """Loads values from preferences."""
        for k, d in preferenceModel.items():
            print(k)
            default = d['default']
            self.tool.setDefaultPreference(self, k, value=default)

        '''
        # TODO: get values from constants.
        self.tool.setDefaultPreference(self, 'openProof', value=False)
        self.tool.setDefaultPreference(self, 'showDrawWindow', value=False)
        self.tool.setDefaultPreference(self, 'paperSize', value='A4')
        self.tool.setDefaultPreference(self, 'templateID', value='PageWide')
        self.tool.setDefaultPreference(self, 'templateName', value='Page Wide')
        self.tool.setDefaultPreference(self, 'sampleName', value='Basic Latin')
        self.tool.setDefaultPreference(self, 'paperPortrait', value=False)
        self.tool.setDefaultPreference(self, 'align', value=0)
        self.tool.setDefaultPreference(self, 'pageAlign', value=0)
        self.tool.setDefaultPreference(self, 'showGlyphSpace', value=False)
        self.tool.setDefaultPreference(self, 'showKernValues', value=False)
        self.tool.setDefaultPreference(self, 'withKerning', value=False)
        self.tool.setDefaultPreference(self, 'withAutoFit', value=False)
        self.tool.setDefaultPreference(self, 'fontSize', value=FONTSIZE_DEFAULT)
        self.tool.setDefaultPreference(self, 'fontSizeProgression', value=FONTSIZE_PROGRESSION_DEFAULT)
        self.tool.setDefaultPreference(self, 'leading', value=LEADING_DEFAULT)
        self.tool.setDefaultPreference(self, 'showMarginValues', value=False)
        self.tool.setDefaultPreference(self, 'showNames', value=False)
        self.tool.setDefaultPreference(self, 'showMissing', value=False)
        self.tool.setDefaultPreference(self, 'doOnePage', value=False)
        self.tool.setDefaultPreference(self, 'repeatLastGlyph', value=False)
        self.tool.setDefaultPreference(self, 'sampleTextPath', value='')
        self.tool.setDefaultPreference(self, 'sortGlyphs', value=False)
        self.tool.setDefaultPreference(self, 'compileText', value=False)
        self.tool.setDefaultPreference(self, 'doNewlines', value=False)
        '''
        self.savePreferences()

    def savePreferences(self):
        self.tool.setPreference('openProof', self.openProof)
        self.tool.setPreference('showDrawWindow', self.showDrawWindow)
        # TODO: get values from constants, merge with setPreferences.
        self.tool.setPreference('paperSize', self.paperSize)
        self.tool.setPreference('templateID', self.templateID)
        self.tool.setPreference('templateName', self.templateName)
        self.tool.setPreference('sampleName', self.sampleName)
        self.tool.setPreference('paperPortrait', self.paperPortrait)
        self.tool.setPreference('align', self.align)
        self.tool.setPreference('pageAlign', self.pageAlign)
        self.tool.setPreference('showGlyphSpace', self.showGlyphSpace)
        self.tool.setPreference('showKernValues', self.showKernValues)
        self.tool.setPreference('withKerning', self.withKerning)
        self.tool.setPreference('withAutoFit', self.withAutoFit)
        self.tool.setPreference('fontSize', self.fontSize)
        self.tool.setPreference('fontSizeProgression', self.fontSizeProgression)
        self.tool.setPreference('leading', self.leading)
        self.tool.setPreference('showMarginValues', self.showMarginValues)
        self.tool.setPreference('showNames', self.showNames)
        self.tool.setPreference('showMissing', self.showMissing)
        self.tool.setPreference('doOnePage', self.doOnePage)
        self.tool.setPreference('repeatLastGlyph', self.repeatLastGlyph)
        self.tool.setPreference('sampleTextPath', self.sampleTextPath)
        self.tool.setPreference('sortGlyphs', self.sortGlyphs)
        self.tool.setPreference('compileText', self.compileText)
        self.tool.setPreference('doNewlines', self.doNewlines)
        self.tool.writePreferences()

    def preferencesChanged(self):
        self.side.update()

    # Proof.

    def proof(self):
        """This is where the call to proof PDF generation is done. First the
        parameters are collected as keyword arguments, then these are then
        passed to the build() function of the template."""

        repeat = self.repeatLastGlyph
        fontSize = int(self.fontSize)
        fontSizeProgression = int(self.fontSizeProgression)
        #self.family.updateRFonts()

        kwargs = {
            'controller': self,
            'tool': self.tool,
            'family': self.family,
            'fontSize': fontSize,
            'fontSizeProgression': fontSizeProgression,
            'leading': self.leading,
            'withKerning': self.withKerning,
            'withAutoFit': self.withAutoFit,
            'showGlyphSpace': self.showGlyphSpace,
            'showKernValues': self.showKernValues,
            'showMarginValues': self.showMarginValues,
            'showNames': self.showNames,
            'showMissing': self.showMissing,
            'doOnePage': self.doOnePage,
            'repeatLastGlyph': repeat,
            'align': self.align,
            'pageAlign': self.pageAlign,
            'paperSize': self.getPaperSize(),
            'sortGlyphs': self.sortGlyphs,
            'compileText': self.compileText,
            'doNewlines': self.doNewlines,
        }

        # Passes arguments to new proof template.
        self.currentProof = self.factory.get(self.templateID, **kwargs)
        self.fileNames = []
        styleKeys = self.styleSheet.getSelectedKeys()

        try:
            self.tool.progressOpen(text='Opening styles', ticks=len(styleKeys))

            # Makes a proof with the template.
            if self.templateID in ('KerningMap'):
                # Non-text proofs.
                self.fileNames = self.currentProof.build(styleKeys)
            else:
                # Gets sample and passes it to <proofObject>.build() function.
                view = self.getParameters(self.templateID)
                sampleName, sample = self.getSample(styleKeys, view)
                self.fileNames = self.currentProof.build(styleKeys, sampleName, sample)

        except Exception as e:
            # TODO: add traceback to reporter.
            tracebackMessage = traceback.format_exc()
            self.proofTraceback = tracebackMessage
            print(tracebackMessage)
        finally:
            # Open the PDF files if the flag is set.
            if self.openProof and not self.fileNames is None and self.fileNames:
                try:
                    cmd = u'open "%s"' % u'" "'.join(self.fileNames)
                    os.system(cmd)
                except Exception as e:
                    for f in self.fileNames:
                        print(type(f))
                    print(traceback.format_exc())

            if self.drawWindow and self.currentProof.pdfs:
                self.drawWindow.drawView.setPDFDocument(self.currentProof.pdfs[0])
                self.drawWindow.show()

            self.setConsole()
            self.tool.progressClose()

        log = getLog()
        log.set()


    # Callbacks.

    def designSpaceCallback(self, sender):
        i = sender.get()
        names = self.getDesignSpaceNames()
        name = names[i]
        self.setDesignSpace(name)
        self.update()

    def removeFromDesignSpace(self, styleKey):
        print("TODO: remove from design space: %s" % str(styleKey))

    def openStyleCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()
        self.editStyleKeys(styleKeys)

    def openFamilyCallback(self, sender):
        self.openFamily()

    def proofCallback(self, sender):
        self.proof()

    # Robofont callbacks.

    def fontWillOpen(self, event):
        """Check if the opening font is one of the Interpolator. Save if first
        if it is dirty. The replace the family style reference by the new font
        instance."""
        # TODO: check.
        self.family.pushStyle(event['font'])

    def fontDidOpen(self, event):
        """Make sure that the open family/styles match the naked fonts of
        RoboFont."""
        # TODO: check.
        pass

    def fontDidClose(self, event):
        """Make sure that the open family/styles match the naked fonts of
        RoboFont."""
        # TODO: check.
        pass

    # Get.

    def getSample(self, styleKeys, view):
        """Returns one of the defined sample sets or a custom sample file."""
        i = view.selectSample.get()
        sampleName = SAMPLENAMES[i]
        sample = SAMPLES[i]

        if sample == SELECTED_SAMPLE:
            # If there is no sample text path, ask for a file first.
            if not self.sampleTextPath:
                self.selectSampleTextCallback()

            if self.sampleTextPath:
                sample = self.readFile(self.sampleTextPath)

        elif sample == ALL_GLYPHS_TAG:
            for styleKey in styleKeys:
                sample = []

                for glyphName in model.getStyle(styleKey).keys():
                    if glyphName == '.notdef':
                        continue
                    sample.append(glyphName)

            sample = '/'.join(sorted(sample))

        return sampleName, sample

    def setFontSize(self, size):
        self.fontSize = int(size)

    def getFontSize(self):
        return self.fontSize

    def setFontSizeProgression(self, size):
        self.fontSizeProgression = int(size)

    def getPaperSize(self):
        """Returns size and dimensions, depending on portrait / landscape
        orientation."""
        view = self.side.getView()

        w, h, margin = PAPERSIZES[self.paperSize]

        if not view.paperPortrait.get():
            h, w = w, h # Swap value

        return (self.paperSize, (w, h, margin))

    def getTemplateID(self):
        for t, n in TEMPLATES.items():
            if n == self.templateName:
                return t

    def getParameters(self, templateID):
        return self.side.getGroup(templateID)

    def getSmallerFontSize(self):

        i = 0
        n = int(FONTSIZES[i])

        while self.fontSize > n:
            i += 1
            n = int(FONTSIZES[i])

        return n, i

        '''
        i = FONTSIZES.index(self.fontSize)

        if i > 0:
            return FONTSIZES[i-1], i-1

        return self.fontSize, 0
        '''

    def tmpGetDesignSpace(self):
        """Answers the current design space."""
        view = self.side.getView()
        i = view.designSpaces.get()
        keys = list(self.family.designSpaces.keys())
        n = keys[i]
        return self.family.designSpaces[n]

    def getStyle(self, styleKey):
        """Answers the updated style of styleId."""
        return self.family.getStyle(styleKey)

    def update(self):
        self.styleSheet.update()

    def setConsole(self):
        """Clears the console and prints out the new lines."""
        self.console.clearLines()
        self.console.message('Template: %s\n' % self.templateName)

        if self.paperPortrait:
            p = 'portrait'
        else:
            p = 'landscape'

        self.console.message('Paper: %s (%s)\n' % (self.paperSize, p))

        if self.sortGlyphs:
            s = 'sorted'
        else:
            s = 'not sorted'

        self.console.message('Sample: %s (%s)\n' % (self.sampleName, s))

        if self.currentProof is not None:
            if self.currentProof.errors:
                for e in self.currentProof.errors:
                    msg = '%s \n' % e
                    self.console.message((msg, 'error'))

        if self.proofTraceback is not None:
            # TODO: change to console traceback.
            self.console.message(self.proofTraceback)

        if not self.fileNames is None and self.fileNames:
            for n in self.fileNames:
                self.console.message('Saved to %s \n' % n)

        self.console.setLines()

    # I/O

    def readFile(self, path):
        """Reads UTF-8 sample text file from path."""
        # TODO: move somewhere else.
        if os.path.exists(path):
            f = open(path, encoding='utf-8', mode='r+')
            t = f.read()
            f.close()
            return t

        return 'Error reading sample file.'
