#coding: utf-8
import os

import importlib
import time

import subprocess

from glyphNameFormatter import GlyphName, __version__
from glyphNameFormatter.unicodeRangeNames import getAllRangeNames, getRangeByName, rangeNameToModuleName
from glyphNameFormatter.data.scriptPrefixes import SCRIPTSEPARATOR, SCRIPTASPREFIX
from glyphNameFormatter.exporters.analyseConflicts import findConflict


def getExportVersionNumber():
    commitNumber = subprocess.check_output(["git", "rev-list", "HEAD", "--count"], cwd=os.path.dirname(__file__))
    commitNumber = commitNumber.strip()
    return "%s - git commit: %s" % (__version__, commitNumber)

_versionNumber = getExportVersionNumber()


def getGithubLink():
    commithash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],  cwd=os.path.dirname(__file__))
    commithash = commithash.strip()
    return "https://github.com/LettError/glyphNameFormatter/tree/%s" % commithash

_githubLink = getGithubLink()


def generateFlat(path, onlySupported=True, scriptSeparator=None, scriptAsPrefix=None, status=0):
    data = [
        "# Glyph Name Formatted Unicode List - GNFUL",
        "# GlyphNameFormatter version %s" % _versionNumber,
        "# Source code: %s" % _githubLink,
        "# Generated on %s" % time.strftime("%Y %m %d %H:%M:%S"),
        "# <glyphName> <hex unicode>",
    ]
    if scriptSeparator is not None:
        data.append("# Separator \"%s\"" % scriptSeparator)
    if scriptAsPrefix is not None:
        data.append("# Prefixed \"%s\"" % scriptAsPrefix)
    data.append("#")
    for rangeName in getAllRangeNames():
        if onlySupported:
            moduleName = rangeNameToModuleName(rangeName)
            try:
                module = importlib.import_module('glyphNameFormatter.rangeProcessors.%s' % moduleName)
            except:
                continue
        data.append("# %s" % rangeName)
        start, end = getRangeByName(rangeName)
        for u in range(start, end+1):
            g = GlyphName(uniNumber=u, scriptSeparator=scriptSeparator, scriptAsPrefix=scriptAsPrefix)
            g.compress()  # should auto compress
            if status is not None:
                if g.status < status:
                    # if the glyph has a status that is less than what we're looking for
                    # then do not include it in the list.
                    continue
            name = g.getName(extension=True)
            if name is None:
                continue
            data.append("%s %04X" % (name, u))

    f = open(path, "w")
    f.write("\n".join(data))
    f.close()

if __name__ == "__main__":

    findConflict(makeModule=True)

    # generate a flat export
    generateFlat("./../names/glyphNamesToUnicode.txt")
    generateFlat("./../names/glyphNamesToUnicode_experimental.txt", status=-1)

    # and because this is a generator we can make any flavor we want:
    for separator, sn in [
            (":", "colon"),
            ("-", "hyphen"),
            ]:
        for asPrefix, pn in [
                (True, "prefixed"),
                (False, "suffixed")
                ]:
            for onlySupported, sp in [
                    (True, "AGDonly"),
                    #(False, "full")    # large files, proceed at own leisurely pace.
                    ]:
                path = "./../names/glyphNamesToUnicode_%s_%s_%s.txt" % (sp, sn, pn)
                generateFlat(path, onlySupported=onlySupported,
                    scriptSeparator=separator,
                    scriptAsPrefix=asPrefix,
                    status=0
                    )
