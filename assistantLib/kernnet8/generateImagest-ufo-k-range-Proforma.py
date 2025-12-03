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

from drawBot import newDrawing, newPage, scale, translate, drawPath, BezierPath, saveImage, fill
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.basePen import decomposeSuperBezierSegment

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

UFOS_PATH = '/Users/petr/Desktop/TYPETR-git/TYPETR-Proforma-Pro/ufo/'
UFOS = (
    (UFOS_PATH + 'Proforma_Pro-Thin_MA16.ufo', 0), 
    (UFOS_PATH + 'Proforma_Pro-Regular_MA76.ufo', 0),
    (UFOS_PATH + 'Proforma_Pro-Bold_MA150.ufo', 0),
    (UFOS_PATH + 'Proforma_Pro-Black_MA220.ufo', 0),  
)
IMAGES_PATH = f'_imageTrain/'

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

def kernImage(imagePath, g1, g2, k, dx=0, italicOffset=0):
    if k < 0:
        kdx = -dx
    else:
        kdx = dx
                
    imagePath = imagePath + f'{g1.name}_{g2.name}_{kdx}.png'
    if os.path.exists(imagePath):
        return # Only make new ones

    path1 = glyphToBezierPath(g1)
    path2 = glyphToBezierPath(g2)

    #if w1 + w1 != w12:
    #    print(c1, c2, w1, w2, w1 + w2, w12, k)
    s = H / g1.font.info.unitsPerEm
    y = -g1.font.info.descender

    #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
    newDrawing()
    newPage(W, H)
    # Experimental: Try equalize left and right part of the image
    #rect(0, 0, W*1/6, H)
    #rect(W*5/6, 0, W*1/6, H)    
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

    #print('Save', imagePath)
    saveImage(imagePath)

def getImagesSubPath(imagesPath, name1, name2):
    imagesPathSub = imagesPath + name1 + '/'
    if not os.path.exists(imagesPathSub):
        os.system(f'mkdir {imagesPathSub}')
    #imagesPathSub += name2 + '/'
    #if not os.path.exists(imagesPathSub):
    #    os.system(f'mkdir {imagesPathSub}')
    #print(imagesPathSub)
    return imagesPathSub
    
def generateFamily(fontPath, italicOffset):
    
    f = RFont( fontPath, showInterface=False)
    imageName = fontPath.replace('.ufo','').split('/')[-1]
    imagesPath = IMAGES_PATH + f'{imageName}_{W}_{H}/'
    print('...', imagesPath)
        
    if not os.path.exists(IMAGES_PATH):
        os.system(f'mkdir {IMAGES_PATH}')
    if not os.path.exists(imagesPath):
        os.system(f'mkdir {imagesPath}')
    
    glyph2Group1 = {}
    glyph2Group2 = {}
    for groupName, group in f.groups.items():
        if 'kern1' in groupName:
            for gName in group:
                glyph2Group1[gName] = groupName
        elif 'kern2' in groupName:
            for gName in group:
                glyph2Group2[gName] = groupName
                    
    # Always include these pairs, even for kerning == 0
    alphaZero = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphaZero += alphaZero + alphaZero.lower()
    
    STEP = 2
    done = set()
    for c1 in alphaZero:
        gName1 = glyph2Group1.get(c1)
        if gName1 is not None:
            for c2 in alphaZero:
                imagesPathSub = getImagesSubPath(imagesPath, c1, c2) # Reduce the amount of images in one folder            
                gName2 = glyph2Group2.get(c2)
                if gName2 is not None:               
                    k = int(round(f.kerning.get((gName1, gName2), 0)))
                    if c1 in f and c2 in f:
                        #kernImage(imagesPathSub, f[c1], f[c2], k, 0, italicOffset=italicOffset) # Make sure to always create the k=0 image.
                        for dx in range(0, abs(k), STEP):
                            if c1 in f and c2 in f:
                                kernImage(imagesPathSub, f[c1], f[c2], k, dx, italicOffset=italicOffset)
                                done.add((c1, c2))

    if 1:
        # Now expand existing kerning groups
        for (name1, name2), k in f.kerning.items():
            k = int(round(k))
            if name1 in f: # Glyph, not a group
                group1 = [name1]
            elif name1 in f.groups:
                    group1 = f.groups[name1]
            else:
                print('### Not a group1', name1)
                continue
            if name2 in f:
                group2 = [name2]
            elif name2 in f.groups:
                group2 = f.groups[name2]
            else:
                print('### Not a group2', name2)
                continue
            for c1 in group1:
                for c2 in group2:
                    for dx in range(0, abs(k), STEP):
                        if c1 not in f or c2 not in f:
                            print('MISSING', c1, c2)

                        elif c1 in f and c2 in f and not (c1, c2) in done:
                            imagesPathSub = getImagesSubPath(imagesPath, gName1, gName2)
                            #print('====', gName1, gName2, dx)
                            kernImage(imagesPathSub, f[c1], f[c2], k, dx, italicOffset=italicOffset)
                            done.add((c1, c2))
    
    f.close()
                    
for fontPath, italicOffset in UFOS:
    print('===', fontPath)
    generateFamily(fontPath, italicOffset)
    