# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
import os

#from fbproject.fbprojecttool import FBProjectTool
#sources = FBProjectTool.TOOL.getSelectedFonts()
from robofab.world import OpenFont
from tnbits.constants import Constants as C
from tnbits.toolbox.font import FontTX
from tnbits.toolbox.file import File
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.character import CharacterTX
from tnbits.toolbox.series import SeriesTX


sourceBase = "/Users/david/Documents/Dropbox/Typefaces/Toro/SP_Instances"
destBase = u"/Users/david/Desktop/testProof"
File.makeFolder(destBase)
sourcePaths = File.collect(sourceBase, subfolderInclude=False)
#sourcePaths = [x.path for x in AllFonts()]


htmlPart1 = """
<html>
<head>
<style type="text/css">
"""

styleSheet = """

html {
	background-color: #fff;
	font-size: 80px;
	line-height: 1em;
	font-family: Verdana;
	margin: 30px;
}
h1 {
	font-size: 12px;
	line-height: 1em;
	font-family: Verdana;
	font-weight: normal;
	color:#ccc;
	margin: 4em 0 1em 0;
	font-weight: bold;
	letter-spacing: 0;
}
h2 {
	font-size: 12px;
	line-height: 1em;
	font-family: Verdana;
	font-weight: normal;
	color:#ccc;
	margin: 0em 0 1.5em 0;
	letter-spacing: 0;

}

hr { clear: both ; margin: 0; visibility:hidden}

h1 a {color: #ccc;}

.fontSize { width: 100px, background: #ccc; position:fixed; right: 30px; top:30px; 	letter-spacing: 0; text-align: center;}
.fontSize {font-family: "Carob Sans", Monaco, Courier; font-size: 10px; color: #999; line-height: 15px; }
.fontSize a {text-decoration: none; color: #999;}

a {text-decoration:none; color: 000;}
a:hover {color: #333}

"""

htmlPart2 = """
</style>


<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<script type="text/javascript">

$(document).ready(function(){


  // Reset Font Size
  var originalFontSize = $('html').css('font-size');
    $(".resetFont").click(function(){
    $('html').css('font-size', originalFontSize);
  });
  // Increase Font Size
  $(".increaseFont").click(function(){
    var currentFontSize = $('html').css('font-size');
    var currentFontSizeNum = parseFloat(currentFontSize, 10);
    var newFontSize = currentFontSizeNum+1;
    $('html').css('font-size', newFontSize);
	document.getElementById('displayFont').innerHTML = newFontSize;
    return false;
  });
  // Decrease Font Size
  $(".decreaseFont").click(function(){
    var currentFontSize = $('html').css('font-size');
    var currentFontSizeNum = parseFloat(currentFontSize, 10);
    var newFontSize = currentFontSizeNum-1;
    $('html').css('font-size', newFontSize);
	document.getElementById('displayFont').innerHTML = newFontSize;

    return false;
  });


  // Increase Font Size
  $(".increaseFontX10").click(function(){
    var currentFontSize = $('html').css('font-size');
    var currentFontSizeNum = parseFloat(currentFontSize, 10);
    var newFontSize = currentFontSizeNum+10;
    $('html').css('font-size', newFontSize);
	document.getElementById('displayFont').innerHTML = newFontSize;
    return false;
  });
  // Decrease Font Size
  $(".decreaseFontX10").click(function(){
    var currentFontSize = $('html').css('font-size');
    var currentFontSizeNum = parseFloat(currentFontSize, 10);
    var newFontSize = currentFontSizeNum-10;
    $('html').css('font-size', newFontSize);
	document.getElementById('displayFont').innerHTML = newFontSize;

    return false;
  });

    var fontSize = $('html').css('font-size');
    var currentFontSizeNum = parseFloat(fontSize, 10);
  document.getElementById('displayFont').innerHTML = currentFontSizeNum;





  // Reset Letter Spacing
  var originalletterSpacing = $('html').css('letter-spacing');
    $(".resetLetterSpacing").click(function(){
    $('html').css('letter-spacing', originalletterSpacing);
  });
  // Increase Letter Spacing
  $(".increaseLetterSpacing").click(function(){
    var currentletterSpacing = $('html').css('letter-spacing');
    var currentletterSpacingNum = parseFloat(currentletterSpacing, 10);
    var newletterSpacing = currentletterSpacingNum+1;
    $('html').css('letter-spacing', newletterSpacing);
	document.getElementById('displayLetterSpacing').innerHTML = newletterSpacing;
    return false;
  });
  // Decrease Letter Spacing
  $(".decreaseLetterSpacing").click(function(){
    var currentletterSpacing = $('html').css('letter-spacing');
    var currentletterSpacingNum = parseFloat(currentletterSpacing, 10);
    var newletterSpacing = currentletterSpacingNum-1;
    $('html').css('letter-spacing', newletterSpacing);
	document.getElementById('displayLetterSpacing').innerHTML = newletterSpacing;

    return false;
  });

    var letterSpacing = $('html').css('letter-spacing');
    var currentletterSpacingNum = parseFloat(letterSpacing, 10);
  document.getElementById('displayLetterSpacing').innerHTML = currentletterSpacingNum;


});
</script>

</head>
<body>

<div class="fontSize">
<a href="#" class="decreaseFontX10">--</a>
<a href="#" class="decreaseFont">-</a>
<span id="displayFont"></span>
<a href="#" class="increaseFont">+</a>
<a href="#" class="increaseFontX10">++</a>

<br />

<a href="#" class="decreaseLetterSpacing">-</a>
<span id="displayLetterSpacing"></span>
<a href="#" class="increaseLetterSpacing">+</a>


</div>

<h1>Proof</h1>
"""

affs = """
"""

htmlContents = u"""
"""

htmlEnd = """
</body>
</html>
"""

names = []
namesToPaths = {}
for sourcePath in sourcePaths:
    scrap, fileAndExt = os.path.split(sourcePath)
    fileName, ext = os.path.splitext(fileAndExt)
    name = fileName.replace('_', ' ')
    names.append(name)
    namesToPaths[name] = sourcePath

names = SeriesTX.getSortedNames(names)
sourcePaths = []
for name in names:
    sourcePaths.append(namesToPaths[name])

for sourcePath in sourcePaths:
    scrap, fileAndExt = os.path.split(sourcePath)
    fileName, ext = os.path.splitext(fileAndExt)
    htmlContents += """
    <h2>%s</h2>
    """ %(fileName.replace('_', ' '))
    if 1 == 1:
        source = OpenFont(sourcePath, showUI=False)
        fileName = fileName.replace("'", "")
        fileName = fileName.replace(" ", "_")
        sourceDestFileName = fileName+ '_master'
        sourceDestPath = os.path.join(destBase, sourceDestFileName+'.otf')
        htmlContents += '<div style="font-family: %s">' %sourceDestFileName

        pua = TX.hex2dec('E000')
        if hasattr(source, 'glyphOrder'):
            glyphOrder = source.glyphOrder
        elif 'org.robofab.glyphOrder' in source.lib:
            glyphOrder = source.lib['org.robofab.glyphOrder']
        else:
            keys = source.keys()
            keys.sort()
            glyphOrder = keys

        gnames = glyphOrder + list(set(source.keys()) - set(glyphOrder))
        ASCII = range(0, 128)
        gnames2 = [CharacterTX.char2GlyphName(unichr(x)) for x in ASCII]
        #gnames2 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz')

        for gname in gnames:
            if gname in source:
                if source[gname].unicodes:
                    u = '&#%s;' %(source[gname].unicodes[0])
                else:
                    source[gname].unicodes = [pua]
                    pua += 1
                    u = '&#%s;' %(pua)

                htmlContents += """<a name="%s %s" href="robofont://?glyph=%s">%s</a>""" %(fileName, gname, gname, u)

        htmlContents += """</div>"""

        affs += """
        @font-face {
                    font-family: %s;
                    src: url(%s.otf);
                    font-weight: normal;
                    font-style: normal;
                    }
        """ %(sourceDestFileName, sourceDestFileName)

        htmlContents += """
        <hr />
        """

        for f in [source]:
            for attr, value in f.info.asDict().items():
                if 'Name' in attr or 'copyright' in attr:
                    try:
                        setattr(f.info, attr, C.FONTINFO_DEFAULTS[attr])
                    except:
                        pass
            f.info.familyName = 'Scrap'
            f.info.styleName = 'Regular'
            f.features.text = ''

        print(sourceDestPath)
        source.generate(sourceDestPath, 'otf')
        FontTX.compile.checkOutlines(sourceDestPath)
        FontTX.compile.fdkAutohint(sourceDestPath)
        source.close()

html = htmlPart1 + affs + styleSheet + htmlPart2 + htmlContents + htmlEnd

htmlPath = os.path.join(destBase, 'index.html')
File.write(html, htmlPath)

if os.name == 'posix':
    os.system('open "%s"' % htmlPath)
elif os.name == 'nt':
    os.startfile('"' + htmlPath + '"')
