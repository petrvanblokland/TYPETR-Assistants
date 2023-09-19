# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     file.py
#
#     FILE
#     These are common functions for finding, opening, and manipulating files.
#

import os

try:
    from AppKit import NSAlert, NSAlertSecondButtonReturn, NSAlertFirstButtonReturn, NSAlertThirdButtonReturn
except:
    print('Can\'t import AppKit')

try:
    from mojo.roboFont import CurrentFont, AllFonts, OpenFont
except:
    #print('(in toolbox.file.File) Can\'t import mojo.roboFont')
    #print('FIXME: deprecated?')
    # TODO: used by very old scripts, remove?
    pass

try:
    from vanilla.dialogs import getFile, getFileOrFolder, putFile
except:
    print('Can\'t import vanilla dialogs')

class File:
    """
    `File` provides methods and shortcuts for dealing with files and paths.
    """

    @classmethod
    def checkFileName(cls, n,
                    extensionInclude=[],
                    extensionExclude=[],
                    extensionRequired=False,
                    nameInclude=[],
                    nameExclude=[],
                    startsWithInclude=[],
                    startsWithExclude=[],
                    ):
        """
        `checkFileName` analyzes a filename to see if it is meets search parameters in the name (_
        nameInclude_, _nameExclude_), beginning of the name (_startsWithInclude_, _startsWithExclude
        _), and extension (_extensionExclude_, _extensionExclude_, _extensionRequired_).
        """
        includeTest = True
        baseName, ext = os.path.splitext(n)
        # is the extension required
        if not ext and extensionRequired:
            return False
        # extension include/exclude
        if ext in extensionExclude:
            return False
        if extensionInclude and ext not in extensionInclude:
            return False
        # name include/exclude
        for e in nameInclude:
            if n.find(e) == -1:
                return False
        for e in nameExclude:
            if n.find(e) != -1:
                return False
        # startsWith include/exclude
        for e in startsWithInclude:
            if len(n) >= len(e) and n[:len(e)] != e:
                return False
        for e in startsWithExclude:
            if not (len(n) < len(e) or len(n) >= len(e) and n[:len(e)] != e):
                return False
        # if passes all tests, return True
        return True

    @classmethod
    def collect(cls,
                     paths=[],
                     subfolderInclude=True,
                     extensionInclude=['.ufo'],
                     extensionExclude=[],
                     nameInclude=[],
                     nameExclude=[],
                     startsWithExclude=['.'],
                     startsWithInclude=[],
                     excludeDirExtension=['.ufo'],
                     note="Collect files..."):
        """
        `collect` is a powerful method that returns a list of all paths within a given directory that
        match the search parameters (see `checkFileName` above). By default, it collects all fonts with a
        '.ufo' extension. if _subfolderInclude_ is true, this will recursively search all subfolders, and include
        them in the list.
        """
        files = []
        if isinstance(paths, str):
            paths = [paths]
        if not paths:
            paths = getFileOrFolder(note, allowsMultipleSelection=True)
        if not paths:
            return []
        for path in paths:
            basePath, fileName = os.path.split(path)
            baseFileName, ext = os.path.splitext(fileName)
            if os.path.isdir(path) and ext not in excludeDirExtension:
                if cls.checkFileName(fileName,
                                 nameInclude=nameInclude,
                                 nameExclude=nameExclude,
                                 startsWithExclude=startsWithExclude,
                                 startsWithInclude=startsWithInclude,
                                 ):
                    names = os.listdir(path)
                    for n in names:
                        npath = os.path.join(path, n)
                        nBaseName, nExt = os.path.splitext(n)
                        if os.path.isdir(npath) and nExt not in excludeDirExtension:
                            if subfolderInclude:
                                files += cls.collect(
                                             paths=[npath],
                                             subfolderInclude=subfolderInclude,
                                             extensionInclude=extensionInclude,
                                             extensionExclude=extensionExclude,
                                             nameInclude=nameInclude,
                                             nameExclude=nameExclude,
                                             startsWithExclude=startsWithExclude,
                                             startsWithInclude=startsWithInclude,
                                             note=note)
                        else:
                            if cls.checkFileName(n,
                                            extensionInclude=extensionInclude,
                                            extensionExclude=extensionExclude,
                                            nameInclude=nameInclude,
                                            nameExclude=nameExclude,
                                            startsWithExclude=startsWithExclude,
                                            startsWithInclude=startsWithInclude):
                                files.append(npath)
            else:
                if cls.checkFileName(fileName,
                         extensionInclude=extensionInclude,
                         extensionExclude=extensionExclude,
                         nameInclude=nameInclude,
                         nameExclude=nameExclude,
                         startsWithExclude=startsWithExclude,
                         startsWithInclude=startsWithInclude):
                    files.append(path)
        return files

    @classmethod
    def collectOptions(self,
                     subfolderInclude=True,
                     extensionInclude=['.ufo'],
                     extensionExclude=[],
                     nameInclude=[],
                     nameExclude=[],
                     startsWithExclude=['.'],
                     startsWithInclude=[],
                     excludeDirExtension=['.ufo'],
                     note="Collect files...",
    returnSelectionMethod=False
    ):
        buttonTitlesValues = [('All Open', 0), ('Current', 1), ('Selection', 2), ('Cancel', 4)]
        messageText = 'Select fonts from...'
        result = []
        method = None
        alert = NSAlert.alloc().init()
        alert.setMessageText_(messageText)
        for buttonTitle, value in buttonTitlesValues:
            alert.addButtonWithTitle_(buttonTitle)
        code = alert.runModal()
        if code == NSAlertFirstButtonReturn:
            result = AllFonts()
            method = 'AllFonts'
        elif code == NSAlertSecondButtonReturn:
            f = CurrentFont()
            if f is not None:
                result = [CurrentFont()]
            else:
                result = []
            method = 'CurrentFont'
        elif code == NSAlertThirdButtonReturn:
            result = File.collect(
                     subfolderInclude=subfolderInclude,
                     extensionInclude=extensionInclude,
                     extensionExclude=extensionExclude,
                     nameInclude=nameInclude,
                     nameExclude=nameExclude,
                     startsWithExclude=startsWithExclude,
                     startsWithInclude=startsWithInclude,
                     excludeDirExtension=excludeDirExtension,
                     note=note
                     )
            method = 'Selection'
        if returnSelectionMethod:
            return result, method
        else:
            return result
        return []

    @classmethod
    def getFont(cls, f, showUI=True):
        if f is None:
            return f
        try:
            if f.path:
                pass
            return f
        except:
            for potentialFont in AllFonts():
                if potentialFont.path is not None and potentialFont.path == f:
                    return potentialFont
        return OpenFont(f, showInterface=showUI)


    @classmethod
    def saveIfUnopened(cls, f):
        try:
            if f.document() is None:
                f.save()
        except:
            pass

    @classmethod
    def getPath(cls, f):
        try:
            return f.path
        except:
            return f

    @classmethod
    def read(cls, filePath=None, fileMessage="Read file from..."):
        """
        `read` reads the file at the given path into a string. Not too much different than doing it
        manually, but it will provide a dialog if no path is specified. This is a convenience function.
        """
        if not filePath:
            filePath = getFile(fileMessage)[0]
            print(filePath)
        if filePath:
            f = open(filePath, 'rU')
            read = f.read()
            return read
        else:
            print(filePath, ': Read unsuccessful.')

    @classmethod
    def write(cls, toPrint='', filePath=None, fileMessage='Write file to...', fileName=''):
        """`write` writes _toPrint_ into a file at the given path. Not too much
        different than doing it manually, but it will provide a dialog if no
        path is specified."""
        if not filePath:
            filePath = putFile(fileMessage, fileName)
        if filePath:
            f = open(filePath, 'wb')
            f.write(toPrint)
            #f.write('\r')
            f.close()
            return toPrint
        else:
            print(filePath, ': Write unsuccessful.')
            return None

    @classmethod
    def rename(cls, sourcePath, destPath):
        os.system('mv "%s" "%s"' % (sourcePath, destPath))

    @classmethod
    def delete(cls, filePath):
        os.system('rm "%s"' % (filePath))

    @classmethod
    def convertLineEndings(cls, temp, mode=1):
        """
        `convertLineEndings` converts line endings to \\r. Helps make metrics machine kerning lists
        readable, among other things.
        """
        import string
        # modes:  0 - Unix, 1 - Mac, 2 - DOS
        if mode == 0:
            temp = string.replace(temp, '\r\n', '\n')
            temp = string.replace(temp, '\r', '\n')
        elif mode == 1:
            temp = string.replace(temp, '\r\n', '\r')
            temp = string.replace(temp, '\n', '\r')
        elif mode == 2:
            import re
            temp = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", temp)
        return temp

    @classmethod
    def getCollection(cls, path=None):
        """
        `getCollection` reads a list of paths from a plist collection file.
        """
        foundPaths = []
        from fontTools.ufoLib.plistlib import readPlist, writePlist
        if not path:
            path = getFile('Get collection plist')
        if path:
            d = readPlist(path)
            if 'paths' in d:
                for p in d['paths']:
                    if os.path.exists(p):
                        foundPaths.append(p)
        return foundPaths

    ####################################
    # Relative Path manipulations
    ####################################

    @classmethod
    def splitPathElements(cls, p):
        """
        `splitPathElements` takes a path and splits it into a list of individual elements (separating
        the filename and each containing folder). It's like `os.path.split` but it works with more than two
        parts.
        """
        go = True
        elements = []
        while go is True:
            directory, base = os.path.split(p)
            if base == '':
                go = False
            else:
                elements.append(base)
                p = directory
        elements.reverse()
        return elements

    @classmethod
    def joinPathElements(cls, elements):
        """
        Given a list of individual path elements, `joinPathElements` . It's like `os.path.join
        ` but it works with more than two parts.
        """
        p = ''
        for e in elements:
            p = os.path.join(p, e)
        return p

    @classmethod
    def getPathAlignment(cls, p1, p2):
        """
        `getPathAlignment` compares two paths and return 3 parts: the portion that exists in both paths,
        the portion that exists in path 1, and the portion that exists in path 2.
        """
        # split paths into elements
        e1 = cls.splitPathElements(p1)
        e2 = cls.splitPathElements(p2)
        # determine relative lengths
        if len(e1) > len(e2):
            longer = e1[:]
            shorter = e2[:]
        else:
            longer = e2[:]
            shorter = e1[:]
        # find congruents
        congruent = True
        congruentElements = []
        longerMin = []
        shorterMin = []
        for x in range(0, len(shorter)):
            shorterElement = shorter[x]
            longerElement = longer[x]
            if congruent and longerElement == shorterElement:
                    congruentElements.append(shorterElement)
            else:
                congruent = False
                shorterMin.append(shorterElement)
                longerMin.append(longerElement)
        x += 1
        for y in range(x, len(longer)):
            if len(longer) > y:
                longerElement = longer[y]
                longerMin.append(longerElement)
        if len(e1) > len(e2):
            e1 = longerMin
            e2 = shorterMin
        else:
            e1 = shorterMin
            e2 = longerMin
        return congruentElements, e1, e2

    @classmethod
    def getRelativePath(cls, p1, p2):
        """
        `getRelativePath` returns a relative path ('../') to p1, relative to p2. There has got to be a better way to do this.
        """
        p1Base = None
        p2Base = None
        if not os.path.isdir(p1):
            p1, p1Base = os.path.split(p1)
        if not os.path.isdir(p2):
            p2, p2Base = os.path.split(p2)
        e1 = cls.splitPathElements(p1)
        e2 = cls.splitPathElements(p2)
        # ??
        if len(e1) > len(e2):
            longer = e1[:]
            shorter = e2[:]
        else:
            longer = e2[:]
            shorter = e1[:]
        congruent = True
        congruentElements = []
        longerMin = []
        shorterMin = []
        for x in range(0, len(shorter)):
            shorterElement = shorter[x]
            longerElement = longer[x]
            if congruent and longerElement == shorterElement:
                    congruentElements.append(shorterElement)
            else:
                congruent = False
                shorterMin.append(shorterElement)
                longerMin.append(longerElement)
       # ??
        x += 1
        for y in range(x, len(longer)):
            if len(longer) > y:
                longerElement = longer[y]
                longerMin.append(longerElement)
       # which is shorter
        if len(e1) > len(e2):
            e1 = longerMin
            e2 = shorterMin
        else:
            e1 = shorterMin
            e2 = longerMin
        # get relative
        rel = ''
        for t in range(0, len(e2)):
            rel += '../'
        p1Short = cls.joinPathElements(e1)
        relDir = os.path.join(rel, p1Short)
        if p1Base:
            relPath = os.path.join(relDir, p1Base)
        else:
            relPath = relDir
        return relPath

    @classmethod
    def getAbsolutePath(cls, p, start):
        """
        Given a relative path and a starting point, `getAbsolutePath` returns an absolute path to the former from the starting point. Again, there has got to be better way to do this.
        """
        # remove any files so we're just dealing with directories
        pBase = None
        startBase = None
        if not os.path.isdir(p):
            p, pBase = os.path.split(p)
        if not os.path.isdir(start):
            start, startBase = os.path.split(start)
        e = cls.splitPathElements(p)
        startElements = cls.splitPathElements(start)
        # subtract ../s from the starting path
        upDirCount = 0
        remainingElements = []
        for x in e:
            if x == '..':
                upDirCount += 1
            else:
                remainingElements.append(x)
        if upDirCount == 0:
            baseElements = startElements
        else:
            baseElements = startElements[:-upDirCount]
        base = cls.joinPathElements(baseElements)
        remaining = cls.joinPathElements(remainingElements)
        absDir = os.path.join(base, remaining)
        if pBase:
            absPath = os.path.join(absDir, pBase)
        else:
            absPath = absDir
        if absPath[0] != '/':
            absPath = '/' + absPath
        return absPath

    ##########################
    ##########################
    ##########################
    # FOLDERS

    @classmethod
    def makeFolder(cls, path):
        """
        `makeFolder` is a shortcut to making a folder (but only if it doesn't exist already).
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def clearFolder(cls, path):
        """
        `clearFolder` removes all files in a given folder.
        """
        names = os.listdir(path)
        for n in names:
            filePath = os.path.join(path, n)
            os.remove(filePath)

    @classmethod
    def splitPathFileExt(cls, path):
        """`splitPathFileExt` is a shortcut that returns a base path, base
        file name, and extension. It is a combination of `os.path.split` and
        `os.path.splitext`."""
        basePath, fileName = os.path.split(path)
        baseFileName, ext = os.path.splitext(fileName)
        return basePath, baseFileName, ext

    @classmethod
    def pathAppendDate(cls, path, date=None):
        """
        `pathAppendDate` appends the date to the end of the path, but before the extension.

        FIXME: Should this be replaced by functions in `toolbox.dating`?
        """
        basePath, baseFile, ext = cls.splitPathFileExt(path)

        if len(baseFile) >= 7 and baseFile[-7] == '_' and baseFile[-6:].isdigit():
            return path

        if not date:
            from datetime import datetime
            date = datetime.now()

        newBaseFile = baseFile + '_' + date.strftime('%Y-%m-%d')
        newPath = os.path.join(basePath, newBaseFile + ext)
        if os.path.exists(newPath):
            newBaseFile = baseFile + '_' + date.strftime('%Y-%m-%dT%H%M%S%Z')
            newPath = os.path.join(basePath, newBaseFile + ext)
        return newPath

    @classmethod
    def zipFolder(cls, source, destBase=None, zipExt='.zip', appendDate=False):
        """
        `zipFolder` creates a zip file of the given folder and its contents.
        """
        basePath, baseFileAndExt = os.path.split(source)
        baseFile, ext = os.path.splitext(baseFileAndExt)
        if destBase:
            dest = os.path.join(destBase, baseFile + zipExt)
        else:
            dest = os.path.join(basePath, baseFile + zipExt)
        if appendDate or os.path.exists(dest):
            dest = cls.pathAppendDate(dest)
        import zipfile
        def zipdir(path, zip):
            os.chdir(path)
            for root, dirs, files in os.walk(path):
                for file in files:
                    zip.write(os.path.join(root.replace(path,'').lstrip('/'), file))
        zip = zipfile.ZipFile(dest, 'w')
        zipdir(source, zip)
        zip.close()


    @classmethod
    def launch(cls, path):
        if os.name == 'posix':
            os.system('open "%s"' % path)
        elif os.name == 'nt':
            os.startfile('"' + path + '"')

if __name__ == "__main__":
    fontOrPaths, selectionMethod = File.collectOptions(returnSelectionMethod=True)

    for i, fontOrPath in enumerate(fontOrPaths):
        f = File.getFont(fontOrPath, showUI=False)
        print(i, f)
        f.close()
    print('done')
