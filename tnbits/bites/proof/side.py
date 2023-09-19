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

import traceback
import os
from vanilla import (Button, PopUpButton, CheckBox, TextBox, Group, EditText,
        RadioGroup)
from vanilla.dialogs import getFile

from tnbits.base.constants.tool import *
from tnbits.base.samples import *
from tnbits.base.text import *
from tnbits.base.view import View
from tnbits.base.views import *
from tnbits.toolbox.transformer import TX
from tnbits.bites.proof.constants import *
from vanilla import Group

COLWIDTH = SIDE - 3*PADDING
INDENT = 80
COMBOWIDTH = COLWIDTH - INDENT
LINE = BUTTON_HEIGHT

class Side(View):
    """Adds all control buttons to a group view."""

    height = 620

    def __init__(self, controller):
        self.controller = controller
        self.view = Group((0, 0, SIDE - 2*PADDING, self.height))
        nsView = self.view.getNSView()
        nsView.setFrame_(((0, 0), (SIDE - 2*PADDING, self.height)))
        nsView.setFlipped_(True)
        x = PADDING
        y = self.height - PADDING
        y = self.buildProof(x, y)
        y = self.buildPaper(x, y)
        y = self.buildDesignSpace(x, y)
        y = self.buildTemplates(x, y)
        y = self.buildGroups(x, y)

    # Views.

    def getController(self):
        return self.controller

    def getView(self):
        return self.view

    def getNSView(self):
        return self.view.getNSView()

    def getGroup(self, templateID):
        view = self.getView()
        return getattr(view, '%sGroup' % templateID)

    # Update.

    def update(self):
        controller = self.getController()
        tool = controller.getTool()
        preferences = tool.getPreferences()

        for key, value in preferences.model.items():
            view = None
            t = value['type']

            if hasattr(self.view, key):
                view = self.view
            else:
                group = self.getGroup(self.controller.templateID)
                if hasattr(group, key):
                    view = group

            if view:
                attr = getattr(view, key)
                if t == PREFTYPE_BOOL:
                    v = preferences.getPreference(key)
                    attr.set(v)

    # Build.

    def buildProof(self, x, y):
        y -= BUTTON_HEIGHT
        self.view.proofButton = Button((x, y, COLWIDTH, BUTTON_HEIGHT), 'Proof',
                sizeStyle='small', callback=self.controller.proofCallback)
        y -= LINE

        s = getAttributedString('Open in Preview')
        self.view.openProof = CheckBox((x, y, COLWIDTH, 16), s,
            sizeStyle='small',
            value=self.controller.openProof, callback=self.savePreferences)
        y -= LINE

        s = getAttributedString('Show Draw Window')
        self.view.showDrawWindow = CheckBox((x, y, COLWIDTH, 16), s,
            sizeStyle='small',
            value=self.controller.showDrawWindow, callback=self.controller.showDrawWindowCallback)
        y -= LINE
        return y

    def buildPaper(self, x, y):
        """Paper selection and orientation."""
        w = SIDE - 4 * PADDING
        h = BUTTON_HEIGHT
        pos = (x, y, w, h)
        y = addTitle(self.view, pos, 'Paper', inverse=True)
        y -= LINE

        self.view.selectPaperSize = PopUpButton((x, y, w, h), PAPERORDER,
                sizeStyle='small', callback=self.savePreferences)
        i = PAPERORDER.index(self.controller.paperSize)
        self.view.selectPaperSize.set(i)
        y -= LINE

        s = getAttributedString('Portrait')
        self.view.paperPortrait = CheckBox((x, y, COLWIDTH, 16), s, sizeStyle='small',
            value=self.controller.paperPortrait, callback=self.savePreferences)
        y -= PADDING + LINE
        return y

    def buildDesignSpace(self, x, y):
        """Variation design space options.

        TODO: debug & extend.
        """
        w = SIDE - 4 * PADDING
        h = BUTTON_HEIGHT
        pos = (x, y, w, h)
        y = addTitle(self.view, pos, 'Design Space', inverse=True)
        y -= LINE

        self.view.designSpaces = PopUpButton((x, y, w, h), [],
                sizeStyle='small', callback=self.controller.designSpaceCallback)
        y -= LINE

        '''
        s = getAttributedString('Interpolate')
        self.view.doInterpolate = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.doInterpolate,
                callback=self.savePreferences)
        y -= LINE

        s = getAttributedString('Auto save')
        self.view.autoSave = CheckBox((x, y, COLWIDTH, 16), s, sizeStyle='small',
            value=self.controller.autoSave, callback=self.savePreferences)
        self.view.selectDesignSpace.enable(self.controller.doInterpolate)
        '''
        #y -= PADDING + LINE
        return y

    def buildTemplates(self, x, y):
        """Selects template to use for generating the proof."""
        w = SIDE - 4 * PADDING
        h = BUTTON_HEIGHT
        pos = (x, y, w, h)
        y = addTitle(self.view, pos, 'Template', inverse=True)
        y -= LINE
        self.view.selectTemplate = PopUpButton((x, y, w, h),
                TEMPLATES_NAMES_ORDER, sizeStyle='small',
                callback=self.savePreferences)

        try:
            i = TEMPLATES_NAMES_ORDER.index(self.controller.templateName)
        except Exception as e:
            print(traceback.format_exc())
            i = 0

        self.view.selectTemplate.set(i)
        y -= PADDING + LINE
        return y

    def buildGroups(self, x, y0):
        """Builds groups for different type of templates."""
        _, (_, h) = self.view.getNSView().frame()
        i = self.view.selectTemplate.get()
        selected = TEMPLATES_NAMES_ORDER[i]

        for t, n in TEMPLATES.items():
            g = Group((0, 0, -0, -0))
            y = self.height - y0 - LINE
            setattr(self.view, '%sGroup' % t, g)

            if t != 'KerningMap':
                y = self.buildSample(g, t, x, y)
                y = self.buildFontParameters(g, t, x, y)
                y = self.buildTextTemplateFlags(g, t, x, y)

            if selected != n:
                g.getNSView().setHidden_(True)

        return y

    # Callbacks.

    def setSize(self, g):
        fontSize = g.fontSizeEntry.get()

        if str(fontSize).isdigit():
            fontSize = int(fontSize)
        else:
            i = g.selectFontSize.get()
            fontSize = FONTSIZES[i]
            g.fontSizeEntry.set(fontSize)

        self.controller.setFontSize(fontSize)

    def setProgressionSize(self, g):
        fontSize = g.fontSizeProgressionEntry.get()

        if str(fontSize).isdigit():
            fontSize = int(fontSize)
        else:
            i = g.selectFontSizeProgression.get()
            fontSize = FONTSIZES[i]
            g.fontSizeProgressionEntry.set(fontSize)

        self.controller.setFontSizeProgression(fontSize)


    def selectSizeCallback(self, sender):
        fontSize = FONTSIZES[sender.get()]
        g = self.getCurrentGroup()
        g.fontSizeEntry.set(fontSize)
        self.controller.setFontSize(fontSize)

    def selectProgressionSizeCallback(self, sender):
        fontSize = FONTSIZES[sender.get()]
        g = self.getCurrentGroup()
        g.fontSizeProgressionEntry.set(fontSize)
        self.controller.setFontSizeProgression(fontSize)

    def getCurrentGroup(self):
        view = self.getView()
        i = view.selectTemplate.get()
        self.controller.templateName = TEMPLATES_NAMES_ORDER[i]
        self.controller.templateID = self.controller.getTemplateID()
        return self.getGroup(self.controller.templateID)

    def savePreferences(self, sender=None):
        """Some of the preferences were changed in the UI. Save the values in
        RoboFont."""
        # FIXME: only save the ones that have changed.
        view = self.getView()
        g = self.getCurrentGroup()

        # Font wide parameters.
        i = view.selectPaperSize.get()
        self.controller.paperSize = PAPERORDER[i]
        self.controller.paperPortrait = view.paperPortrait.get()

        if self.controller.templateID in ('TextProgression', 'PageWide',
                'Overlay', 'AllMetrics', 'StylesPerLine', 'HTML', 'ReadingEdge'):
            # Template specific parameters.
            i = g.selectSample.get()
            self.controller.sampleName = SAMPLENAMES[i]
            self.controller.withKerning = g.withKerning.get()
            self.controller.showGlyphSpace = g.showGlyphSpace.get()
            self.controller.showKernValues = g.showKernValues.get()
            self.controller.showMarginValues = g.showMarginValues.get()
            self.controller.showNames = g.showNames.get()
            self.setSize(g)
            self.controller.leading = LEADINGS[g.selectLeading.get()]
            self.controller.sortGlyphs = g.sortGlyphs.get()
            self.controller.compileText = g.compileText.get()
            self.controller.showMissing = g.showMissing.get()
            self.controller.doOnePage = g.doOnePage.get()
            self.controller.repeatLastGlyph = g.repeatLastGlyph.get()
            self.controller.doNewlines = g.doNewlines.get()

            if self.controller.templateID == 'TextProgression':
                self.setProgressionSize(g)
            elif self.controller.templateID == 'PageWide':
                self.controller.pageAlign = g.pageAlign.get()
            elif self.controller.templateID == 'StylesPerLine':
                self.controller.withAutoFit = g.withAutoFit.get()

                if self.controller.withAutoFit == 1:
                    g.selectLeading.enable(False)
                else:
                    g.selectLeading.enable(True)

            elif self.controller.templateID == 'Overlay':
                self.controller.align = g.align.get()

            # Set the sample text path. Test if the file really exists.
            if self.controller.sampleTextPath is not None and \
                    os.path.exists(self.controller.sampleTextPath):
                n = TX.path2FileName(self.controller.sampleTextPath)
                s = getAttributedString(n)
                p = self.controller.sampleTextPath
            else:
                n = 'No sample file selected'
                s = getAttributedString(n)
                p = ''

            g.selectedSampleFileName.set(s)
            self.controller.tool.setPreference('sampleTextPath', p)

            # Enables / disables sample file button.
            i = self.controller.getSampleIndex()

            if SAMPLES[i] == SELECTED_SAMPLE:
                g.selectSampleFile.enable(True)
                g.compileText.enable(True)
            else:
                g.selectSampleFile.enable(False)
                g.compileText.enable(False)

        self.controller.openProof = view.openProof.get()
        self.controller.savePreferences()

        # Enable / disable the right groups.
        for t in TEMPLATES:
            g = getattr(view, '%sGroup' % t)

            if t == self.controller.templateID:
                g.getNSView().setHidden_(False)
            else:
                g.getNSView().setHidden_(True)

        # Updates reporter samples.
        self.controller.setConsole()

    def selectSampleTextCallback(self, sender=None):
        """Selecting a sample file path."""
        paths = getFile(messageText='Custom sample text',
                        title='Select a .txt UTF-8 file.',
                        allowsMultipleSelection=False,
                        fileTypes=('txt',))

        if paths is not None:
            self.controller.sampleTextPath = paths[0]
            g = self.getGroup(self.controller.templateID)
            n = TX.path2FileName(paths[0])
            s = getAttributedString(n)
            g.selectedSampleFileName.set(s)
            self.savePreferences()

    def buildFontParameters(self, g, templateID, x, y):
        """Sets font size and leading."""
        w = SIDE - 4 * PADDING
        h = BUTTON_HEIGHT
        pos = (x, y, w, h)
        y = addTitle(g, pos, 'Parameters')

        s = getAttributedString('Font size')
        cw = COMBOWIDTH / 2
        size = str(self.controller.getFontSize())
        x0 = x + INDENT
        x1 = x0 + cw + PADDING

        g.selectFontSizeLabel = TextBox((x, y+2, INDENT, 16), s,
                sizeStyle='small')
        g.fontSizeEntry = EditText((x0, y, cw, 20),
                callback=self.savePreferences, sizeStyle='small')

        g.selectFontSize = PopUpButton((x1, y, cw - PADDING, 16),
                                FONTSIZES, sizeStyle='small',
                                callback=self.selectSizeCallback)
        g.fontSizeEntry.set(size)

        if size in FONTSIZES:
            i = FONTSIZES.index(size)
        else:
            i = 0

        g.selectFontSize.set(i)

        # Second font size for text progression.
        if templateID == "TextProgression":
            y += LINE
            fsp = str(self.controller.fontSizeProgression)
            s = getAttributedString('Start at size')
            g.fontSizeProgressionLabel = TextBox((x, y+2, INDENT, 16),
                    s, sizeStyle='small')

            g.fontSizeProgressionEntry = EditText((x0, y, cw, 20),
                    callback=self.savePreferences, sizeStyle='small')

            g.fontSizeProgression = PopUpButton( (x1, y, cw - PADDING, 16),
                    FONTSIZES, sizeStyle='small',
                    callback=self.selectProgressionSizeCallback)
            g.fontSizeProgressionEntry.set(fsp)

            if fsp in FONTSIZES:
                i = FONTSIZES.index(fsp)
            else:
                i = 0

            g.fontSizeProgression.set(i)

        if templateID == 'TextProgression':
            try:
                g.fontSizeProgression.enable(True)
            except Exception as e:
                print(traceback.format_exc())

        # Leading.

        y += LINE
        s = getAttributedString('Leading')
        g.selectLeadingLabel = TextBox((x, y+2, INDENT-PADDING, 16), s,
                sizeStyle='small')
        leadings = []

        for leading in LEADINGS:
            leadings.append('%0.1f' % leading)

        g.selectLeading = PopUpButton((x+INDENT, y, COMBOWIDTH, 16), leadings,
            sizeStyle='small', callback=self.savePreferences)
        g.selectLeading.set(leadings.index('%0.1f' % self.controller.leading))

        if self.controller.withAutoFit == 1:
            g.selectLeading.enable(False)
        else:
            g.selectLeading.enable(True)

        if templateID == "StylesPerLine":
            y += LINE
            s = getAttributedString('Auto fit')
            g.withAutoFit = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small',
                value=self.controller.withAutoFit, callback=self.savePreferences)

        if templateID == "Overlay":
            y += LINE
            # TODO: disable for templates other than overlay.
            s = getAttributedString('Align')
            g.alignTemplateLabel = TextBox((x, y, INDENT-PADDING, 16),
                    s, sizeStyle='small')
            g.align = RadioGroup((INDENT + PADDING, y, COLWIDTH-INDENT,
                16), ALIGNMENT_VALUES, isVertical=False, sizeStyle='small',
                callback=self.savePreferences)
            g.align.set(self.controller.align)

        y += LINE
        #y -= PADDING
        #pos = (x, y, COLWIDTH, 1)
        #addHR(self.view, pos, '%sFontParameters' % templateID, UILightBlue)
        #y -= PADDING + LINE
        return y

    def buildTextTemplateFlags(self, group, t, x, y):
        """Sets display flags."""
        s = getAttributedString('With kerning')
        group.withKerning = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.withKerning,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Show glyph space')
        group.showGlyphSpace = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.showGlyphSpace,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Show kern values')
        group.showKernValues = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.showKernValues,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Show margin values')
        group.showMarginValues = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.showMarginValues,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Show names')
        group.showNames = CheckBox((x, y, COLWIDTH, 16), s, sizeStyle='small',
                value=self.controller.showNames,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Show missing')
        group.showMissing = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.showMissing,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Do one page')
        group.doOnePage = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.doOnePage,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Repeat last glyph')
        group.repeatLastGlyph = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.repeatLastGlyph,
                callback=self.savePreferences)
        y += LINE
        s = getAttributedString('Do newlines')
        group.doNewlines = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.doNewlines,
                callback=self.savePreferences)
        #y += PADDING
        #pos = (x, y, COLWIDTH, 1)
        #addHR(self.view, pos, '%sTextTemplateFlags' % t, UILightBlue)
        #y += PADDING + LINE
        return y

    def buildSample(self, group, templateID, x, y):
        """Sets sample."""
        w = SIDE - 4 * PADDING
        h = BUTTON_HEIGHT
        pos = (x, y, w, h)
        y = addTitle(group, pos, 'Sample')

        group.selectSample = PopUpButton(
                                (x, y, w, h), SAMPLENAMES,
                                sizeStyle='small',
                                callback=self.savePreferences)

        i = self.controller.getSampleIndex()
        group.selectSample.set(i)

        # Button for sample file selection and showing of selected file name.
        y += LINE
        s = getAttributedString('Sample')
        group.selectSampleFile = Button((x, y, w, h), 'Select',
                sizeStyle='small', callback=self.selectSampleTextCallback)

        if SAMPLES[i] == SELECTED_SAMPLE:
            group.selectSampleFile.enable(True)
        else:
            group.selectSampleFile.enable(False)

        y += LINE

        # TODO: move this to status.
        customSampleFileName = TX.path2FileName(self.controller.sampleTextPath or \
                '') or 'No sample file selected'
        s = getAttributedString(customSampleFileName)
        group.selectedSampleFileName = TextBox((x, y, w, h), s,
                sizeStyle='small')

        y += LINE
        s = getAttributedString('Sort glyphs')
        group.sortGlyphs = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.sortGlyphs,
                callback=self.savePreferences)

        y += LINE
        s = getAttributedString('Compile text')
        group.compileText = CheckBox((x, y, COLWIDTH, 16), s,
                sizeStyle='small', value=self.controller.compileText,
                callback=self.savePreferences)

        y += LINE
        #y += PADDING
        #pos = (x, y, COLWIDTH, 1)
        #addHR(self.view, pos, '%sSample' % t, UILightBlue)
        #y += PADDING + LINE

        if templateID == "PageWide":
            s = getAttributedString('Page Align')
            group.pageAlignTemplateLabel = TextBox((x, y, INDENT-PADDING, 16),
                    s, sizeStyle='small')

            group.pageAlign = RadioGroup((INDENT + PADDING, y, COLWIDTH-INDENT,
                16), ALIGNMENT_VALUES, isVertical=False, sizeStyle='small',
                callback=self.savePreferences)

            group.pageAlign.set(self.controller.pageAlign)
            y += LINE

        return y
