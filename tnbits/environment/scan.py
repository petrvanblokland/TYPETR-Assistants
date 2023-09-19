# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     analyzer.py
#
import os
import subprocess
import traceback
import importlib

class Scan(object):

    libs = {
        'deprecated': ['fbtools', 'fbits', 'fbot2', 'tnbits'],
        'required': ['tntools'],
        'recommended':['tnTestFonts', 'fontMake'],
        'robofont': ['vanilla', 'fontParts', 'feaPyFoFum', 'dialogKit',
            'fontMath', 'compositor', 'defcon', 'defconAppKit', 'fontTools',
            'booleanOperations', 'designSpaceDocument', 'woffTools', 'drawBot',
            'extractor', 'feaTools2', 'ufoLib', 'mutatorMath', 'fontCompiler',
            'cu2qu', 'ufo2svg', 'ufo2fdk', 'glyphNameFormatter']}

    def __init__(self, reporter):
        self.reporter = reporter

    def run(self, doImports=True, doListing=False):
        """Resets reporter and runs analysis taking care of exceptions."""

        self.reporter.clearLines()

        try:
            if doImports:
                self.doImports()
            if doListing:
                self.doSitePackagesListing()
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            self.reporter.setStackTrace(msg)

        self.reporter.setLines()

    def doPipListing(self):
        # Outside application scope.
        #cmd = '/usr/local/bin/pip list'
        #p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = p.communicate()

        #self.update(out)
        #self.update(err)
        pass

    def matches(self, f, libname):
        if f.lower().startswith(libname.lower()):
            return True

        return False

    def doSitePackagesListing(self, base='/Library/Python/2.7/site-packages'):
        # Simply list.
        files = os.listdir(base)

        for fileName in sorted(files):
            if fileName.endswith('.pyc'):
                continue

            for key, l in self.libs.items():
                    for value in l:
                        if self.matches(fileName, value):
                            if key == 'deprecated':
                                self.update(fileName + '\n', lineType='error')
                            elif key == 'required':
                                self.update(fileName + '\n', lineType='error')
                            elif key == 'recommended':
                                self.update(fileName + '\n', lineType='highlight')
                            elif key == 'robofont':
                                self.update(fileName + '\n', lineType='warning')

            if fileName.endswith('.pth'):
                f = open(base + '/' + fileName, 'r')

                for line in f:
                    if not line.startswith('#') and ('tntools' in line.lower() or 'tnbits' in line.lower()):
                        self.update('%s\n' % fileName)
                        self.update('\t %s' % line, lineType='error')

    def doImports(self):
        self.update('Importing type libraries...\n\n')


        for libType, libNames in self.libs.items():
            for name in libNames:
                mod = None

                try:
                    mod = importlib.import_module(name)
                except Exception as e:
                    if libType != 'deprecated':
                        self.update('* %s\n' % e, lineType='warning')
                        print(e)

                if mod is not None:
                    if libType == 'deprecated':
                        self.update('* Found %s module %s, no longer supported\n' % (libType, mod), lineType='warning')
                    else:
                        self.update('* Successfully imported %s module %s\n' % (libType, mod), lineType='highlight')
                        if libType == 'robofont' and not 'RoboFont.app' in mod.__file__:
                            self.update('* %s not imported from RoboFont App\n' % name, lineType='warning')

    def update(self, message, lineType='plaintext'):
        self.reporter.addLine((message, lineType))

