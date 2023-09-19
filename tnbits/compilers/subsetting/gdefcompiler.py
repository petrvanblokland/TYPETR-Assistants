# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     gdefcompiler.py
#
#     http://www.microsoft.com/typography/otspec/gpos.htm
#
import copy
from tnbits.compilers.subsetting.states import *
from tnbits.compilers.subsetting.gtablecompiler import GTableBaseCompiler

tobedeveloped = True

class GDEFCompiler(GTableBaseCompiler):

    TABLE_TAG = 'GDEF'

    #    C O M P I L E  2  T T X / X M L

    def decompile(self, gTable):
        # Decompile the fonttools gTable (GDEF) into a construct of dict, list and State instances.
        # The result of the decompile is a State instance "gdef", that holds gsub.scripts
        # for the separate decompiled scripts.
        classDefs = copy.copy(gTable.table.GlyphClassDef.classDefs)
        if gTable.table.LigCaretList is not None:
            ligCaretList = copy.copy(gTable.table.LigCaretList.Coverage.glyphs)
        else:
            ligCaretList = None
        if gTable.table.AttachList is not None:
            attachList = copy.copy(gTable.table.AttachList) # None so far. What is the expected layout?
        else:
            attachList = None
        # gTable.table.LigCaretList.LigGlyph???
        markAttachClassDef = copy.copy(gTable.table.MarkAttachClassDef.classDefs)
        return GDEFState(classDefs, gTable.table.GlyphClassDef.Format,
            ligCaretList, attachList, markAttachClassDef, gTable.table.MarkAttachClassDef.Format)

    def compile2XML(self, g):
        # Compile the "g" State to the FontTools XML, so we can use that to compile to fonttools objects.
        self.newOutput() # Reset output stream
        self.writeXmlHeader()
        self.write('<ttFont sfntVersion="OTTO" ttLibVersion="2.2">\n')
        self.tagRoot()
        self.tagVersion('1.0')
        if g.classDef:
            self.tagGlyphClassDef(g.classDefFormat)
            for glyphName, classDef in sorted(g.classDef.items()):
                self.tagClassDef(glyphName, classDef)
        self._tagGlyphClassDef()
        if g.ligCaretList: # For now...
            raise 'tobeimplemented'
        else:
            self.write("""\t<LigCaretList>\n\t\t<Coverage Format="1">\n\t\t</Coverage>\n\t\t<!-- LigGlyphCount=0 -->\n\t</LigCaretList>\n""")
        if g.attachList: # For now...
            raise 'tobeimplemented'
        else:
            self.write("""\t<AttachList><Coverage Format="1">\n\t\t</Coverage>\n\t\t<!-- LigGlyphCount=0 -->\n\t\t</AttachList>\n""")

        if g.markAttachClassDef:
            self.tagMarkAttachClassDef(g.markAttachClassDefFormat)
            for glyphName, classDef in sorted(g.markAttachClassDef.items()):
                self.tagClassDef(glyphName, classDef)
            self._tagMarkAttachClassDef()
        self._tagRoot()
        self.write('</ttFont>\n')
        return self.getOutput()

