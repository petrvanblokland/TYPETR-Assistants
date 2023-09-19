# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    xmlrepairparser.py
#

import BeautifulSoup
from tnbits.toolbox.parsers.xmlparser import XmlParser

class XmlRepairMan(XmlParser):
    """The `XmlRepairMan` class takes any kind of text (or lists/dictionaries of text) and
    creates verified XML as output. This function is especially used to gather HTML, user generated
    XML or other invalid XML structures and generate validated XML for storage.

    For documentation on BeautifulSoup see:

    http://www.crummy.com/software/BeautifulSoup/documentation.html#Quick%20Start
    """

    TAG_ROOT = 'root'

    @classmethod
    def repair(cls, data, default=None):
        """The `repair` method uses several sequential methods to convert an arbitrary
        set of `data` into a valid XML string."""
        if not data:
            return default
        # If already valid, then nothing needs to be done. Just return the data.
        if isinstance(data, str) and cls.isValidXml(data, addroot=False):
            return data
        # Try to do some basis find-replace on common HTML tags to make them into XML tags.
        # If data is a tuple, list or dictionary, combine it into a single string.
        xml = cls.TX.value2Xml(data)
        if cls.isValidXml(xml, addroot=False):
            return xml
        # The xml is not valid. Try adding a root, because it's a common
        # problem that there is not one single root.
        if cls.isValidXml(xml, addroot=True):
            return u"<%s>%s</%s>" % (cls.TAG_ROOT, xml, cls.TAG_ROOT)
            # return u"<%s>%s</%s>" % (C.ROOTID, xml, C.ROOTID)

        # The XML is not valid. Now, let's see what to do with it.
        # First try simple HTML to XML conversions
        # Also &amp; and &nbsp; are converted into <amp/> and <nbsp/> tags.
        """
        xml = cls.TX.html2Xml(xml)
        if cls.isValidXml(xml):
            return xml
        """
        xml = xml.encode('ascii', 'xmlcharrefreplace')
        soup = BeautifulSoup.BeautifulSoup(xml)
        soup = ('%s' % soup).replace('&', '&amp;') # Make XML level of entities
        if cls.isValidXml(soup):
            return soup
        # Maybe something
        # Now this needs more serious repair
        print('Not valid XML, still need to repair something that even Beautifulsoup can\'t.')
        return soup

    @classmethod
    def test(cls, wrong, right=''):
        repaired = cls.repair(wrong)
        if right != repaired:
            print('Cannot repair: ', wrong, repaired, 'to', right)

if __name__ == '__main__':
    xrm = XmlRepairMan
    print('Repair test start')
    #XML stuff
    #xrm.test('<!doctype html><aaa>zzzzz</aaa>',     '<!doctype html><aaa>zzzzz</aaa>')
    xrm.test('<?xml version="1.0" encoding="utf-8"?><aa>bb</aa>', '<?xml version="1.0" encoding="utf-8"?><aa>bb</aa>')
    # HTML stuff
    xrm.test('<aaa>zzzzz</aaa>', '<aaa>zzzzz</aaa>')
    xrm.test('<aaa><br><hr></aaa>', '<aaa><br /><hr /></aaa>')
    xrm.test('<aa.a><br><hr></aaa>', '<aa.a><br /><hr /></aa.a>')
    # Aloha stuff
    xrm.test('<aaa><br class="GENTICS_ephemera">', '<aaa><br class="GENTICS_ephemera" /></aaa>')
    # Other data types
    xrm.test(('<aaa>', 'zzzzz', '</aaa>'), '<aaa>zzzzz</aaa>')
    xrm.test({'aaa':'zzzzz'}, '<aaa>zzzzz</aaa>')
    xrm.test(('<aaa>', 'zzzzz', '</aaaa>'), '<aaa>zzzzz</aaa>')
    # Wrong tagging
    xrm.test('<aaa>zzzzzzz', '<aaa>zzzzzzz</aaa>')
    xrm.test('<aaa>zzz<zzzz', '<aaa>zzz</aaa>')
    xrm.test('<a<b<c<d<e', '<a><b><c><d></d></c></b></a>')
    xrm.test('<a tt="zz"<b<c<d<e', '<a tt="zz"><b><c><d></d></c></b></a>')
    xrm.test('<aaa>zzz<aaa>', '<aaa>zzz</aaa><aaa></aaa>')
    # Ampersand stuff
    xrm.test('<aaa zz="aa&bb">aaaaa<zzzz', '<aaa zz="aa&amp;amp;bb">aaaaa</aaa>')
    xrm.test('<aaa zz="aa&amp;amp;bb">aaaaa<zzzz', '<aaa zz="aa&amp;amp;bb">aaaaa</aaa>')
    xrm.test('<aaa>zzz&amp;aaaaa<zzzz', '<aaa>zzz&amp;amp;aaaaa</aaa>')
    xrm.test('<aaa>zzz&aaaaa<zzzz', '<aaa>zzz&amp;aaaaa;</aaa>') # Not entirely right
    xrm.test('<aaa>zzz&nbsp;</aaa>', '<aaa>zzz&amp;aaaaa;</aaa>') # Not entirely right
    print('Repair test ended')
