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
from fontTools.ttLib import TTFont

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
        if 'Upgrade' in name:
            print(name)
    xx = dd


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
    'Upgrade-Black',
    'Upgrade-BlackItalic',
    'Upgrade-Bold',
    'Upgrade-Book',
    'Upgrade-Cover',
    'Upgrade-ExtraBlack',
    'Upgrade-ExtraLight',
    'Upgrade-Hairline',
    'Upgrade-HairlineItalic',
    'Upgrade-Light',
    'Upgrade-Medium',
    'Upgrade-Normal',
    'Upgrade-Regular',
    'Upgrade-Semibold',
    'Upgrade-Standard',
    'Upgrade-Thin',
    'Upgrade-ThinItalic',
    'Upgrade-UltraBlack',
    'Upgrade-UltraBlackItalic',

)
FONT_PATH = '/Library/Fonts/'
FONTS = (
    'Upgrade_CG-Bold.otf',
    'Upgrade_CG-Book.otf',
    'Upgrade_CG-Cover.otf',
    'Upgrade_CG-Light.otf',
    'Upgrade_CG-Medium.otf',
    'Upgrade_CG-Normal.otf',
    'Upgrade_CG-Regular.otf',
    'Upgrade_CG-Semibold.otf',
    'Upgrade_CG-Standard.otf',
    'Upgrade_Try-Black_Italic.ttf',
    'Upgrade_Try-Black.ttf',
    'Upgrade_Try-Bold_Italic.ttf',
    'Upgrade_Try-Bold.ttf',
    'Upgrade_Try-Book_Italic.ttf',
    'Upgrade_Try-Book.ttf',
    'Upgrade_Try-ExtraBlack_Italic.ttf',
    'Upgrade_Try-ExtraBlack.ttf',
    'Upgrade_Try-ExtraLight_Italic.ttf',
    'Upgrade_Try-ExtraLight.ttf',
    'Upgrade_Try-Hairline_Italic.ttf',
    'Upgrade_Try-Hairline.ttf',
    'Upgrade_Try-Italic.ttf',
    'Upgrade_Try-Light_Italic.ttf',
    'Upgrade_Try-Light.ttf',
    'Upgrade_Try-Medium_Italic.ttf',
    'Upgrade_Try-Medium.ttf',
    'Upgrade_Try-Regular.ttf',
    'Upgrade_Try-Semibold_Italic.ttf',
    'Upgrade_Try-Semibold.ttf',
    'Upgrade_Try-Semibook_Italic.ttf',
    'Upgrade_Try-Semibook.ttf',
    'Upgrade_Try-Semilight_Italic.ttf',
    'Upgrade_Try-Semilight.ttf',
    'Upgrade_Try-Semimedium_Italic.ttf',
    'Upgrade_Try-Semimedium.ttf',
    'Upgrade_Try-Thin_Italic.ttf',
    'Upgrade_Try-Thin.ttf',
    'Upgrade_Try-UltraBlack_Italic.ttf',
    'Upgrade_Try-UltraBlack.ttf',
    'Upgrade-Black_CG.otf',
    'Upgrade-Black_Italic.otf',
    'Upgrade-Black.otf',
    'Upgrade-Bold_Italic.otf',
    'Upgrade-Bold.otf',
    'Upgrade-Book_Italic.otf',
    'Upgrade-Book.otf',
    'Upgrade-ExtraBlack_Italic.otf',
    'Upgrade-ExtraBlack.otf',
    'Upgrade-ExtraLight.otf',
    'Upgrade-Hairline_CG.otf',
    'Upgrade-Hairline_Italic.otf',
    'Upgrade-Hairline.otf',
    'Upgrade-Italic.otf',
    'Upgrade-Light_CG.otf',
    'Upgrade-Light_Italic.otf',
    'Upgrade-Light.otf',
    'Upgrade-Medium_Italic.otf',
    'Upgrade-Medium.otf',
    'Upgrade-Regular_CG.otf',
    'Upgrade-Regular.otf',
    'Upgrade-Semibold_CG.otf',
    'Upgrade-Semibold_Italic.otf',
    'Upgrade-Semibold.otf',
    'Upgrade-Thin_Italic.otf',
    'Upgrade-Thin.otf',
    'Upgrade-UltraBlack_CG.otf',
    'Upgrade-UltraBlack_Italic.otf',
    'Upgrade-UltraBlack.otf',
)
IMAGE_PATH = '_imageTrainSansItalic/'

def generateFamily(fontName):
    
    imageName = fontName.replace('.ttf','').replace('.otf','')
    imagesPath = IMAGE_PATH + f'{imageName}_{W}_{H}/'
    print('...', imagesPath)
        
    if not os.path.exists(IMAGE_PATH):
        os.system(f'mkdir {IMAGE_PATH}')
    if not os.path.exists(imagesPath):
        os.system(f'mkdir {imagesPath}')

    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha += alpha + alpha.lower() + '™()[]{}%.,\\/“”‘’0123456789'
    
    for uni1 in range(33, 256):
        for uni2 in range(33, 256):
            c1 = chr(uni1)
            c2 = chr(uni2)  

            s1 = FormattedString(c1, font=FONT_PATH+fontName, fontSize=H, fill=0)
            s2 = FormattedString(c2, font=FONT_PATH+fontName, fontSize=H, fill=0)
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
                imagePath = imagesPath + f'{uni1}_{uni2}_{k}.png'
                #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
                if k > 4 or (c1 in alpha and c2 in alpha): 
                    newDrawing()
                    newPage(W, H)
                    text(s1, (W/2 - tw1, Y))
                    text(s2, (W/2, Y))
                    saveImage(imagePath)
                    #print(s1, s2, k)
                    
for fontName in FONTS:
    if 'Upgrade' in fontName:
        generateFamily(fontName)
