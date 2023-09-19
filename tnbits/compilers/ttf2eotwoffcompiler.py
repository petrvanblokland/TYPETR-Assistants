# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttfwoffeotcompiler.py
#
from fontTools.ttLib import TTFont
import struct, os, tempfile
from fontTools.ttLib.sfnt import calcChecksum

class TTF2EOTWOFFCompiler(object):

    TTF_FIELDS = {
        'copyright': 0,
        'familyName': 1,
        'stylename': 2,
        'fullname': 4,
        'family': 1,
        'style': 2,
        'full': 4,
        'version': 5,
        'psname': 6,
        'trademark': 7,
        'manufacturer': 8,
        'foundry': 8,
        'designer': 9,
        'description': 10,
        'vendorurl': 11,
        'designerurl': 12,
        'license': 13,
        'licenseurl': 14,

        'name': (
            # PlatformID, EncodingID
            # http://www.microsoft.com/typography/otspec/name.htm
            (1,0), #mac,roman
            (3,1), #windows, unicode
        ),
        'cmap': (
                #PlatformID, EncodingID
                # http://www.microsoft.com/typography/otspec/name.htm
                (0,3), #Unicode, BMP
                (0,4), #Unicode, full
                (0,6), #Unicode, full
                (3,1), #Windows, Unicode BMP
                (3,0), #Windows, Symbol
                )
    }
    @classmethod
    def createEOTFromPath(cls, ttfpath, dstpath):
        from time import time
        t = time()
        ttf = TTFont(ttfpath)
        cls.createEOT(ttf, dstpath)
        print('EOT %02f' % (time() - t))

    @classmethod
    def createWOFFFromPath(cls, ttfpath, dstpath):
        from time import time
        t = time()
        ttf = TTFont(ttfpath)
        cls.createWOFF(ttf, dstpath)
        print('WOFF %02f' % (time() - t))

    @classmethod
    def getTTFNameField(cls,ttfont,nameid):

        if nameid in cls.TTF_FIELDS: #convert friendly name to ID
            nameid = cls.TTF_FIELDS[nameid]

        for args in cls.TTF_FIELDS['name']:
            name = ttfont['name'].getName(nameid,*args)

            if name is not None:
                return name.string.replace('\x00','') #some font names seem to have nulls in?

        return None

    @classmethod
    def createEOT(cls,ttf,dest):
        #EOT

        tempTTF = tempfile.TemporaryFile()
        ttf.save(tempTTF)
        tempTTF.seek(0,2)
        ttfsize = tempTTF.tell()

        eot = open(dest,"wb")

        # EOT format 20001 (same as used by ttf2eot)
        # http://www.w3.org/Submission/EOT/#Version21

        def write(format,*args):
            #EOT is little-endian, whereas OT is big
            if format[0] not in ('<','>'):
                format = '<' + format

            data = struct.pack(format,*args)
            eot.write(data)


        write('L',0) #EOT total size placeholder
        write('L',ttfsize) #FontDataSize
        write('L',0x00020001) #EOT version
        write('L',0x00000000) #Processing flags (web object)
        write('10x') #panose numbers, all 0
        write('B',1) #charset, 0x01 == default
        write('B',ttf['OS/2'].fsSelection & 1) #italic; this has to actually match the TTF
        write('L',ttf['OS/2'].usWeightClass) #weight; this has to actually match the TTF
        write('H',0x00) #fsType. Print & preview, editable, or none?
        write('H',0x504C) #magic number for EOT
        write('L',ttf['OS/2'].ulUnicodeRange1)
        write('L',ttf['OS/2'].ulUnicodeRange2)
        write('L',ttf['OS/2'].ulUnicodeRange3)
        write('L',ttf['OS/2'].ulUnicodeRange4)
        write('L',ttf['OS/2'].ulCodePageRange1)
        write('L',ttf['OS/2'].ulCodePageRange2)
        #write('6L',0,0,0,0,0,0) #unicode and codepage ranges zeroed
        write('L',ttf['head'].checkSumAdjustment)
        write('4L',0,0,0,0) #reserved

        #all these string lengths below are doubled due to UTF-16 representation
        family = cls.getTTFNameField(ttf,'familyName')
        style = cls.getTTFNameField(ttf,'stylename')
        fullname = cls.getTTFNameField(ttf,'fullname')
        version = cls.getTTFNameField(ttf,'version')
        urls = ""

        family = family.encode("utf_16_le")
        style = style.encode("utf_16_le")
        fullname = fullname.encode("utf_16_le")
        version = version.encode("utf_16_le")
        root = "\0".join(urls).encode("utf_16_le")

        write('H',0) #padding1
        write('H',len(family)) #family name length
        write('{0}s'.format(len(family)),family) #family name
        write('H',0) #padding2
        write('H',len(style)) #style name length
        write('{0}s'.format(len(style)),style) #style name
        write('H',0) #padding3
        write('H',len(fullname)) #full name length
        write('{0}s'.format(len(fullname)),fullname) #fullname name
        write('H',0) #padding4
        write('H',len(version)) #version name length
        write('{0}s'.format(len(version)),version) #version name
        write('H',0) #padding5
        write('H',len(root)) #root name length (allowed URLs)
        write('{0}s'.format(len(root)),root) #root name

        #END OF HEADER

        #append the whole TTF file to the EOT
        tempTTF.seek(0)
        while True:
            chunk = tempTTF.read(16384)
            if len(chunk) == 0:
                break
            eot.write(chunk)


        #update total size
        fullsize = eot.tell()
        eot.seek(0)
        write('L',fullsize)

        eot.close()
        tempTTF.close()

    @classmethod
    def createWOFF(cls,ttf,dest):
        #WOFF

        tempTTF = tempfile.TemporaryFile()
        ttf.save(tempTTF)
        tempTTF.seek(0,2)
        ttfsize = tempTTF.tell()
        tempTTF.close()

        woff = open(dest,"wb")

        # woff format
        # http://people.mozilla.com/~jkew/woff/woff-spec-latest.html

        def write(format,*args):
            #woff is big-endian, as is OT
            if format[0] not in ('<','>'):
                format = '>' + format

            data = struct.pack(format,*args)
            woff.write(data)


        tabletags = [k for k in ttf.keys() if len(k)==4 and k != 'DSIG']
        numtables = len(tabletags)

        #WOFF HEADER

        write('L',0x774F4646) #0 signature 'wOFF'
        write('L',0x00010000) #4 flavor: 0x00010000 for TTF, 0x4F54544F for CFF
        write('L',0) #8 total size placeholder
        write('H',numtables) #12 number of tables
        write('H',0) #14 reserved
        write('L',ttfsize) #16 total uncompressed original font size placeholder
        write('H',1) #20 major version (arbitrary)
        write('H',0) #22 minor version (arbitrary)
        write('L',0) #24 metadata offset placeholder (0 if none)
        write('L',0) #28 metadata length placeholder
        write('L',0) #32 metadata original length placeholder
        write('L',0) #36 private data offset placeholder (0 if none)
        write('L',0) #40 private data length placeholder

        headersize = woff.tell()

        #44 TABLE DIRECTORY
        tabledir = {}
        for tag in sorted(tabletags): #directory in alpha order
            #just put in placeholders for now; we'll fill in the values when we go through the tables later
            tabledir[tag] = woff.tell()
            write('5L',0,0,0,0,0)

        directorySize = woff.tell() - headersize

        #FONT TABLES
        for tag in tabletags: #original font order
            data = ttf.getTableData(tag)
            datalength = len(data)

            myOffset = woff.tell()

            remainder = myOffset % 4
            if remainder > 0:
                woff.write('\0'*(4-remainder))
                myOffset += (4-remainder)

            #go back and write the table directory entries
            woff.seek(tabledir[tag])
            write('4s',tag)
            write('L',myOffset) #table offset
            write('L',datalength) #compressed length
            write('L',datalength) #uncompressed length
            if tag == 'head':
                write('L',calcChecksum(data[:8] + '\0\0\0\0' + data[12:]))  #40 + 20(i-1) + 12 original checksum
            else:
                write('L',calcChecksum(data)) #40 + 20(i-1) + 12 original checksum

            #come back to the present
            woff.seek(myOffset)
            woff.write(data)

        fullsize = woff.tell()
        remainder = fullsize % 4
        if remainder > 0:
            woff.write('\0'*(4-remainder))
            fullsize += (4-remainder)



        #go back and update some statistics
        woff.seek(8)
        write('L',fullsize) #full file size

        #woff.seek(16)
        #write('L',fullsize-directorySize-headersize) #data size

        woff.close()

