# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#
#     Auxiliary functions for TTX operations.
#     DJR 2014.
#
# ----------------------------------------------------------------------------------------------------------------------
#
#   ttxfindreplace.py
#
import re

class TTXFindReplace:
    """
    Auxiliary functions for TTX operations.
    """

    @classmethod
    def emptyTag(cls, tag, src):
        replaceTerm = '<%s>\r</%s>' % (tag, tag)
        searchTerm = re.compile('<%s.*?>.*?</%s>' % (tag, tag), re.DOTALL)
        newDestText, num = re.subn(searchTerm, replaceTerm, src)
        return newDestText

    @classmethod
    def removeTag(cls, tag, src):
        replaceTerm = '\r' % (tag, tag)
        searchTerm = re.compile('<%s.*?>.*?</%s>' % (tag, tag), re.DOTALL)
        newDestText, num = re.subn(searchTerm, replaceTerm, src)
        return newDestText


    @classmethod
    def getTTGlyph(cls, gname, text):
        searchTerm = re.compile(r'<TTGlyph name="%s"([^>]*/>|.*?</TTGlyph>)' % (gname), re.DOTALL)
        result = re.search(searchTerm, text)
        if result:
            return result.group()
        else:
            return None

    @classmethod
    def setTTGlyph(cls, gname, glyphText, src):
        searchTerm = re.compile(r'<TTGlyph name="%s"([^>]*/>|.*?</TTGlyph>)' % (gname), re.DOTALL)
        dest, num = re.subn(searchTerm, glyphText, src)
        return dest

    @classmethod
    def getTag(cls, tag, src):
        searchTerm = re.compile('<%s.*?>.*?</%s>' % (tag, tag), re.DOTALL)
        result = re.search(searchTerm, src)
        if result:
            return result.group()
        else:
            return None

    @classmethod
    def getSelfClosingTag(cls, tag, src):
        searchTerm = re.compile('<%s.*?>' % (tag), re.DOTALL)
        result = re.search(searchTerm, src)
        if result:
            return result.group()
        else:
            return None

    @classmethod
    def replace(cls, find, replace, src):
        text, num = re.subn(find, replace, src, flags=re.MULTILINE)
        # print('\tFIND AND REPLACE', num, len(find), len(replace), len(text))
        return text

if __name__ == "__main__":
    print(TTXFindReplace.getSelfClosingTag('a', 'Hello <a href="asf" /> asd'))
