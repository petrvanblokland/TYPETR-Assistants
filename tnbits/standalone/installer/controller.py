# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Type Network installer appication.
#    Copyright (c) 2017+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    controller.py
#

import os, os.path
import glob
import subprocess
import traceback
from vanilla import Window, Button, SecureEditText
from vanilla.dialogs import getFolder
from AppKit import NSUserDefaults
from tnbits.base.console import Console
from tnbits.base.constants.tool import *
from tnbits.base.windows import *
from tnbits.environment.scan import Scan
from tnbits.standalone.installer.exception import InstallerException
from tnbits import VERSION, PHASE

class Controller(object):
    """Implements the Type Network installer."""
    echoPythonPath = 'echo $PYTHONPATH'
    tnToolsPackage = 'tntools'
    tnToolsRelease = 'tnTools-%s-%s' % (VERSION, PHASE)
    tnToolsZip = '%s.zip' % tnToolsRelease
    tmpBase = '/tmp'

    def __init__(self, delegate):
        """Initializes objects and connects them."""
        self.delegate = delegate
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        setBackgroundColor(self.window)
        self._doVerbose = True
        self._doSuppressWarnings = False
        self.password = ''
        self.mode = ''
        self.cmds = []
        self.build()
        self.window.open()
        self.sitePackages = self.getSitePackages()
        print(self.sitePackages)

    def getSitePackages(self):
        base = '/Library/Frameworks/Python.framework/Versions'
        path = base

        # FIXME: what if there are multiple 3.x pythons?
        for dirName in os.listdir(base):
            v = '%s/%s' % (base, dirName)
            self.reporter.addLine(('%s\n' % v, 'highlight'))

            if dirName.startswith('3'):
                path  = '%s/%s' % (v, 'lib/python3.6/site-packages')

        self.reporter.setLines()
        return path

    def build(self):
        """Sets up GUI."""
        x = PADDING
        y = PADDING
        dx = BUTTON_WIDTH + PADDING
        self.window.scanPackages = Button((x, y, BUTTON_WIDTH, BUTTON_HEIGHT_REGULAR),
                'scan', callback=self.doScanCallback)
        x += dx
        self.window.install = Button((x, y, BUTTON_WIDTH, BUTTON_HEIGHT_REGULAR),
                'install', callback=self.doRunInstallCallback)
        x += dx
        self.window.uninstall = Button((x, y, BUTTON_WIDTH, BUTTON_HEIGHT_REGULAR),
                'uninstall', callback=self.doRunUninstallCallback)

        pos = (0, 15, -0, -0)
        self.reporter = Console(self, pos=pos)
        self.window.reporter = self.reporter.getView()
        self.scan = Scan(self.reporter)

    # Password.

    def askPass(self):
        """Dialog with NSSecureTextField."""
        padding = 4
        buttonWidth = 80
        dx = -buttonWidth - padding
        x = dx
        y = 40
        self.askPassWindow = Window((300, 75), minSize=(300, 75), maxSize=(300, 75), title='Please enter your password...', closable=True, )
        self.askPassWindow.secureEditText = SecureEditText((10, 10, -10, 22),
                                            callback=self.secureEditTextCallback)

        self.askPassWindow.cancel = Button((x, y, buttonWidth, 16), 'cancel',
                            sizeStyle='small', callback=self.cancelCallback)
        x += dx
        if self.mode == 'install':
            cb = self.doInstallCallback
        elif self.mode == 'uninstall':
            cb = self.doUninstallCallback
        self.askPassWindow.okay = Button((x, y, buttonWidth, 16), 'OK',
                            sizeStyle='small', callback=cb)
        self.askPassWindow.open()

    def checkPass(self):
        cmd = 'echo "%s" | sudo -S pwd' % self.password
        out, err = self.doCommand(cmd)

        if len(out) > 0:
            return True

        return False

    # Installation

    def install(self):
        """
        Installs the bits in site packages and tools to a specified folder
        (with a pth file directing to it).
        """
        self.clearCommands()
        self.reporter.clearLines()
        path = self.getToolsPath()
        print(path)

        if path is None:
            return

        self.executeInstallCommands(path)
        #self.setRoboFontPath(path + '/tntools')
        self.reporter.addLine(('%s\n' % 'Finished installing.', 'highlight'))

    def getToolsPath(self):
        msg = 'Please select a folder to install the tools...'
        folder = getFolder(messageText=msg)

        if folder is not None and len(folder) > 0:
            return folder[0]

    def executeInstallCommands(self, path):
        """Places tools sources in selected folder."""
        # Optionally removes previously installed tools from site packages.
        # TODO: add 'are you sure?'

        # TODO: check permissions of scripts install folder.
        root = False
        packageFolder = self.sitePackages + '/' + self.tnToolsPackage

        if os.path.exists(packageFolder):
            self.addCommand('rm -r %s' % packageFolder.replace(' ', '\ '), root=True)

        p = '%s/%s' % (self.tmpBase, self.tnToolsRelease)
        self.addCommand('unzip %s.zip -d %s' % (self.tnToolsRelease, self.tmpBase))
        # Moves scripts folder to user-specified location.
        self.addCommand('mv %s/src/tntools %s' % (p, path.replace(' ', '\ ')), root=root)
        # Moves the rest (tnbits) to site-packages.
        self.addCommand('mv %s/%s %s' % (self.tmpBase, self.tnToolsRelease, self.sitePackages), root=True)
        pthPath = '%s/%s' % (self.sitePackages, self.tnToolsRelease)
        self.createPth(pthPath)

        print(self.cmds)
        for cmd in self.cmds:
            self.doCommand(cmd)

    def uninstall(self):
        """Removes bits and tools from site packages."""
        self.clearCommands()
        self.reporter.clearLines()
        self.setUninstallToolsCommands()

        for cmd in self.cmds:
            self.doCommand(cmd)

        self.reporter.addLine(('%s\n' % 'Finished uninstalling.', 'highlight'))

    def setUninstallToolsCommands(self):

        '''
        # Removes pth file.
        if os.path.exists('%s/%s.pth' % (self.sitePackages, self.tnToolsPackage)):
            self.addCommand('rm %s/%s.pth' % (self.sitePackages, self.tnToolsPackage), root=True)
        '''


        # Removes previously unpacked archives from tmp folder.
        for n in ('tnBits', 'tnTools', 'tnbits', 'tntools'):
            b = '%s/%s*' % (self.tmpBase, n)
            l = glob.glob(b)
            for p in l:
                self.addCommand('rm -r %s' % p)
                self.reporter.addLine(('Removing %s\n' % p, 'highlight'))

            # Makes sure no older version exists in site packages.
            b = '%s/%s*' % (self.sitePackages, n)
            l = glob.glob(b)

            for p in l:
                self.addCommand('rm -r %s' % p, root=True)
                self.reporter.addLine(('Removing %s\n' % p, 'highlight'))

    # Command line.

    def clearCommands(self):
        self.cmds = []

    def addCommand(self, cmd, askpass=False, root=False):
        """Adds a command to the global commands list."""
        if root:
            cmd = 'echo "%s" | sudo -S ' % self.password + cmd #+ ' <pwd.txt'

        self.cmds.append(cmd)

    def doCommand(self, cmd):
        """Executes command in shell with subprocess."""
        if 'sudo -S ' in cmd:
            msg = cmd.split('sudo -S ')[-1]
        else:
            msg = cmd

        print(cmd)
        msg = '$ %s\n' % msg
        cmdLine = (msg, 'highlight')
        self.reporter.addLine(cmdLine)

        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except Exception as e:
            print(traceback.format_exc())

        if len(err) > 0:
            if err != 'Password:':
                self.reporter.addLine((err, 'error'))
        elif len(out) > 0:
            self.reporter.addLine((out, 'plaintext'))

        return out, err

    # Callbacks.

    def saveClearCallback(self, console, clear):
        pass

    def doScanCallback(self, sender):
        """Scans site packages contents."""
        self.scan.run(doImports=False, doListing=True)

    def doRunInstallCallback(self, sender):
        """Runs bits & tools installation."""
        self.mode = 'install'
        self.askPass()

    def doInstallCallback(self, sender):
        self.askPassWindow.close()

        if self.checkPass():
            try:
                self.install()
                print('finished')
            except Exception as e:
                msg = traceback.format_exc()
                print(msg)
                self.reporter.setStackTrace(msg)

            self.reporter.setLines()
        else:
            self.askPass()

    def cancelCallback(self, sender):
        self.askPassWindow.close()
        self.cancel = True

    def secureEditTextCallback(self, sender):
        self.password = sender.get()

    def doRunUninstallCallback(self, sender):
        self.mode = 'uninstall'
        self.askPass()

    def doUninstallCallback(self, sender):
        self.askPassWindow.close()

        try:
            self.uninstall()
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            self.reporter.setStackTrace(msg)

        self.reporter.setLines()

    # File.

    def createPth(self, path):
        """Creates the pth file that directs to the tools sources."""
        pth = '%s/%s' % (self.tmpBase, 'tntools.pth')
        f = open(pth, 'w')
        f.write('%s/src/\n' % path)

        f.close()
        self.addCommand('mv %s %s' % (pth, self.sitePackages), root=True)

    def createPassFile(self):
        """Creates a temporary file for password.

        NOTE: not used, using pipe approach instead.
        """
        filename = 'pwd.txt'
        f = open(filename, 'w')
        f.write('%s\n' % self.password)
        f.close()

    # RoboFont preferences.
    #WONTFIX: can only be done by identically sandboxed applications;
    # solution could be to run installer as an extension inside RoboFont.

    '''
    def setRoboFontPath(self, path):
        """Update the tools path.
        """
        defaults = NSUserDefaults.standardUserDefaults()
        defaults['pythonDir'] = path
        #defaults = NSUserDefaults.alloc().init()
        #defaults.addSuiteNamed_('com.typemytype.robofont.plist')
        #print(defaults.stringForKey_('pythonDir'))
    '''

    # Default functions
    # TODO: connect.

    def updateView(self):
        pass

    def terminate(self):
        pass

    def getView(self):
        return self.window

    def savePreferences(self, sender):
        pass
