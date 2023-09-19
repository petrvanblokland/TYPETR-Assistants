# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttxdecompiler.py
#
import os
#import json
from fontTools.ttLib import TTFont
from cStringIO import StringIO
from fontTools.misc.xmlWriter import XMLWriter

#from lib.fontObjects.doodleFontCompiler.ttfCompiler import TTFCompilerSettings as CS
from tnbits.compilers.ttfcompilersettings import TTFCompilerSettings as CS

from tnbits.toolbox.transformer import TX
from tnbits.model.hinting.storage.hintlib import HintLib

class TTXDecompiler(object):

    @classmethod
    def getGPOS(cls, font):
        return cls.getTable('GPOS', font)

    @classmethod
    def getGSUB(cls, font):
        return cls.getTable('GSUB', font)

    @classmethod
    def getTable(self, name, font, path=None):
        # The method answers the TTX decompiled data if it exists in the font.
        # Otherwise try to find the source .TTF or .OTF and decompile from there.
        # This is a temp provision, as long as there is no standard format how
        # to store the data in a UFO. It is not problem to store the XML, but
        # it is clear how to decompile a single table using fontTools.
        gpos = None
        table = None
        if path is None:
            path = font.fileName
        attrName = '_table_' + name
        if hasattr(font, attrName):
            # It's in the font. Answer it.
            table = getattr(font, attrName)(font)
        elif path is not None:
            # Try to find the source TTF file and read it from there
            for extension in ('otf', 'ttf'):
                ttfpath = '.'.join(path.split('.')[:-1]) + '.' + extension
                if os.path.exists(ttfpath):
                    ttffont = TTFont(ttfpath)
                    table = ttffont[name]
                    setattr(self, attrName, table)
                    break
        return table

    @classmethod
    def decompileFromBinary(cls, source, font):
        """
        Extract all tables from the font that have to do with hints and save the
        in the font.lib area, as long as the real UFO location is not determined.
        Test on all tables separate, they may not be available in this font.
        Nor may all glyphs have hinting at this stage.
        This class method gets call by RoboFont on opening a binary font through
        subscription by addObserver(cls, "openBinaryFontCallback", "binaryFontWillOpen")
        QUICKFIND (quick find label in often used files)
        """
        fontLib = font.lib

        # Make assembly conversion happen in the source font
        source.disassembleInstructions = True

        if 'GPOS' in source:
            # As there is no defined format to store the GPOS in the font,
            # for now we just add the TTX-XML decompile, so we can reconstruct
            # the original GPOS when reading the UFO again.
            # Also add the TTX-gpos to font._table_GPOS, if it is needed as Python structure.
            font._table_GPOS = gpos = source['GPOS']
            output = StringIO()
            writer = XMLWriter(output)
            gpos.toXML(writer, source)
            # Store in the font.lib
            HintLib.setData(font, 'GPOS', output.getvalue())

        if 'GSUB' in source:
            # As there is no defined format to store the GSUB in the font,
            # for now we just add the TTX-XML decompile, so we can reconstruct
            # the original GPOS when reading the UFO again.
            font._table_GSUB = gsub = source['GSUB']
            output = StringIO()
            writer = XMLWriter(output)
            gsub.toXML(writer, source)
            # Store in the font.lib
            HintLib.setData(font, 'GSUB', output.getvalue())

        if 'OS/2' in source:
            # @@@ Make this to work with HintLib
            fontLib[CS.fbHintOS2LibKey] = source['OS/2'].__dict__    # Used as object with attribute values
            fontLib[CS.fbHintOS2LibKey + '.dict'] = d = source['OS/2'].__dict__    # Used as object with attribute values
            panose = d.get('panose')
            if panose is not None: # Make the TTX structure flat into the main dictionary
                for panoseKey, panoseValue in panose.__dict__.items():
                    d['panose.%s' % panoseKey] = panoseValue
                del d['panose']

        if 'gasp' in source:
            # @@@ Make this to work with HintLib
            gaspRange = source['gasp'].__dict__.get('gaspRange')
            if gaspRange is not None:
                gaspdict = {}
                for key, value in gaspRange.items():
                    gaspdict[str(key)] = str(value)
                fontLib[CS.fbHintGaspLibKey] = gaspdict    # Used as object with attribute values
                fontLib[CS.fbHintGaspLibKey + '.dict'] = gaspdict    # Used as object with attribute values

        if 'maxp' in source:
            # @@@ Make this to work with HintLib
            fontLib[CS.fbHintMaxp] = maxp = source['maxp'].__dict__    # Used as object with attribute values
            fontLib[CS.fbHintMaxp + '.dict'] = maxp    # Used as object with attribute values

        if 'cvt ' in source:
            # Font lib key with the space after cvt!
            fontLib[CS.fbHintCvtLibKey] = cvtValues = list(source['cvt '].values) # Keep untouched
            # Convert into a dictionary of dictionaries, so we can work on it.
            # The font compiler will compile this back into fontLib['com.robofont.fbhint.cvt ']
            fontLib[CS.fbHintCvtLibKey + '.dict'] = cvtDict = {}
            for index, value in enumerate(cvtValues):
                # Note that all keys in font.lib and glyph.lib dicts MUST be string.
                cvtDict[str(index)] = dict(value=value, name='cvtName%03d' % index, id=index, baseGlyph='')

        if 'fpgm' in source:
            try:
                HintLib.setSrc(font, 'fpgm', TX.program2Source(source['fpgm'].program.getAssembly()))
            except AttributeError:
                pass # No prep program, ignore.

        if 'prep' in source:
            try:
                HintLib.setSrc(font, 'prep', TX.program2Source(source['prep'].program.getAssembly()))
            except AttributeError:
                pass # No prep program, ignore.

        if 'glyf' in source:
            glyphs = source['glyf']
            for glyphName in glyphs.keys():
                dstGlyph = font[glyphName]
                try:
                    HintLib.setSrc(dstGlyph, 'glyf', TX.program2Source(glyphs[glyphName].program.getAssembly()))
                except AttributeError:
                    pass # Glyph has no hinting, ignore.


