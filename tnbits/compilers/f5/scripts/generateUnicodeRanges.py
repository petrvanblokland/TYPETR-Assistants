import sys
import os
import urllib2
from lxml import etree


def myHex(n):
    s = "0x%.4X" % n
    s = " " * (8 - len(s)) + s
    return s


_outputFile = None

def myPrint(t=""):
    f = _outputFile or sys.stdout
    f.write(t)
    f.write("\n")

rangesUrl = "http://www.microsoft.com/typography/otspec/os2.htm"
scriptTagsUrl = "http://www.microsoft.com/typography/otspec/scripttags.htm"


req = urllib2.Request(rangesUrl, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen( req )
broken_html = con.read()


outputPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "unicodeRangesData.py")
_outputFile = open(outputPath, "w")

html = etree.HTML(broken_html)
for node in html.xpath("body/div/table/tr/th"):
    if node.text == "Unicode Range":
        break

myPrint("#")
myPrint("# Generated from:")
myPrint("#    " + rangesUrl)
myPrint("#    " + scriptTagsUrl)
myPrint("# by scripts/" + os.path.basename(__file__))
myPrint("#")
myPrint("# *** DO NOT EDIT ***")
myPrint("#")
myPrint("")
myPrint("unicodeRanges = [")
myPrint("#     bit   name                                           from        to")
table = node.getparent().getparent()
bitNum = None
lastLine = ""
for rowNode in table.xpath("tr"):
    if rowNode[0].tag == "th":
        continue
    row = []
    for col in rowNode:
        row.append(col.text.strip())
    if len(row) == 2:
        # last line, reserved
        lastLine = " ".join(row)
        row.append(None)
    else:
        bit, name, rng = row
        if bit:
            bitNum = int(bit)
        #XXX
        fr, to = rng.split("-")
        fr = int(fr, 16)
        to = int(to, 16)
        myPrint("    ( %3d, %r,%s %s, %s )," % (bitNum, name, " " * (40 - len(name)), myHex(fr), myHex(to)))

myPrint("    #    " + lastLine)
myPrint("]")


myPrint()
myPrint()


req = urllib2.Request(scriptTagsUrl, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen( req )
broken_html = con.read()

html = etree.HTML(broken_html)
for node in html.xpath("body/div/table/tr/th"):
    if node.text == "Script":
        break

myPrint("otScriptTags = dict([")
table = node.getparent().getparent()
for rowNode in table.xpath("tr"):
    if rowNode[0].tag == "th":
        continue
    row = []
    for col in rowNode:
        row.append(col.text.strip())
    assert len(row) == 2
    script, scriptTag = row
    scriptTag += " " * (4 - len(scriptTag))
    myPrint("    (%r, %r)," % (scriptTag, script))

myPrint("])")


if _outputFile is not None:
    _outputFile.close()
