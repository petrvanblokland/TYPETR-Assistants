# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    extensionmaker.py
#

import time, shutil
from fontTools.ufoLib.plistlib import readPlist, writePlist
"""

    PlugInMaker for Doodle / RoboFont
    Independent from the builder in the app itself.

    Take code from the svn tree
    Copy to new plugin build location
    Update version / build numbers
    Update info.plist

    When finished see if the Doodle app is running,
    see if can install the plugin from the script.



"""
import os

class ExtensionMaker(object):
    EXTENSION   = "RoboFontExt"
    LIBNAME     = "lib"
    APPNAME     = "RoboFont"
    DEVELOPER   = "Petr van Blokland & David Berlow"

    def __init__(self, name, versionNumber, infoDir, srcDir, dstDir, makeRelease=False, developer=None):
        self.name = name
        self.versionNumber = versionNumber
        self.buildNumber = self.makeBuildNumber()
        self.srcDir = srcDir
        self.dstDir = dstDir
        self.buildDir = dstDir + '/build'
        self.infoDir = infoDir

        # Find a next id for the file, in case the button is hit again
        # within a second. This can be done better, by removing the
        # existing directory first, instead of creating a new file name.
        cnt = 0
        while True:
            self.fileName = "%s_%s_%s.%02d.%s"%(self.name, self.versionNumber, self.buildNumber, cnt, self.EXTENSION)
            self.pluginRoot = os.path.join(self.buildDir, self.fileName)
            if os.path.exists(self.pluginRoot):
                cnt += 1
            else:
                break

        self.libRoot = self.srcDir #os.path.join(self.srcDir, self.LIBNAME)
        self.libDst = os.path.join(self.pluginRoot, self.LIBNAME)
        self.libFBHint = os.path.join(self.libDst, 'fbhint')
        self.makeRelease = makeRelease      # remove .py, hide build / version numbers
        self.developer = developer or self.DEVELOPER

    def make(self):
        # make the dirs we need
        if not os.path.exists(self.libDst):
            os.makedirs(self.libDst)
        self.makeInfo()
        print('FBHint:', self.libFBHint)
        print(self.libRoot)
        print(self.libDst)
        shutil.copytree(self.libRoot, self.libFBHint)
        # Copy start script
        startSrc = os.path.join(self.libRoot, 'hinter', 'tool', "activatehinter.py")
        shutil.copy(startSrc, self.libDst)

    def makeInfo(self):
        infoPathRead = os.path.join(self.infoDir, "info.plist")
        infoPathWrite = os.path.join(self.pluginRoot, "info.plist")
        if not os.path.exists(infoPathRead):
            print("Warning: can't find info.plist")
            return
        self.info = readPlist(infoPathRead)
        self.info['timeStamp'] = time.time()
        self.info['developer'] = self.developer
        self.info['version'] = self.buildNumber
        self.info['name'] = self.name

        f = open(infoPathWrite, 'w')
        writePlist(self.info, f)
        f.close()

    def copyStartScript(self):
        shutil.copy()
    def makeBuildNumber(self):
        # same format as Doodle's build number
        #return time.strftime("%y%d%m%H%M%S", time.localtime())
        return time.strftime("%y%d%m%H%M", time.localtime())

    def installPlugInByCallingApp(self, appName=None):
        from AppKit import NSWorkspace
        if appName is None:
            appName = self.APPNAME
        ws = NSWorkspace.sharedWorkspace()
        ws.openFile_withApplication_(self.pluginRoot, appName)
        print("Done")


