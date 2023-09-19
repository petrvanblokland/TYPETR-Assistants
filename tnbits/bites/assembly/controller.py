# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    controller.py
#

from glob import glob
import time
import os, os.path
import traceback
import shutil
import logging
from multiprocessing import Pool, cpu_count
from fontmake.font_project import FontProject
from defcon import Font
from AppKit import NSImageNameAdvanced, NSImageNameFolderSmart, \
        NSSegmentedControl, NSSegmentSwitchTrackingSelectOne, NSImage
from fontTools.ttLib import TTFont
from fontTools.varLib import load_designspace
from fontTools.designspaceLib import DesignSpaceDocument
from mutatorMath.ufo.document import DesignSpaceDocumentReader

from tnbits.base.constants.tool import *
from tnbits.base.static import *
from tnbits.base.controller import BaseController
from tnbits.base.tools import *
from tnbits.base.toolbar import Toolbar
from tnbits.base.handler import BitsHandler
from tnbits.toolbox.transformer import TX
from tnbits.base.scroll import ScrollGroup
from tnbits.bites.assembly.constants import *
from tnbits.bites.assembly.dialogs.importdialog import ImportDialog
from tnbits.bites.assembly.dialogs.adddesignspacedialog import AddDesignSpaceDialog
from tnbits.bites.assembly.side import Side
from tnbits.bites.assembly.designspaceview import DesignSpaceView
from tnbits.bites.assembly.status import Status
from tnbits.compilers.featurevariations import addConditionalSubstitutions

def assembleInterpolatableFont(path):
    project = FontProject()
    ufos = [Font(path)]
    project.build_interpolatable_ttfs(ufos)

def assembleVarFont(dsp):
    project = FontProject()
    project.build_variable_font(dsp)

def assembleFromDesignSpace(dsp, **args):
    project = FontProject()
    project.run_from_designspace(designspace_path=dsp, output=["ttf-interpolatable", "variable"], **args)

class Controller(BaseController):
    """Implements internal logic between different parts of the Bakery tool.
    TODO: mojo.ui.OpenGlyphWindow on error.
    TODO: Make sure this is RoboFont3 or stand alone application; DefCon
    version in RoboFont1.8 is too old.

    - https://www.microsoft.com/typography/otspec/otvaroverview.htm
    - https://variationsguide.typenetwork.com/
    - http://letterror.com/2014/09/19/mutatormath/

    Generating instances:
    - http://typedrawers.com/discussion/2565/generating-static-instances-from-variable-font-file
    - https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
    - https://gist.github.com/simoncozens/b3b7d132b0ad2427924cbddc1f28ef35
    """

    sideClosed = False

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self.processes = cpu_count()
        self.loadPreferences()
        items = self.getToolbarItems()
        self.toolbar = Toolbar(self, items=items)
        self.side = Side(self)
        nsview = self.side.getNSView()
        pos = (0, 0, SIDE + 2*UNIT, -3*UNIT)
        self.tool.set('side', ScrollGroup(nsview, pos))
        pos = (SIDE, 0, -0, -3*UNIT)
        self.designSpaceView = DesignSpaceView(self, pos=pos)
        self.tool.set('designSpaceView', self.designSpaceView.getView())
        self.status = Status(self)
        self.tool.set('status', self.status.getView())
        h = BitsHandler(self.designSpaceView.prompt)
        addLogger('ufo2ft', h)
        addLogger('cu2qu', h)
        addLogger('fontmake', h)
        addLogger('fontTools', h)
        addLogger('tnbits', h)

    def getToolbarItems(self):
        dsIconPath = '%s/resources/DS.png' % ROOT_TNBITS
        dsIcon = NSImage.alloc().initWithContentsOfFile_(dsIconPath)
        gsubIconPath = '%s/resources/GSUB.png' % ROOT_TNBITS
        gsubIcon = NSImage.alloc().initWithContentsOfFile_(gsubIconPath)

        '''
        switchView = NSSegmentedControl.alloc().initWithFrame_(((0, 0), (64, 64)))
        cell = switchView.cell()
        cell.setTrackingMode_(NSSegmentSwitchTrackingSelectOne)
        cell.setSegmentCount_(2)
        cell.setImage_forSegment_(dsIcon, 0)
        cell.setImage_forSegment_(gsubIcon, 1)
        switchView.sizeToFit()
        '''

        items = [
            {"itemIdentifier": "assemble",
             "label": "Bake",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.assembleCallback},
            {"itemIdentifier": "makeXml",
             "label": "XML",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.makeXmlCallback},
            #{"itemIdentifier": "switchView",
            # "label": "Switch View",
            # "view": switchView,
            # "callback": self.switchViewCallback},
            {"itemIdentifier": "scanLibraries",
             "label": "Scan",
             "imagePath": None,
             "imageNamed": NSImageNameFolderSmart,
             "callback": self.scanLibrariesCallback},
            {"itemIdentifier": "clear",
             "label": "Clear",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.clearCallback},
            {"itemIdentifier": "side",
             "label": "Side",
             "imagePath": None,
             "imageNamed": NSImageNameAdvanced,
             "callback": self.sideCallback},
        ]

        return items

    def getBasePath(self):
        if self.family:
            p = self.family.familyID
            return '/'.join(p.split('/')[:-1])

    # Design Space.

    def writeDesignSpace(self, masterKeys):
        self.designSpace.writeToXML(masterKeys)

    def setDesignSpaceCallback(self, sender):
        # TODO: partially merge with setDesignSpace(), don't set popup.
        i = int(sender.get())
        names = self.getDesignSpaceNames()
        n = names[i]
        self.setDesignSpace(n)

        if n == ANY:
            self.designSpace = None
        else:
            self.designSpace = self.family[n]

        self.designSpaceView.update()
        self.setStatus()

    # Run.

    def makeXml(self, masterKeys=None):
        if masterKeys is None:
            masterKeys = self.designSpace.getMasterKeys()

        try:
            self.writeDesignSpace(masterKeys)
            self.designSpaceView.updateXml()
        except Exception as e:
            msg = traceback.format_exc()
            self.designSpaceView.xmlView.showError(e, msg)

    def getRunArguments(self):
        """Arguments to be passed to a fontmake project run. The values below
        make Decovar build without errors. See also fontmake.__main__.py.

        'use_production_names' = False
        'reverse_direction' = True
        'remove_overlaps' = True
        'subroutinize' = True
        """
        args = {}

        for k, _ in options.items():
            v = getattr(self, '_' + k)
            args[k] = v
        return args

    def assemble(self):
        """This is where we assemble the variation font."""
        project = FontProject()
        masterKeys = self.designSpace.getMasterKeys()

        if len(masterKeys) < 2:
            return

        self.designSpaceView.prompt.clearLines()
        self.makeXml(masterKeys=masterKeys)
        args = self.getRunArguments()
        dsp = self.designSpace.getXMLPath()
        #p = Pool(1)
        start = time.time()
        try:
            self.designSpaceView.prompt.message('> FontMake arguments: %s\n' % args)
            #p.map(partial(assembleFromDesignSpace, **args), [dsp])
            project.run_from_designspace(designspace_path=dsp, output=["ttf-interpolatable", "variable"], **args)
        except Exception as e:
            self.handleError(e)
            return False

        end = time.time()
        dt = (end - start)
        self.designSpaceView.prompt.message('> Finished building in %.2f seconds, moving generated files.\n' % dt)

        for d in fontmake_folders:
            try:
                self.moveOutputs(d)
            except Exception as e:
                self.handleError(e)

        return True

    def assembleParallel(self):
        # TODO: pass arguments when applicable.
        paths = []
        masterKeys = self.designSpace.getMasterKeys()

        if len(masterKeys) < 2:
            return

        self.makeXml(masterKeys=masterKeys)
        #args = self.getRunArguments()
        dsp = self.designSpace.getXMLPath()
        reader = DesignSpaceDocumentReader(dsp, ufoVersion=3)
        paths.extend(reader.getSourcePaths())
        self.designSpaceView.prompt.clearLines()

        if self.processes > len(paths):
            processes = len(paths)
        else:
            processes = self.processes

        p = Pool(processes)


        self.mkdirs(fontmake_folders)
        self.designSpaceView.prompt.message('> %s available processes\n' % self.processes)
        self.designSpaceView.prompt.message('> using %s processes\n' % processes)

        try:
            p.map(assembleInterpolatableFont, paths)
        except Exception as e:
            self.handleError(e)
            return False

        try:
            p.map(assembleVarFont, [dsp])
        except Exception as e:
            self.handleError(e)
            return False

        for d in fontmake_folders:
            self.moveOutputs(d)

        self.designSpaceView.prompt.message('> Finished building, moving generated files...')
        return True

    def mkdirs(self, l):
        for d in l:
            if not os.path.exists(d):
                os.makedirs(d)

        if not os.path.exists('variable_ttf'):
            os.makedirs('variable_ttf')

    def handleError(self, e):
        logging.exception('Got an exception of type %s', type(e))
        msg = traceback.format_exc()
        print(msg)
        self.designSpaceView.prompt.showError(e, msg, clear=False)

    def getVarPath(self):
        fp = self.family.getPath()
        d = 'variable_ttf'
        fn = self.family.name
        dsn = self.designSpace.name
        return '%s/%s/%s-%s-VF.ttf' % (fp, d, fn, dsn)

    def gsub(self):
        path = self.getVarPath()
        if os.path.exists(path):
            f = TTFont(path)
            print(f)

            try:
                addConditionalSubstitutions(f, example_gsub)
            except Exception as e:
                #logging.exception('Got an exception of type %s' % type(e))
                msg = traceback.format_exc()
                print(msg)
                self.designSpaceView.prompt.showError(e, msg, clear=False)

    def checkInterpolatable(self, dsp):
        """Checks generated interpolatable masters."""
        axes, internal_axis_supports, base_idx, normalized_master_locs, masters, instances = load_designspace(dsp)
        folder = self.family.getPath() + '/' + 'master_ttf_interpolatable'
        files = glob(os.path.join(folder, '*.ttf'))
        d = {}
        fonts = []

        for f in files:
            font = TTFont(f)
            fonts.append(font)
            o = font.getGlyphOrder()
            d[f] = o
            self.designSpaceView.prompt.message('%s: %d glyphs\n' % (f, len(o)))

        baseName = masters[base_idx]['filename'].replace('.ufo', '.ttf')
        basePath = folder + '/' + baseName

        # reload base (the default master).
        self.designSpaceView.prompt.message('%s is base.\n' % baseName)
        base = TTFont(basePath)
        o0 = base.getGlyphOrder()
        s0 = set(o0)

        # TODO: use subset
        for f, o in d.items():
            s = set(o)

            d = s.difference(s0)

            if d:
                n = f.split('/')[-1]
                msg = ', '.join(str(e) for e in d)
                self.designSpaceView.prompt.message(('Diff with %s: %s\n' % (n, msg), 'error'))

    def moveOutputs(self, output):
        # Moves files back to masters location.
        # TODO: don't overwrite folder if it already exists.
        o = self.family.getPath() + '/' + output
        shutil.rmtree(o, ignore_errors=True)
        shutil.move(output, o)
        self.designSpaceView.prompt.message('> Generated files at:\n> %s\n' % o)

    # Callbacks.

    def openFamilyCallback(self, sender):
        self.openFamily()

    def openStyleCallback(self, sender):
        # TODO: Maybe also for instance?
        if self.mode == 'tool':
            styleKeys = self.masters.getSelectedKeys()
            self.editStyleKeys(styleKeys)

    def scanLibrariesCallback(self, sender):
        """Scans system to see if necessary libraries exist."""
        try:
            self.designSpaceView.scanLibraries()
        except Exception as e:
            print(traceback.format_exc())

    def sideCallback(self, sender):
        if not self.sideClosed:
            self.tool.get('side').show(False)
            _, _, w, h = self.tool.getPosSize()
            self.designSpaceView.move(-(SIDE + 2*UNIT), 0)
            self.sideClosed = True
        else:
            self.tool.get('side').show(True)
            _, _, w, h = self.tool.getPosSize()
            self.designSpaceView.move(SIDE + 2*UNIT, 0)
            self.sideClosed = False

    def showNumbersCallback(self, sender):
        self.designSpaceView.showNumbers()

    def clearCallback(self, sender):
        self.designSpaceView.clear()

    '''
    def switchViewCallback(self, sender):
        if sender.isSelectedForSegment_(0):
            self.designSpaceView.show()
            self.side.show()
            #self.editor.show(False)
        elif sender.isSelectedForSegment_(1):
            self.designSpaceView.show(False)
            self.side.show(False)
            #self.editor.show()
    '''

    def assembleCallback(self, sender):
        success = False

        try:
            success = self.assemble()
        except Exception as e:
            msg = traceback.format_exc()
            self.designSpaceView.prompt.showError(e, msg, clear=False)
        else:
            self.designSpaceView.prompt.setLines()
            if success:
                # TODO: open font folder?
                self.designSpaceView.preview.update()

    def doGSUBCallback(self, sender):
        self.gsub()

    def makeXmlCallback(self, sender):
        self.makeXml()

    def fixMastersCallback(self, sender):
        self.fixMasters()

    def importCallback(self, sender):
        self.openImportDialog()

    def importDesignSpaceCallback(self, designSpaceName, path):
        """Imports a design space document, see also:

        https://github.com/LettError/designSpaceDocument

        NOTE: has been moved to fontTools
        TODO: choose append / clear / overwrite.
        TODO: import instances (without paths).
        """
        self.tool.removeDialog('import')

        if path is None or designSpaceName is None:
            return

        doc = DesignSpaceDocument()
        doc.read(path)
        designSpace = self.family[designSpaceName]

        for axis in doc.axes:
            designSpace.addAxis(axis.tag, axis.name, axis.minimum,
                    axis.maximum, defaultValue=axis.default)

        for source in doc.sources:
            '''
            designSpaceDocument SourceDescriptor attributes:
            filename
            path
            name
            location
            copyLib
            copyInfo
            copyGroups
            copyFeatures
            muteKerning
            muteInfo
            mutedGlyphNames
            familyName
            styleName
            '''
            styleKey = TX.path2StyleKey(source.path)

            try:
                designSpace.asMaster(styleKey)
            except AssertionError as e:
                msg = 'Cannot identify master style key (%s, %s)' % styleKey
                print(msg)
                #self.designSpaceView.prompt.message((msg, 'error'))
                print(traceback.format_exc())

            for name, value in source.location.items():
                tag, _ = designSpace.getAxisByName(name)
                designSpace.setStyleInterpolationAxis(styleKey, tag, value)

        '''
        testCase = expanduser('~/Fonts/Decovar/sources/2-build/Decovar-Regular24SkelA.ufo')
        styleKey = TX.path2StyleKey(testCase)
        print(designSpace.getStyleInterpolationAxis(styleKey, 'SKLA'))
        print(designSpace.getStyleInterpolationAxis(styleKey, 'Inline Skeleton'))
        print(designSpace.getStyleInterpolations(styleKey))
        '''

        for instance in doc.instances:
            '''
            designSpaceDocument InstanceDescriptor attributes:
            filename
            path
            name
            location
            familyName
            localisedFamilyName
            styleName
            localisedStyleName
            postScriptFontName
            styleMapFamilyName
            localisedStyleMapFamilyName
            localisedStyleMapStyleName
            styleMapStyleName
            glyphs
            mutedGlyphNames
            kerning
            info
            '''
            if not instance.path is None:
                styleKey = TX.path2StyleKey(instance.path)
                try:
                    designSpace.asInstance(styleKey)
                except AssertionError as e:
                    msg = 'Cannot identify instance style key (%s, %s)' % styleKey
                    #self.designSpaceView.prompt.message((msg, 'error'))
                    print(msg)
                    print(traceback.format_exc())

        designSpace.save()
        self.designSpace = designSpace
        self.designSpaceView.update()

    def addDesignSpaceCallback(self, name):
        if name is None:
            return
        elif not name:
            return

        self.tool.removeDialog('addDesignSpace')
        self.family.addDesignSpace(name)
        self.setDesignSpace(name)
        self.designSpaceView.update()

    def removeDesignSpace(self):
        view = self.side.getView()

        if self.designSpace:
            self.family.removeDesignSpace(self.designSpace.name)
            name = self.family.getFirstName()
            self.setDesignSpace(name)
            self.designSpaceView.update()

    # Dialogs.

    def openImportDialog(self):
        dialog = ImportDialog(self, self.importDesignSpaceCallback)
        self.tool.addDialog('import', dialog)

    def openAddDesignSpace(self):
        dialog = AddDesignSpaceDialog(self, self.family,
                self.addDesignSpaceCallback)
        self.tool.addDialog('addDesignSpace', dialog)

    # Preferences.

    def loadPreferences(self):
        """Loads values from preferences."""
        self._runFrom = self.tool.getPreference('runFrom') or 0

        for k in options.keys():
            p = self.tool.getPreference(k)
            setattr(self, '_' + k, p)

        self.savePreferences()

    def savePreferences(self, sender=None):
        print('to be implemented')

    # Get.

    def getStylesDict(self, styleKeys):
        """Gets a DoodleFont or FloqModel Style. NOTE: Can be DefCon Font,
        DoodleFont or tnbits model Style.
        """
        stylesDict = {}

        # Collects styles in a dictonary.
        # TODO: add progress bar, opens all fonts so will be slow.
        for styleKey in styleKeys:
            _, styleId = styleKey
            style = self.family.getStyle(styleKey)
            stylesDict[styleKey] = style

        return stylesDict

    # Set.

    def setFamily(self, family):
        """Callback from tool to set up font family."""
        self.family = family
        self.setTitle(family)
        name = self.family.getFirstName()
        self.setDesignSpace(name)
        self.designSpaceView.update()

    def setDesignSpace(self, name):
        # TODO: set current ds name from preferences.
        view = self.side.getView()

        if name is None or name == ANY:
            self.designSpace = None
        else:
            self.designSpace = self.family[name]

        names = self.getDesignSpaceNames()
        view.selectDesignSpace.setItems(names)

        if not name is None:
            i = names.index(name)
            view.selectDesignSpace.set(i)

        self.setStatus()
        self.designSpaceView.updateXml()

    def setStatus(self):
        self.status.set(self.designSpace)
