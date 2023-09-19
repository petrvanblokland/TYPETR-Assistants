
import os
#import tempfile # Not used store file in local UFO folder instead.

from compositor import Font as FeatureFont
from compositor.textUtilities import convertCase

from tnbits.model.objects.style import nakedStyle
from fontCompiler.emptyCompiler import EmptyOTFCompiler

class FeatureCompiler(object):

    def __init__(self, style):
        self.setStyle(style)

    def __del__(self):
        self.destroyFeatureStyle()
        self.style.removeObserver(self, "Font.Changed")

    def setStyle(self, style):
        self.style = nakedStyle(style)
        self.featureStyle = None

    def getFeatureStyle(self):
        if self.featureStyle is None:
            report = self._compileFeatureStyle()
            #if report:
            #    print(report)
        return self.featureStyle

    def destroyFeatureStyle(self):
        if self.featureStyle is not None:
            path = self.featureStyle.path
            self.featureStyle = None
            os.remove(path)

    def getCompiledString(self, settings, s):
        # TODO: Needs a better string-->glyphNames split.
        glyphNames = s.split('')
        return self.getCompiledGlyphNames(settings, glyphNames)

    def getCompiledGlyphNames(self, settings, glyphNames):
        if self.featureStyle is None:
            report = self._compileFeatureStyle()
            #if report:
            #    print(report)
        return self._compileString(settings, glyphNames)

    def _compileFeatureStyle(self, showReport=True):
        # compile
        # If there is an existing TTF/OTF near the UFO, then use that one.
        report = []
        self.featureStyle = None

        if not self.style or not self.style.path:
            return None # Cannot construct a feature TTF font file.

        # Check if the cached feature font already exist.
        # User should remember to remove the font, if new features are added to the ufo.
        ttfPath = self.style.path.replace('.ufo', '_FEA.ttf')
        if os.path.exists(ttfPath):
            self.featureStyle = FeatureFont(ttfPath)
            return ['Feature font path: "%s"' % ttfPath]
        otfPath = self.style.path.replace('.ufo', '_FEA.otf')
        if os.path.exists(otfPath):
            self.featureStyle = FeatureFont(otfPath)
            return ['Feature font path: "%s"' % otfPath]

        # Else save the font at a temp path.
        # Potential error:
        #   File "/Applications/RoboFont.app/Contents/Resources/lib/python2.7/fontTools/ttLib/__init__.py", line 180, in __init__
        #   self.reader = sfnt.SFNTReader(file, checkChecksums, fontNumber=fontNumber)
        #   File "/Applications/RoboFont.app/Contents/Resources/lib/python2.7/fontTools/ttLib/sfnt.py", line 90, in __init__
        #      raise ttLib.TTLibError("Not a TrueType or OpenType font (bad sfntVersion)")
        # fontTools.ttLib.TTLibError: Not a TrueType or OpenType font (bad sfntVersion)

        #path = tempfile.mkstemp()[1]
        path = ttfPath # TTF Preference.
        if EmptyOTFCompiler is not None:
            compiler = EmptyOTFCompiler()
            # clean up
            if self.style.info.openTypeOS2WinDescent is not None and self.style.info.openTypeOS2WinDescent < 0:
                self.style.info.openTypeOS2WinDescent = abs(self.style.info.openTypeOS2WinDescent)
            self.style.info.postscriptNominalWidthX = None
            reports = compiler.compile(self.style, path)
            # load the compiled font
            if os.path.exists(path) and reports["makeotf"] is not None and "makeotfexe [FATAL]" not in reports["makeotf"]:
                self.featureStyle = FeatureFont(path)
            else:
                if showReport:
                    if reports["makeotf"] is not None:
                        for line in reports["makeotf"].splitlines():
                            if line.startswith("makeotfexe [NOTE] Wrote new font file "):
                                continue
                            report.append(line)
                    report.append("Error while compiling features\n")
                    report.append("\n".join(report))
        else:
            report.append()
        return report

    def _compileString(self, settings, glyphNames):
        # get the settings
        script = settings["script"]
        language = settings["language"]
        case = settings["case"]
        for tag, state in settings["gsub"].items():
            self.featureStyle.gsub.setFeatureState(tag, state)
        # process
        glyphRecords = self.featureStyle.process(glyphNames, script=script, langSys=language, rightToLeft=False,
            case=case)
        records = []
        for glyphRecord in glyphRecords:
            records.append(glyphRecord.glyphName)
        return records

if 0:
    f = CurrentFont()
    fc = FeatureCompiler(f)
    d = dict(case='Unchanged', script='latn', language='dflt', gsub=dict(ss07=False, ss04=True, smcp=False, frac=True))
    print(fc.getCompiledGlyphNames(d, ('a', 'b', 'c', 'e', 'd', 'one', 'two', 'slash', 'four', 'five')))
