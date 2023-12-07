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

W, H = 32, 32
Y = H/4

UFOS_PATH1 = '/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade-Sans/ufo-frozen/'
UFOS_PATH2 = '/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade-Sans/ufo/'
UFOS_PATH3 = '/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade FROZEN PUBLISHED 2018-01-18/'
UFOS = (
    #UFOS_PATH1+'Upgrade_Frozen-Bold_Italic.ufo',    #UFOS_PATH1+'Upgrade_Frozen-Bold.ufo',    (UFOS_PATH1+'Upgrade_Frozen-Book_Italic.ufo', -40),     #UFOS_PATH1+'Upgrade_Frozen-Book.ufo',    #UFOS_PATH1+'Upgrade_Frozen-Light_Italic.ufo',    #UFOS_PATH1+'Upgrade_Frozen-Light.ufo',    (UFOS_PATH1+'Upgrade_Frozen-Medium_Italic.ufo', -50),    #UFOS_PATH1+'Upgrade_Frozen-Medium.ufo',    (UFOS_PATH1+'Upgrade_Frozen-Regular_Italic.ufo', -45),    #UFOS_PATH1+'Upgrade_Frozen-Regular.ufo',    #UFOS_PATH1+'Upgrade_Frozen-Semibold_Italic.ufo',
    #UFOS_PATH1+'Upgrade_Frozen-Semibold.ufo',    
)
XXX = (
    UFOS_PATH1+'Upgrade_Frozen-ExtraBlack_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraBlack.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraLight_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraLight.ufo',    UFOS_PATH1+'Upgrade_Frozen-Hairline_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Hairline.ufo', 
    UFOS_PATH2+'Upgrade-Semibold_Italic_140.ufo',    UFOS_PATH2+'Upgrade-Semibold_140.ufo',    UFOS_PATH2+'Upgrade-Regular_Italic_84.ufo',    UFOS_PATH2+'Upgrade-Regular_84.ufo',    UFOS_PATH2+'Upgrade-Light_Italic_32.ufo',    UFOS_PATH2+'Upgrade-Light_32.ufo',    UFOS_PATH2+'Upgrade-Black_Italic_212.ufo',    UFOS_PATH2+'Upgrade-Black_212.ufo',

    UFOS_PATH1+'Upgrade_Frozen-Semibold_Italic.ufo',
    UFOS_PATH1+'Upgrade_Frozen-Semibold.ufo',    UFOS_PATH1+'Upgrade_Frozen-Black_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Black.ufo',    UFOS_PATH1+'Upgrade_Frozen-Bold_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Bold.ufo',    UFOS_PATH1+'Upgrade_Frozen-Book_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Book.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraBlack_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraBlack.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraLight_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-ExtraLight.ufo',    UFOS_PATH1+'Upgrade_Frozen-Hairline_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Hairline.ufo',    UFOS_PATH1+'Upgrade_Frozen-Light_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Light.ufo',    UFOS_PATH1+'Upgrade_Frozen-Medium_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Medium.ufo',    UFOS_PATH1+'Upgrade_Frozen-Regular_Italic.ufo',    UFOS_PATH1+'Upgrade_Frozen-Regular.ufo',)
XXX = (
    UFOS_PATH1+'Upgrade-Black_Italic_212.ufo',
    #'Upgrade-Black_Condensed_196.ufo',
    #'Upgrade-Black_Condensed_Italic_196.ufo',
    #'Upgrade-Black_Extended_250.ufo',
    #'Upgrade-Black_Extended_Italic_250.ufo',
    
    #'Upgrade-Hairline_8.ufo',
    #'Upgrade-Hairline_Italic_8.ufo',
    #'Upgrade-Hairline_Condensed_8.ufo',
    #'Upgrade-Hairline_Condensed_Italic_8.ufo',
    #'Upgrade-Hairline_Extended_8.ufo',
    #'Upgrade-Hairline_Extended_Italic_8.ufo',
    
    UFOS_PATH1+'Upgrade-Light_32.ufo',
    UFOS_PATH1+'Upgrade-Light_Italic_32.ufo',
    #'Upgrade-Light_Condensed_31.ufo',
    #'Upgrade-Light_Condensed_Italic_31.ufo',
    #'Upgrade-Light_Extended_32.ufo',
    #'Upgrade-Light_Extended_Italic_32.ufo',
    
    UFOS_PATH1+'Upgrade-Regular_84.ufo',
    UFOS_PATH1+'Upgrade-Regular_Italic_84.ufo',
    #'Upgrade-Regular_Condensed_82.ufo',
    #'Upgrade-Regular_Condensed_Italic_82.ufo',
    #'Upgrade-Regular_Extended_86.ufo',
    #'Upgrade-Regular_Extended_Italic_86.ufo',
    
    UFOS_PATH1+'Upgrade-Semibold_140.ufo',
    UFOS_PATH1+'Upgrade-Semibold_Italic_140.ufo',
    #'Upgrade-Semibold_Condensed_136.ufo',
    #'Upgrade-Semibold_Condensed_Italic_136.ufo',
    #'Upgrade-Semibold_Extended_156.ufo',
    #'Upgrade-Semibold_Extended_Italic_156.ufo',
    
    #'Upgrade-UltraBlack_276.ufo',
    #'Upgrade-UltraBlack_Condensed_226.ufo',
    #'Upgrade-UltraBlack_Condensed_Italic_226.ufo',
    #'Upgrade-UltraBlack_Extended_414.ufo',
    #'Upgrade-UltraBlack_Extended_Italic_414.ufo',

    UFOS_PATH2+'Upgrade_Frozen-Bold_Italic.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Bold.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Book_Italic.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Book.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Medium_Italic.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Medium.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Regular_Italic.ufo',
    UFOS_PATH2+'Upgrade_Frozen-Regular.ufo',

)
UFOSXX = (
    'Upgrade-UltraBlack_276.ufo',
    'Upgrade-Black_Italic_212.ufo',
    'Upgrade-Hairline_8.ufo',
    'Upgrade-Hairline_Italic_8.ufo',
    'Upgrade-Light_32.ufo',
    'Upgrade-Light_Italic_32.ufo',
    'Upgrade-Regular_84.ufo',
    'Upgrade-Regular_Italic_84.ufo',
    'Upgrade-Semibold_140.ufo',
    'Upgrade-Semibold_Italic_140.ufo',

    #'Upgrade-Black_212.ufo',
    #'Upgrade-UltraBlack_Italic_276.ufo',
)
UFOSXX = (
    'Upgrade-Black_Italic.ufo',    'Upgrade-Black.ufo',    'Upgrade-Light_Italic.ufo',    'Upgrade-Light.ufo',    'Upgrade-Semibold_Italic.ufo',    'Upgrade-Semibold.ufo',
    'Upgrade-UltraBlack_Italic.ufo',    'Upgrade-UltraBlack.ufo',
)

IMAGES_PATH = '/Volumes/Archiv-T1/TYPETR-KernNet-TrainingImages-Italic-K=0/'

def kernImage(imagePath, g1, g2, k, dx=0, italicOffset=0):
    if k < 0:
        kdx = -dx
    else:
        kdx = dx
                
    imagePath = imagePath + f'{g1.name}_{g2.name}_{kdx}.png'
    if os.path.exists(imagePath):
        return # Only make new ones

    im1 = g1.getRepresentation("defconAppKit.NSBezierPath")
    im2 = g2.getRepresentation("defconAppKit.NSBezierPath")
    #if w1 + w1 != w12:
    #    print(c1, c2, w1, w2, w1 + w2, w12, k)
    s = W / g1.font.info.unitsPerEm
    y = -g1.font.info.descender

    #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
    newDrawing()
    newPage(W, H)
    # Experimental: Try equalize left and right part of the image
    #rect(0, 0, W*1/6, H)
    #rect(W*5/6, 0, W*1/6, H)    
    scale(s, s)
    save()
    translate(W/s/2-(k-kdx)/2 - g1.width + italicOffset, y)
    drawPath(im1)
    restore()
    translate(W/s/2+(k-kdx)/2 + italicOffset, y)
    drawPath(im2)
    saveImage(imagePath)

def getImagesSubPath(imagesPath, name):
    imagesPathSub = imagesPath + name + '/'
    if not os.path.exists(imagesPathSub):
        os.system(f'mkdir {imagesPathSub}')
    return imagesPathSub
    
def generateFamily(fontPath, italicOffset):
    
    f = OpenFont( fontPath, showInterface=False)
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
    
    for c1 in alphaZero:

        imagesPathSub = getImagesSubPath(imagesPath, c1) # Reduce the amount of images in one folder            
        gName1 = glyph2Group1.get(c1)
        if gName1 is not None:
            for c2 in alphaZero:
                gName2 = glyph2Group2.get(c2)
                if gName2 is not None:
                    step = 4               
                    k = int(round(f.kerning.get((gName1, gName2), 0)))
                    if c1 in f and c2 in f:
                        kernImage(imagesPathSub, f[c1], f[c2], k, 0, italicOffset=italicOffset) # Make sure to always create the k=0 image.
                        for dx in range(0, abs(k), step):
                            if c1 in f and c2 in f:
                                kernImage(imagesPathSub, f[c1], f[c2], k, dx, italicOffset=italicOffset)

    # Now expand existing kerning groups
    for (name1, name2), k in f.kerning.items():
        imagesPathSub = getImagesSubPath(imagesPath, name1)
        k = int(round(k))
        if name1 in f: # Glyph, not a group
            group1 = [name1]
        elif name1 in f.groups:
                group1 = f.groups[name1]
        else:
            continue
        if name2 in f:
            group2 = [name2]
        elif name2 in f.groups:
            group2 = f.groups[name2]
        else:
            continue
        for gName1 in group1:
            for gName2 in group2:
                step = 8               
                for dx in range(0, abs(k), step):
                    if gName1 in f and gName2 in f:
                        kernImage(imagesPathSub, f[gName1], f[gName2], k, dx, italicOffset=italicOffset)
    
    f.close()
                    
for fontPath, italicOffset in UFOS:
    print('===', fontPath)
    generateFamily(fontPath, italicOffset)
    