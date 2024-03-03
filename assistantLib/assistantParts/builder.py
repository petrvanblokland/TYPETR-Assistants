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
        projectPath = self.filePath2ParentPath(self.PROJECT_PATH)
        vfDirPath = projectPath + '_otf/'
        if not os.path.exists(vfDirPath):
            os.mkdir(vfDirPath)

        for f in AllFonts():
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
        command = ["/usr/local/bin/fontmake", "-o", "variable", "-m", dsPath, "--output-path", vfPath, ">", errorPath, "2>", errorPath]
        print(' '.join(command))
        #try:
        #    subprocess.run(command, check=True)
        #    print("Fontmake completed successfully.")
        #except subprocess.CalledProcessError as e:
        #    print(f"Fontmake failed with error: {e}")
        #    #subprocess.run(('open', errorPath))

        print(f'... Generating VF from {dsPath}')
        fontProject = FontProject()
        try:
            fontProject.run_from_designspace(dsPath, 
                output='variable',
                output_dir=vfDirPath, 
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
            print("... Font build successful!")
        except Exception as e:
            print(f"... Font build failed: {e}")

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
        for fontPath in (
            projectPath + '_otf/Segoe_UI_Display-Hairline_Italic_MA32.otf',
            projectPath + '_otf/Segoe_UI_Display-Light_Italic_MA98.otf',
            projectPath + '_otf/Segoe_UI_Display-Regular_Italic_MA168.otf',
            projectPath + '_otf/Segoe_UI_Display-Bold_Italic_MA323.otf',):

            pdfName = fontPath.split('/')[-1].replace('.otf', '-%03d.pdf' % self.BUILD_VERSION)
            print(f'... Generating PDF {pdfName}')
            
            db.newDrawing()
        
            #self.proofGlyphSet(fontPath, unicode2Glyph)
            self.proofGlyphSet(fontPath, unicode2Glyph, addSpaceMarker=True)

            self.proofWaterfall(fontPath, unicode2Glyph)

            self.proofText(fontPath, unicode2Glyph, DIACRITICS)
            self.proofText(fontPath, unicode2Glyph, ALICE_TEXT)
            self.proofText(fontPath, unicode2Glyph, CYRILLIC_NONSLAVIC_TEXT)
            self.proofText(fontPath, unicode2Glyph, GREEK_KERNING)

            exportPath = projectPath + '_export/' + pdfName
            db.saveImage(exportPath)

    def proofGlyphSet(self, fontPath, unicode2Glyph, addSpaceMarker=False):

        W, H = 595, 842
        M = 72
        SIZE = 36
        CW = W - 2 * M
        lineHeight = 1.2
        spaceMarkerColor = 0.7, 0.7, 0.7, 1 # Light gray for vertical space markers

        #fontVariations = dict(wght=weight, opsz=36)
        fontVariations = {}

        lines = []
        # Make full glyph set, sorted by unicode
        if addSpaceMarker:
            fs = db.FormattedString(font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=spaceMarkerColor) #, fontVariations=fontVariations)
            fs.appendGlyph('spacemarker')
        else:
            fs = db.FormattedString(font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=0) #, fontVariations=fontVariations)

        lines.append(fs)
        # TODO: Better to draw text for each glyph, so we can add name and margins
        for uni, g in sorted(unicode2Glyph.items()):
            fs += db.FormattedString(chr(uni), font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=0) #, fontVariations=fontVariations)
            if addSpaceMarker:
                fs += db.FormattedString(font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=spaceMarkerColor) #, fontVariations=fontVariations)
                fs.appendGlyph('spacemarker')
            if not g.width:
                fs += ' '

            tw, th = db.textSize(fs)
            if tw > CW:
                lines.append(fs)
                if addSpaceMarker:
                    fs = db.FormattedString(font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=spaceMarkerColor) #, fontVariations=fontVariations)
                    fs.appendGlyph('spacemarker')
                else:
                    fs = db.FormattedString(font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight, fill=0) #, fontVariations=fontVariations)
        lines.append(fs)

        # Output text lines
        y = 0
        for line in lines:
            if y < M:
                db.newPage(W, H)
                y = H - M - SIZE
                db.text(db.FormattedString(fontPath.split('/')[-1], fontSize=10, font=fontPath), (M, H-M/2))
            db.text(line, (M, y))
            y -= SIZE * lineHeight


    def proofWaterfall(self, fontPath, unicode2Glyph):
        # Make waterfall

        W, H = 595, 842
        M = 72
        SIZE = 18
        CW = W - 2 * M
        lineHeight = 1.2

        db.newPage(W, H)
        y = H - M - SIZE
        db.text(db.FormattedString(fontPath.split('/')[-1], fontSize=10, font=fontPath), (M, H-M/2))
        fs = db.FormattedString()
        for size in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 52, 56):
            # TODO: Add size here
            fs += db.FormattedString('Hamburgefonstiv\n', font=fontPath, fontSize=size, lineHeight=size * lineHeight) #, fontVariations=fontVariations)
        db.textBox(fs, (M, M, CW, H - 2*M))


    def proofText(self, fontPath, unicode2Glyph, text):
        # Make waterfall

        W, H = 595, 842
        M = 72
        SIZE = 18
        CW = W - 2 * M
        lineHeight = 1.2

        fs = db.FormattedString(text, font=fontPath, fontSize=SIZE, lineHeight=SIZE * lineHeight) #, fontVariations=fontVariations)

        while fs:
            db.newPage(W, H)
            fs = db.textBox(fs, (M, M, CW, H - 2*M))



