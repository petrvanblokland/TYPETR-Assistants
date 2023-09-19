# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

import os, shutil
from tnbits.toolbox.file import File
#from tnbits.compilers.ttf2web import TTF2WEB

from tnbits.compilers.ttf3web import ttf3web as TTF2WEB

import gzip


import os
import http.client
import socket
from urllib.parse import urlencode

from tnbits.constants import Constants
C = Constants
from tnbits.toolbox.transformer import TX
from tnbits.proofing import webproof
from tnbits.toolbox.character import CharacterTX
from tnbits.toolbox.file import File
from tnbits.toolbox.font import FontTX
from tnbits.toolbox import TX


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



#end MyXMLWriter



class P:
    from tnbits.toolbox.character import CharacterTX
    from tnbits.toolbox.file import File
    from tnbits.toolbox.font import FontTX
    from tnbits.toolbox import TX
    import unicodedata
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
        #print('Do TTF2WEB %s  %s' % (filePath, outputPath))
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



#end P




