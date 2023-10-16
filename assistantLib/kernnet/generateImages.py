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

if 0:
    for name in installedFonts():
        if 'Lucida' in name:
            print(name)

W, H = 32, 32
Y = H/4
FONTS = (
    '188Sans-Oblique',
    '188Sans-CondensedThinOblique',
    '188Sans-ExtendedBlackOblique',

    'Avenir-BookOblique', 
    'Avenir-HeavyOblique', 
    'Avenir-LightOblique', 
    'Avenir-MediumOblique', 
    'Avenir-Oblique', 
    'AvenirNext-BoldItalic', 
    'AvenirNext-DemiBoldItalic', 
    'AvenirNext-Italic',
    'AvenirNext-MediumItalic',
    'AvenirNextCondensed-BoldItalic',
    'AvenirNextCondensed-DemiBoldItalic', 
    'AvenirNextCondensed-Italic',
    'AvenirNextCondensed-MediumItalic',
         
    'LucidaBright-Italic',
    'LucidaSans-DemiItalic',
    'LucidaSans-Italic',
    
    'HelveticaNeue-Italic',
    'Helvetica-BoldOblique',
    'Helvetica-LightOblique',
    'HelveticaNeue-BoldItalic',
    'HelveticaNeue-LightItalic',
    'HelveticaNeue-MediumItalic',
    'HelveticaNeue-ThinItalic',

    'Upgrade-BoldItalic',
    'Upgrade-BookItalic',
    'Upgrade-Italic',
    'Upgrade-ExtraBlackItalic',
    'Upgrade-ExtraLightItalic',
    'Upgrade-LightItalic',
    'Upgrade-MediumItalic', 
    'Upgrade-SemiboldItalic', 
)
IMAGE_PATH = '_imageTrainSansItalic/'

def generateFamily(fontName):
    
    path = IMAGE_PATH + f'{fontName}_{W}_{H}/'
    print('...', path)

    if not os.path.exists(IMAGE_PATH):
        os.system(f'mkdir {IMAGE_PATH}')
    if not os.path.exists(path):
        os.system(f'mkdir {path}')

    for uni1 in range(33, 512):
        for uni2 in range(33, 512):
            c1 = chr(uni1)
            c2 = chr(uni2)  

            s1 = FormattedString(c1, font=fontName, fontSize=H, fill=0)
            s2 = FormattedString(c2, font=fontName, fontSize=H, fill=0)
            tw1, _ = textSize(s1)
            tw2, _ = textSize(s2)
            if tw1 and tw2:
                w1 = int(round(tw1 * 1000/H))
                w2 = int(round(tw2 * 1000/H))
                s12 = s1 + s2
                w12, _ = textSize(s1 + s2)
                w12 = int(round(w12 * 1000/H))
                k = w12 - (w1 + w2)
                #if w1 + w1 != w12:
                #    print(c1, c2, w1, w2, w1 + w2, w12, k)
                imagePath = path + f'{uni1}_{uni2}_{k}.png'
                if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
                    newDrawing()
                    newPage(W, H)
                    text(s1, (W/2 - tw1, Y))
                    text(s2, (W/2, Y))
                    saveImage(imagePath)
                    #print(s1, s2, k)
                    
for fontName in FONTS:
    generateFamily(fontName)

    