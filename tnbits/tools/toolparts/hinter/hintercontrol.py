# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010 buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    hintercontrol.py
#

from vanilla import Group, TextBox, Button, CheckBox, PopUpButton, TextEditor
from AppKit import NSView, NSBezierPath, NSColor
import string, os, os.path

from tnbits.constants import Constants

class HinterControl(Group):
    """Controls the main hints debugging interface, including font selection
    and step buttons."""

    C = Constants

    LINE = 16

    C0 = 4
    C1 = 164
    C2 = 326
    C3 = 488
    C4 = 650
    C5 = 832
    C6 = 984

    families = []
    fonts = []
    unicodeRanges = []
    glyphs = []
    sizes = range(6, 16)

    def __init__(self, posSize, delegate, fontsFolder):
        super(HinterControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        self.families = sorted(fontsFolder.keys())
        self.fonts = sorted(fontsFolder[self.delegate.family])

        # Boxes.
        self.familiesBox = PopUpButton((self.C0, 2, 150, 30), self.families, callback=self.familyCallback)
        self.familiesBox.set(2)
        self.fontsBox = PopUpButton((self.C0, 32, 150, 30), self.fonts, callback=self.fontCallback)
        self.unicodeRanges = delegate.simulator.getUnicodeRangeNames()
        self.unicodesBox = PopUpButton((self.C0, 62, 150, 30), self.unicodeRanges, callback=self.unicodesCallback)
        self.unicodesBox.set(1)
        self.glyphs = delegate.simulator.getGlyphNames(self.unicodeRanges[1])
        self.glyphsBox = PopUpButton((self.C0, 92, 150, 30), self.glyphs, callback=self.glyphCallback)
        self.pointSizesBox = PopUpButton((self.C0, 122, 150, 30), map(str, self.sizes), callback=self.pointSizeCallback)
        self.pointSizesBox.set(self.sizes.index(self.delegate.size))

        # Buttons.
        self.stepOver = Button((self.C1, 4, 150, self.LINE), 'Step Over', callback=self.stepOverCallback)

        self.stepInto = Button((self.C2, 4, 150, self.LINE), 'Step Into', callback=self.stepIntoCallback)
        self.stepInto.getNSButton().setEnabled_(False)

        self.stepOut = Button((self.C3, 4, 150, self.LINE), 'Step Out', callback=self.stepOutCallback)
        self.stepOut.getNSButton().setEnabled_(False)

        self.run = Button((self.C4, 4, 150, self.LINE), 'Run', callback=self.runCallback)

        self.stop = Button((self.C5, 4, 150, self.LINE), 'Stop', callback=self.stopCallback)
        self.stop.getNSButton().setEnabled_(False)

        self.stepLabel = TextBox((self.C6, 4, 150, self.LINE), 'Step index: -')
        self.nextInstruction = TextEditor((self.C1, 24, -10, -10), '', callback=self.nextInstructionCallback)

    def update(self, message='', stepIndex=None, isCall=False, isInsideCall=False):
        """
        Sets current step index and next instruction message.
        """
        self.setStepIndex(stepIndex)
        self.setNextInstruction(message)
        self.setStepInto(isCall)
        self.setStepOut(isInsideCall)
        self.setRun(stepIndex)
        self.setStop(stepIndex)
        view = self.getNSView()
        view.setNeedsDisplay_(True)

    def setStepInto(self, isCall):
        if isCall is True:
            self.stepInto.getNSButton().setEnabled_(True)
        else:
            self.stepInto.getNSButton().setEnabled_(False)

    def setStepOut(self, isInsideCall):
        if isInsideCall is True:
            self.stepOut.getNSButton().setEnabled_(True)
        else:
            self.stepOut.getNSButton().setEnabled_(False)

    def setRun(self, stepIndex):
        if stepIndex is None:
            self.run.getNSButton().setEnabled_(True)
        else:
            self.run.getNSButton().setEnabled_(False)

    def setStop(self, stepIndex):
        if stepIndex is None:
            self.stop.getNSButton().setEnabled_(False)
        else:
            self.stop.getNSButton().setEnabled_(True)

    def familyCallback(self, sender):
        """
        Gets selected family name, passes parameters to delegate, updates rest
        of the boxes down to glyphs.
        """
        family = self.families[sender.get()]
        font = self.delegate.fontsFolder[family][0]
        self.delegate.updateFamily(family, font)
        self.updateFonts(family)

    def fontCallback(self, sender):
        """
        Gets selected font name, passes parameter to delegate, updates boxes
        below down to glyphs.
        """
        font = self.fonts[sender.get()]
        self.delegate.updateFont(font)
        self.updateUnicodeRanges()

    def unicodesCallback(self, sender):
        """
        Sets new glyph set.
        """
        unicodeRange = self.unicodeRanges[sender.get()]
        self.updateGlyphs(unicodeRange)

    def glyphCallback(self, sender):
        """
        Passes glyph name to delegate.
        """
        i = sender.get()
        glyph = self.glyphs[i]
        self.delegate.updateGlyph(glyph)

    def sortFonts(self, fonts):
        if len(fonts) == 0 or len(fonts) == 1:
            return fonts

        sFonts = []
        sFonts.append(fonts[0])

        for f in fonts[1:]:
            found = False
            for s in sFonts:
                if len(f) < len(s):
                    sFonts.insert(len(sFonts) - 1, f)
                    found = True
                    break

            if found is False:
                sFonts.append(f)

        return sFonts

    def getShortest(self, names):
        i = 0
        l = None

        for name, j in enumerate(names):
            k = len(name)
            if l is None:
                l = k
            elif k < l:
                i = j
                l = k

        return i

    def updateFonts(self, family):
        """
        Loads new font names into box, updates boxes below down to glyphs.
        """
        self.fonts = []
        fonts = self.delegate.fontsFolder[family]
        self.fonts = sorted(fonts)
        #i = self.getShortest(self.fonts)
        self.fontsBox.setItems(self.fonts)
        self.fontsBox.set(0)
        self.updateUnicodeRanges()

    def updateUnicodeRanges(self):
        """
        Gets the corresponding Unicode ranges for the font from the simulator.
        Loads new Unicode range names into box, updates boxes below down to glyphs.
        """
        self.unicodeRanges = self.delegate.simulator.getUnicodeRangeNames()
        self.unicodesBox.setItems(self.unicodeRanges)
        self.unicodesBox.set(1)
        self.updateGlyphs(self.unicodeRanges[1])

    def updateGlyphs(self, unicodeRange):
        """
        Sets glyph names for given Unicode range.
        """
        self.glyphs = self.delegate.simulator.getGlyphNames(unicodeRange)
        self.glyphsBox.setItems(self.glyphs)
        self.delegate.updateGlyph(self.glyphs[0])

    def pointSizeCallback(self, sender):
        self.delegate.updateSize(self.sizes[sender.get()])

    def nextInstructionCallback(self, sender):
        pass

    def stepOverCallback(self, sender):
        """
        # TODO: disable when last instruction has been reached.
        # TODO: Should call instructioncontrol only to prevent double call.
        """
        self.delegate.stepOver()

    def stepIntoCallback(self, sender):
        self.delegate.stepInto()

    def stepOutCallback(self, sender):
        self.delegate.stepOut()

    def runCallback(self, sender):
        """
        Runs entire program until next step index.
        """
        self.delegate.run()

    def stopCallback(self, sender):
        """
        Stops current debugging procedure, returns to 'zero'-state.
        """
        self.delegate.stop()
        self.setStop(None)
        self.setRun(None)

    def setNextInstruction(self, msg):
        self.nextInstruction.set(msg)

    def setStepIndex(self, i):
        if i is None:
            self.stepLabel.set('Step index: -')
        elif isinstance(i, int):
            self.stepLabel.set('Step index: %d' % i)
