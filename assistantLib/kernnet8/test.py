# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   generateImages.py
#
import os
from drawBot import *
from fontParts.fontshell.font import RFont

#from fontParts.world import OpenFont
from drawBot import BezierPath, newPage, drawPath, fill, stroke, strokeWidth, translate
from fontTools.pens.basePen import BasePen

# This file contains a function to train a predictive kerning model using the KernNet class.
# The function is called with four parameters:
#   1. The path to the directory containing the data that the model will be trained on.
#   2. The number of training epochs that PyTorch will train the model for.
#   3. The fraction of training examples that will be used for model validation.
#   4. The batch size used during training.
#
# The script assumes that training images are stored as follows:
#
# Main_Directory (The path to this directory is what the function requires)
#
#   Sub_Directory_1
#       Image_1.png
#       ...
#       Image_X.png
#
#   ...
#
#   Sub_Directory_Y
#       Image_1.png
#       ...
#       Image_Z.png
#
#
# The function will work fine if there is only a single subdirectory.
# The subdirectories do not need to have the same number of images.
#
# Subdirectories currently follow this naming convention: Name_32_32
# Example: PrestiDeck-Book_32_32
#
# Single images follow this naming convention: LeftGlyphName_RightGlyphName_KerningValue
# Example: A.sc_ampersand.sc_-15

W, H = 48, 48
Y = H/4

class DrawBotPathPen(BasePen):
    def __init__(self, glyphSet, path):
        super().__init__(glyphSet)
        self.path = path

    def _moveTo(self, p):
        self.path.moveTo(p)

    def _lineTo(self, p):
        self.path.lineTo(p)

    def _curveToOne(self, p1, p2, p3):
        self.path.curveTo(p1, p2, p3)

    def _closePath(self):
        self.path.closePath()

UFOS_PATH = '/Users/petr/Desktop/TYPETR-git/TYPETR-Proforma-Pro/ufo/'
UFOS = (
    (UFOS_PATH + 'Proforma_Pro-Thin_MA16.ufo', 0), 
    (UFOS_PATH + 'Proforma_Pro-Regular_MA76.ufo', 0),
    (UFOS_PATH + 'Proforma_Pro-Bold_MA150.ufo', 0),
    (UFOS_PATH + 'Proforma_Pro-Black_MA220.ufo', 0),  
)
IMAGES_PATH = f'_imageTrain-'


f = RFont( UFOS[1][0], showInterface=False)
from fontParts.world import OpenFont
from drawBot import newDrawing, newPage, scale, translate, drawPath, BezierPath, saveImage, fill
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.basePen import decomposeSuperBezierSegment

glyph2Group1 = {}
glyph2Group2 = {}

for groupName, group in f.groups.items():
    for gName in group:
        if 'kern1' in groupName:
            glyph2Group1[gName] = groupName
        elif 'kern2' in groupName:
            glyph2Group2[gName] = groupName
       
gName1 = 'A'
gName2 = 'V'     
# --- Setup ---
g1 = f[gName1]
g2 = f[gName2]

k = f.kerning.get((glyph2Group1[g1.name], glyph2Group2[g2.name]), 0)
print(k)

W, H = 48, 48
s = H / f.info.unitsPerEm
y = -f.info.descender
italicOffset = 0

# --- Convert glyphs to BezierPaths via RecordingPen ---
def glyphToBezierPath(glyph):
    recPen = RecordingPen()
    glyph.draw(recPen)
    bp = BezierPath()
    for op, pts in recPen.value:
        if op == "moveTo":
            bp.moveTo(pts[0])
        elif op == "lineTo":
            bp.lineTo(pts[0])
        elif op == "curveTo":
            bp.curveTo(*pts)
        elif op == "qCurveTo":
            bp.qCurveTo(*pts)
        elif op == "closePath":
            bp.closePath()
    return bp

path1 = glyphToBezierPath(g1)
path2 = glyphToBezierPath(g2)

if k < 0:
    direction = -1
else:
    direction = 1

newDrawing()
for kdx in range(0, abs(k)+8, 8):
    kdx *= direction
    # --- Draw ---
    newPage(W, H)
    fill(0)
    scale(s, s)

    # Draw glyph A
    save()
    translate(W/s/2 - kdx/2 - g1.width + italicOffset, y)
    drawPath(path1)
    restore()
    
    # Draw glyph V
    save()
    translate(W/s/2 + kdx/2, y)
    drawPath(path2)
    restore()
    
    strokeWidth(2)
    stroke(0)
    line((W/2/s, 0), (W/2/s, H/s))
    
    stroke(None)
    fill(0, 0, 0, 0.1)
    rect(W/s/2 - kdx/2 - g1.width, 0, g1.width, H/s)
    
    fill(0, 0, 0.5, 0.1)
    rect(W/s/2 + kdx/2, 0, g2.width, H/s)
    