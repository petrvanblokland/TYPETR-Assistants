# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   buolder.py
#
#   This part support various ways to be build fonts.
#
import sys, os
from math import *
from vanilla import *
import drawBot as db

from fontmake.font_project import FontProject

from mojo.UI import OpenGlyphWindow
from mojo.roboFont import CurrentFont, AllFonts

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.data import * # Import anchors names
from assistantLib.kerningSamples import DIACRITICS
from assistantLib.kerningSamples.cyrillic import * # Also has Greek
from assistantLib.kerningSamples.dutch import *
from assistantLib.kerningSamples.jills import ALICE_TEXT

class AssistantPartBuilder(BaseAssistantPart):
    """This part support various ways to be build fonts.
    """

    BUILD_VERSION = 0 # Build version number. To be redefined by inheriting assistant class.

    DESIGN_SPACE_VF = None # To be redefined by inheriting assistant class.

    def initMerzBuilder(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""

    def updateMerzBuilder(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return 

    def updateBuilder(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width.
        Answer the boolean flag if something was changed to the glyph."""
        changed = False
        g = info['glyph']
        if g is None:
            return changed # Nothing changed.
        
        return changed

    def buildBuilder(self, y):

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.buildOTFButton = Button((C0, y, CW, L), 'Build OTF', callback=self.buildOTFCallback)
        c.w.buildVFButton = Button((C1, y, CW, L), 'Build VF', callback=self.buildVFCallback)
        c.w.proofButton = Button((C2, y, CW, L), 'Proof PDF', callback=self.proofCallback)
        y += L

        return y

    def buildOTFCallback(self, sender):
        """For all open fonts, save the UFO and generate an OTF."""
        projectPath = self.filePath2ParentPath(self.PROJECT_PATH)
        vfDirPath = projectPath + '_otf/'
        if not os.path.exists(vfDirPath):
            os.mkdir(vfDirPath)

        for f in AllFonts():
            f.save() # Just to be sure we're generating from the latest version, in case we start using fontmake for this.
            otfName = f.path.split('/')[-1].replace('.ufo', '.otf')
            print(f'... Generating {otfName}')
            f.generate("otfcff", path=vfDirPath + otfName, autohint=True)

    def buildVFCallback(self, sender):
        """Build a quick VF to test interpolation and such. This is not replacing the main build.py,
        which runs in the background, can have a multi-stage sequecen of design spaces, etc.
        """
        projectPath = self.filePath2ParentPath(self.PROJECT_PATH)

        vfDirPath = projectPath + 'vf/'
        if not os.path.exists(vfDirPath):
            os.mkdir(vfDirPath)

        dsPath = projectPath + self.DESIGN_SPACE_VF
        errorPath = projectPath + f'build-errors-{self.BUILD_VERSION:03d}.txt'
        vfPath = vfDirPath + self.DESIGN_SPACE_VF.replace('.designspace', '-%03d.ttf' % self.BUILD_VERSION)

        #os.system(f'rm {vfPath}/*.ttf')
        #command = ["/usr/local/bin/fontmake", "-o", "variable", "-m", dsPath, "--output-path", vfPath, ">", errorPath, "2>", errorPath]
        #cmd = f'fontmake -o variable -m {dsPath} --output-path {vfPath}' #, ">", errorPath, "2>", errorPath]
        #print(cmd)
        #return 
        
        #print(' '.join(command))
        #try:
        #    subprocess.run(command, check=True)
        #    print("Fontmake completed successfully.")
        #except subprocess.CalledProcessError as e:
        #    print(f"Fontmake failed with error: {e}")
        #    #subprocess.run(('open', errorPath))

        print(f'... Generating VF from {dsPath}')
        fontProject = FontProject()

        fontProject.run_from_designspace(dsPath, 
            output='variable',
            output_dir=vfDirPath,
            master_path=projectPath, 
            interpolate=True, 
            #remove_overlaps=True, 
            #optimize_cff=True, 
            autohint=True, 
            #use_afdko=True, 
            #subset=True, 
            #keep_glyphnames=True, 
            #keep_overlaps=True, 
            #keep_direction=True, 
            #notoSans=True, 
            #optimize=True, 
            #family_name=None, 
            #style_name=None, 
            #mtlk=False, 
            #notdef_outline=False, 
            verbose=True)

    def proofCallback(self, sender):
        f = CurrentFont() # Get it for checking glyph widths, unicodes, etc.
        unicode2Glyph = {} # Sort the glyphs by unicode and remember their names
        for g in f:
            if g.unicode:
                unicode2Glyph[g.unicode] = g

        projectPath = self.filePath2ParentPath(self.PROJECT_PATH)
        vfDirPath = projectPath + 'vf/'
        fontPath = vfDirPath + self.DESIGN_SPACE_VF.replace('.designspace', '-%03d.ttf' % self.BUILD_VERSION)

        #fontVariations
        #for weight in (100, 200, 300, 350, 400, 600, 700):
        # @@@ For now. These need to go into the actual project assistant code.
        for fontPath in (
            projectPath + '_otf/Segoe_UI_Display-Hairline_Italic_MA32.otf',
            projectPath + '_otf/Segoe_UI_Display-Light_Italic_MA98.otf',
            projectPath + '_otf/Segoe_UI_Display-Regular_Italic_MA168.otf',
            projectPath + '_otf/Segoe_UI_Display-Bold_Italic_MA323.otf',

            projectPath + '_otf/Segoe_UI_Small-Hairline_Italic_MA97.otf',
            projectPath + '_otf/Segoe_UI_Small-Light_Italic_MA160.otf',
            projectPath + '_otf/Segoe_UI_Small-Regular_Italic_MA200.otf',
            projectPath + '_otf/Segoe_UI_Small-Bold_Italic_MA300.otf',

            projectPath + '_otf/Segoe_UI_Text-Hairline_Italic_MA62.otf',
            projectPath + '_otf/Segoe_UI_Text-Light_Italic_MA98.otf',
            projectPath + '_otf/Segoe_UI_Text-Regular_Italic_MA168.otf',
            projectPath + '_otf/Segoe_UI_Text-Bold_Italic_MA323.otf',
            ):
            pdfName = fontPath.split('/')[-1].replace('.otf', '-%03d.pdf' % self.BUILD_VERSION)
            print(f'... Generating PDF {pdfName}')
            
            db.newDrawing()
        
            #self.proofGlyphSet(fontPath, unicode2Glyph)
            pn = 0
            pn = self.proofGlyphSet(fontPath, unicode2Glyph, pageNumber=pn, showSpaceMarker=True, showNames=True)

            pn = self.proofWaterfall(fontPath, unicode2Glyph, pageNumber=pn)

            pn = self.proofText(fontPath, unicode2Glyph, DIACRITICS, pageNumber=pn)
            pn = self.proofText(fontPath, unicode2Glyph, ALICE_TEXT, pageNumber=pn, maxPages=2)
            pn = self.proofText(fontPath, unicode2Glyph, CYRILLIC_NONSLAVIC_TEXT, pageNumber=pn, maxPages=2)
            pn = self.proofText(fontPath, unicode2Glyph, GREEK_KERNING, pageNumber=pn, maxPages=2)

            exportPath = projectPath + '_export/' + pdfName
            db.saveImage(exportPath)

    def _addPageNumber(self, pn, fontPath, xy, fontSize=None):
        """And the pagenumber to the current open DrawBot page."""
        if fontSize is None:
            fontSize = 10
        fs = db.FormattedString(f'– {pn} –', align='center', font=fontPath, fontSize=fontSize)
        db.text(fs, xy)

    def proofGlyphSet(self, fontPath, unicode2Glyph, showSpaceMarker=False, showNames=False, pageNumber=0, fontSize=0):
        """Draw glyphset pages, sorted by unicode. With showSpaceMarker the zero-width /spacemarker is added to between all glyphs,
        ignoring any accidental kerning showing. The lines are space in plain spacing.
        Answer the last used page number.
        """

        W, H = 595, 842
        M = 72
        if fontSize is None:
            fontSize = 24
        NAME_SIZE = 1 # Really small name size
        CW = W - 2 * M
        lineHeight = 1.2
        spaceMarkerColor = 0.7, 0.7, 0.7, 1 # Light gray for vertical space markers

        #fontVariations = dict(wght=weight, opsz=36)
        fontVariations = {}

        x = M
        y = 0
        hadZeroWidth = False

        # Make full glyph set, sorted by unicode
        if showSpaceMarker:
            spm = db.FormattedString(font=fontPath, fontSize=fontSize, lineHeight=fontSize * lineHeight, fill=spaceMarkerColor) #, fontVariations=fontVariations)
            spm.appendGlyph('spacemarker')
        else:
            spm = db.FormattedString(font=fontPath, fontSize=fontSize, lineHeight=fontSize * lineHeight, fill=0) #, fontVariations=fontVariations)

        for uni, g in sorted(unicode2Glyph.items()):
            if y < M:
                db.newPage(W, H)
                pageNumber += 1
                self._addPageNumber(pageNumber, fontPath, (M + CW/2, M/2))
                db.text(db.FormattedString(fontPath.split('/')[-1], fontSize=10, font=fontPath), (M, H-M/2))
                y = H - M - fontSize - lineHeight/2
            
            if x == M or hadZeroWidth: # Line starts with a space marker
                fs = spm
            else:
                fs = db.FormattedString()
            
            fs += db.FormattedString(chr(uni), font=fontPath, fontSize=fontSize, lineHeight=fontSize * lineHeight, fill=0) #, fontVariations=fontVariations)
            fs += spm

            db.text(fs, (x, y))

            # If showing names and unicodes
            if showNames:
                nameString = db.FormattedString('%04X\n/%s' % (uni, g.name), font=fontPath, fontSize=NAME_SIZE, lineHeight=NAME_SIZE * lineHeight, fill=(0.7, 0.7, 0.7, 1)) # Very small name in gray
                db.text(nameString, (x, y - fontSize * 0.2))

            tw, th = db.textSize(fs)
            if tw == 0:
                tw += fontSize / 3
                hadZeroWidth = True
            else:
                hadZeroWidth = False
            x += tw

            if x > W - M - tw:
                x = M
                y -= fontSize * lineHeight

        return pageNumber

    def proofWaterfall(self, fontPath, sample=None, unicode2Glyph, pageNumber=0):
        # Make waterfall

        W, H = 595, 842
        M = 72
        SIZE = 18
        captionSize = 10
        CW = W - 2 * M
        lineHeight = 1.2
        if sample is None:
            sample = 'Hamburgefonstiv'

        db.newPage(W, H)
        pageNumber += 1
        self._addPageNumber(pageNumber, fontPath, (M + CW/2, M/2))
        y = H - M 
        db.text(db.FormattedString(fontPath.split('/')[-1], fontSize=10, font=fontPath), (M, H-M/2))
        fs = db.FormattedString()
        for fontSize in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 52, 56):
            fs += db.FormattedString(f'{fonSize}pt\n' font=fontPath, fontSize=captionSize, lineHeight=captionSize * lineHeight)
            fs += db.FormattedString(f'{sample}\n', font=fontPath, fontSize=fontSize, lineHeight=fontSize * lineHeight) #, fontVariations=fontVariations)
        db.textBox(fs, (M, M, CW, H - 2*M))

        return pageNumber

    def proofText(self, fontPath, unicode2Glyph, text, pageNumber=0, maxPages=None):
        # Make waterfall

        W, H = 595, 842
        M = 72
        SIZE = 18
        CW = W - 2 * M
        lineHeight = 1.2

        fs = db.FormattedString(text, font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight) #, fontVariations=fontVariations)

        pageCount = 0
        while fs:
            db.newPage(W, H)
            pageNumber += 1
            self._addPageNumber(pageNumber, fontPath, (M + CW/2, M/2))
            fs = db.textBox(fs, (M, M, CW, H - 2*M))
            if maxPages is not None and pageCount >= maxPages:
                break
            pageCount += 1

        return pageNumber


