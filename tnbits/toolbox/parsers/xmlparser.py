# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    (c) 2006-2011 buro@petr.com, www.petr.com, www.xierpa.com
#
#    X I E R P A  L I B
#
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    xmlparser.py
#
from tnbits.toolbox.parsers.parser import Parser
from lxml import etree

class XmlParser(Parser):
    """
    The `XmlParser` class is based on the `etree`.
    """

    TAG_MODULE = 'module'

    @classmethod
    def toString(cls, doc, encoding=None, skiproot=True):
        """The `toString` class method answers unicode string this
        way. Unicode encoding gives problems (BOM and such)."""
        xml = ''
        if skiproot:
            root = doc.getroot()
            if root is not None and len(root):
                xml = etree.tostring(root, encoding=encoding or 'utf-8')
        else:
            xml = etree.tostring(doc, encoding=encoding or 'utf-8')
        if xml:
            xml = xml.decode(encoding or 'utf-8')
        return xml

    @classmethod
    def saveTree(cls, doc, fspath):
        """The `saveTree` class method saves the `doc` into the `fspath`
        file."""
        f = open(fspath, 'wb')
        f.write(u'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(cls.toString(doc, encoding='utf-8', skiproot=False))
        f.close()

    @classmethod
    def isValidXml(self, xml, addroot=True):
        """The `isvalidxml` method answers id `xml` is a
        valid XML string. The method adds a module root tag, so the `xml`
        does not need to have a root tag."""
        try:
            if addroot and xml and not xml.startswith('<?'):
                xml = u'<%s>%s</%s>' % (self.TAG_MODULE, xml or '', self.TAG_MODULE)
            etree.fromstring(xml)
            return True
        except etree.XMLSyntaxError:
            pass
        return False
