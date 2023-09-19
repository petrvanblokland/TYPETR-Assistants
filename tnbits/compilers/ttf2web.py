# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            ttf2web.py
import re, os, shutil, sys, getopt, zlib, gzip, struct, tempfile, math, random
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import AbstractPen, BasePen, _TestPen
from tnbits.base.future import chr

class SVGPen(BasePen):
    def __init__(self,*arg,**args):
        self._svg = []
        BasePen.__init__(self,*arg,**args)

    def _moveTo(self, pt):
        self._svg.append("M %i %i" % (pt[0], pt[1]))

    def _lineTo(self, pt):
        self._svg.append("L %i %i" % (pt[0], pt[1]))

    def _curveToOne(self, bcp1, bcp2, pt):
        self._svg.append("C %i %i %i %i %i %i" % (bcp1[0], bcp1[1], bcp2[0], bcp2[1], pt[0], pt[1]))

    def _closePath(self):
        self._svg.append("Z")

    def getSVGPath(self):
        return ' '.join(self._svg)



class TTF2WEB:

    CHARSETS = {
        # Latin-1 / 1252
        0 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 8364, 8218, 402, 8222, 8230, 8224, 8225, 710, 8240, 352, 8249, 338, 381, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 732, 8482, 353, 8250, 339, 382, 376, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 0xFB00, 0xFB01, 0xFB02, 0xFB03, 0xFB04, 0xFB05, 0xFB06],

        # Central Europe / 1250
        1 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 8364, 8218, 8222, 8230, 8224, 8225, 8240, 352, 8249, 346, 356, 381, 377, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 8482, 353, 8250, 347, 357, 382, 378, 160, 711, 728, 321, 164, 260, 166, 167, 168, 169, 350, 171, 172, 173, 174, 379, 176, 177, 731, 322, 180, 181, 182, 183, 184, 261, 351, 187, 317, 733, 318, 380, 340, 193, 194, 258, 196, 313, 262, 199, 268, 201, 280, 203, 282, 205, 206, 270, 272, 323, 327, 211, 212, 336, 214, 215, 344, 366, 218, 368, 220, 221, 354, 223, 341, 225, 226, 259, 228, 314, 263, 231, 269, 233, 281, 235, 283, 237, 238, 271, 273, 324, 328, 243, 244, 337, 246, 247, 345, 367, 250, 369, 252, 253, 355, 729],

        # Cyrillic / 1251
        2 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 1026, 1027, 8218, 1107, 8222, 8230, 8224, 8225, 8364, 8240, 1033, 8249, 1034, 1036, 1035, 1039, 1106, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 8482, 1113, 8250, 1114, 1116, 1115, 1119, 160, 1038, 1118, 1032, 164, 1168, 166, 167, 1025, 169, 1028, 171, 172, 173, 174, 1031, 176, 177, 1030, 1110, 1169, 181, 182, 183, 1105, 8470, 1108, 187, 1112, 1029, 1109, 1111, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103],

        # Greek / 1253
        3 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 8364, 8218, 402, 8222, 8230, 8224, 8225, 8240, 8249, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 8482, 8250, 160, 901, 902, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 8213, 176, 177, 178, 179, 900, 181, 182, 183, 904, 905, 906, 187, 908, 189, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974],

        # Turkish / 1254
        4 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 8364, 8218, 402, 8222, 8230, 8224, 8225, 710, 8240, 352, 8249, 338, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 732, 8482, 353, 8250, 339, 376, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 286, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 304, 350, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 287, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 305, 351, 255],

         # Baltic / 1257
        7 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 8364, 8218, 8222, 8230, 8224, 8225, 8240, 8249, 168, 711, 184, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 8482, 8250, 175, 731, 160, 162, 163, 164, 166, 167, 216, 169, 342, 171, 172, 173, 174, 198, 176, 177, 178, 179, 180, 181, 182, 183, 248, 185, 343, 187, 188, 189, 190, 230, 260, 302, 256, 262, 196, 197, 280, 274, 268, 201, 377, 278, 290, 310, 298, 315, 352, 323, 325, 211, 332, 213, 214, 215, 370, 321, 346, 362, 220, 379, 381, 223, 261, 303, 257, 263, 228, 229, 281, 275, 269, 233, 378, 279, 291, 311, 299, 316, 353, 324, 326, 243, 333, 245, 246, 247, 371, 322, 347, 363, 252, 380, 382, 729],
    }


    CHARSET_FULL = 'full'
    CHARSET_CUSTOM = 'custom'

    #add lines to this when we add new levels of font obfuscation
    FONTMUNGE_VERSION = (
        'Copy original file; manual EOT/WOFF conversion',
        'Zero name fields',
        'Rewrite glyph names',
        'Fix PS/CFF name agreement for Safari 5.1',
        'Leave font name in license name field',
        'Auto-fix full-name field to be family + style',
    )

    @classmethod
    def obfuscationVersion(cls):
        return len(cls.FONTMUNGE_VERSION)


    TTF = None
    OTF = None

    TTF_FIELDS = {
        'copyright': 0,
        'familyname': 1,
        'stylename': 2,
        'fullname': 4,
        'family': 1,
        'style': 2,
        'full': 4,
        'version': 5,
        'psname': 6,
        'trademark': 7,
        'manufacturer': 8,
        'foundry': 8,
        'designer': 9,
        'description': 10,
        'vendorurl': 11,
        'designerurl': 12,
        'license': 13,
        'licenseurl': 14,

        'name': (
            # PlatformID, EncodingID
            # http://www.microsoft.com/typography/otspec/name.htm
            (3,1), #windows, unicode
            (1,0), #mac,roman
        ),
        'cmap': (
                #PlatformID, EncodingID
                # http://www.microsoft.com/typography/otspec/name.htm
                (3,10), #Windows, Unicode SMP
                (3,1), #Windows, Unicode BMP
                (3,0), #Windows, Symbol
                (0,3), #Unicode, BMP
                )
    }

    HAS_BEEN_SUBSET = False
    fontWeight = 'normal'

    def nameRecordIsUnicode(self, namerecord):
        return (namerecord.platformID == 0 or (namerecord.platformID == 3 and namerecord.platEncID in (0, 1, 10)))

    def __init__(self,otf,ttf=None):
        import StringIO
        if isinstance(otf,TTFont):
            self.OTF = otf
            self.TTF = ttf
        elif isinstance(otf, StringIO.StringIO):
            self.OTF = TTFont(otf,recalcBBoxes=False)
            self.TTF = ttf and TTFont(ttf,recalcBBoxes=False)
        else:
            self.OTF = TTFont(otf,recalcBBoxes=False)
            if ttf:
                self.TTF = TTFont(ttf,recalcBBoxes=False)

        if not self.TTF:
            self.TTF = self.OTF

        #older IE requires webfonts to have installable embedding, so just do this for all
        # on second thought, this restriction only applies to raw TTF fonts, and causes issues with other Microsoft stuff, so forget it
        #self.TTF['OS/2'].fsType=0

        #EOT doesn't work if name 4 (full name) doesn't start with name 1 (family)
        # so, just always set the full name to be family + style (unless style is Regular) to avoid issues
        fonts = [ self.TTF ]
        if self.TTF != self.OTF:
            fonts.append(self.OTF)
        for font in fonts:
            family = self.getTTFNameField('family', font)
            style = self.getTTFNameField('style', font)

            for namerecord in font['name'].names:
                if namerecord.nameID == 4:
                    namerecord.string = family
                    if style != 'Regular':
                        namerecord.string += ' ' + style

                    #need to encode the name string differently depending on unicode-ness of the platform/encoding
                    # this criteria from fontTools/ttLib/tables/_n_a_m_e

                    namerecord.string = namerecord.string.encode('utf_16_be' if self.nameRecordIsUnicode(namerecord) else 'latin1')


    STARTSWITHLETTER = re.compile(r'^\w',re.UNICODE)
    @classmethod
    def findFontsInDir(cls,dir,ext,depth=0,startwithletter=False):
        result = []

        if depth == 0:
            ext = ext.lower()
        elif depth > 20:
            print("Stopping directory recursion at depth 20.")
            return result

        if startwithletter and depth > 0 and not cls.STARTSWITHLETTER.search(os.path.basename(dir)):
            return result

        if os.path.isdir(dir) and not dir.lower().endswith('.ufo'):
            for file in os.listdir(dir):
                result.extend(cls.findFontsInDir(dir.rstrip(r'\/') + '/' + file, ext, depth+1, startwithletter))
        elif dir.lower().endswith('.' + ext):
            result.append(dir)

        return result

    def getTTFNameField(self,nameid,font=None):
        if not font:
            font = self.OTF

        if nameid in self.TTF_FIELDS: #convert friendly name to ID
            nameid = self.TTF_FIELDS[nameid]

        for args in self.TTF_FIELDS['name']:
            name = font['name'].getName(nameid,*args)

            if name is not None:
                return name.string.decode('utf_16_be' if self.nameRecordIsUnicode(name) else 'ascii')

        return u''

    def getTTFCmap(self,font=None):
        if not font:
            font = self.OTF
        for args in self.TTF_FIELDS['cmap']:
            cmap = font['cmap'].getcmap(*args)

            if cmap is not None:
                return cmap.cmap

        raise Exception('cmap not found')


    def getTTFOTFeatureTags(self,font=None):
        if not font:
            font = self.OTF
        features = set()

        if 'GSUB' in font:

            for feat in font['GSUB'].table.FeatureList.FeatureRecord:

                if feat.FeatureTag not in self.OPENTYPE_FEATURE_NAMES:
                    continue

                features.add(feat.FeatureTag)

        return features


    def randomBase62(self,length=8,base=62):
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[:max(base,2)]
        return ''.join([random.choice(chars) for i in range(length)])

    def setFontWeight(self,weight):
        self.fontWeight = weight
        self.TTF['OS/2'].usWeightClass = int(weight)
        if self.TTF != self.OTF:
            self.OTF['OS/2'].usWeightClass = int(weight)

    def mungeNameFields(self,name="Unlicensed Font",url="http://webtype.com/"):
        """
        `mungeNameFields` overwrites every name record in the font with a generic
        Webtype string or appropriate non-font-specific value.
        """

        from hashlib import md5

        uniqueid = u"Munged-" + self.randomBase62(length=10)

        '''
        'copyright': 0,
        'familyname': 1,
        'stylename': 2,
        'fullname': 4,
        'family': 1,
        'style': 2,
        'full': 4,
        'version': 5,
        'psname': 6,
        'trademark': 7,
        'manufacturer': 8,
        'foundry': 8,
        'designer': 9,
        'description': 10,
        'vendorurl': 11,
        'designerurl': 12,
        'license': 13,
        'licenseurl': 14,
        '''

        #zero out various TTF name fields
        licensename = self.getTTFNameField('psname')
        fonts = [ self.TTF ]
        if self.TTF != self.OTF:
            fonts.append(self.OTF)
        for font in fonts:
            for namerecord in font['name'].names:
                oldvalue = namerecord.string
                if namerecord.nameID in (1,4,8,9,16,3):
                    #names to zero out to discourage desktop installation
                    namerecord.string = name or uniqueid #some platforms don't like empty names
                elif namerecord.nameID == 6: #PSName
                    #psname must match cff table font name or OS X font book will flag the font as invalid and it won't work in Safari 5.1
                    namerecord.string = uniqueid
                    if 'CFF ' in font:
                        font['CFF '].cff.fontNames[0] = namerecord.string
                elif namerecord.nameID in (0,7,10,):
                    #copyright, trademark, more extended fields
                    namerecord.string = "Web use only; not licensed for further use or distribution by website users."
                elif namerecord.nameID in (2,17):
                    #style name
                    namerecord.string = u"Regular"
                elif namerecord.nameID==5:
                    #version
                    #namerecord.string = u"Version 1.{0}".format(len(self.FONTMUNGE_VERSION))
                    # UPDATE 2014-09 leave version untouched
                    pass
                elif namerecord.nameID == 13:
                    #license -- tack psname on beginning so that we can identify the font
                    namerecord.string = u"{0} licensed for web use only".format(licensename)
                elif namerecord.nameID in (11,12,14):
                    #URLs
                    namerecord.string = url
                else:
                    namerecord.string = u""

                #need to encode the name string differently depending on unicode-ness of the platform/encoding
                # this criteria from fontTools/ttLib/tables/_n_a_m_e

                namerecord.string = namerecord.string.encode('utf_16_be' if self.nameRecordIsUnicode(namerecord) else 'latin1')


    def mungeGlyphNames(self):
        """
        `mungeGlyphNames` overwrites all the glyph names in the font with generaic "gXXX" values.
        Of course the cmap must still identify most of the glyphs, but at least it makes it slightly harder.
        """
        digits = int(math.ceil(math.log10(len(self.TTF.getGlyphOrder()))))
        self.TTF.setGlyphOrder(["g%.{0}d".format(digits) % i for i in range(len(self.TTF.getGlyphOrder()))])
        if self.OTF != self.TTF:
            digits = int(math.ceil(math.log10(len(self.OTF.getGlyphOrder()))))
            self.OTF.setGlyphOrder(["g%.{0}d".format(digits) % i for i in range(len(self.OTF.getGlyphOrder()))])

    def generateSignature(self):
        """
        `mungeDSIG` zaps the current digitial signature and replaces it with
        a generic Type Network one, according to the rules at http://www.microsoft.com/typography/otspec/dsig.htm
        """

        """
        from: http://www.microsoft.com/typography/otspec/dsig.htm

        Format 1: For whole fonts, with either TrueType outlines and/or CFF data
        PKCS#7 or PKCS#9. The signed content digest is created as follows:
        1 If there is an existing DSIG table in the font,
            1 Remove DSIG table from font.
            2 Remove DSIG table entry from sfnt Table Directory.
            3 Adjust table offsets as necessary.
            4 Zero out the file checksum in the head table.
            5 Add the usFlag (reserved, set at 1 for now) to the stream of bytes
        2 Hash the full stream of bytes using a secure one-way hash (such as MD5) to create the content digest.
        3 Create the PKCS#7 signature block using the content digest.
        4 Create a new DSIG table containing the signature block.
        5 Add the DSIG table to the font, adjusting table offsets as necessary.
        6 Add a DSIG table entry to the sfnt Table Directory.
        7 Recalculate the checksum in the head table.

        Prior to signing a font file, ensure that all the following attributes are true.
            The magic number in the head table is correct.
            Given the number of tables value in the offset table, the other values in the offset table are consistent.
            The tags of the tables are ordered alphabetically and there are no duplicate tags.
            The offset of each table is a multiple of 4. (That is, tables are long word aligned.)
            The first actual table in the file comes immediately after the directory of tables.
            If the tables are sorted by offset, then for all tables i (where index 0 means the the table with the smallest offset), Offset[i] + Length[i] <= Offset[i+1] and Offset[i] + Length[i] >= Offset[i+1] - 3. In other words, the tables do not overlap, and there are at most 3 bytes of padding between tables.
            The pad bytes between tables are all zeros.
            The offset of the last table in the file plus its length is not greater than the size of the file.
            The checksums of all tables are correct.
            The head table's checkSumAdjustment field is correct.
        """

        #TODO: actually do all of the above

        #for now, just kill the old DSIG table because it is made invalid by all the obfuscation anyway
        if 'DSIG' in self.TTF:
            del(self.TTF['DSIG'])

        if self.TTF != self.OTF and 'DSIG' in self.OTF:
            del(self.OTF['DSIG'])

    @classmethod
    def subsetTTFont(cls,ttfont,chars):
        temp = cls(ttfont)
        temp.subsetGlyphs(chars)
        return temp.TTF

    def subsetGlyphs(self,exact=None):
        from fontTools.ttLib.tables._g_l_y_f import Glyph

        fonts = [ self.TTF ]
        if self.TTF != self.OTF:
            fonts.append(self.OTF)

        for font in fonts:
            cmap = self.getTTFCmap(font)

            #OKAY! Now we have a list of unicodes to get rid of

            cffstrings = {}
            if 'CFF ' in font:
                temp = font['CFF '].cff.values()[0].CharStrings
                cffstrings = dict([(k,temp[k]) for k in temp.keys()])

            glyphs2keep = set([cmap[uni] for uni in cmap.keys() if chr(uni) in exact])

            if 'glyf' in font:
                for glyphname in [g for g in glyphs2keep if g in font['glyf']]:
                    glyph = font['glyf'][glyphname]
                    if glyph.isComposite and hasattr(glyph,'components'):
                        for c in glyph.components:
                            glyphs2keep.add(c.glyphName)

            #keep ligatures
            if 'GSUB' in font:

                #all of the glyph mappings are done by glyph name, so we need to map glyph names back to unicodes
                reverse_cmap = {}

                for uni in sorted(cmap.keys(),reverse=True):
                    reverse_cmap[cmap[uni]] = chr(uni)

    #            for feat in [x for x in font['GSUB'].table.FeatureList.FeatureRecord if x.FeatureTag in ('liga','smcp','salt')]:
                for feat in font['GSUB'].table.FeatureList.FeatureRecord:
                    for lindex in feat.Feature.LookupListIndex:
                        lookup = font['GSUB'].table.LookupList.Lookup[lindex]

                        for subtable in lookup.SubTable:
                            if hasattr(subtable,'mapping'):
                                for k,v in subtable.mapping.items():
                                    if k in reverse_cmap and reverse_cmap[k] in exact:
                                        glyphs2keep.add(v)

                            if hasattr(subtable,'alternates'):
                                for fromglyph,toglyphs in subtable.alternates.items():
                                    if fromglyph in reverse_cmap and reverse_cmap[fromglyph] in exact:
                                        glyphs2keep.update(toglyphs)

                            elif hasattr(subtable,'ligatures') or (hasattr(subtable,'ExtSubTable') and hasattr(subtable.ExtSubTable,'ligatures')):
                                ligatures = subtable.ligatures if hasattr(subtable,'ligatures') else subtable.ExtSubTable.ligatures
                                for first,others in ligatures.items():
                                    for lig in others:
                                        for fromglyph in set([first] + lig.Component):
                                            if fromglyph in reverse_cmap and reverse_cmap[fromglyph] in exact and lig.LigGlyph not in glyphs2keep:
                                                glyphs2keep.add(lig.LigGlyph)


            for glyphname in font.getGlyphOrder():
                #deleting glyphs causes all kinds of issues, so just zero the glyph data
                if glyphname not in glyphs2keep:
                    self.HAS_BEEN_SUBSET = True
                    if 'glyf' in font and glyphname in font['glyf']:
                        font['glyf'][glyphname] = Glyph()
                    elif 'CFF ' in font and glyphname in cffstrings:
                        cffstrings[glyphname].setBytecode("\x0e")

    def createTTF(self,dest):
        # actually use the OTF for this
        self.OTF.save(dest)

    def createEOT(self,dest,compress=False):
        #EOT

        #CFF based EOTs don't work, so don't bother
        #if 'CFF ' in self.TTF:
        #    return

        tempttf = tempfile.NamedTemporaryFile()
        self.TTF.save(tempttf)

        if compress:
            #using Google's sfnttool for now
            tempttf.seek(0,2)
            absfile = dest #absfile = dest if dest.startswith('/') else os.getcwd() + '/' + dest
            cmd = "java -jar /home/chris/dev/sfntly/java/dist/tools/sfnttool/sfnttool.jar -e -x {0} {1}".format(tempttf.name,absfile)
            print(cmd, tempttf.tell())
            os.system(cmd)
            tempttf.close()
            return

        eot = open(dest,"wb")

        # EOT format 20001 (same as used by ttf2eot)
        # http://www.w3.org/Submission/EOT/#Version21

        def write(format,*args):
            #EOT is little-endian, whereas OT is big
            if format[0] not in ('<','>'):
                format = '<' + format

            data = struct.pack(format,*args)
            eot.write(data)

        flags = 0

        if self.HAS_BEEN_SUBSET:
            flags |= 1

        if compress:
            flags |= 4

        write('L',0) #EOT total size placeholder
        write('L',0) #FontDataSize placeholder
        write('L',0x00020001) #EOT version
        write('L',flags) #Processing flags (web object)
        write('10x') #panose numbers, all 0
        write('B',1) #charset, 0x01 == default
        write('B',self.TTF['OS/2'].fsSelection & 1) #italic; this has to actually match the TTF
        write('L',self.TTF['OS/2'].usWeightClass) #weight; this has to actually match the TTF
        write('H',0x00) #fsType. print(& preview, editable, or none?)
        write('H',0x504C) #magic number for EOT
        for a in ('ulUnicodeRange1','ulUnicodeRange2','ulUnicodeRange3','ulUnicodeRange4','ulCodePageRange1','ulCodePageRange2'):
            write('L',getattr(self.TTF['OS/2'],a) if hasattr(self.TTF['OS/2'],a) else 0)
        #write('6L',0,0,0,0,0,0) #unicode and codepage ranges zeroed
        write('L',self.TTF['head'].checkSumAdjustment)
        write('4L',0,0,0,0) #reserved

        #all these string lengths below are doubled due to UTF-16 representation
        family = self.getTTFNameField('familyname',self.TTF)
        style = self.getTTFNameField('stylename',self.TTF)
        fullname = self.getTTFNameField('fullname',self.TTF)
        version = self.getTTFNameField('version',self.TTF)
        urls = []

        family = family.encode("utf_16_le")
        style = style.encode("utf_16_le")
        fullname = fullname.encode("utf_16_le")
        version = version.encode("utf_16_le")
        root = "\0".join(urls).encode("utf_16_le")

        write('H',0) #padding1
        write('H',len(family)) #family name length
        write('{0}s'.format(len(family)),family) #family name
        write('H',0) #padding2
        write('H',len(style)) #style name length
        write('{0}s'.format(len(style)),style) #style name
        write('H',0) #padding3
        write('H',len(fullname)) #full name length
        write('{0}s'.format(len(fullname)),fullname) #fullname name
        write('H',0) #padding4
        write('H',len(version)) #version name length
        write('{0}s'.format(len(version)),version) #version name
        write('H',0) #padding5
        write('H',len(root)) #root name length (allowed URLs)
        write('{0}s'.format(len(root)),root) #root name

        #END OF HEADER

        if compress:
            # Monotype "MicroType Express" compression spec
            # http://www.w3.org/Submission/MTX/

            # hacked above with Google's sfnttool
            pass

        else:
            #append the whole TTF file to the EOT
            tempttf.seek(0)
            while True:
                chunk = tempttf.read(16384)
                if len(chunk) == 0:
                    break
                eot.write(chunk)
            ttfsize = tempttf.tell()
            eot.seek(4)
            write('L',ttfsize)
            tempttf.close()

        #update total size
        eot.seek(0,2)
        fullsize = eot.tell()
        eot.seek(0)
        write('L',fullsize)

        eot.close()


    def createWOFF(self,dest,meta=""):
        #WOFF
        from fontTools.ttLib.sfnt import calcChecksum

        woff = open(dest,"w+b")

        # woff format
        # http://people.mozilla.com/~jkew/woff/woff-spec-latest.html

        def write(format,*args,**kwargs):
            #woff is big-endian, as is OT
            if format[0] not in ('<','>'):
                format = '>' + format

            data = struct.pack(format,*args)
            woff.write(data)


        tabletags = [k for k in self.OTF.keys() if len(k)==4 and k != 'DSIG']
        numtables = len(tabletags)

        flavor = 0x4F54544F if 'CFF ' in tabletags else 0x00010000

        #WOFF HEADER
        write('L',0x774F4646) #0 signature 'wOFF'
        write('L',flavor) #4 flavor: 0x00010000 for TTF, 0x4F54544F for CFF
        write('L',0) #8 total size placeholder
        write('H',numtables) #12 number of tables
        write('H',0) #14 reserved
        write('L',0) #16 total uncompressed original font size placeholder
        write('H',1) #20 major version (arbitrary)
        write('H',0) #22 minor version (arbitrary)
        write('L',0) #24 metadata offset placeholder (0 if none)
        write('L',0) #28 metadata length placeholder
        write('L',0) #32 metadata original length placeholder
        write('L',0) #36 private data offset placeholder (0 if none)
        write('L',0) #40 private data length placeholder

        headersize = woff.tell()

        #44 TABLE DIRECTORY
        tabledir = {}
        for tag in sorted(tabletags): #directory in alpha order
            #just put in placeholders for now; we'll fill in the values when we go through the tables later
            tabledir[tag] = woff.tell()
            write('5L',0,0,0,0,0,note=tag)

        directorysize = woff.tell() - headersize

        #FONT TABLES
        origtableoffset = {}
        realtableoffset = {}

        origtablelength = {}
        realtablelength = {}
        tablechecksum = {}

        data_totalsize = 0
        compressed_totalsize = 0

        myoffset = woff.tell()
        fakeoffset = 12 + numtables*16
        for tag in tabletags: #original font order
            realtableoffset[tag] = myoffset
            origtableoffset[tag] = fakeoffset

            data = self.OTF.getTableData(tag)

            #zero out whole-font checksum in head table
            if tag == 'head':
                data = data[:8] + '\0\0\0\0' + data[12:]

            origtablelength[tag] = datalength = len(data)
            tablechecksum[tag] = checksum = calcChecksum(data)

            if datalength > 1000:
                compressed = zlib.compress(data)
                realtablelength[tag] = compressedlength = len(compressed)

                if compressedlength >= datalength:
                    compressed = data
                    realtablelength[tag] = compressedlength = datalength
            else:
                compressed = data
                realtablelength[tag] = compressedlength = datalength

            #go back and write the table directory entries
            woff.seek(tabledir[tag])
            write('4s',tag)
            write('L',myoffset) #table offset
            write('L',compressedlength) #compressed length
            write('L',datalength) #uncompressed length
            write('L',checksum) #table checksum

            #come back to the present
            woff.seek(myoffset)
            woff.write(compressed)

            data_totalsize += datalength
            compressed_totalsize += compressedlength

            myoffset += compressedlength
            remainder = myoffset % 4
            if remainder > 0:
                add = 4-remainder
                woff.write('\0'*add)
                myoffset += add
                compressed_totalsize += add

            fakeoffset += datalength
            remainder = fakeoffset % 4
            if remainder > 0:
                add = 4-remainder
                fakeoffset += add
                data_totalsize += add


        #METADATA
        metasize = 0
        if meta:
            if isinstance(meta,unicode):
                meta = meta.encode('utf-8')
            compressed = zlib.compress(meta)
            metasize = len(compressed)
            woff.write(compressed)
            woff.seek(24)
            write('L',myoffset) #24 metadata offset placeholder (0 if none)
            write('L',metasize) #28 metadata length placeholder
            write('L',len(meta)) #32 metadata original length placeholder


        fullsize = myoffset + metasize

        #go back and write full size
        woff.seek(8)
        write('L',fullsize) #full file size

        #data size
        woff.seek(16)
        write('L',data_totalsize + 12 + numtables*16) #data size + sfnt header (12) + sfnt directory (#tables*16)


        woff.flush()

        #go back and write whole-font checksum
        checksumdata = ""

        logval = int(math.floor(math.log(numtables,2)))
        searchrange = pow(2,logval)*16

        checksumdata += struct.pack('>LHHHH',flavor,numtables,searchrange,logval,numtables*16-searchrange)

        for tag in sorted(tabletags):
            checksumdata += struct.pack('>4sLLL',tag,tablechecksum[tag],origtableoffset[tag],origtablelength[tag])

        checksums = [calcChecksum(checksumdata)]

        for tag in tabletags:
            checksums.append(tablechecksum[tag])

        wholechecksum = sum(checksums) & 0xFFFFFFFF

        checksumadjustment = (0xB1B0AFBA - wholechecksum) & 0xFFFFFFFF

        # write the checksum to the file
        woff.seek(realtableoffset['head'] + 8)
        write('L', checksumadjustment)

        woff.close()

    def createWOFF2(self, dest):
        import sys, re
        from wofftools.utilities import calcPaddingLength, padData
        from wofftools.sfnt import getSFNTData, sfntDirectorySize, sfntDirectoryEntrySize
        from wofftools.woff import packTestHeader, packTestDirectory, packTestMetadata, packTestPrivateData, woffHeaderSize
        from fontTools.ttLib.sfnt import sfntDirectoryFormat, sfntDirectorySize, sfntDirectoryEntryFormat, sfntDirectoryEntrySize

        tempttf = tempfile.TemporaryFile()
        self.TTF.save(tempttf)
        tempttf.seek(0)

        metadata = None
        privateData = None

        fontTables, compData, tableOrder, tableChecksums = getSFNTData(tempttf)

        fontDirectory = []
        for tag in tableOrder:
            fontDirectory.append(dict(
                tag=tag,
                offset=0,
                length=0,
                checksum=0,
                transformFlag=0
            ))

        woffHeader = dict(
            signature="wOF2",
            flavor="OTTO" if 'CFF ' in fontTables else "\000\001\000\000",
            numTables=len(fontDirectory),
            totalCompressedSize = len(compData),
            reserved=0,
            majorVersion=0,
            minorVersion=0,
            metaOffset=0,
            metaLength=0,
            metaOrigLength=0,
            privOffset=0,
            privLength=0,
            searchRange=0,
            entrySelector=0,
            rangeShift=0,
        )

        woffHeader["totalSfntSize"] = sfntDirectorySize + (len(fontDirectory) * sfntDirectoryEntrySize)
        for i, entry in enumerate(fontDirectory):
            tag = entry["tag"]
            origData, transformData = fontTables[tag]
            entry["origLength"] = len(origData)
            entry["transformLength"] = len(transformData)
            woffHeader["totalSfntSize"] += entry["origLength"]
            woffHeader["totalSfntSize"] += calcPaddingLength(woffHeader["totalSfntSize"])

        woffHeader["length"] = woffHeaderSize + len(packTestDirectory(fontDirectory))
        woffHeader["length"] += len(compData)
        woffHeader["length"] += calcPaddingLength(woffHeader["length"])

        # setup the metadata
        if metadata:
            compMetadata = brotli.compress(metadata, brotli.MODE_TEXT)
            woffHeader["metaOffset"] = woffHeader["length"]
            woffHeader["metaLength"] = len(compMetadata)
            woffHeader["metaOrigLength"] = len(metadata)
            woffHeader["length"] += len(compMetadata)
            if privateData is not None:
                woffHeader["length"] += calcPaddingLength(len(compMetadata))

        # setup the private data
        if privateData is not None:
            woffHeader["privOffset"] = woffHeader["length"]
            woffHeader["privLength"] = len(privateData)
            woffHeader["length"] += len(privateData)

        out = open(dest, 'wb')
        out.write(padData(packTestHeader(woffHeader) + packTestDirectory(fontDirectory) + compData))

        if metadata is not None:
            if privateData is not None:
                out.write(padData(compMetadata))
            else:
                out.write(compMetadata)

        if privateData is not None:
            out.write(privateData)

        out.close()

        return

    def createSVG(self, dest):
        #use TTF for SVG
        svg = open(dest,'w')

        svg.write("""<?xml version="1.0" encoding="utf-8" ?>""")
        svg.write("""<svg version="1.1" xmlns = 'http://www.w3.org/2000/svg'>""")
        svg.write("""<defs>""")
        svg.write("""<font id='web' horiz-adv-x="1000">\n""")

        fontface = {
            "units-per-em": self.TTF['head'].unitsPerEm,
            "bbox": ",".join([str(getattr(self.TTF['head'],x)) for x in ['xMin','yMin','xMax','yMax']]),
        }

        for s,o in {'cap-height':'sCapHeight','x-height':'sxHeight'}.items():
            if hasattr(self.TTF['OS/2'],o):
                fontface[s] = getattr(self.TTF['OS/2'],o)

        if hasattr(self.TTF['OS/2'],'sTypoAscender') and self.TTF['OS/2'].sTypoAscender:
            fontface['ascent'] = self.TTF['OS/2'].sTypoAscender
            fontface['descent'] = self.TTF['OS/2'].sTypoDescender
        elif hasattr(self.TTF['OS/2'],'usWinAscent') and self.TTF['OS/2'].usWinAscent:
            fontface['ascent'] = self.TTF['OS/2'].usWinAscent
            fontface['descent'] = self.TTF['OS/2'].usWinDescent
        elif 'vhea' in self.TTF and hasattr(self.TTF['vhea'],'ascent') and self.TTF['vhea'].ascent:
            fontface['ascent'] = self.TTF['vhea'].ascent
            fontface['descent'] = self.TTF['vhea'].descent

        #font-face
        svg.write("""<font-face font-family="web" {0} />\n""".format(" ".join(['{0}="{1}"'.format(k,fontface[k]) for k in fontface.keys()])))

        #glyphs
        cmap = self.getTTFCmap(self.TTF)
        glyphset = self.TTF.getGlyphSet()

        pen = SVGPen(glyphset)

        #add .notdef glyph
        notdef = self.TTF.getGlyphNames()[0]
        glyphset[notdef].draw(pen)
        svg.write("""<missing-glyph horiz-adv-x="{adv}" d="{path}" />""".format(adv=self.TTF['hmtx'].metrics[notdef][0],path=pen.getSVGPath()))

        uni2glyph = {}
        for uni,glyphname in cmap.items():
            if uni in (0,10,13):
                continue

            pen = SVGPen(glyphset)
            glyphset[glyphname].draw(pen)

            char = chr(uni)

            glyph = {
                'unicode': "&#x{0:02X};".format(uni) if char in '"&<>"' else char,
                'd': pen.getSVGPath(),
            }

            if glyphname in self.TTF['hmtx'].metrics:
                glyph['horiz-adv-x'] = self.TTF['hmtx'].metrics[glyphname][0]

            uni2glyph[uni] = glyph

        for uni in sorted(uni2glyph.keys()):
            glyph = uni2glyph[uni]
            svg.write("""<glyph {0} />\n""".format(" ".join([u'{0}="{1}"'.format(k,glyph[k]) for k in glyph.keys()])).encode('utf-8'))

        svg.write("""</font></defs></svg>\n""")

        svg.close()



    def buildCSS(self, outpath, fontname="TestFont"):
        #full woff/eot/ttf specification
        return """
            @font-face {{
             src: url("{path}.eot"); /* IE < 9 */
             src: url("{path}.eot?#") format("embedded-opentype"), /* IE 9 */
                url("{path}.woff") format("woff"),
                url("{path}.ttf") format("opentype"),
                url("{path}.svg#web") format("svg");
             font-family: "{fontname}";
             font-style: normal;
             font-weight: {weight};
            }}
            @font-face {{
             src: url("{path}.eot"); /* IE < 9 */
             src: url("{path}.eot?#") format("embedded-opentype"); /* IE 9 */
             font-family: "{fontname} EOT";
             font-style: normal;
             font-weight: {weight};
            }}
            @font-face {{
             src: url("{path}.woff") format("woff");
             font-family: "{fontname} WOFF";
             font-style: normal;
             font-weight: {weight};
            }}
            @font-face {{
             src: url("{path}.woff2") format("woff");
             font-family: "{fontname} WOFF2";
             font-style: normal;
             font-weight: {weight};
            }}
            @font-face {{
             src: url("{path}.ttf") format("opentype");
             font-family: "{fontname} TTF";
             font-style: normal;
             font-weight: {weight};
            }}
            @font-face {{
             src: url("{path}.svg#web") format("svg");
             font-family: "{fontname} SVG";
             font-style: normal;
             font-weight: {weight};
            }}
        """.format(
            path=outpath,
            fontname=fontname,
            weight=self.fontWeight,
        )


    @classmethod
    def dieargs(cls):
        print("""
NOTE: Most of this will work with Python 2.6 but WOFF2 requires Python 2.7

Usage: python ttf2web.py
       [--formats={ttf,eot,woff,svg,compressed-eot,woff2}]
       [--chars="ABC 123"] [--cprange1=number] [--txtfile=file.txt]
       [--font-weight=100|200|300|400|500|600|700|800|900|normal|bold]
       [--no-munge] [--name="Munged Name"] [--url="License URL"]
       [--test] [--gzip]
       [--metafile=file.xml]
       infiles outdir
Options:
 --formats: comma-delimited list of formats to build. Default: ttf,eot,woff,svg
 --chars: for subsetting, a literal list of Unicode characters to be included
          in the font. All other characters will be removed
 --txtfile: for subsetting, a text file containing all the Unicode chars to
            include in the font
 --cprange1: for subsetting, a bitmap indicating Windows codepages to include
             in the font. Sum of these numbers:
                1 = Latin 1 / Win 1252
                2 = CE / Win 1250
                4 = Cyrillic / Win 1251
                8 = Greek / Win 1253
                16 = Turkish / Win 1254
                128 = Baltic / Win 1257
 --font-weight: set the OS/2 usWeightClass value: 100-900 or "normal" or "bold"
 --no-munge: don't obfuscate name fields
 --font-name: obfuscate name fields with this font name
 --url: set license URL name fields to this URL
 --test: in addition to the fonts, will create test HTML and CSS files to make
         sure the fonts work as intended
 --gzip: also output gzipped versions of TTF, EOT, and SVG
 --metafile: a file containing XML for the WOFF metadata section
 --add-final: tack on "-final" to output filenames (for Webtype)
        """)
        sys.exit(1)

if __name__ == "__main__":
    try:
        options, args = getopt.getopt(sys.argv[1:],'',['asdf','metafile=','txtfile=','cprange1=','chars=','font-weight=','test','gzip','add-final','font-name=','url=','formats=','no-munge'])

        options = dict([(k[2:],v) for k,v in options])

        if not options.get('formats'):
            options['formats'] = 'ttf,eot,woff,svg'

        formats = options['formats'].split(',')

        metainfo = ""
        if options.get('metafile'):
            if not os.path.exists(options['metafile']):
                raise Exception("Metafile doesn't exist.")
            fh = open(options['metafile'],'r')
            metainfo = fh.read()
            fh.close()

        if options.get('font-weight'):
            if options['font-weight'] == 'normal':
                options['font-weight'] = '400'
            elif options['font-weight'] == 'bold':
                options['font-weight'] = '700'
            elif not re.search(r'^[1-9]00$',options['font-weight']):
                raise Exception("font-weight must be one of: 100, 200, 300, 400, 500, 600, 700, 800, 900, normal, bold")

        #SUBSETTING
        options['chars'] = set(options['chars'].decode('utf-8') if 'chars' in options else u'')

        SHOULD_SUBSET = bool(options['chars'])
        if options.get('txtfile'):
            if not os.path.exists(options['txtfile']):
                raise Exception("Txtfile doesn't exist.")
            SHOULD_SUBSET = True
            fh = open(options['txtfile'],'r')
            options['chars'].update(fh.read().decode('utf-8'))
            fh.close()

        if options.get('cprange1'):
            SHOULD_SUBSET=True
            bitmap = int(options['cprange1'])
            validrange = False
            for bit in TTF2WEB.CHARSETS:
                if bitmap & 2**bit:
                    validrange = True
                    options['chars'].update([chr(x) for x in TTF2WEB.CHARSETS[bit]])
            if not validrange:
                raise Exception("Invalid cprange1 argument. Should be sum of " + ', '.join([str(2**k) for k in TTF2WEB.CHARSETS.keys()]))

        if SHOULD_SUBSET and not options['chars']:
            raise Exception("Subsetting resulted in empty charset.")

        if not args:
            TTF2WEB.dieargs()

        indir = args[:-1]
        outdir = args[-1]

        for d in indir:
            if not os.path.exists(d):
                raise Exception("Source dir/file '{0}' not found.".format(d))

        if not os.path.exists(outdir):
            os.makedirs(outdir)
        elif not os.path.isdir(outdir):
            raise Exception("Specified output location not a directory: {0}".format(outdir))

        if 'test' in options:
            css = open(outdir + '/test.css','w')
            html = open(outdir + '/test.html','w')
            html.write("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Test</title><link rel='stylesheet' href='test.css'></head><body><dl>")
            css.write("dl { font-size: 36px; } dt { font-family: sans-serif; } dd { text-rendering: optimizeLegibility; }\n")

        allfiles = set()
        for d in indir:
            allfiles.update(TTF2WEB.findFontsInDir(d,ext='ttf'))
            allfiles.update(TTF2WEB.findFontsInDir(d,ext='otf'))

        skipnext = False
        count = len(allfiles)
        allfiles = sorted(allfiles)
        fontfiles = set()
        for i in range(count):
            if skipnext:
                skipnext = False
                continue
            fontfiles.add(allfiles[i])
            if i < count-1 and allfiles[i].endswith('.otf') and allfiles[i+1].endswith('.ttf') and allfiles[i][:-4]==allfiles[i+1][:-4]:
                skipnext = True

        for fontfile in fontfiles:
            fontfilebase = os.path.basename(fontfile)[:-4]
            outbase = outdir + '/' + fontfilebase

            if 'add-final' in options:
                outbase += '-final'

            otffile = fontfile if fontfile.endswith('.otf') else fontfile[:-4] + '.otf'
            ttffile = fontfile if fontfile.endswith('.ttf') else fontfile[:-4] + '.ttf'

            if not os.path.exists(otffile):
                otffile = ttffile
            elif not os.path.exists(ttffile):
                ttffile = otffile

            munger = TTF2WEB(otf=otffile, ttf=ttffile if os.path.exists(ttffile) else None)
            fontname = re.sub('^\W+','',munger.getTTFNameField('fullname'))

            if 'font-weight' in options:
                munger.setFontWeight(options['font-weight']);

            if 'test' in options:
                css.write(munger.buildCSS(fontname=fontfilebase,outpath=fontfilebase))
                teststring = u"AVALT oft fjord iffy find ĄąČčĘęĖė на русском языке Λάτρης της Ελλάδας ο διάσημος Βρετανός"
                html.write("""<dt>All Formats CSS</dt><dd style='font-family:{fontname},"Comic Sans MS";'>{teststring}</dd>""".format(teststring=teststring, fontname=fontfilebase).encode('utf-8'))
                for fmt in formats:
                    html.write("""<dt>{fmt}</dt><dd style='font-family:"{fontname} {fmt}","Comic Sans MS";'>{teststring}</dd>""".format(teststring=teststring, fontname=fontfilebase, fmt=fmt.upper()).encode('utf-8'))

            if 'no-subset' not in options and options['chars']:
                munger.subsetGlyphs(options['chars'])

            #munger.mungeGlyphNames()

            nameargs = {}
            if options.get('font-name'):
                nameargs['name'] = options['font-name']
            if options.get('url'):
                nameargs['url'] = options['url']

            if 'no-munge' not in options:
                munger.mungeNameFields(**nameargs)

            munger.generateSignature()

            ttffile = outbase + ".ttf"
            if 'ttf' in formats:
                munger.createTTF(ttffile)

            wofffile = outbase + ".woff"
            if 'woff' in formats:
                munger.createWOFF(wofffile,meta=metainfo)

            eotfile = outbase + ".eot"
            if 'eot' in formats:
                munger.createEOT(eotfile)

            if 'compressed-eot' in formats:
                munger.createEOT(outbase + '-compressed.eot',compress=True)

            if 'woff2' in formats:
                munger.createWOFF2(outbase + '.woff2')

            svgfile = outbase + ".svg"
            if 'svg' in formats:
                munger.createSVG(svgfile)

            #gzip TTF and EOT
            if 'gzip' in options:
                flavors = {ttffile: 1, eotfile: 2, svgfile: 4}
                for f in (ttffile,eotfile,svgfile):
                    if os.path.exists(f):
                        gzfile = open(f + ".gz","wb")
                        ffile = open(f,"rb")
                        gz = gzip.GzipFile(filename="{0}-{1}".format(fontfilebase,flavors[f]),mode="wb",fileobj=gzfile)
                        gz.write(ffile.read())
                        gz.close()
                        ffile.close()
                        gzfile.close()

        if 'test' in options:
            html.write("</dl></body></html>")
            css.close()
            html.close()

    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

