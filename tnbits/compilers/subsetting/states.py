# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    states.py
#


import os
import weakref
import json

DEBUG = False

class State(object):
    # Base class of generic storage instance.
    CLASSKEY = '__cls__'

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def __del__(self):
        # Make sure to clear all references on deletion
        if DEBUG:
            print('XXX Deleting', self)
        for name, attr in self.__dict__.items():
            if isinstance(attr, (list, tuple, dict, set)):
                # States in the list will automatically get a delete call too if no references left.
                # Since all references in the network are weak, any reference from the other side will
                # disappear automatic.
                setattr(self, name, None)

    @classmethod
    def _fromDict(cls, d):
        dd = cls()
        for key, item in d.items():
            dd[key] = item

    @classmethod
    def _fromObject(cls, o, root=None):
        # Recursively transform the dicts into a state if they contain the
        # hidden state class name and leave other objects untouched.
        if isinstance(o, (list, tuple)):
            result = [] # Answer a list of states or other values
            for d in o:
                result.append(cls._fromObject(d))
        elif isinstance(o, dict):
            className = o.get(cls.CLASSKEY)
            if className is not None:
                result = cls() # Answer a single state
                for key, value in o.items():
                    setattr(result, key, cls._fromObject(value))
        else:
            result = o
        return result

    @classmethod
    def _asObject(cls, o, root=None):
        # Recursively transform states into dicts.
        # Convert all other object to standard Python classes.
        if isinstance(o, str):
            result = o
        elif isinstance(o, (list, tuple, set)):
            # Inheriting instance need to reconstruct set-->list into set again,
            # since that difference will not be store in the json
            result = []
            for oo in o:
                result.append(cls._asObject(oo))
        elif isinstance(o, dict):
            result = {}
            for key, item in o.items():
                result[key] = cls._asObject(item)
        elif isinstance(o, State):
            result = {cls.CLASSKEY: o.__class__.__name__} # So we can reconstruct
            for key, item in o.items():
                if key.startswith('_'):
                    continue # Ignore this class name key and other local attributes
                result[key] = cls._asObject(item)
        elif isinstance(o, (int, float)):
            result = o
        elif o is None:
            result = 'None'
        else:
            result = str(o)
        return result

    def items(self):
        return self.__dict__.items()

class GDEFState(State):
    # Root instance of GDEF decompiled data
    def __init__(self, classDef, classDefFormat, ligCaretList, attachList,
            markAttachClassDef, markAttachClassDefFormat):
        self.classDef = classDef # Dictionary glyphName:classDefId
        self.classDefFormat = classDefFormat
        self.ligCaretList = ligCaretList # List with glyphNames
        self.attachList = attachList
        self.markAttachClassDef = markAttachClassDef # Dictionary glyphName:classDefId
        self.markAttachClassDefFormat = markAttachClassDefFormat

    def deleteGlyph(self, glyphName):
        if glyphName in self.classDef:
            del self.classDef[glyphName]
        if glyphName in self.ligCaretList:
            del self.ligCaretList[self.ligCaretList.index(glyphName)]
        if glyphName in self.markAttachClassDef:
            del self.markAttachClassDef[glyphName]

    def getGlyphNames(self):
        # Answer a set with all glyph names in the state.
        return set(self.classDef.keys()).union(self.ligCaretList).union(self.markAttachClassDef.keys())

class GState(State):
    # Root instance of GPOS and GSUB decompiled data.
    # The self.scripts holds the network of script--language--feature--lookup states.
    #
    #    The GState instances hold the real references to the state instances.
    #    The rest of the network links is made by weakrefs.
    #
    #    GState ----> @scripts{} ----> script
    #    GState ----> @languages[] ----> language
    #    GState ----> @features[] ----> feature
    #    GState ----> @lookups[] ----> lookup
    #
    #    script ----> @languages{}(weak) ----> language
    #
    #    language ----> @script(weak) ----> script
    #    language ----> @features[](weak) ----> feature
    #
    #    feature ----> @languages[](weak) ----> language
    #    feature ----> @lookups[](weak) ----> lookup
    #
    #    lookup ----> @languages[](weak) ----> language
    #    lookup ----> @features[](weak) ----> feature
    #    lookup ----> @subs[](weak) ----> lookup
    #
    def __init__(self):
        self.scripts = {}
        self.languages = []
        self.features = []
        self.lookups = []
        self.errors = []

    def addScript(self, name, script):
        """Add the script to the script dictionary. For convenience the script is answered."""
        self.scripts[name] = script
        return script

    def addLanguage(self, language):
        """Add the language to the language list. For convenience the language is answered."""
        self.languages.append(language)
        return language

    def addFeature(self, feature):
        """Add the feature to the feature list. For convenience the feature is answered."""
        self.features.append(feature)
        return feature

    def addLookup(self, lookup):
        """Add the lookup to the lookup list. For convenience the lookup is answered."""
        self.lookups.append(lookup)
        return lookup

    @classmethod
    def fromJson(cls, s):
        """If s evaluates to a list, then assume that the content are dicts, that all
        convert to a single state. If s evaluates to a dict, then create a single state."""
        assert isinstance(s, str)
        return cls._fromObject(json.loads(s))

    def asJson(self):
        """Convert self to an object of standard Python instances, so it can be dumped by json."""
        self._updateIndices() # Make sure that all indices are valid, since we'll skip the weakrefs
        return json.dumps(self._asObject(self))

    def _getStatesOfGlyphs(self, states, glyphNames):
        """Answer the states that contain the named glyphs."""
        if not isinstance(glyphNames, (list, tuple)):
            glyphNames = [glyphNames]
        glyphStates = []
        for state in states:
            for glyphName in glyphNames:
                if glyphName in state.getGlyphNames():
                    glyphStates.append(state)
                    break
        return glyphStates

    def getScriptsOfGlyphs(self, glyphNames):
        """Answer the scripts that contain the named glyphs."""
        return self._getStatesOfGlyphs(self.scripts)

    def getLanguagesOfGlyphs(self, glyphNames):
        """Answer the languages that contain the named glyphs."""
        return self._getStatesOfGlyphs(self.languages)

    def getFeaturesOfGlyphs(self, glyphNames):
        """Answer the features that contain the named glyphs."""
        return self._getStatesOfGlyphs(self.features)

    def getLookupsOfGlyphs(self, glyphNames, lookups=None):
        """Answer the lookups that contain the named glyphs."""
        if lookups is None:
            lookups = self.lookups
        return self._getStatesOfGlyphs(lookups, glyphNames)

    def deleteScript(self, scriptName):
        # Delete the script from self.scripts, including all depending references.
        # If the script is in self.scripts, then delete it. Otherwise ignore the call
        # (in other words, make sure that it is not in the output, no matter if it originally existed.
        # Before deleting the script, delete all references in the the script<-->languages<-->features<-->lookups first.
        # If one of them gets empty, then delete that state instance too.
        if self.scripts.get(scriptName) is None:
            # Ignore, this font doesn't have a script with that name
            return
        # Now remove all references to this script from the language, features and lookups.
        # The main problem is to remove the elements from the list while running through,
        # since deleting an item will change the index and the length of the list.
        # So we'll aggregate them in a separate list and then replace the list at the end.
        # Note that we only need to cleanup the real links, not the weakrefs, as the lists
        # with the real links are just used for re-indexing. When used they give a None
        # if the referenced state not longer exists.
        # In the end, as a result of the cleanup, all script, language, feature state instances
        # should have been deleted.
        #
        # First delete the script from the self.scripts table dictionary, so all weakrefs become None
        # Make sure that there are no (local) variables refering to the script, because then it
        # will remain existing, which causes the weakref not to go to None.
        del self.scripts[scriptName]
        # Now run through all lookups-->feature-->language-->(possibly deleted)script
        # to see what has become obsolete.
        lookups = [] # New list with lookups that did not become empty after subset.
        for index, lookup in enumerate(self.lookups):
            languages = [] # Build separate list and then restore it later.
            # Remove the languages that have the current script as parent
            for language in lookup.languages:
                if not language.script is None: # Deletion of the script made the weakref None?
                    languages.append(language) # Otherwise keep it.
                if DEBUG:
                    print('Deleting language(%s) from script(%s) #%d' % (language, scriptName, index))
            # Set the new list with the languages-->script removed. The lookup instance will
            # replace the languages by weakref links.
            # Note that the languages are not garbage collected yet, as self.languages still
            # holds the hard reference. These will be cleaned later.
            lookup.languages = languages
            # Check if there still is a language referring to the features, otherwise remove the feature too.
            features = []
            for feature in lookup.features:
                languages = [] # Build separate list and then restore it.
                for language in feature.languages:
                    if language.script is not None: # Language parent is not referring to deleted script?
                        languages.append(language) # Then keep it.
                    elif DEBUG:
                        print('Deleting language(%s) from lookup-->feature' % language)
                feature.languages = languages
                if languages: # Still a language left for this feature? Then keep feature.
                    features.append(feature)
                elif DEBUG:
                    print('Deleting empty feature(%s) from lookup' % feature)
            # Set the new list with the feature-->language-->script removed
            # Note that the features are not garbage collected yet, as self.features still
            # holds the hard reference. These will be cleaned later.
            lookup.features = features
            if languages or features or lookup.referencingLookups:
                # Still languages or features or other lookup using this lookup?
                lookups.append(lookup) # Then keep it.
            elif DEBUG:
                print('Deleting lookup(%s)' % lookup, lookup.getGlyphNames())

        # Set the new cleaned list of lookups.
        # The calling application should run a cleanUp() once all subsetting is done,
        # to disconnect all the hard links. This will make the weakrefs render to None,
        # and make the removed instances be garbage collected.
        self.lookups = lookups

    def cleanUp(self):
        # Now clean up the hard links in self.languages and self.features to, which will
        # drop the deleted language and features instances in garbage collection of Python,
        # because there are just weakrefs left over to them.
        # Remove the hard link to orphan languages (where the script has been deleted)
        # Clean up the lookups first, as they are just dependent on their content
        lookups = self.lookups # These are the real hard instances, not weakrefs.
        self.lookups = [] # Take them over, so they will last a short while, we can build the new list here.
        for lookup in lookups:
            if lookup.keepIt() and (lookup.hasAliveParent() or lookup.referencingLookups):
                # Keep it? Only when not orphaned or empty or referred to.
                self.lookups.append(lookup)
        lookups = None # Dropping the hard reference to deleted lookups.

        # Then cleanup the features, as they are dependent on the existence of the lookups
        # Remove the hard link to orphan languages (where the script has been deleted)
        features = self.features # These are the real hard instances, not weakrefs.
        self.features = []
        for feature in features:
            if feature.keepIt() and feature.hasAliveParent(): # Keep it? Only when not orphaned or empty.
                self.features.append(feature)
        features = None # Dropping the hard references to deleted features.

        # Finally clean the languages as they are dependent on the features and the existence of the script.
        languages = self.languages # These are the real hard instances, not weakrefs.
        self.languages = [] # Take them over, so they will last a short while, we can build the new list here.
        for language in languages:
            if language.keepIt() and language.hasAliveParent(): # Keep it? Only when not orphaned by script and its features.
                self.languages.append(language)
        languages = None # Dropping the hard references to deleted languages.
        # Finally clean the scripts as they are dependent on the languages that still exist

        scripts = self.scripts
        self.scripts = {} # Take them over, so they will last a short while, we can build the new dictionary  here.
        for scriptName, script in scripts.items():
            if script.keepIt(): # Keep it? Only where there are still valid languages there.
                self.scripts[scriptName] = script
        scripts = None # Dropping the hard references to deleted scripts.

    def deleteGlyph(self, glyphName):
        # In case that the font no longer contains the glyph, then also all references
        # in the GSUB table should be removed. This process is similar to that of deleting
        # a script. If the reference is deleted, then also the parent must be deleted if
        # the contained list becomes empty. This cleaning is done in one cleanup swipe.
        for lookup in self.lookups:
            lookup.deleteGlyph(glyphName)

    def deleteInputGlyph(self, glyphName):
        # Delete the glyph as entry, if it in the input side of the lookup
        for lookup in self.lookups:
            lookup.deleteInputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        # Delete the glyph as entry, if it is in the output side of the lookup
        for lookup in self.lookups:
            lookup.deleteOutputGlyph(glyphName)

    def attachIndexedReferences(self):
        # If all scripts, features and lookups are decompiled, we can build the feature
        # list that knows which language and script is referencing to it. The scripts
        # and lookups will be appended to the features with a direct reference.
        # Then in reverse the features and lookups are added as weakref in the script
        # and lookup instances, to allow direct access and to avoid hard circle references.
        # Note that on compiling, we can no longer use the existing index numbers,
        # since the content of the features may have changed. So there we need to
        # lookup the actual index of the lookup and the feature in the list as it is.
        # @@@ Later: Add error reports if the indices are not matching the available data set.
        for _, script in self.scripts.items(): # name, script
            for _, language in script.languages.items():
                for featureIndex in language.featureIndices: # name, language
                    feature = self.features[featureIndex]
                    # Add forward link language-(weak)->feature
                    language.addFeature(feature)
                    # Add direct back link in local set (not written to json)
                    feature.addLanguage(language)
                    for lookupIndex in feature.lookupIndices:
                        lookup = self.lookups[lookupIndex]
                        # Make weak link from feature to lookup, instead of index reference
                        feature.addLookup(lookup)
                        # Add the direct back link to the set as features<--lookup
                        lookup.addFeature(feature)
                        # Add the direct back link io the set as language<--lookup
                        lookup.addLanguage(language)
        # Handle anything special to this table
        # Necessary for GSUB lookup6/lookup7 and GPOS lookup8/lookup9
        self.attachIndexReferencedLookups()

    def attachIndexReferencedLookups(self):
        # If this is a lookup type 8 (or 9) for GSUB and type 6 (or 7)
        # for GPOS, then there can be substitution references to other
        # lookups. Fill them in with the real links if they are present.
        # As now there is a direct link, the index numbers become obsolete.
        # Editing the total list of lookups may cause them to have different
        # index numbers on output.
        for lookup in self.lookups:
            # Attach in reversed direction too. Supply self.lookups as resource for
            # the lookups to refer to. The call only has effect for the referencing
            # lookups. It is ignored by all other lookup types.
            lookup.attachIndexReferencedLookups(self.lookups)

    def _updateIndices(self):
        # Update all index lists, so they match with the exiting weakref links
        for feature in self.features:
            feature.lookupIndices = ids = []
            for lookup in feature._lookups:
                lookup = lookup() # Link through the weakref
                if lookup in self.lookups: # If it exists, add the index
                    ids.append(self.lookups.index(lookup))
        for script in self.scripts.values():
            for language in script.languages.values():
                language.featureIndices = ids = []
                for feature in language._features:
                    feature = feature() # Link through the weakref
                    if feature in self.features: # If it exists, add the index
                        ids.append(self.features.index(feature))
        # Update the index of the referenced lookups in type 8 (or 9) for GSUB
        # and type 6 (or 7) for GPOS.
        for lookup in self.lookups:
            lookup.updateLookupIndices(self.lookups)

    def monitorLookups(self, glyphNames, lookups=None):
        lookups = self.getLookupsOfGlyphs(glyphNames, lookups)
        print('===== Lookups:', len(lookups))
        for index, lookup in enumerate(lookups):
            print('XXXXX', index, glyphNames, lookup, lookup.getGlyphNames())

    #    Q U E R Y  T O O L S

    def getGlyphNames(self):
        """Answer the set with all glyph names of the state. Combines all input glyphs
        and all output glyphs, seen from the perspective of the current scripts and lanages."""
        glyphNames = []
        for script in self.scripts.values():
            for language in script.languages.values():
                for feature in language.features:
                    for lookup in feature.lookups:
                        for glyphName in lookup.getGlyphNames():
                            glyphNames.append(glyphName)
        #
        #for lookup in self.lookups:
        #    for glyphName in lookup.getGlyphNames():
        #        glyphNames.append(glyphName)
        return set(glyphNames)

    def getInputGlyphNames(self):
        # Answer the set of glyph names that are used on the input side of the lookups.
        glyphNames = []
        for script in self.scripts.values():
            for language in script.languages.values():
                for feature in language.features:
                    for lookup in feature.lookups:
                        for glyphName in lookup.getGlyphNames():
                            glyphNames.append(glyphName)
        #for lookup in self.lookups:
        #    for glyphName in lookup.getInputGlyphNames():
        #        glyphNames.append(glyphName)
        return set(glyphNames)

    def getUniqueLookups(self):
        # Answer the dictionary with a set of unique related lookups, with their tag as key.
        lookups = {}
        for feature in self.features:
            if not feature.tag in lookups:
                lookups[feature.tag] = []
            for lookup in feature._lookups:
                lookup = lookup()
                lookups[feature.tag].append(lookup)
        return lookups

    def findLookupsUsingGlyph(self, glyphName):
        lookups = []
        for lookup in self.lookups:
            if glyphName in lookup.getGlyphNames():
                lookups.append(lookup)
        return lookups

    def isUsingGlyph(self, glyphName):
        return len(self.getLookupsUsingGlyph(glyphName)) > 0

    def getIndexOfLookup(self, lookup):
        if lookup in self.lookups:
            return self.lookups.index(lookup)
        return None

    def glyphUsage(self, glyphName):
        """Answer a report dictionary with lines of text about the usage of _glyphName_ in self."""
        usage = ['']
        for lookup in set(self.lookups):
            u = lookup.glyphUsage(glyphName)
            if u:
                usage.append('\tUsage %s' % u)
            if glyphName in lookup.getGlyphNames():
                usage.append('\tLookup type=%s' % (lookup.type))
                for feature in set(lookup.features):
                    usage.append('\t\tFeature name=%s' % feature.tag)
                    for language in set(feature.languages):
                        usage.append('\t\t\tLanguage name=%s, script=%s' % (language.tag, language.script.tag))
        return usage

class GPOSState(GState):
    pass

class GSUBState(GState):

    NOGLYPH = '<span style="color:red;">NOGLYPH(%s)</span>'

    def saveSpecimenPage(self, font, path):
        if not path.endswith('.html'):
            path += '.html'
        parts = path.split('/')
        path = '/'.join(parts[:-1]) + '/proof/GSUBspecs/'
        try:
            os.makedirs(path)
        except:
            pass
        f = open(path + parts[-1], 'w+')
        f.write('<html><head>\n')
        f.write('<title>Specimen GSUB</title>\n')
        f.write('<meta content="text/html;charset=UTF-8" http-equiv="Content-Type"/>\n')
        f.write('<style>')
        f.write('body {font-family: Verdana; font-size:13px;}')
        f.write('table, tr, td, th {margin: 0;font-size:13px;}')
        f.write('table {width: 100%;border-collapse:collapse; border-spacing:0;}')
        f.write('td {vertical-align: top;}')
        f.write('td.line1 {border-top: 1px solid #808080;}')
        f.write('span.gray {color:#AAAAAA;}')
        f.write('span.noUnicode {color:green;}')
        path = '.'.join(font.path.split('/')[-1].split('.')[:-1])
        f.write("""@font-face {
               src: url('../fonts/%(path)s.eot'); /* IE < 9 */
               src: url('../fonts/%(path)s.eot?#') format("embedded-opentype"), /* IE 9 */
                    url('../fonts/%(path)s.woff') format("woff"),
                    url('../fonts/%(path)s.ttf') format("opentype"),
                    url('../fonts/%(path)s.svg') format("svg");
               font-family: Segoe;
               font-style: normal;
               font-weight: normal;
               }
             span.currentFont { color: #800000;
             font-family: Segoe, "Zero Width Space", "FB Unicode Fallback";
             }
             span.featured { color: red;
             font-family: Segoe, "Zero Width Space", "FB Unicode Fallback";
             }
        """ % dict(path=path))
        f.write('</style>')
        f.write('</head><body>\n')
        f.write('<h1>Script-language-feature-lookup</h1>\n')
        self.saveSpecimenPage_Scripts(f, font)
        f.write('</body></html>\n')
        f.close()

    def saveSpecimenPage_Scripts(self, f, font):
        f.write('<table>\n')
        f.write('<tr><th>Script</th></tr>\n')
        for _, script in sorted(self.scripts.items()):
            f.write('<tr>\n')
            f.write('<td class="line1" width="10%%">%s</td>\n' % script.tag)
            f.write('<td class="line1">\n')
            self.saveSpecimenPage_Languages(f, font, script)
            f.write('</td>\n')
            f.write('</tr>\n')
        f.write('</table>\n')

    def saveSpecimenPage_Languages(self, f, font, script):
        f.write('<table>\n')
        for lIndex, (languageName, language) in enumerate(sorted(script.languages.items())):
            f.write('<tr>')
            line = {True:1, False:0}[lIndex!=0]
            f.write('<td class="line%d" width="10%%">%s</td>\n' % (line, languageName))
            f.write('<td class="line%d">\n' % line)
            self.saveSpecimenPage_Features(f, font, language)
            f.write('</td>\n')
            f.write('</tr>')
        f.write('</table>\n')

    def saveSpecimenPage_Features(self, f, font, language):
        f.write('<table>')
        for fIndex, feature in enumerate(language.features):
            f.write('<tr>')
            line = {True:1, False:0}[fIndex!=0]
            f.write('<td class="line%d" width="10%%">%s</td>\n' % (line, feature.tag))
            f.write('<td class="line%d">\n' % line)
            self.saveSpecimenPage_Lookups(f, font, feature.lookups)
            f.write('</td>\n')
            f.write('</tr>')
        f.write('</table>')

    def saveSpecimenPage_Lookups(self, f, font, lookups):
        f.write('<table>')
        for luIndex, lookup in enumerate(lookups):
            extendedLookups = []
            if lookup is None:
                pass # Lookup in the list became None, ignore in the output
            elif lookup.type == 7:
                for subLookup in lookup.subs:
                    extendedLookups.append(subLookup.extension)
            else:
                extendedLookups.append(lookup)
            for lookup in extendedLookups:
                f.write('<tr>')
                self.saveSpecimenPage_Lookup(f, font, lookup, luIndex)
                f.write('</tr>')
        f.write('</table>')

    def saveSpecimenPage_Lookup(self, f, font, lookup, luIndex):
        hook = 'saveSpecimenPage_Lookup%d' % lookup.type
        getattr(self, hook)(f, font, lookup, luIndex)

    def saveSpecimenPage_Lookup1(self, f, font, lookup, luIndex):
        class_ = {True:'line1', False:'line0'}[luIndex!=0]
        f.write('<td class="%s" width="15%%">#%d&nbsp;Lookup%d %0X<br/>Simple Substitution</td>\n' % (class_, luIndex, lookup.type, id(lookup)))
        f.write('<td class="%s">\n' % class_)
        f.write('<table>')
        if hasattr(lookup, 'single'):
            for sourceGlyph, targetGlyph in sorted(lookup.single.items()):
                f.write(u'<tr><td width="45%%">\n')
                f.write(self.getFormattedGlyphName(font, sourceGlyph))
                f.write('</td><td>–></td><td width="45%%">')
                f.write(self.getFormattedGlyphName(font, targetGlyph))
                f.write('</td></tr>')
        else:
            f.write('<tr><td><span style="color:red;">XXXXX Lookup1 missing single attribute></span></td></tr>')
        f.write('</table>')
        f.write('</td>\n')

    def saveSpecimenPage_Lookup2(self, f, font, lookup, luIndex):
        # Ligatures
        class_ = {True:'line1', False:'line0'}[luIndex!=0]
        f.write('<td class="%s" width="15%%">#%d&nbsp;Lookup%d %0X<br/>Multiple substitution</td>\n' % (class_, luIndex, lookup.type, id(lookup)))
        f.write('<td class="%s">\n' % class_)
        f.write('<table>')
        if hasattr(lookup, 'coverage'):
            for index, glyph in enumerate(lookup.coverage.glyphs):
                glyphs = []
                for glyphName in lookup.sequences[index]:
                    glyphs.append(self.getFormattedGlyphName(font, glyphName))
                f.write(u'<tr><td width="45%%">\n')
                f.write(', '.join(glyphs))
                f.write('<br/>')
                f.write('</td><td>–></td><td width="45%%">')
                f.write(self.getFormattedGlyphName(font, glyph))
                f.write('</td></tr>')
        else:
            f.write('<tr><td><span style="color:red;">XXXXX Lookup2 missing coverage attribute></span></td></tr>')
        f.write('</table>')
        f.write('</td>\n')

    def saveSpecimenPage_Lookup3(self, f, font, lookup, luIndex):
        #class_ = {True:'line1', False:'line0'}[luIndex!=0]
        print('saveSpecimenPage_Lookup3: to_be_implemented')

    def saveSpecimenPage_Lookup4(self, f, font, lookup, luIndex):
        # Ligatures
        class_ = {True:'line1', False:'line0'}[luIndex!=0]
        f.write('<td class="%s" width="15%%">#%d&nbsp;Lookup%d %0X<br/>Ligatures</td>\n' % (class_, luIndex, lookup.type, id(lookup)))
        f.write('<td class="%s">\n' % class_)
        f.write('<table>')
        if hasattr(lookup, 'ligatures'):
            for sourceGlyph, ligature in lookup.ligatures.items():
                self.saveSpecimenPage_LigatureSet(f, font, sourceGlyph, ligature)
        else:
            f.write('<tr><td><span style="color:red;">XXXXX Lookup4 missing ligature attribute></span></td></tr>')
        f.write('</table>')
        f.write('</td>\n')

    def saveSpecimenPage_Lookup5(self, f, font, lookup, luIndex):
        #class_ = {True:'line1', False:'line0'}[luIndex!=0]
        print('saveSpecimenPage_Lookup5: to_be_implemented')

    def saveSpecimenPage_Lookup6(self, f, font, lookup, luIndex):
        # Ligatures
        class_ = {True:'line1', False:'line0'}[luIndex!=0]
        f.write('<td class="%s" width="15%%">#%d&nbsp;Lookup%d %0X<br/>Chaining Contextual Substitution</td>\n' % (class_, luIndex, lookup.type, id(lookup)))
        f.write('<td class="%s">\n' % class_)
        f.write('<table>')
        if hasattr(lookup, 'chains'):
            for chain in lookup.chains:
                f.write(u'<tr><td width="45%%">\n')
                if chain.backtrackCoverage:
                    f.write('Backtrack[')
                    for btCoverage in chain.backtrackCoverage:
                        glyphs = []
                        for glyphName in btCoverage.glyphs:
                            glyphs.append(self.getFormattedGlyphName(font, glyphName))
                        f.write('(%s)' % ', '.join(glyphs))
                    f.write(']<br/>')
                if chain.inputCoverage:
                    f.write('Input[')
                    for iCoverage in chain.inputCoverage:
                        glyphs = []
                        for glyphName in iCoverage.glyphs:
                            glyphs.append(self.getFormattedGlyphName(font, glyphName))
                        f.write('(%s)' % ', '.join(glyphs))
                    f.write(']<br/>')
                if chain.lookAheadCoverage:
                    f.write('Lookahead[')
                    for laCoverage in chain.lookAheadCoverage:
                        glyphs = []
                        for glyphName in laCoverage.glyphs:
                            glyphs.append(self.getFormattedGlyphName(font, glyphName))
                        f.write('(%s)' % ', '.join(glyphs))
                    f.write(']<br/>')
                if chain.lookups:
                    f.write('Chain lookups<br/>')
                    lookups = []
                    for chainLookup in chain.lookups:
                        lookups.append(chainLookup.lookup)
                    self.saveSpecimenPage_Lookups(f, font, lookups)
                f.write('</td>')
        else:
            f.write('<tr><td><span style="color:red;">XXXXX Lookup6 missing chains attribute></span></td></tr>')
        f.write('</table>')
        f.write('</td>\n')

    def saveSpecimenPage_LigatureSet(self, f, font, sourceGlyph, ligature):
        for ligatureSources in ligature:
            f.write(u'<tr><td width="45%%">\n')
            sourceGlyphs = [self.getFormattedGlyphName(font, sourceGlyph)]
            if font[sourceGlyph].unicode is not None:
                unicodes = ['&#x%04X;' % font[sourceGlyph].unicode]
            else:
                unicodes = ['*%s*' % sourceGlyph]
            for glyphName in ligatureSources.components:
                if font[glyphName].unicode is not None:
                    unicodes.append('&#x%04X;' % font[glyphName].unicode)
                else:
                    unicodes.append('*%s*' % glyphName)
                sourceGlyphs.append(self.getFormattedGlyphName(font, glyphName))
            f.write(', '.join(sourceGlyphs))
            f.write('</td><td>–></td><td width="45%%">')
            f.write(self.getFormattedGlyphName(font, ligatureSources.lig))
            # Write actual combination
            f.write('&nbsp;[&nbsp;<span class="featured">%s</span>&nbsp;]' % ''.join(unicodes))
            f.write('</td>')
            f.write('</tr>\n')

    def getFormattedGlyphName(self, font, glyphName):
        if font[glyphName] is None:
            glyphName = self.NOGLYPH % glyphName
        elif font[glyphName].unicode:
            glyphName = '%s&nbsp;<span class="gray">#%04X</span>&nbsp;[&nbsp;<span class="currentFont">&#x%04X;</span>&nbsp;]'  % (glyphName, font[glyphName].unicode, font[glyphName].unicode)
        else:
            glyphName = '<span class="noUnicode">%s</span>' % glyphName
        return glyphName

class Lookup(State):
    # The Lookup is the parent of sets of lookup subs with the same type.
    def __init__(self, type, flag):
        self.type = type
        self.flag = flag
        self.subs = [] # Storage of the sub lookups,
        # Data attributes to be added, depending on the lookup format
        # References to parents to be filled on 2nd decompile phase.
        self._languages = []     # List of weakref languages for this lookup.
        self._features = []      # List of weakref parent features for this lookup.

    def isList(self):
        return True # To differentiate from the child Lookup instance

    def hasAliveParent(self):
        # Answer if there is at least one feature alive for this lookup.
        # Note that for lookup with other lookup references, we also have to check
        # if there still is a live reference there too.
        return len(self.features) > 0 and len(self.languages) > 0

    def keepIt(self):
        # Keep the lookup if one of the subs needs to be kept.
        keepIt = False
        for sub in self.subs:
            if not isinstance(sub.keepIt(), bool):
                sub.keepIt()
                pass
        for sub in self.subs:
            if sub.keepIt():
                keepIt = True
                break
        return keepIt

    def getGlyphNames(self):
        """Answer the list with all glyph names of the lookup (from input and output)."""
        glyphNames = []
        for sub in self.subs:
            for glyphName in sub.getGlyphNames():
                if not glyphName in glyphNames:
                    glyphNames.append(glyphName)
        return glyphNames

    def getInputGlyphNames(self):
        """Answer the set with all input glyph names of the lookup."""
        glyphNames = []
        for sub in self.subs:
            subNames = sub.getInputGlyphNames()
            if subNames is not None:
                for name in sub.getInputGlyphNames():
                    if not name in glyphNames:
                        glyphNames.append(name)
        return glyphNames
    '''
    def _getStatesOfGlyphs(self, states, glyphNames):
        """Answer the states that contain the named glyphs."""
        if not isinstance(glyphNames, (list, tuple)):
            glyphNames = [glyphNames]
        states = []
        for state in states:
            for glyphName in glyphNames:
                if glyphName in state.getGlyphNames():
                    states.append(script)
                    break
        return states
    '''
    def glyphUsage(self, glyphName):
        """Answer the result of digging into the lookup to find glyph names, relations and positions."""
        usages = []
        for sub in self.subs:
            usage = sub.glyphUsage(glyphName)
            if usage:
                usages.append(usage)
        return ', '.join(usages)

    def deleteGlyph(self, glyphName):
        # Delete the glyph as entry from all glyph lists in the lookup
        for sub in self.subs:
            sub.deleteGlyph(glyphName)

    def deleteInputGlyph(self, glyphName):
        # Delete the glyph as entry, if it is in the input side of the lookup
        for sub in self.subs:
            sub.deleteInputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        # Delete the glyph as entry, if it is in the output side of the lookup
        for sub in self.subs:
            sub.deleteOutputGlyph(glyphName)

    # self.referencingLookups

    def attachReferencingLookup(self, lookup):
        # Backward referencing of indexed lookup
        for sub in self.subs:
            sub.attachReferencingLookup(lookup)

    def attachIndexReferencedLookups(self, lookups):
        # Forward referencing of indexed lookup
        for sub in self.subs:
            sub.attachIndexReferencedLookup(self, lookups)

    def _get_referencingLookups(self):
        # Allow testing if another lookup is referencing to this lookup.
        # Answer the list with real lookup instances. This means that if the
        # answers list is empty, there are no other lookups referring to self.
        # Remove the dead wood.
        return self.subs[0].referencingLookups

    referencingLookups = property(_get_referencingLookups)

    def getFeatureTalk(self, tag, groupset, indent=0):
        ft = []
        if len(self.subs) > 1:
            ft.append('%slookup %s {\n' % (indent*'\t', 'XXX'))
            indent += 1
        for sub in self.subs:
            ft.append(sub.getFeatureTalk(tag, groupset, indent))
        if len(self.subs) > 1:
            ft.append('%s} %s;\n' % (indent*'\t', 'XXX'))
        return ''.join(ft)

    # self.languages

    def _get_languages(self):
        # API to weakref self._languages attribute
        # Beware that the answered list is constructed. Is it not the real self._languages.
        # For changes, the entire list needs to be replace by self.languages = newLanguages
        languages = []
        for language in self._languages:
            language = language() #  Get the real language state
            if language is not None: # Is it still valid, then answer it
                languages.append(language)
        return tuple(languages) # Make read-only

    def _set_languages(self, languages):
        # API to weakref self._languages attribute
        self._languages = []
        for language in languages:
            self.addLanguage(language)

    languages = property(_get_languages, _set_languages)

    def addLanguage(self, language):
        self._languages.append(weakref.ref(language))
        return language # Answer the language for convenience

    # self.features

    def _get_features(self):
        # API to weakref self._features attribute
        # Beware that the answered list is constructed. Is it not the real self._features.
        # For changes, the entire list needs to be replace by self.features = newFeatures
        # Use self.addFeature(feature) to add single features.
        features = []
        for feature in self._features:
            feature = feature() #  Get the real feature state
            if feature is not None: # Is it still valid, then answer it
                features.append(feature)
        return tuple(features) # Make read-only

    def _set_features(self, features):
        # API to weakref self._features attribute
        self._features = []
        for feature in features:
            self.addFeature(feature)

    features = property(_get_features, _set_features)

    # features

    def addFeature(self, feature):
        self._features.append(weakref.ref(feature))

class LookupSub(State):
    # The LookupSub instance is the "real" feature object, that holds the data for the feature
    # line and lists of links that point back to the parent scripts, languages and features.
    # The references go as weak links as: script-(weak)->language-(weak)->feature-(weak)->lookup
    # and then the reverse script<-(weak)-language<-(weak)-feature<-(weak)-lookup
    # The com
    # LookupType 1    @single
    # LookupType 2    @coverage, @sequence
    # LookupType 3    ... (etc)
    # GSUB and GPOS have their own lookup type dependent inheriting classes from this one.
    # Then lookup.type is available as class variable to test the type of a lookup.
    # All attribute who's name does not start with _ are stored into json
    # Dynamic references such as the self._languages and self._features and all weakrefs are
    # not stored json, they will be rebuild upon reading from the updated index lists.
    #
    # self.referencingLookups
    # This is the (expanded) set of lookup instances that refer to self

    def initializeReferencingLookups(self):
        if not hasattr(self, '_referencingLookups'):
            self._referencingLookups = []

    def attachReferencingLookup(self, lookup):
        self.initializeReferencingLookups()
        self._referencingLookups.append(weakref.ref(lookup))

    def attachIndexReferencedLookup(self, parent, lookups):
        # Attach the referenced lookup.
        pass

    def _get_referencingLookups(self):
        # Allow testing if another lookup is referencing to this lookup.
        # Answer the list with real lookup instances. This means that if the
        # answers list is empty, there are no other lookups referring to self.
        self.initializeReferencingLookups()
        referencingLookups = []
        for lookupRef in self._referencingLookups:
            lookup = lookupRef()
            if lookup is not None:
                referencingLookups.append(lookup)
        return referencingLookups

    referencingLookups = property(_get_referencingLookups)

class Feature(State):
    # The instance reference between script-->language and the lookup instance.
    # I would have called this the lookup, reversed with the naming of the Lookup class,
    # but since all GSUB documentation calls this the feature (as a set of lookups) we'll
    # keep it that way.
    # All attribute who's name does not start with _ are stored into json
    # Dynamic references such as the self._languages and self._features are not stored json,
    # they will be rebuild upon reading from the updated index lists.
    def __init__(self, tag, params, lookupIndices):
        self.tag = tag
        self.params = params
        self.lookupIndices = lookupIndices # Indices of the referred lookup instances. Becomes obsolete after parsing.
        # Direct references to lookup and languages will be filled on 2nd decompile phase.
        self._languages = [] # List of weakrefs to parent languages of this lookup.
        self._lookups = [] # List of weakref to the lookup instances.

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.tag)

    def hasAliveParent(self):
        # Answer if there is at least one feature alive for this lookup.
        return len(self.languages) > 0

    def keepIt(self):
        # Answer if this feature should be kept (if there is at least
        # one valid lookup)
        keepIt = False
        for lookup in self.lookups:
            # Test on None, the language of our weakref may have been deleted by a cleanup.
            if lookup is not None and lookup.keepIt():
                keepIt = True
                break
        return keepIt

    # self.lookups

    def _get_lookups(self):
        # API to weakref self._lookups attribute
        # Beware that the answered list is constructed. Is it not the real self._lookups.
        # For changes, the entire list needs to be replace by self.lookups = newLookups
        lookups = []
        for lookup in self._lookups:
            lookup = lookup() #  Get the real lookup state
            if lookup is not None: # Is it still valid, then answer it
                lookups.append(lookup)
        return tuple(lookups) # Make read-only

    def _set_lookups(self, lookups):
        # API to weakref self._lookups attribute.
        # Add all lookups to self._lookups as weakref, if the lookup is not None
        self._lookups = []
        for lookup in lookups:
            if lookup is not None:
                self.addLookup(lookup)

    lookups = property(_get_lookups, _set_lookups)

    def addLookup(self, lookup):
        assert lookup is not None
        self._lookups.append(weakref.ref(lookup))

    # self.languages

    def _get_languages(self):
        # API to weakref self._languages attribute
        # Beware that the answered list is constructed. It is not the real self._languages.
        # For changes, the entire list needs to be replace by self.languages = newLanguages
        languages = set()
        for language in self._languages:
            language = language() # Get the real language state
            if language is not None: # Is it still valid, then answer it
                languages.add(language)
        return tuple(languages) # Make read only

    def _set_languages(self, languages):
        # API to weakref self._languages attribute
        self._languages = []
        for language in languages:
            self.addLanguage(language)

    languages = property(_get_languages, _set_languages)

    def addLanguage(self, language):
        self._languages.append(weakref.ref(language))
        return language # Answer the language for convenience

    def getGlyphNames(self):
        glyphNames = []
        for lookup in self.lookups:
            for glyphName in lookup.getGlyphNames():
                glyphNames.append(glyphName)
        return glyphNames

class Script(State):
    # The instance that holds the script-->languages references.
    def __init__(self, tag):
        self.tag = tag
        self._languages = {} # Dictionary of weakrefs to the the script languages. Key is the language tag. Includes default "dflt"

    def getDefault(self):
        # Answer the default, stored as "dflt" key. If the default does not exist, then answer None
        return self.languages.get('dflt')

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.tag)

    def keepIt(self):
        """Answer if the script is still valid. It needs at least one valid languages."""
        keepIt = False
        for language in self.languages.values():
            if language.keepIt():
                keepIt = True
                break
        return keepIt

    # self.languages

    def _get_languages(self):
        # API to weakref self._languages attribute
        # Beware that the answered dictionary is constructed. It is not the real self._languages.
        # For changes, the entire dictionary needs to be replace by self.languages = newLanguages
        languages = {}
        for key, language in self._languages.items():
            language = language() # Get the real language state
            if language is not None: # Is it still valid, then answer it
                languages[key] = language
        return languages # It a new dictionary. Changing it won't reflect in the original self._languages

    def _set_languages(self, languages):
        # API to weakref self._languages attribute
        self._languages = []
        for name, language in languages.items():
            self.addLanguage(name, language)

    languages = property(_get_languages, _set_languages)

    def addLanguage(self, name, language):
        self._languages[name] = weakref.ref(language)
        return language # Answer the language for convenience

class Language(State):
    # The instance that holds the language-->feature references
    # All attribute who's name does not start with _ are stored into json
    # Dynamic references such as the self._languages and self._features are not stored json,
    # they will be rebuild upon reading from the updated index lists.
    def __init__(self, tag, featureIndices, lookupOrder, reqFeatureIndex, script):
        self.tag = tag
        self.featureIndices = featureIndices # Indices of the referred feature instances. Becomes obsolete after parsing.
        self._features = [] # List of the weakref feature instances.
        self.script = script # Set weakref to the parent script
        self.lookupOrder = lookupOrder
        self.reqFeatureIndex = reqFeatureIndex

    def __repr__(self):
        return '%s(%s)-->%s' % (self.__class__.__name__, self.tag, self.script)

    def hasAliveParent(self):
        # Answer if there is at least one feature alive for this lookup.
        return self.script is not None

    def keepIt(self):
        # Answer if this language should be kept (if the script does still exists)
        # and if there is still one or more valid features in the list.
        keepIt = False
        for feature in self.features:
            # Check if this feature has been deleted by a cleanup.
            if feature is not None and feature.keepIt():
                keepIt = True
                break
        return self.script is not None and keepIt

    # self.features

    def _get_features(self):
        # API to weakref self._features attribute.
        # Beware that the answered list is constructed. Is it not the real self._features.
        # For changes, the entire list needs to be replace by self.languages = newLanguages
        features = []
        for feature in self._features:
            feature = feature() # Get the real language state
            if feature is not None: # Is it still valid, then answer it
                features.append(feature)
        return tuple(features) # Make read-only

    def _set_features(self, features):
        self._features = []
        for feature in features:
            self.addFeature(feature)

    features = property(_get_features)

    def addFeature(self, feature):
        self._features.append(weakref.ref(feature))

    # self.script

    def _get_script(self):
        # API to weakref self._script attribute
        if self._script is not None:
            return self._script()
        return None

    def _set_script(self, script=None):
        # API to set weakref self._script attribute
        # If script is None or omitted, then clear the attribute.
        if script is not None:
            script = weakref.ref(script)
        self._script = script

    script = property(_get_script, _set_script)

    def getGlyphNames(self):
        glyphNames = []
        for feature in self.features:
            for glyphName in feature.getGlyphNames():
                glyphNames.append(glyphName)
        return glyphNames

class Coverage(State):
    def __init__(self, glyphs, format):
        self.glyphs = glyphs
        self.format = format

    def keepIt(self):
        # Keep this coverage if there is one or more glyphs in the list.
        return len(self.glyphs) > 0

    def deleteGlyph(self, glyphName):
        while glyphName in self.glyphs:
            del self.glyphs[self.glyphs.index(glyphName)]

class Chain(State):
    # GSUB lookup type 6 container
    def __init__(self):
        self.lookups = []

    def keepIt(self):
        # Check if there is something remaining to be used.
        hasInput = False
        hasBacktrack = False
        hasLookAhead = False
        for coverage in self.inputCoverage:
            if coverage.keepIt():
                hasInput = True
                break
        for coverage in self.backtrackCoverage:
            if coverage.keepIt():
                hasBacktrack = True
                break
        if not hasBacktrack:
            for coverage in self.lookAheadCoverage:
                if coverage.keepIt():
                    hasLookAhead = True
                    break
        return hasInput and (hasBacktrack or hasLookAhead)

    def deleteGlyph(self, glyphName):
        # Delete the glyphName from all coverages.
        self.deleteOutputGlyph(glyphName)
        self.deleteInputGlyph(glyphName)

    def deleteInputGlyph(self, glyphName):
        # Delete the glyphName from the input coverage
        for coverage in self.backtrackCoverage:
            coverage.deleteGlyph(glyphName)
        for coverage in self.lookAheadCoverage:
            coverage.deleteGlyph(glyphName)
        for coverage in self.inputCoverage:
            coverage.deleteGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        for lookup in self.lookups:
            lookup.deleteOutputGlyph(glyphName)

class ChainLookup(State):
    # Storage of the link between a lookup type 6 subsLookup and the actual lookup
    # Just store the lookup index for now. In the 2nd phase of the decompile, the
    # actual lookup will be referenced in self.lookup. After that the lookupIndex
    # becomes invalid. For debug purposed we'll keep the original index.
    def __init__(self, lookupIndex, sequenceIndex):
        self.orgLookupIndex = self.lookupIndex = lookupIndex
        self._lookup = None # To be set from the index after all lookups are defined from source.
        self.sequenceIndex = sequenceIndex

    def keepIt(self):
        if self.lookup is not None:
            return self.lookup.keepIt()
        return False

    # self.lookup

    def _get_lookup(self):
        # API to weakref self._lookup attribute
        if self._lookup is not None:
            return self._lookup()
        return None

    def _set_lookup(self, lookup=None):
        # API to wekref self._lookup attribute
        # If lookup is None or omitted, then clear the attribute
        if lookup is not None:
            lookup = weakref.ref(lookup)
        self._lookup = lookup

    lookup = property(_get_lookup, _set_lookup)

    def glyphUsage(self, glyphName):
        return self.lookup.glyphUsage(glyphName)

    def deleteOutputGlyph(self, glyphName):
        self.lookup.deleteOutputGlyph(glyphName)

class PairPos(State):
    # GPOS extension position container
    def __init__(self, type, format):
        self.type = type
        self.format = format

    def glyphUsage(self, glyphName):
        return 'PairPos=(value1:%s value2:%s)' % (self.value1.glyphUsage(glyphName), self.value2.glyphUsage(glyphName))

class Pair(State):
    # GPOS extension storage of pair values
    def glyphUsage(self, glyphName):
        return 'Pair'

class PairValue(State):
    # GPOS extension storage of pair values
    def __init__(self, secondGlyph, value1, value2):
        self.secondGlyph = secondGlyph
        self.value1 = Value(value1)
        self.value2 = Value(value2)

    def glyphUsage(self, glyphName):
        v1 = self.value1.glyphUsage(glyphName)
        v2 = self.value2.glyphUsage(glyphName)
        if v1 or v2:
            return 'Pairvalue=(value1:%s value2:%s)' % (v1, v2)
        return ''

class Anchor(State):
    def __init__(self, x, y, format, class_=None):
        # Used as baseAnchor there is no class defined.
        # Used as markAnchor there is a class.
        self.x = x
        self.y = y
        self.format = format
        self.class_ = class_

    def glyphUsage(self, glyphName):
        return 'Anchor=(x:%s y:%s format:%s)' % (self.x, self.y, self.format)

class ClassGroup(State):
    # GPOS container of class groups. Many more attributes added on decompile
    def __init__(self, type, format):
        self.type = type
        self.format = format

class ClassDef(State):
    def __init__(self, format):
        self.format = format

class Value(State):
    def __init__(self, gValue, valueFormat=None):
        # Also?
        # XPlaDevice
        # YPlaDevice
        # XAdvDevice
        # YAdvDevice
        self.valueFormat = valueFormat
        self.XPlacement = self.YPlacement = self.XAdvance = self.YAdvance = None
        if gValue is not None:
            if hasattr(gValue, 'XAdvance'):
                self.XAdvance = gValue.XAdvance
            if hasattr(gValue, 'XPlacement'):
                self.XPlacement = gValue.XPlacement
            if hasattr(gValue, 'YAdvance'):
                self.YAdvance = gValue.YAdvance
            if hasattr(gValue, 'YPlacement'):
                self.YPlacement = gValue.YPlacement

    def glyphUsage(self, glyphName):
        return 'Value=(Adv:%s,%s Pos:%s,%s)' % (self.XAdvance, self.YAdvance, self.XPlacement, self.YPlacement)

class Ligature(State):
    # Lookup data containers for ligature glyph and component names.
    def __init__(self, glyphName, ligName, components):
        self.glyph = glyphName
        self.lig = ligName
        self.components = components

    def keepIt(self):
        # Answer if this ligature is still valid.
        return self.glyph and self.lig and len(self.components) > 0

    def glyphUsage(self, glyphName):
        """Answer the glyph usage if the glyph name matches."""
        if self.glyph != glyphName:
            return ''
        usages = ['Ligature=(Glyph:%s Lig:%s' % (self.glyph, self.lig)]
        for component in self.components:
            usages.append(component.glyphUsage(glyphName))
        return ' '.join(usages)

    #   C F F

class CFFState(State):
    """Supports the storage and API of a complete CFF structure."""
    pass
