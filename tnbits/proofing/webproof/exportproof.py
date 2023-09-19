# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
import unicodedata
import os, shutil
import gzip

from tnbits.constants import Constants as C
from tnbits.toolbox.character import CharacterTX
from tnbits.toolbox.file import File
from tnbits.toolbox.font import FontTX
from tnbits.toolbox.transformer import TX

from tnbits.objects.truetypefont import TrueTypeFont
from tnbits.compilers.ttf2web import TTF2WEB



class MyXMLWriter(object):
    def __init__(self, path=None):
        self.contents = []
        self.indent = 0
        self.path = path

    def begintag(self, tag, attrs={}, **kwargs):
        kwargs.update(attrs)
        for key, value in kwargs.items():
            tag+=' %s="%s"' %(key, value)
        self.contents.append('%s<%s>'% ('\t'*self.indent, tag) )
        self.indent += 1

    def endtag(self, tag, **kwargs):
        self.indent -= 1
        self.contents.append('%s</%s>'% ('\t'*self.indent, tag))

    def simpletag(self, tag, attrs={}, **kwargs):
        kwargs.update(attrs)
        for key, value in kwargs.items():
            tag+=' %s="%s"' %(key, value)
        self.contents.append('%s<%s>'% ('\t'*self.indent, tag))

    def selfclosingtag(self, tag, attrs={}, **kwargs):
        kwargs.update(attrs)
        for key, value in kwargs.items():
            tag+=' %s="%s"' %(key, value)
        self.contents.append('%s<%s />'% ('\t'*self.indent, tag))

    def tag(self, tagName, contents, attrs={}, **kwargs):
        kwargs.update(attrs)
        self.begintag(tagName, kwargs)
        self.write(contents)
        self.endtag(tagName)

    def write(self, content):
        self.contents.append('\t'*self.indent+content)

    def save(self, path=None):
        newContents = ''
        for content in self.contents:
            try:
                newContents += u'\n' + content
            except:
                print(content)
        myString = newContents
        return myString.encode('utf-8')




class P:
    """
    Utilities.
    """
    @classmethod
    def getFileSize(cls, font):
        return os.path.getsize(font.path) / float(1000)

    @classmethod
    def getFileFormat(cls, font):
        if 'glyf' in font.getTableNames():
            return 'TrueType-Flavored OpenType'
        elif 'CFF ' in font.getTableNames():
            return 'Postscript-Flavored OpenType'
        else:
            return 'Format unknown'

    @classmethod
    def getInOrder(cls, glyphNames, glyphOrder):
        inOrder = []
        for glyph in glyphOrder:
            if glyph in glyphNames:
                inOrder.append(glyph)
        return inOrder

    @classmethod
    def sortByUnicode(cls, chars):
        charDup = []
        for char in chars:
            if len(char) > 1:
                char = char[0]
            charDup.append((ord(char), char))
        charDup.sort()
        return [char[1] for char in charDup]

    @classmethod
    def getBinaryAtPosition(cls, b, p):
        bitPosition = 1 << p
        total = b & bitPosition
        return total >> p

    @classmethod
    def jsescape(self, text):
        #s = ''
        #for t in text:
            #s+='&#%s;' %ord(t)
            #s+='\%s' %ord(t)
        text = text.replace("\\", "\\\\'")
        text = text.replace("'", "\\'")

        return text

    @classmethod
    def doTTF2Web(cls, filePath, outputPath, title='proof'):
        #print('Do TTF2WEB %s %s' % (filePath, outputPath))
        # get web path
        webBasePath = outputPath
        File.makeFolder(webBasePath)
        metainfo = ""
        outputFileName = os.path.split(filePath)[1]
        outputFileBase = os.path.splitext(outputFileName)[0]
        webPath = os.path.join(webBasePath, outputFileBase)
        # spit out files
        ttffile = webPath + ".ttf"

        if ttffile == filePath:
            newfile = filePath[:-4] + '-pre-ttf2web.ttf'
            shutil.move(filePath, newfile)
            filePath = newfile

        munger = TTF2WEB(filePath)

        munger.createTTF(ttffile)
        wofffile = webPath + ".woff"
        munger.createWOFF(wofffile,meta=metainfo)
        eotfile = webPath + ".eot"
        munger.createEOT(eotfile)
        svgfile = webPath + ".svg"
        munger.createSVG(svgfile)
        #gzip TTF and EOT
        if 1 == 0:
            flavors = {ttffile: 1, eotfile: 2, svgfile: 4}
            for fileToGzip in (ttffile,eotfile,svgfile):
                gzfile = open(fileToGzip + ".gz","wb")
                ffile = open(fileToGzip,"rb")
                gz = gzip.GzipFile(filename="{0}-{1}".format(os.path.basename(outputFileBase),flavors[fileToGzip]),mode="wb",fileobj=gzfile)
                gz.write(ffile.read())
                gz.close()
                ffile.close()
                gzfile.close()


class Proof:

    # FUNCTIONS
    # To be put somewhere useful later.

    SPACER = unichr(8203)
    LATIN1_STRING = ''.join([unichr(u) for u in C.CODEPAGE_LATIN_1 if unicodedata.category(unichr(u)) != "Cc"])

    SMALLSIZES = range(9, 14)
    MEDIUMSIZES = range(14, 48)
    LARGESIZES = range(48, 120)

    MEDIUMSIZESPREVIEW = [14, 18, 24, 36]
    LARGESIZESPREVIEW = [48, 60, 72, 96, 120]

    RENDERING_DEFAULT = 'auto'
    RENDERING_OPTIMIZELEGIBILITY = 'optimize-legibility'
    RENDERING_OPTIMIZESPEED = 'optimize-speed'

    SMOOTHING_DEFAULT = 'auto'
    SMOOTHING_SUBPIXEL_ANTIALIASED = 'subpixel-antialiased'
    SMOOTHING_ANTIALIASED = 'antialiased'
    SMOOTHING_NONE = 'none'

    TABLEDESCRIPTIONS = {
                         'GlyphOrder': 'Not really a table, but it exists!',
                         'cmap': 'Character to glyph mapping',
                         'head': 'Font header',
                         'hhea': 'Horizontal header',
                         'hmtx': 'Horizontal metrics',
                         'maxp': 'Maximum profile',
                         'name': 'Naming table',
                         'OS/2': 'OS/2 and Windows specific metrics',
                         'post': 'PostScript information',

                        'cvt ':	'Control Value Table',
                        'fpgm': 'Font program',
                        'glyf':	'Glyph data',
                        'loca':	'Index to location',
                        'prep':	 'CVT Program',

                        'CFF':	'PostScript font program (compact font format)',
                        'VORG': 'Vertical Origin',
                        'EBDT':	'Embedded bitmap data',
                        'EBLC':	'Embedded bitmap location data',
                        'EBSC':	'Embedded bitmap scaling data',
                        'BASE':	'Baseline data',
                        'GDEF':	'Glyph definition data',
                        'GPOS':	'Glyph positioning data',
                        'GSUB':	'Glyph substitution data',
                        'JSTF':	'Justification data',
                        'DSIG':	'Digital signature',
                        'gasp':	'Grid-fitting/Scan-conversion',
                        'hdmx':	'Horizontal device metrics',
                        'kern':	 'Kerning',
                        'LTSH':	'Linear threshold data',

                        'PCLT':	'PCL 5 data',
                        'VDMX':	'Vertical device metrics',
                        'vhea':	'Vertical Metrics header',
                        'vmtx': 	'Vertical Metrics',
                         }

    def __init__(self, font, xml=None, outputpath=None, webfontbase=None, extraheadcontent="", extrabodycontent=""):
        self.font = font
        self.xml = xml or MyXMLWriter(outputpath)
        self.extraheadcontent = extraheadcontent
        self.extrabodycontent = extrabodycontent
        self.webfontbase = webfontbase




    def showFileInfo(self):
        xml = self.xml
        f = self.font
        xml.tag('a','' , {'class':'anchor', 'id':self.getFamilyName()+"_fileInfo"}
            )

        #xml.write('<a class="anchor" id="self.getFamilyName()+"_fileInfo"></a>')
        xml.begintag('section', {'class':'fileInfo'})



        xml.tag('h2', 'File Info')
        # the filename
        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('td', 'File path')
        xml.tag('td', self.font.path)
        xml.endtag('tr')
        # the format
        xml.begintag('tr')
        xml.tag('td', 'File format')
        xml.tag('td', P.getFileFormat(self.font))
        xml.endtag('tr')
        # the filesize
        xml.begintag('tr')
        xml.tag('td', 'File size')
        xml.tag('td', '%s kb' %P.getFileSize(self.font))
        xml.endtag('tr')

        count = len(self.font.keys())
        xml.begintag('tr')
        xml.tag('td', 'Glyph Count')
        xml.tag('td', '%s' %count)
        xml.endtag('tr')


        # the glyph efficiency
        xml.begintag('tr')
        xml.tag('td', 'Glifficency')
        size = P.getFileSize(self.font)
        efficiency = size/float(count)*1000
        xml.tag('td', '%.000f bytes per glyph' % (efficiency) )

        xml.begintag('tr')
        xml.tag('td', 'Units Per Em')
        xml.tag('td', '%s' %f['head'].unitsPerEm)
        xml.endtag('tr')


        xml.begintag('tr')
        xml.tag('td', 'Feature tables')
        featureTables = []
        for tableName in ['GSUB', 'GPOS']:
            if tableName in f.getTableNames():
                featureTables.append(tableName)
        xml.tag('td', '%s' %', '.join(featureTables))
        xml.endtag('tr')

        xml.begintag('tr')
        xml.tag('td', 'Kerning tables')
        featureTables = []
        for tableName in ['GPOS', 'kern']:
            if tableName in f.getTableNames():
                featureTables.append(tableName)
        xml.tag('td', '%s' %', '.join(featureTables))
        xml.endtag('tr')

        xml.begintag('tr')
        xml.tag('td', 'TrueType hinting tables')
        featureTables = []
        for tableName in ['cvt ', 'fpgm', 'prep', 'gasp', 'VDMX']:
            if tableName in f.getTableNames():
                featureTables.append(tableName)
        xml.tag('td', '%s' %', '.join(featureTables))
        xml.endtag('tr')

        xml.endtag('table')

        self.showVerticalMetrics()

        self.showTextDecoration()

        self.showStyleMappingInfo()


        self.showTables()



        xml.endtag('section')

    def showTextDecoration(self):
        xml = self.xml
        f = self.font

        xml.tag('h3', 'Text Decoration')
        xml.begintag('div', {'class': 'sample currentFont'})
        xml.tag('span', u'Hp Underline', {'style': 'text-decoration: underline'})
        xml.selfclosingtag('br')
        xml.tag('span', u'Hp Strikethrough', {'style': 'text-decoration: line-through;'})
        xml.endtag('div')

        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('td', 'post underlinePosition')
        xml.tag('td', '%s' %f['post'].underlinePosition)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'post underlineThickness')
        xml.tag('td', '%s' %f['post'].underlineThickness)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 yStrikeoutSize')
        xml.tag('td', '%s' %f.os2.yStrikeoutSize)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 yStrikeoutPosition')
        xml.tag('td', '%s' %f.os2.yStrikeoutPosition)
        xml.endtag('tr')
        xml.endtag('table')


    def showTables(self):
        xml = self.xml
        xml.tag('h3', 'All OpenType Tables')
        xml.begintag('table')
        for tableName in self.font.getTableNames():
            xml.begintag('tr')
            xml.tag('td', "%s" %tableName)
            tableDescription = self.TABLEDESCRIPTIONS.get(tableName)
            if tableName == 'kern':
                pairCount = len(self.font.kern.kernTables[0].kernTable)
                tableDescription = 'Flat Kerning; Pair count: ' + str(pairCount)
            xml.tag('td', tableDescription or '')
            xml.endtag('tr')
        xml.endtag('table')

    @classmethod
    def formatHTMLString(cls, htmlString):
        htmlString = htmlString.replace('&', '&amp;')
        htmlString= htmlString.replace('<', '&lt;')
        htmlString = htmlString.replace('>', '&gt;')
        return htmlString

    def showSizes(self, sizes, characters=LATIN1_STRING):
        xml = self.xml

        xml.begintag('ul', {'id':'char_set_nav'})

        xml.begintag('li')
        #xml.begintag('p')
        xml.selfclosingtag('input', {'type': "radio", 'class': "characterSelectionRadio", 'name': "textSelection", 'value': "repertoire", 'checked': "true"})
        xml.write(' <span class="current_char_set">Repertoire</span> |')
        xml.endtag('li')

        xml.begintag('li')
        xml.selfclosingtag('input', {'type': "radio", 'class': "characterSelectionRadio", 'name': "textSelection", 'value': "latin-1", })
        xml.write(' Latin-1 |')
        xml.endtag('li')

        xml.begintag('li')
        xml.selfclosingtag('input', {'type': "radio", 'class': "characterSelectionRadio", 'name': "textSelection", 'value': "ascii",})
        xml.write(' ASCII |')
        xml.endtag('li')

        xml.begintag('li')
        xml.selfclosingtag('input', {'type': "radio", 'class': "characterSelectionRadio", 'name': "textSelection", 'value': "wgl", })
        xml.write(' WGL |')
        xml.endtag('li')

        xml.begintag('li')
        xml.selfclosingtag('input', {"type":"radio", 'class': "characterSelectionRadio", 'name': "textSelection", 'value': "pangram", })
        xml.write(' Pangram |')
        xml.endtag('li')

        xml.begintag('li')
        xml.write(' Custom ')
        #xml.selfclosingtag('input', type="text", class="text_input", size="50")
        xml.write('<input type="text" class="text_input" size="50">')

        xml.endtag('li')

        xml.endtag('ul')



        xml.endtag('div')
        xml.endtag('div')

        #anchor top
        xml.tag('a', '',{'class':'anchor', 'id':'top'})


        xml.begintag('div', id="wrap")

        xml.begintag('section', id="All_sizes")


        xml.tag('h2', 'Sizes')

        # selection
        #xml.simpletag('input', type='radio')
        #xml.simpletag('input', type='radio')



        proofString = ''

        allChars = []
        for uniSet in self.font.unicodes.values():
            allChars += list(uniSet)
        allChars, self.font.glyphOrder
        allChars.sort()
        allChars = u''.join([unichr(x) for x in allChars])



        for character in allChars:
            g = self.font.glyphByUnicode(ord(character))
            if g is not None:
                proofString += character + self.SPACER
            else:
                pass

        for size in sizes:
            xml.tag('div', "%s" %size, {'class': 'sizeLabel'})
            xml.tag('div', self.formatHTMLString(proofString), {'contenteditable': True, 'class': 'sample sizes currentFont', 'style': 'font-size: %spx' %(size)})
        xml.endtag('section')

    def showFeatures(self):
        font = self.font
        xml = self.xml

        xml.tag('a','', {'class':'anchor', 'id':self.getFamilyName()+"_features"})


        xml.begintag('section', {'class':'features'})

        xml.tag('h2', 'OpenType Features')
        #glyphOrder = font.glyphOrder
        hasGsub = False
        try:
            if font.gsub:
                hasGsub = True
        except:
            pass
        if hasGsub:
            defaultLanguageTag = 'dflt'
            defaultScriptTag = 'DFLT'

            languageTags = [l.tag for l in font.gsub.languages]
            scriptTags = [l.script.tag for l in font.gsub.languages]
            if defaultLanguageTag not in languageTags and languageTags:
                defaultLanguageTag = languageTags[0]
            if defaultScriptTag not in scriptTags and scriptTags:
                defaultScriptTag = scriptTags[0]
            #print('defaultLanguageTag "%s"' % defaultLanguageTag)
            #print('defaultScriptTag "%s"' % defaultScriptTag)

            for feature in font.gsub.features:
                for language in feature.languages:
                    if language.tag == defaultLanguageTag and language.script.tag == defaultScriptTag:
                        try:
                            featureTitle = C.OPENTYPE_FEATURE_TAGS.get(feature.tag) or ''
                            gnames = feature.getGlyphNames()
                            chars = []
                            for gname in gnames:
                                char = CharacterTX.glyphName2Char(gname)
                                if char and char not in chars:
                                    chars.append(char)
                            chars = P.sortByUnicode(chars)
                            output = ''.join(chars)
                            xml.begintag('h3')
                            xml.simpletag('input', {'class': "ot_feature_enable", 'type': 'checkbox', 'name': feature.tag, 'checked': 'checked', 'alt': '+'})
                            xml.write('{%s} %s' %(feature.tag, featureTitle))
                            xml.endtag('h3')
                            xml.tag('p', self.formatHTMLString(output), {'contenteditable': True, 'class': 'sample %s %s currentFont' %(feature.tag, self.getFamilyName()) })
                        except:
                            print('error %s' % feature.tag)
        else:
            xml.tag('p', 'This font has no OpenType features.')
        xml.endtag('section')

    def showVerticalMetrics(self):
        xml = self.xml

        xml.tag('h3', 'Vertical Metrics')
        xml.tag('div', u'HÉhpo<br />HphÉo', {'class': 'sample verticalMetrics currentFont'})

        self.showVerticalMetricsInfo()

        self.showVerticalMetricsChecks()

    CHECKPASS = u'😀'
    CHECKFAIL = u'👎'

    def showVerticalMetricsChecks(self):
        xml = self.xml
        f = self.font

        xml.begintag('table')
        xml.begintag('tr')
        if f['hhea'].ascent == f['OS/2'].usWinAscent and abs(f['hhea'].descent) == abs(f['OS/2'].usWinDescent):
            xml.tag('td', self.CHECKPASS)
            xml.tag('td', u'hhea and usWin values are equal.')
        else:
            xml.tag('td', self.CHECKFAIL)
            xml.tag('td', u'%s hhea and usWin values are not equal.' %self.CHECKFAIL)
        xml.endtag('tr')
        xml.begintag('tr')
        if f['hhea'].lineGap == 0:
            xml.tag('td', self.CHECKPASS)
            xml.tag('td', u'%s hhea lineGap is 0.')
        else:
            xml.tag('td', self.CHECKFAIL)
            xml.tag('td', u'%s hhea lineGap is not 0.')
        xml.endtag('tr')
        xml.begintag('tr')

        if ( f['OS/2'].usWinAscent + abs(f['OS/2'].usWinDescent) ) - ( f['OS/2'].sTypoAscender + abs(f['OS/2'].sTypoDescender) ) == f['OS/2'].sTypoLineGap:
            xml.tag('td', self.CHECKPASS)
            xml.tag('td', u'sTypoLineGap is equal to the difference of the usWin and sTypo values.')
        else:
            xml.tag('td', self.CHECKFAIL)
            calculatedLinegap = ( f['OS/2'].usWinAscent + abs(f['OS/2'].usWinDescent) ) - ( f['OS/2'].sTypoAscender + abs(f['OS/2'].sTypoDescender))
            xml.tag('td', u'sTypoLineGap is not equal to the difference of the usWin and sTypo values, %s.' %calculatedLinegap)


        xml.endtag('table')

    def showVerticalMetricsInfo(self):
        f = self.font
        xml = self.xml
        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('td', 'hhea ascent')
        xml.tag('td', '%s' %f['hhea'].ascent)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'hhea descent')
        xml.tag('td', '%s' %f['hhea'].descent)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'hhea lineGap')
        xml.tag('td', '%s' %f['hhea'].lineGap)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 usWinAscent')
        xml.tag('td', '%s' %f['OS/2'].usWinAscent)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 usWinDescent')
        xml.tag('td', '%s' %f['OS/2'].usWinDescent)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 sTypoAscender')
        xml.tag('td', '%s' %f['OS/2'].sTypoAscender)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 sTypoDescender')
        xml.tag('td', '%s' %f['OS/2'].sTypoDescender)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 sTypoLineGap')
        xml.tag('td', '%s' %f['OS/2'].sTypoLineGap)
        xml.endtag('table')

    def showKerning(self):
        pass
        # does kern table exist
        # does gpos exist
        # spot check

    def showStyleMappingInfo(self):
        xml = self.xml
        f = self.font
        xml.tag('h3', 'Style Mapping Info')
        # values
        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 usWeightClass')
        xml.tag('td', '%s' %f['OS/2'].usWeightClass)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 usWidthClass')
        xml.tag('td', '%s' %f['OS/2'].usWidthClass)
        xml.endtag('tr')
        xml.begintag('tr')
        xml.tag('td', 'OS/2 fsSelection Italic')
        italicBit = P.getBinaryAtPosition(f['OS/2'].fsSelection, 0)
        if italicBit:
            selectionLabel = "Italic"
        else:
            selectionLabel = "Roman"
        xml.tag('td', '%s' %selectionLabel)
        xml.endtag('tr')

        xml.begintag('tr')
        xml.tag('td', 'OS/2 fsSelection Bold')
        boldBit = P.getBinaryAtPosition(f['OS/2'].fsSelection, 5)
        if boldBit:
            selectionLabel = "Bold"
        else:
            selectionLabel = "Regular"
        xml.tag('td', '%s' %selectionLabel)
        xml.endtag('tr')


        xml.endtag('table')

        # warning

    def showOS2UnicodeRanges(self):
        xml = self.xml
        f = self.font

        rangesValue1 = f['OS/2'].ulUnicodeRange1
        rangesValue2 = f['OS/2'].ulUnicodeRange2
        rangesValue3 = f['OS/2'].ulUnicodeRange3
        rangesValue4 = f['OS/2'].ulUnicodeRange4

        binaryRanges = '{0:032b}'.format(rangesValue1)[::-1] + '{0:032b}'.format(rangesValue2)[::-1] + '{0:032b}'.format(rangesValue3)[::-1] + '{0:032b}'.format(rangesValue4)[::-1]

        ranges = []
        for i, b in enumerate(binaryRanges):
            if int(b) == 1:
                ranges.append(i)

        xml.tag('h3', 'OS/2 Unicode Ranges')
        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('th', 'Bit')
        xml.tag('th', 'Min')
        xml.tag('th', 'Max')
        xml.tag('th', 'Name')
        xml.endtag('tr')

        for bit in ranges:

            uniranges = FontTX.unicodes.rangesForBit(bit)
            for unirange in uniranges:
                xml.begintag('tr')
                name = FontTX.unicodes.nameForRange(unirange)
                xml.tag('td', '%s' %bit)
                xml.tag('td', '%s' %unirange[0])
                xml.tag('td', '%s' %unirange[1])
                xml.tag('td', '%s' %name)
                xml.endtag('tr')

        xml.endtag('table')


    def showUnicodeChart(self):
        xml = self.xml
        f = self.font
        xml.tag('h3', 'Character Repertoire')

        allChars = []
        for uniSet in f.unicodes.values():
            allChars += list(uniSet)

        rangeList = C.UNICODE_RANGES.keys()
        rangeList.sort()
        xml.begintag('table')

        rowLength = len(C.HEXADECIMALDIGITS)

        for r in rangeList:
            min, max = r
            contains, doesNotContain = FontTX.unicodes.getSupport(r, allChars)
            if contains:
                xml.begintag('tr', {'class': 'header'})
                xml.tag('td', '')
                rangeName = FontTX.unicodes.nameForRange(r)
                xml.tag('td', rangeName, {'colspan': len(C.HEXADECIMALDIGITS)}, )
                xml.endtag('tr')

                xml.begintag('tr', {'class': 'collabel'})
                xml.tag('td', '')
                for e, i in enumerate(C.HEXADECIMALDIGITS):
                    colclass='odd'
                    if int(e/2.0) == e/2.0:
                        colclass='even'
                    xml.tag('td', i, {'class': colclass})
                xml.endtag('tr')

                for row in range(min, max, rowLength):
                    rowContains, rowDoesNotContain = FontTX.unicodes.getSupport((row, row+rowLength), allChars)
                    if rowContains:
                        xml.begintag('tr')
                        rowChars = ''
                        for u in range(row, row+rowLength):
                            g = f.glyphByUnicode(u)
                            if g is not None:
                                rowChars += '/' + g.name
                        #rowLabel = '<a href="robofont://%s?spaceCenter=%s">%s</a>' %(self.getRelativePath(), rowChars, str(TX.dec2hex(row)[:-1]))
                        rowLabel = '<a title="%s">%s</a>' %(rowChars, TX.dec2hex(row)[:-1])
                        xml.tag('td', rowLabel, {'class': 'rowlabel'})
                        for u in range(row, row+rowLength):
                            colclass='odd'
                            if int(u/2.0) == u/2.0:
                                colclass='even'
                            if u in rowContains:
                                g = f.glyphByUnicode(u)
                                if g is not None:
                                    gname = g.name
                                else:
                                    gname = ''

                                display = '<a title="%s">&#%s;</a>' %(gname, u)
                                xml.tag('td', display, {'class': 'tableSample %s %s currentFont' %(colclass, self.getFamilyName())})
                            else:
                                xml.tag('td', "&#%s;" %u, {'class': 'tableSample %s %s' %(colclass, "missing")})

        xml.endtag('table')


    def showCharacters(self):
        xml = self.xml

        xml.tag('a','', {'class':'anchor', 'id':self.getFamilyName()+"_characters"})



        xml.begintag('section', {'class':'characters'})


        xml.tag('h2', 'Characters')
        xml.tag('p', 'Note: This unicode chart shows the full character repertoire, but not the full glyph repertoire.')
        f = self.font
        self.showUnicodeChart()
        self.showOS2UnicodeRanges()
        self.showCodePageRanges()
        xml.endtag('section')

    def showCodePageRanges(self):

        def omitControls(codepage=[]):
            if not codepage:
                codepage = []
            newCodepage = []
            for c in codepage:
                if unicodedata.category(unichr(c)) != 'Cc':
                    newCodepage.append(c)
            return newCodepage

        xml = self.xml
        f = self.font

        allChars = []
        for uniSet in f.unicodes.values():
            allChars += list(uniSet)

        rangesValue1 = f['OS/2'].ulCodePageRange1
        rangesValue2 = f['OS/2'].ulCodePageRange2
        binaryRanges = '{0:032b}'.format(rangesValue1)[::-1] + '{0:032b}'.format(rangesValue2)[::-1]
        ranges = []
        for i, b in enumerate(binaryRanges):
            if int(b) == 1:
                ranges.append(i)

        doneCodepages = []

        if ranges:

            xml.tag('h3', 'OS/2 Codepage Ranges')

            xml.begintag('table')

            xml.begintag('tr')
            xml.tag('th', 'Bit')
            xml.tag('th', 'Name')
            xml.tag('th', 'Coverage')
            xml.tag('th', 'Missing')
            xml.endtag('tr')


            for bit in ranges:
                codepage = omitControls(FontTX.codepages.codePageForBit(bit))
                missingCharacters = list(set(codepage) - set(allChars))

                xml.begintag('tr')
                xml.tag('td', '%s' %bit)
                xml.tag('td', '%s' %FontTX.codepages.nameForBit(bit))
                xml.tag('td', '%s/%s' %(len(codepage)-len(missingCharacters), len(codepage)), {'class': 'sub'})
                xml.tag('td', ''.join([unichr(u) for u in missingCharacters]))

                xml.endtag('tr')
                doneCodepages.append(codepage)

            xml.endtag('table')

        xml.tag('h3', self.formatHTMLString('Repertoire missing less than 15% of codepage'))

        xml.begintag('table')
        xml.begintag('tr')
        xml.tag('th', 'Bit')
        xml.tag('th', 'Name')
        xml.tag('th', 'Coverage')
        xml.tag('th', 'Missing')
        xml.endtag('tr')

        for number, codepage in C.CODEPAGES.items():
            if codepage not in doneCodepages:
                codepage = omitControls(codepage)
                missingCharacters = list(set(codepage) - set(allChars))
                if len(missingCharacters) / float(len(codepage)) < .15:
                    xml.begintag('tr')
                    xml.tag('td', "%s" %C.FONTINFO_OS2_CODEPAGE_RANGES.get(number) or '')
                    xml.tag('td', "%s" %number or '')
                    xml.tag('td', '%s/%s' %(len(codepage)-len(missingCharacters), len(codepage)), {'class': 'sub'})
                    xml.tag('td', ''.join([unichr(u) for u in missingCharacters]))
                    xml.endtag('tr')
        xml.endtag('table')

    def showHintingInfo(self):
        xml.begintag('section', id=self.getFamilyName()+"_hintingInfo")

        # glyph hint is a bunch of parameters and one call
        pass
        # paratype is more like a program
        pass

        xml.endtag('section')

    def getFileName(self):
        path = self.font.path
        fileBase, fileNameAndExt = os.path.split(path)
        fileName, ext = os.path.splitext(fileNameAndExt)
        return fileName

    def getFamilyName(self):
        fileName = self.getFileName()
        familyName = fileName.replace('-', '')
        familyName = familyName.replace('_', '')
        return familyName

    def getRelativePath(self):
        both, relativePath, path2Path = File.getPathAlignment(self.font.path, self.xml.path)
        relativePath = '/'.join(relativePath)
        return relativePath

    def getAtFontFace(self):
        familyName = self.getFamilyName()
        relativePath = self.getRelativePath()
        relativePathNoExt = os.path.splitext(relativePath)[0]
        aff = """@font-face {{
                           src: url('{url}.eot'); /* IE < 9 */
                           src: url('{url}.eot?#') format("embedded-opentype"), /* IE 9 */
                                url('{url}.woff') format("woff"),
                                url('{url}.ttf') format("opentype"),
                                url('{url}.svg') format("svg");
                           font-family: {font};
                           font-style: normal;
                           font-weight: normal;
                           }}
                    .currentFont {{
                         font-family: {font}, "Zero Width Space", "FB Unicode Fallback";
                         }}

                     .{font} {{
                         font-family: {font}, "Zero Width Space", "FB Unicode Fallback";
                         }}

                """.format(url=relativePathNoExt, font=familyName)
        return aff

    def getFeatureTags(self, omit=[]):
        allFeatureTags = []
        for feature in self.font.gsub.features:
            if feature.tag not in allFeatureTags and feature.tag not in omit:
                allFeatureTags.append(feature.tag)
        return allFeatureTags

    def getFeatureAsClass(self, featureTag):
        return """
            .%s {
        	font-feature-settings:"%s" 1; /* generic */
            -moz-font-feature-settings: "%s=1"; /* Firefox 4.0 to 14.0 */
            -moz-font-feature-settings: "%s" on; /* Firefox 15.0 onwards */
        	-ms-font-feature-settings:"%s" 1; /* ie */
        	-webkit-font-feature-settings:"%s" 1; /* safari, chrome */
        	-o-font-feature-settings:"%s" 1; /* old opera */
            }
            """ %(featureTag,featureTag,featureTag,featureTag,featureTag,featureTag,featureTag)

    def getStylesheet(self):
        stylesheet = """

		#header-wrap {
			    position: fixed;
				_position:absolute;
				top:0;
				 _top:expression(eval(document.body.scrollTop));

			    height: 55px;
			    top: 0;
			    width: 100%;
			    /* z-index: 100; */
				background-color: white;
				padding-top:10px;
				padding-left:10px;
				min-width:900px;

				border-bottom: 2px solid #E6E7E8;

			}

			#wrap {
			  /* max-width: 900px; */
			  margin: 70px auto;
  		  	padding-left:15px;
  		  	padding-right:15px;

			}



			a.anchor{
			display: block; position: relative; top: -70px; visibility: hidden;
			}

			section.anchor{
			display: block; position: relative; top: -85px;;
			}

			#All_sizes {
			}

			#char_set_nav{
			/*padding-top:5px;*/
			/* display:inline; */
			}

			.current_char_set {
			color: red;
			}

        body {
              margin: 0px;
              padding: 0px;
              font-family: Verdana;
              font-size: 11px;



              word-wrap: break-word;
              background: #ffffff;
			text-rendering: optimizeLegibility;
              }

        ul, p {
              margin: 0px;
              padding: 0px;
			}

        table {
            font-size: 11px;
        }

        section {
            padding: 5px, 0px, 5px, 0px;
            background: #fff;
        }

        .title {
            font-size: 16px;
            float:left;
            margin-right:1em;
        }

        .clear {
		    line-height: 0px;
		    clear: both;
		    font-size: 0px;
		    margin: 0px;
		    padding: 0px;
		    height: 0px;
		}



        h1 {

            font-size: 36px;
            font-weight: normal;
            }

        h2 {
                font-size: 14px;
                }
        h3 { font-size: 12px; padding-top: 2em; }

        th {color: #666; font-weight: normal; font-style: italic;}
        td {padding: .3em;}

        .tableBreak { backgroud: #f3f3f3; }

        /* all samples including features, etc */
        .sample {
           font-size: 40px;
           /* margin: .5em 0; */
           }

        .sizes {
       		margin-top: .1em;
	   	 	margin-bottom: .5em;
	   }

        .tableSample {
                      text-align: center;
                      font-size: 20px;
                      }
        .verticalMetrics {
                          border: 1px solid red;
                          width: 15em;
                          font-size: 40px;

                          }
        .nofeature {
         color: #999;
         }
        td {padding: .3em; margin-right: .3em;}
        .sizeLabel {
                    font-family: Verdana;
                    font-size: 10px;
                    line-height: 15px;
                    display: block;
                    padding-top:5px;

                    }
        .odd {
              background: #ccc;
              }
        .even {
            background: #ccc;
               }

        .missing, .missing a {
                              color: #ccc;
                                  font-family: "Times", "Times New Roman", "Courier New";
                              }

        a {text-decoration: none; color: #333 }
        a:hover {color: #006699}
        .char {font-size: 16px}
        .header td {text-align: left;}
        .even {background: #CAE8F9;}
        .odd {background: #CAF8F9;}
        .collabel, .rowlabel {color: #ccc;}
        .rowlabel a {color: #ccc; text-decoration: none}
        th {text-align: left;}

#header li {
	display: inline-block;
}

#tabs ul{
float:left;
	}

#tabs li {
	/* padding-right: 1em; */
	margin-right: 1em;
	background:#F1F2F2;
}


.ui-state-default {
	background: -webkit-linear-gradient(top, #FFF 75%,#EEE);
}
.ui-tabs-active {
	border-bottom: 1px solid #FFF;
	background: #FFF;
}
.warning { color: red; }

        """
        return stylesheet

    def htmlBegin(self):
        xml = self.xml

        xml.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        #doctype


        xml.begintag('html')
        xml.begintag('head')

         #<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>

        xml.tag('script', '' , src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js")


        jscustomtext = u"""

        	$(function() {

		$(".text_input").keyup(function(){
				//use this version to change all inputs with class "sizes"
			   //$(".sizes").val(this.value);


			   //use this to change all divs, etc w/ class "sizes"
			   $(".sizes").html($('.text_input').val());

			});

	}); // end ready

	"""

        xml.tag('script', jscustomtext, language="JavaScript")
        xml.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        xml.tag('title', 'Proof: %s' %self.getFamilyName().replace(" ", ""))


        stylesheet = self.getStylesheet()
        stylesheet += self.getAtFontFace()
        #for tag in self.getFeatureTags():
        #    stylesheet += self.getFeatureAsClass(tag)
        xml.tag('style', stylesheet, {'type': "text/css"})

        xml.tag('script', '', src="http://code.jquery.com/jquery-1.9.1.js")
        xml.tag('script', '', src="http://code.jquery.com/ui/1.10.3/jquery-ui.js")

        #xml.tag('script', '', src="jquery/jquery.js")
        #xml.tag('script', '', src="jquery/jquery-ui.js")

        allChars = []
        for uniSet in self.font.unicodes.values():
            allChars += list(uniSet)
        allChars, self.font.glyphOrder
        allChars.sort()
        allChars = u''.join([unichr(x) for x in allChars])


        latin1 = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
        #allChars = latin1

        ascii = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

        wgl = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƒǺǻǼǽǾǿˆˇˉ˘˙˚˛˜˝΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяѐёђѓєѕіїјљњћќѝўџҐґẀẁẂẃẄẅỲỳ–—―‗‘’‚‛“”„†‡•…‰′″‹›‼‾⁄ⁿ₣₤₧€℅ℓ№™Ω℮⅛⅜⅝⅞←↑→↓↔↕↨∂∆∏∑−∕∙√∞∟∩∫≈≠≡≤≥⌂⌐⌠⌡─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬▀▄█▌▐░▒▓■□▪▫▬▲►▼◄◊○●◘◙◦☺☻☼♀♂♠♣♥♦♪♫ﬁﬂ'

        pangrams = u'Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliet Kilo Lima Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey Xylophone Yankee Zulu. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Jackdaws love my big sphinx of quartz. Victors flank gypsy who mixed up on job quiz. Wolves exit quickly as fanged zoo chimps jabber. Five jumbo oxen graze quietly with packs of dogs. Grumpy wizards make toxic brew for the evil queen and jack.  Lazy movers quit hard packing of jewelry boxes. Ban foul, toxic smogs which quickly jeopardize lives. Hark! Toxic jungle water vipers quietly drop on zebras for meals! New farm hand, picking just six quinces, proves strong but lazy. Back in my quaint garden, jaunty zinnias vie with flaunting phlox. Waltz, nymph, for quick jigs vex Bud. Crazy Fredericka bought many very exquisite opal jewels. Jolly housewives made inexpensive meals using quick-frozen vegetables. Sixty zippers were quickly picked from the woven jute bag. Call 1 (800) 435 8293 Jaded zombies acted quaintly but kept driving their oxen forward. Six big juicy steaks sizzled in a pan as five workmen left the quarry.  Will Major Douglas be expected to take this true-false quiz very soon? A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent. Jimmy and Zack, the police explained, were last seen diving into a field of buttered quahogs. Monique, the buxom coed, likes to fight for Pez with the junior varsity team. The jukebox music puzzled a gentle visitor from a quaint valley town. Just work for improved basic techniques to maximize your typing skills. When we go back to Juarez, Mexico, do we fly over picturesque Arizona? Murky haze enveloped a city as jarring quakes broke forty-six windows. Nancy Bizal exchanged vows with Robert J. Kumpf at Quincy Temple. The quick brown fox jumps over the lazy dog.  Pack my box with five dozen liquor jugs. Brick quiz whangs jumpy veldt fox. Quick wafting zephyrs vex bold Jim. Sphinx of black quartz, judge my vow. The five boxing wizards jump quickly. Pickled, Gorbachev jumps tawny fax quiz. Sympathizing would fix Quaker objectives. Doxy with charming buzz quaffs vodka julep. Raving zibet chewed calyx of pipsqueak major. J. Hoefler cabled: “puzzling over waxy kumquats.” Oozy quivering jellyfish expectorated by mad hawk. By Jove, my quick study of lexicography won a prize. Lazy jackal from raiding xebec prowls the quiet cove. Six boys guzzled cheap raw plum vodka quite joyfully. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified. Six big devils from Japan quickly forgot how to waltz. Quixotic knights’ wives are found on jumpy old zebras. Guzzling of jaunty exile wrecks havoc at damp banquet. How razorback-jumping frogs can level six piqued gymnasts! When waxing parquet decks, Suez sailors vomit jauntily abaft. Frozen buyer just quickly keyed shocking weaver’s complexion. Qu’est-ce c’est chez le vieux forgerondu coin J’ai pu boire le meilleur whisky? Fabled reader with jaded, roving eye seized by quickened impulse to expand budget. Breezily jingling $3,416,857,209, wise advertiser ambles to the bank, his exchequer amplified.'


        js = u"""
        $(function() {
                        $( "#tabs" ).tabs();
                    });

    var setCustomText = function() {
			if (document.getElementById("customTextInput").value.length == 0) {
			} else {
			}
						$('div.sizes').text(document.getElementById("customTextInput").value);
    }
    var changeSizeText = function() {
        if (this.checked && this.value == 'ascii') {
			$('div.sizes').text('%s');
        } else if (this.checked && this.value == 'latin-1') {
			$('div.sizes').text('%s');
        } else if (this.checked && this.value == 'wgl') {
        $('div.sizes').text('%s');
        } else if (this.checked && this.value == 'repertoire') {
        $('div.sizes').text('%s');
        } else if (this.checked && this.value == 'pangram') {
        var getPangramAtLength = function() {
        var pangrams = '%s';
        var pangrams = pangrams.slice(0, 2000);
        var pangramLength = pangrams.length;
        var sizeMin = 90;
        var sizeMax = 9;
        var currentSize = this.style.fontSize.slice(0,-2);
        var sizeProgress = (currentSize - sizeMin) / (sizeMax - sizeMin);
        var minPangramLength = 10;
        var cutoff = minPangramLength + (pangramLength-minPangramLength) * sizeProgress;
        if (cutoff < 25) {
        cutoff = 30;
        }
        //console.log(currentSize+" "+sizeProgress+" "+cutoff);
        this.innerHTML = pangrams.slice(0, cutoff);
            }
            $('div.sizes').each(getPangramAtLength);
        } else if (this.checked && this.value == 'custom') {
        setCustomText();
        }
    }

		var enableOTFeature = function() {

			var feat = this.name;
			var w3c = '"' + feat + '" ' + (this.checked ? "1" : "0");
			var mozold = '"' + feat + '=' + (this.checked ? "1" : "0");
			var moz = '"' + feat + ' ' + (this.checked ? "on" : "off");

			$('p.' + feat).css({
				"font-feature-settings": w3c	,
				"-moz-font-feature-settings": mozold,
				"-moz-font-feature-settings": moz,
				"-ms-font-feature-settings": w3c,
				"-webkit-font-feature-settings": w3c,
				"-o-font-feature-settings": w3c,
			});

		}

    $(document).ready(function(){

		$('input.ot_feature_enable').each(enableOTFeature).click(enableOTFeature);
    $('input.characterSelectionRadio').each(changeSizeText).click(changeSizeText)
    $('#customTextInput').keyup(setCustomText);

    })


        """ % ( P.jsescape(ascii), P.jsescape(latin1), P.jsescape(wgl),  P.jsescape(allChars),  P.jsescape(pangrams) )

        xml.tag('script', js, type="text/javascript")

        xml.write(self.extraheadcontent)

        xml.endtag('head')

    def build(self):
        xml = self.xml
        self.htmlBegin()
        xml.begintag('body spellcheck="false"')

        xml.begintag('div','',id="header-wrap")
        xml.begintag('div','',id="header")

        xml.begintag('a','', href="#top")
        xml.tag('span', self.getFamilyName(), {'class': 'currentFont title' })
        xml.endtag('a')


        #xml.begintag('div', id="tabs")
        xml.begintag('ul', '', id="tabs")

        xml.begintag('li')
        xml.tag('a', 'Sizes', href="#top")
        xml.endtag('li')

        xml.begintag('li')
        xml.tag('a', 'File Info', href="#"+self.getFamilyName()+"_fileInfo")
        xml.endtag('li')

        xml.begintag('li')
        xml.tag('a', 'Characters', href="#"+self.getFamilyName()+"_characters")
        xml.endtag('li')

        xml.begintag('li')
        xml.tag('a', 'Features', href="#"+self.getFamilyName()+"_features")
        xml.endtag('li')

        xml.endtag('ul')

        xml.write('<br class="clear"/>')




        self.showSizes(self.SMALLSIZES+self.MEDIUMSIZES+self.LARGESIZES)
        self.showFileInfo()
        self.showCharacters()
        self.showFeatures()

        xml.endtag('div')

        xml.write(self.extrabodycontent)

        xml.endtag('body')
        xml.endtag('html')


    @classmethod
    def simpleBuild(cls, ttfpath, outputpath=None, webfontbase=None, extraheadcontent="", extrabodycontent=""):
        print("Building proof of %s with outputpath %s and webfontbase %s" % (ttfpath, outputpath, webfontbase))
        p = cls(TrueTypeFont(ttfpath), outputpath=outputpath, webfontbase=webfontbase, extraheadcontent=extraheadcontent, extrabodycontent=extrabodycontent)
        p.build()
        result = p.xml.save()
        if outputpath:
            File.write(result, outputpath)
        P.doTTF2Web(ttfpath, webfontbase)
        return result

    @classmethod
    def buildPaths(cls, paths):
        launched = []
        outputPaths = []
        for path in paths:
            basePath, fileAndExt = os.path.split(path)
            fileName, ext = os.path.splitext(fileAndExt)
            outputFolder = os.path.join(basePath, 'proof')
            fontOutputFolder = os.path.join(outputFolder, 'fonts')
            outputPath = os.path.join(outputFolder, fileName+'.html')
            outputPaths.append((outputPath, fileName))
            print('Building path %s' % path)
            P.doTTF2Web(path, fontOutputFolder)
            ttfSourcePath = os.path.join(fontOutputFolder, fileName+'.ttf')
            #print('error with %s' % ttfSourcePath)
            cls.simpleBuild(ttfSourcePath, outputPath, webfontbase=fontOutputFolder)
            if outputPath not in launched:
                #File.launch(outputPath)
                launched.append(outputPath)
        # Build index page
        xml = MyXMLWriter(os.path.join(outputFolder, 'index.html'))
        xml.begintag('html')
        xml.begintag('head')
        style = """
        body {font-family: Verdana; font-size: 12px}
        """
        xml.tag('style', style, {'type': 'text/css'})
        xml.endtag('head')
        xml.begintag('body')
        xml.tag('h1', 'Proof index')
        xml.begintag('ul')
        for outputPath, fileName in outputPaths:
            both, relativePath, path2Path = File.getPathAlignment(outputPath, outputFolder)
            relativePath = '/'.join(relativePath)
            xml.begintag('li')
            xml.tag('a', fileName.replace("_", " "), {'href': relativePath})
            xml.endtag('li')
        xml.endtag('ul')
        xml.endtag('body')
        xml.endtag('html')
        File.write(xml.save(), xml.path)

    @classmethod
    def buildPathsWithExistingFonts(cls, basepaths):
        launched = []
        outputPaths = []
        for path in basepaths:
            basePath, fileName = os.path.split(path)
            outputFolder = os.path.join(basePath, 'proof')
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)
            outputPath = os.path.join(outputFolder, fileName+'.html')
            outputPaths.append((outputPath, fileName))

            #copy fonts into proof folder so they will work in firefox
            outputFontsFolder = os.path.join(outputFolder,'fonts')
            if not os.path.exists(outputFontsFolder):
                os.makedirs(outputFontsFolder)

            for ext in ('.ttf','.otf','.eot','-compressed.eot','.woff','.svg'):
                srcfont = path + ext
                destfont = os.path.join(outputFontsFolder, fileName + ext)
                if os.path.exists(srcfont):
                    shutil.copy(srcfont,destfont)

            ttfSourcePath = os.path.join(outputFontsFolder, fileName+'.ttf')
            #print('error with %s' % ttfSourcePath)
            cls.simpleBuild(ttfSourcePath, outputPath, webfontbase=outputFontsFolder)
            if outputPath not in launched:
                #File.launch(outputPath)
                launched.append(outputPath)
        # Build index page
        xml = MyXMLWriter(os.path.join(outputFolder, 'index.html'))
        xml.begintag('html')
        xml.begintag('head')
        style = """
        body {font-family: Verdana; font-size: 12px}
        """
        xml.tag('style', style, {'type': 'text/css'})
        xml.endtag('head')
        xml.begintag('body')
        xml.tag('h1', 'Proof index')
        xml.begintag('ul')
        for outputPath, fileName in outputPaths:
            both, relativePath, path2Path = File.getPathAlignment(outputPath, outputFolder)
            relativePath = '/'.join(relativePath)
            xml.begintag('li')
            xml.tag('a', fileName.replace("_", " "), {'href': relativePath})
            xml.endtag('li')
        xml.endtag('ul')
        xml.endtag('body')
        xml.endtag('html')
        File.write(xml.save(), xml.path)



if __name__ == "__main__":
    import vanilla
    paths = vanilla.dialogs.getFile(allowsMultipleSelection=True)

    launched = []

    outputPaths = []
    for path in paths:
        basePath, fileAndExt = os.path.split(path)
        fileName, ext = os.path.splitext(fileAndExt)
        outputFolder = os.path.join(basePath, 'proof')
        fontOutputFolder = os.path.join(outputFolder, 'fonts')
        outputPath = os.path.join(outputFolder, fileName+'.html')
        P.doTTF2Web(path, fontOutputFolder)
        ttfSourcePath = os.path.join(fontOutputFolder, fileName+'.ttf')
        #print('error with %s' % ttfSourcePath)
        ttfont = TrueTypeFont(ttfSourcePath)
        outputPaths.append(((ttfont.os2.usWidthClass, ttfont.os2.usWeightClass), outputPath, fileName))

        print('ttfont path %s' % ttfont.path)
        xml = MyXMLWriter(outputPath)
        p = Proof(ttfont, xml)
        p.build()
        File.write(p.xml.save(), p.xml.path)






        if outputPath not in launched:
            #File.launch(outputPath)
            launched.append(outputPath)

    xml = MyXMLWriter(os.path.join(outputFolder, 'index.html'))
    xml.begintag('html')
    xml.begintag('head')

    ##need to add @font-face for all styles here with corresponding font classes

    outputPaths.sort()

    aff = ""
    for sorter, outputPath, fileName in outputPaths:
        both, relativePath, path2Path = File.getPathAlignment(outputPath, outputFolder)
        relativePath = '/'.join(relativePath)
        relativePath = 'fonts/'+relativePath

        familyName = fileName.replace("-", "")
        familyName = familyName.replace(" ", "")
        familyName = familyName.replace("_", "")
        #removes hyphens and spaces in file names, should be able to write this in one line

        relativePathNoExt = os.path.splitext(relativePath)[0]
        aff += """@font-face {
                           src: url('%s.eot'); /* IE < 9 */
                           src: url('%s.eot?#') format("embedded-opentype"), /* IE 9 */
                                url('%s.woff') format("woff"),
                                url('%s.ttf') format("opentype"),
                                url('%s.svg') format("svg");
                           font-family: %s;
                           font-style: normal;
                           font-weight: normal;
                           }


                     .%s {
                         font-family: %s, "Zero Width Space", "FB Unicode Fallback";
                         }

                """ %(relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      familyName, familyName, familyName)

    #returns aff (list of all @font-face declarations)

    #this adds the @font-face declarations to the stylesheet
    style = aff+"""
    body {
    font-family: Verdana;
    font-size: 12px;
    margin:0;
    padding:0;
    }

    .sample {
    margin-bottom:15px;
    margin-top:5px;
    font-size: 20px;
    }

    #wrap {
    margin-left:10px;
    }

    a:link, a:visited, a:hover, a:active {
    color: #000000;
    text-decoration: none;
    border-bottom:1px solid #ccc;

    }

    a:hover {
    border-bottom:1px solid #000;
    }
    """
    xml.tag('style', style, {'type': 'text/css'})
    xml.endtag('head')

    #index.html
    xml.begintag('body')

    xml.begintag('div', {'id':'wrap'})

    xml.tag('h1', 'Proof index')


    #next I need to separate italic and regular, and sort all by os2 weight


    for sorter, outputPath, fileName in outputPaths:
        both, relativePath, path2Path = File.getPathAlignment(outputPath, outputFolder)
        relativePath = '/'.join(relativePath)
        xml.begintag('div', {'class':'label'})
        xml.tag('a', fileName.replace("_", " "), {'href': relativePath})
        xml.endtag('div')


        sample= """
        ABCDEFGHIJKLMNOPQRSTUVWXYZ<br/>
        abcdefghijklmnopqrstuvwxyz<br/>
        0123456789%=<+>$#'"?!&(/)[\]{|}*.,:;_-
        """

        className = fileName.replace("-", "")
        className = className.replace(" ", "")
        className = className.replace("_", "")

        xml.begintag('div',  {'class':'sample '+className})
        xml.write(sample)
        xml.endtag('div')

    xml.endtag('div')

    xml.endtag('body')
    xml.endtag('html')
    File.write(xml.save(), xml.path)


    print('done')


if __name__ == "__main__2":
    path = u"/Users/david/Desktop/asdf/Fern_Banner_Beta-Light.ttf"
    base, fileAndExt = os.path.split(path)
    proofBase = os.path.join(base, 'proof')
    outputPath = os.path.join(proofBase, fileAndExt.replace('.ttf', '.html'))
    webFontBase = os.path.join(proofBase, 'fonts')
    Proof.simpleBuild(path, outputPath, webFontBase)
