# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     floqstate.py
#
from tnbits.constants import Constants

class FloqState(object):
    # The FloqState is the root class for both Floq and FloqMeme classes.
    #    Attributes
    #    self.parent        Get/set the parent of this Floq or FloqMeme (stored as weakref)
    #
    C = Constants 
    
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

    @classmethod
    def getAllStyles(cls):
        # Answer all open style/fonts. This is a centralized method, as we may redirect it for online usage.
        return [] #AllFonts()

    getAllFonts = getAllStyles

    @classmethod
    def getFontName(cls, font):
        # Answer the font style name. If it does not exist, set it to 'Regular'
        if not font.info.styleName: # In case there is no style name, force it into.
                font.info.styleName = 'Regular'
        return font.info.styleName
    
    @classmethod
    def setFontName(cls, font, styleName):
        font.info.styleName = styleName
        
    @classmethod
    def getFontFamilyName(cls, font):
        # Answer the font family name. If it does not exist, set it to 'Untitled'
        if not font.info.familyName:
            font.info.familyName = 'Untitled' # In case there is no name, force it into.
        return font.info.familyName

    @classmethod
    def setFontFamilyName(cls, font, familyName):
        font.info.familyName = familyName
        
