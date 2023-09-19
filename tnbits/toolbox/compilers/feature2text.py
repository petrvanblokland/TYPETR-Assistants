# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#


#from tnbits.contributions.fbFeaTools.parser import parseFeatures
from tnbits.toolbox.character import CharacterTX

class Replacer(object):

    def __init__(self, type, target, replacement, preceding=None, trailing=None):
        self.type = type
        self.target = target
        self.replacement = replacement
        self.preceding = preceding
        self.trailing = trailing

    def __repr__(self):
        p = t = ''
        if self.preceding:
            p = 'p%s >> ' % self.preceding
        if self.trailing:
            t = ' << t%s' % self.trailing
        return 'R%d(%s%s%s -> %s)' % (self.type, p, self.target, t, self.replacement)

    def _expandGroups(self, nameItem, groups):
        expanded = []
        if isinstance(nameItem, (list, tuple)):
            expanded = []
            for names in nameItem:
                expanded.append(self._expandGroups(names, groups))
            return expanded

        if nameItem in groups:
            expanded = []
            for expandedName in self._expandGroups(groups[nameItem], groups):
                expanded.append(expandedName)
            return expanded

        return nameItem

    def flattenedGlyphNames(self, names):
        flattenedNames = set()
        if isinstance(names, str):
            flattenedNames.add(names)
        elif isinstance(names, (list, tuple)):
            for name in names:
                flattenedNames = flattenedNames.union(self.flattenedGlyphNames(name))
        return flattenedNames

    def expandGroups(self, groups):
        self.target = self._expandGroups(self.target, groups)
        self.replacement = self._expandGroups(self.replacement, groups)
        self.preceding = self._expandGroups(self.preceding, groups)
        self.trailing = self._expandGroups(self.trailing, groups)

    def match(self, pattern):
        for index, target in enumerate(self.target):
            if index >= len(pattern):
                return 0, None
            if not isinstance(target, (list, tuple)):
                target = [target]
            glyphName = CharacterTX.char2GlyphName(pattern[index])
            if not glyphName in target:
                return 0, None
        return len(self.target), self.replacement

    def getGlyphNames(self):
        """Answer the set of all glyph names in self. At this point all glyph groups need to be expanded."""
        glyphNames = set()
        if self.replacement is not None:
            glyphNames = glyphNames.union(self.flattenedGlyphNames(self.replacement))
        if self.preceding is not None:
            glyphNames = glyphNames.union(self.flattenedGlyphNames(self.preceding))
        if self.trailing is not None:
            glyphNames = glyphNames.union(self.flattenedGlyphNames(self.trailing))
        if self.target is not None:
            glyphNames = glyphNames.union(self.flattenedGlyphNames(self.target))
        return glyphNames

class LookupWriter(object):

    def __init__(self, scriptTag, languageTag, featureName, featureEngine):
        self.fe = featureEngine
        self.scriptTag = scriptTag
        self.languageTag = languageTag
        self.featureName = featureName

    def gsubType1(self, target, replacement):
        self.fe.replace1(self.scriptTag, self.languageTag, self.featureName, target, replacement)

    def gsubType2(self, target, replacement):
        raise NotImplementedError

    def gsubType3(self, target, replacement):
        self.fe.replace3(self.scriptTag, self.languageTag, self.featureName, target, replacement)

    def gsubType4(self, target, replacement):
        self.fe.replace4(self.scriptTag, self.languageTag, self.featureName, target, replacement)

    def gsubType5(self, target, replacement):
        raise NotImplementedError

    def gsubType6(self, precedingContext, extractedTargets, trailingContext, replacement):
        self.fe.replace6(self.scriptTag, self.languageTag, self.featureName, precedingContext, extractedTargets, trailingContext, replacement)

class FeatureWriter(object):

    def __init__(self, scriptTag, languageTag, name, featureEngine):
        self.fe = featureEngine
        self.scriptTag = scriptTag
        self.languageTag = languageTag
        self.name = name
        self.includeDefault = True

    def script(self, scriptTag):
        self.scriptTag = scriptTag

    def language(self, languageTag, includeDefault=True):
        self.languageTag = languageTag
        self.includeDefault = includeDefault

    def featureReference(self, name):
        """Keep the set of referenced feature names here."""
        self.fe.addFeatureReferences(name)

    def lookup(self, name):
        return LookupWriter(self.scriptTag, self.languageTag, name, self.fe)

    def lookupReference(self, lookupName):
        print('TODO [FeatureWriter.lookupReference] script:', self.scriptTag, 'language:', self.languageTag, 'lookupName:', lookupName)
        #pass

    def gsubType1(self, target, replacement):
        #assert len(targets) == len(replacements)
        self.fe.replace1(self.scriptTag, self.languageTag, self.name, target, replacement)

    def gsubType2(self, target, replacement):
        raise NotImplementedError

    def gsubType3(self, target, replacement):
        self.fe.replace3(self.scriptTag, self.languageTag, self.name, target, replacement)

    def gsubType4(self, target, replacement):
        self.fe.replace4(self.scriptTag, self.languageTag, self.name, target, replacement)

    def gsubType5(self, target, replacement):
        raise NotImplementedError

    def gsubType6(self, precedingContext, extractedTargets, trailingContext, replacement):
        self.fe.replace6(self.scriptTag, self.languageTag, self.name, precedingContext, extractedTargets, trailingContext, replacement)

class Writer(object):

    def __init__(self, featureEngine):
        self.fe = featureEngine
        self.scriptTag = None
        self.languageTag = None

    def classDefinition(self, name, content):
        self.fe.addGroup(name, content)

    def script(self, scriptTag):
        self.scriptTag = scriptTag

    def languageSystem(self, scriptTag, languageTag):
        self.scriptTag = scriptTag
        self.languageTag = languageTag

    def feature(self, name):
        return FeatureWriter(self.scriptTag, self.languageTag, name, self.fe)

    def subtableBreak(self):
        print('[writer.subtableBreak]')

class Feature2Text(object):
    def __init__(self, source):
        self.compile(source)

    def compile(self, source):
        self.writer = Writer(self)
        self.groups = {}
        self.scripts = {}
        self.featureReferences = set() # Total set of referenced features.
        # Parse the source and have data stored by calling the writer lookup functions.
        # Results are stored in self.groups, self.scripts and self.featureReferences.
        parseFeatures(self.writer, source)
        # Now we have a feature dict structure in self.scripts
        # And all the groups in self.groups. Run through the scripts to expand all group references.
        # It seems to be a better solution to do this only once (and make the main parsing simpler,
        # with the cost of a bit of memory), than to do it on the fly (slower and more complex parsing).
        # Note that this "self.scripts" cannot be used for decompile, since it lost all group connections.
        self.scripts = self.expandFeatureGroups(self.scripts)
        # External selectors, need to be defined but the calling application before usage.
        self.script = None
        self.language = None

    def addFeatureReferences(self, name):
        """Add name to the total set of names of features required in the current source. This is defined by
        the “feature aalt { feature ornm; }” in a feature source."""
        self.featureReferences.add(name)

    def getFeatureNames(self):
        """Answer the list of all (unique) feature names, no matter in which language or script
        they are defined."""
        featureNames = set()
        for _, script in self.scripts.items():
            for _, language in script.items():
                for featureName in language.keys():
                    featureNames.add(featureName)
        return featureNames

    def getLanguageNames(self):
        languageNames = set()
        for _, script in self.scripts.items():
            for languageName in script.keys():
                if languageName is not None:
                    languageNames.add(languageName)
        return languageNames

    def getScriptNames(self):
        scriptNames = set()
        for scriptName in self.scripts.keys():
            if scriptName is not None:
                scriptNames.add(scriptName)
        return scriptNames

    def getGlyphNames(self):
        glyphNames = set()
        for _, script in self.scripts.items():
            for _, language in script.items():
                for _, features in language.items():
                    for _, feature in features.items():
                        for replacer in feature:
                            for glyphName in replacer.getGlyphNames():
                                glyphNames.add(glyphName)
        return glyphNames

    def getGroupNames(self):
        """Answer the list of group names, with the initial "@" removed."""
        groupNames = []
        for groupName in self.groups.keys():
            groupNames.append(groupName[1:]) # Remove initial @
        return groupNames

    def expandFeatureGroups(self, o):
        if isinstance(o, (list, tuple)):
            expandedList = []
            for oo in o:
                for item in self.expandFeatureGroups(oo):
                    expandedList.append(item)
            return expandedList
        if isinstance(o, dict):
            expandedDict = {}
            for key, item in o.items():
                key = self.expandFeatureGroups(key)
                item = self.expandFeatureGroups(item)
                for k in key:
                    expandedDict[k] = item
            return expandedDict
        # It is a string, check against group name
        if o in self.groups:
            return self.groups[o]
        if isinstance(o, Replacer):
            o.expandGroups(self.groups)
            return [o]
        return [o] # Always make a list.

    def __repr__(self):
        return "[Feature2Text groups:%d]" % (len(self.groups))

    def __getitem__(self, scriptTag):
        return self.scripts.get(scriptTag)

    def addGroup(self, name, content):
        self.groups[name] = content

    def getFeature(self, scriptTag, languageTag, featureTag):
        #if scriptTag == 'CRT':
        #    pass
        """Answer the feature dictionary, indicated by the tags."""
        if not scriptTag in self.scripts:
            self.scripts[scriptTag] = {}
        script = self.scripts[scriptTag]
        if not languageTag in script:
            script[languageTag] = {}
        language = script[languageTag]
        if not featureTag in language:
            language[featureTag] = {}
        return language[featureTag]

    def replace1(self, scriptTag, languageTag, featureTag, target, replacement):
        # Replacement:
        # [target] --> [replacement]
        # @target --> @replacement
        # target --> replacement
        if isinstance(target, str) and target.startswith('@'):
            if target in self.groups:
                target = self.groups[target]
            else: # For now print(the error)
                print('### Feature2Text.replace1: Target "%s" not in groups' % target)
                return
        if isinstance(replacement, str) and replacement.startswith('@'):
            if replacement in self.groups:
                replacement = self.groups[replacement]
            else: # For now print(the error)
                print('### Feature2Text.replace1: Replacement "%s" not in groups' % target)
                return
        if isinstance(target, (list, tuple)):
            assert len(target) == len(replacement)
            for index, t in enumerate(target):
                self.replace1(scriptTag, languageTag, featureTag, t, replacement[index])
        else:
            self.add(1, target, scriptTag, languageTag, featureTag, target, replacement)

    def replace3(self, scriptTag, languageTag, featureTag, target, replacement):
        # Expand
        assert isinstance(target, str)
        if target.startswith('@'):
            for t in self.groups[target]:
                self.replace3(scriptTag, languageTag, featureTag, t, replacement)
        else:
            self.add(3, target, scriptTag, languageTag, featureTag, target, replacement)

    def replace4(self, scriptTag, languageTag, featureTag, target, replacement):
        # Ligatures:
        # [glyph, glyph, ...] --> glyph
        # [glyph, [glyph, ...], ...] --> glyph
        # Target always is a list

        if isinstance(target, str) and target.startswith('@'):
            target = self.groups[target]
        assert isinstance(target, (list, tuple))
        if isinstance(target[0], (list, tuple)):
            for t in target[0]:
                self.replace4(scriptTag, languageTag, featureTag, [t] + target[1:], replacement)
        else:
            self.add(4, target[0], scriptTag, languageTag, featureTag, target, replacement)

    def replace6(self, scriptTag, languageTag, featureTag, preceding, target, trailing, replacement):
        #return

        if isinstance(target, str) and target.startswith('@'):
            target = self.groups[target]
        if not isinstance(target, (list, tuple)):
            target = [target]
        if isinstance(target[0], (list, tuple)):
            for t in target[0]:
                self.replace6(scriptTag, languageTag, featureTag, preceding, [t] + target[1:], trailing, replacement)
        elif target[0].startswith('@'):
            if target[0] in self.groups:
                tgroup = self.groups[target[0]]
            else: # For now print(the error)
                print('### Feature2Text.replace6: Target[0] "%s" not in groups' % target[0])
                return
            for t in tgroup:
                self.replace6(scriptTag, languageTag, featureTag, preceding, [t] + target[1:], trailing, replacement)
        else:
            self.add(6, target[0], scriptTag, languageTag, featureTag, target, replacement, preceding, trailing)

    def replace(self, type, scriptTag, languageTag, featureTag, target, replacement, preceding=None, trailing=None):
        done = False
        if isinstance(target, (tuple, list)):
            if isinstance(replacement, (tuple, list)) and len(target) == len(replacement):
                for index, t in enumerate(target):
                    self.replace(type, scriptTag, languageTag, featureTag, t, replacement[index], preceding, trailing)
                    done = True
        if not done:
            self.add(type, target, scriptTag, languageTag, featureTag, target, replacement, preceding, trailing)

    def add(self, type, key, scriptTag, languageTag, featureTag, target, replacement, preceding=None, trailing=None):
        feature = self.getFeature(scriptTag, languageTag, featureTag)
        r = Replacer(type, target, replacement, preceding, trailing)
        if not key in feature:
            feature[key] = []
        feature[key].append(r)

    def getLanguages(self, scriptName, scripts):
        """Answer the dictionary of languages defined by script."""
        for name in (scriptName, None, 'dflt'):
            if name in scripts:
                return scripts[name]
        return None

    def getFeatures(self, languageName, languages):
        for name in (languageName, None, 'dflt'):
            if name in languages:
                return languages[name]
        return None

    def parse(self, glyph, pattern):
        """"Try to find matches the of the patterns on in the available lookups, depending on the selected
        self.script and self.language. If they are not defined, then try the 'dflt' selection.
        Answer the tuple of (newIndex, result). If not script or language is defined, or if there is no pattern
        match, then answer (1, glyph), meaning there is no pattern change through any feature."""
        glyphName = CharacterTX.char2GlyphName(glyph)
        languages = self.getLanguages(self.script, self.scripts) # Get available language in the selected script.
        if languages is not None:
            features = self.getFeatures(self.language, languages) # Get available feature set in the selected script/language.
            if features is not None:
                for featureName, feature in features.items():
                    # Feature is a dictionary of glyphName:lookup pairs, where the key be a string name
                    # It is assumed that all group @name references in the feature are expanded at this point.
                    if glyphName in feature:
                        for lookup in feature[glyphName]:
                            nextIndex, match = lookup.match(pattern)
                            if nextIndex:
                                g = CharacterTX.glyphName2Char(match)
                                if g is None:
                                    g = glyph
                                return nextIndex, g
        return 1, glyph

    def parseText(self, s):
        parsedGlyphs = []
        index = 0
        while index < len(s):
            c = s[index]
            skip, result = self.parse(c, s[index:index+10])
            if skip:
                index += skip
                parsedGlyphs.append(result)
            else:
                index += 1
                parsedGlyphs.append(c)
        return ''.join(parsedGlyphs)

    def show(self):
        print('-'*60)
        print(fe)
        print('.'*60)
        for key, group in sorted(fe.groups.items()):
            print('\t', key, '=', group)
        print('.'*60)
        for scriptTag, languages in sorted(fe.scripts.items()):
            print(scriptTag)
            for languageTag, features in sorted(languages.items()):
                print('\t', languageTag)
                for featureName, feature in sorted(features.items()):
                    print('\t\t', featureName)
                    for target, replacement in sorted(feature.items()):
                        print('\t\t\t', target, '=>', replacement)

    def test(self):
        """Test all combinations for these features."""
        for scriptTag in self.scripts:
            print(scriptTag)
            for languageTag in self.scripts[scriptTag]:
                print('\t', languageTag)
                for featureTag in self.scripts[scriptTag][languageTag]:
                    print('\t\t', featureTag)
                    for target, features in self.scripts[scriptTag][languageTag][featureTag].items():
                        for feature in features:
                            print('\t\t\t', feature)
                            #for t in feature.target:
                            #    print('\t\t\t', t, '->', feature.replacement)


if __name__ == '__main__':
    featureSource = """

        @one_frac = [one onesuperior];
        @two_frac = [two twosuperior];
        @three_frac = [three threesuperior];
        @fraction = [fraction slash];

        feature frac { # Fractions
            sub @one_frac @fraction @two_frac by onehalf;
            sub @one_frac @fraction four by onequarter;
            sub @three_frac @fraction four by threequarters;
        } frac;

        feature liga {
            sub f f i by f_f_i;
            sub f f l by f_f_l;
            sub f f j by f_f_j;
            sub f f b by f_f_b;
            sub f f h by f_f_h;
            sub f i by f_i;
            sub f j by f_j;
            sub f l by f_l;
            sub f b by f_b;
            sub f h by f_h;
            sub f f by f_f;
        } liga;
    """
    fe = Feature2Text(featureSource)
    #fe.show()


    fe.script = 'dflt'
    fe.language = 'dflt'
    fe.selectedFeatures = set(('sups','liga'))

    t = '1/2 1/4 3/4 2/3 ffi fj ffl fi fb'

    print(t)
    print(fe.parseText(t))

    print('Scripts', fe.getScriptNames())
    print('Languages', fe.getLanguageNames())
    print('Features', fe.getFeatureNames())
    print('Glyphs', fe.getGlyphNames())

    #fe.test()
