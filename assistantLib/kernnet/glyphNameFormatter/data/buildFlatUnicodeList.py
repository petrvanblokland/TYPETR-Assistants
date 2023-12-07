"""
This will parse the large ucd xml into a simple list that is workable and
is fair enough for download and embeding.

starts with the # unicode description/version

format
<unicode> \t <unicode name>

download from
http://www.unicode.org/Public/8.0.0/ucdxml/ucd.all.flat.zip
"""

import os
from xml.etree import cElementTree as ET

# after download it will be in the download folder :)
path = os.path.expanduser("~/Downloads/ucd.all.flat.xml")

tree = ET.parse(path)

flat = []
for i in tree.iter():
    if i.tag.endswith("description"):
        flat.insert(0, "# %s" % i.text)
    if i.tag.endswith("char"):
        n = i.attrib.get("na")
        if n:
            flat.append("%s\t%s" % (i.attrib.get("cp"),  n))


f = open("flatUnicode.txt", "w")
f.write("\n".join(flat))
f.close()

