
from tnbits.toolbox.file import File
from tnbits.toolbox.font import FontTX
from tnbits.toolbox.glyph import GlyphTX
from tnbits.constants import Constants as C
import datetime
from collections import OrderedDict
from fbot2.glyphNameLib import GlyphName
from mojo.roboFont import OpenFont
from defcon.objects.uniData import UnicodeData
###########
# LINES
###########

class FeatureValidateCache(object):
    def __init__(self):
        self.validGroups = []
        self.validGlyphs = []
        self.validLookups = []

class FeatureBase(object):

    NEWLINE = '\r'

    VERBOSE = False

    def __init__(self):
        pass

    def __repr__(self):
        return '<%s:%s>' %(self.getType(), self.getName())

    def getType(self):
        return 'null'

    ### name
    def getName(self):
        if 'name' in self.__dict__:
            return self.name
        else:
            return None
    def setName(self, name=None):
        self.name = name

    ### title
    def getTitle(self):
        if 'title' in self.__dict__:
            return self.title
        else:
            return None

    def setTitle(self, title=None):
        self.title = title

    ### font
    def getFont(self):
        return self._font or None
    def setFont(self, font):
        self._font = font
    def getUnicodeData(self):
        try:
            return self.getFont().naked().unicodeData
        except:
            u  = UnicodeData()
            u.setParent(self.getFont())
            return u

    def collapse(self):
        if not self.getGroups() and not self.getContents():
            return None
        else:
            return self

    #### references ####

    def makeReferences(self, l):
        """
        Given a list of references, convert any passed strings and inline groups to Reference Objects.
        """
        referenceList = []
        for s in l:
            # if this is passed a string, it is either a glyphRef or groupRef
            if s is None:
                pass
            elif type(s) is str:
                if len(s) > 1 and s[0] == '@':
                    referenceList.append(FeatureGroupRef(s[1:]))
                else:
                    referenceList.append(FeatureGlyphRef(s))
            # if it is passed an inline group, make sure the inline group also contains references
            elif s.getType() is 'groupInline':
                refs = self.makeReferences(s.getContents())
                referenceList.append(FeatureGroupInline(refs))
            # otherwise just add it
            else:
                referenceList.append(s)
        return referenceList

    def flattenReferences(self, references):
        """
        Return a flat list of references, breaking apart any inline groups.
        """
        newReferences = []
        for ref in references:
            if ref.getType() is 'groupInline':
                newReferences += ref.getReferences()
            else:
                newReferences.append(ref)
        return newReferences

    def getReferences(self):
        """
        Return a list reference objects that are contained in self.
        """
        references = []
        for c in self.getContents():
            references += c.getReferences()
        return references

    def getReferencesByType(self, types=[]):
        """
        Return a list of only certain references, based on their string types.
        """
        allRefs = self.getReferences()
        typedRefs = []
        for ref in allRefs:
            if ref.getType() in types:
                typedRefs.append(ref)
        return typedRefs

    def getGlyphReferences(self):
        return self.getReferencesByType(['glyphRef'])

    def getGroupReferences(self):
        return self.getReferencesByType(['groupRef'])

    def getLookupReferences(self):
        return self.getReferencesByType(['lookupRef'])

    def getScriptsToLanguagesMap(self):
        scriptsToLanguages = OrderedDict()
        scripts = self.getContentsByType(['script'])
        for script in scripts:
                scriptsToLanguages[script] = script.getContentsByType(['language'])
        return scriptsToLanguages

    #### validation ####

    def getCache(self):
        if not 'cache' in self.__dict__:
            self.cache = FeatureValidateCache()
        return self.cache

    def clearCache(self):
        self.cache = FeatureValidateCache()

    def validate(self, source):
        validated = True
        references = self.getReferences()
        for ref in references:
            if not ref.validate(source):
                validated = False
        return validated

    def makeValidGroups(self, source, tabs=0):
        if self.VERBOSE: print(self.tabs(tabs) + 'makeValidGroups', self)
        groups = self.getGroups()
        newGroups = []
        for g in groups:
            gv = g.makeValid(source, tabs=tabs+1)
            if gv:
                newGroups.append(gv)
                #groups[groups.index(g)] = gv
            else:
                #groups.pop(groups.index(g))
                if self.VERBOSE: print(self.tabs(tabs) + 'removing group:', g.write())
        self.setGroups(newGroups)
        return newGroups

    def makeValidContents(self, source, tabs=0):
        contents = self.getContents()
        if self.VERBOSE: print(self.tabs(tabs) +  'makeValidContents', self, contents)
        newContents = []
        origLen = len(contents)
        for x, c in enumerate(contents):
            if self.VERBOSE: print(self.tabs(tabs) + '%s/%s: Content Item' % (x+1, origLen), c,)
            if self.VERBOSE:
                try:
                    print(c.getSource(), c.getDest())
                except:
                    print('')
            cv = c.makeValid(source, tabs=tabs+1)
            if cv:
                #if self.VERBOSE: print(self.tabs(tabs) + 'replacing content:', c)
                newContents.append(cv)
            else:
                if self.VERBOSE: print(self.tabs(tabs) + 'removing content:', c)
        self.setContents(newContents)
        return newContents

    def makeValid(self, source=None, tabs=0):
        if source is None:
            source = self
        if self.VERBOSE: print(self.tabs(tabs) + 'Base makeValid', self)
        self.makeValidGroups(source, tabs=tabs)
        self.makeValidContents(source, tabs=tabs)
        if self is source:
            self.clearCache()
        # what is required
        return self.collapse()

    #### contents ####

    def getContents(self):
        if 'contents' in self.__dict__:
            return self.contents
        else:
            return []

    def setContents(self, contents=[]):
        self.contents = self.makeReferences(contents)

    def getContentsByType(self, types):
        contentsByTypes = []
        if self.getType() in types:
            contentsByTypes.append(self)
        contents = self.getContents()
        if contents:
            for c in contents:
                if c:
                    contentsByTypes += c.getContentsByType(types=types)
                else:
                    pass
        return contentsByTypes

    def getContentNames(self, contents):
        return [c.getName() for c in contents]

    def getLanguageSystems(self):
        scriptsToLanguages = self.getScriptsToLanguagesMap()
        languageSystems = [('DFLT', 'dflt'), ('latn', 'dflt')]
        for script, languages in scriptsToLanguages.items():
            if script.getName() != 'latn':
                languageSystems.append((script.getName(), 'dflt'))
            for language in languages:
                languageSystems.append((script.getName(), language.getName()))
        print(languageSystems)
        return languageSystems

    #### groups ####

    def getGroups(self):
        if 'groups' in self.__dict__:
            return self.groups
        else:
            return []

    def setGroups(self, groups=[]):
        self.groups = self.makeReferences(groups)

    def getGroupNames(self):
        if 'groups' in self.__dict__:
            return [group.name for group in self.groups]
        else:
            return []


    def collectGroups(self, source):
        groupList = []
        groupList += source.getGroups()
        for c in source.getContents():
            if c:
                groupList += c.collectGroups(c)
            else:
                pass
        return groupList

    def collectGroupNames(self, source):
        groupList = []
        groupList += source.getGroupNames()
        for c in source.getContents():
            if c:
                groupList += c.collectGroupNames(c)

        return groupList


    #### write ####

    def write(self, tabs=0):
        lines = []
        #lines += self.writeGroups(tabs=tabs)
        #lines += self.writeLanguageSystems(tabs=tabs)
        lines += self.writeContents(tabs=tabs)
        return lines

    def tabs(self, tabs=0):
        return '\t' * tabs

    def writeStr(self, tabs=0):
        lines = self.write(tabs=tabs)
        s = ''
        for line in lines:
            if s == '':
                s += str(line)
            else:
                s += self.NEWLINE + str(line)
        return s

    def writeMeta(self, tabs=0):
        lines = []
        lines.append('# '+'='*50)
        if self.getFont():
            lines.append('# OpenType Features for %s %s' % (self.getFont().info.familyName, self.getFont().info.styleName))
        lines.append('# Generated on %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        lines.append('# '+'='*50)
        return lines

    def writeGroups(self, tabs=0):
        lines = []
        for g in self.collectGroups(self):
            lines.append(g.write(tabs=tabs+1))
        return lines

    def writeContents(self, tabs=0):
        """
        """
        lines = []
        for c in self.getContents():
            result = c.write(tabs=tabs+1)
            if type(result) is list:
                lines += result
            else:
                lines.append(result)
        return lines

    def writeLanguageSystems(self, tabs=0):
        tabs += 1
        languageSystems = self.getLanguageSystems()
        lines = []
        for script, language in languageSystems:
            lines.append(self.tabs(tabs) + 'languagesystem %s %s;' %(script, language))
        return lines

    def writeReferences(self, refs, tagged=[]):
        """
        Write a list of references.
        """
        if refs:
            s = ''
            for x, ref in enumerate(refs):
                refStr = ref.write()
                if x in tagged:
                    refStr += "'"
                if s == '':
                    s += refStr
                else:
                    s += ' ' + refStr
            return s
        else:
            return ''

    #### glyph manipulations ####

    def sort(self, names):
        # cannedDesign
        return self.getUnicodeData().sortGlyphNames(names, [dict(type="cannedDesign", allowPseudoUnicode=True)])

    def getLigatures(self,
                     glyphNames=None,
                     excludeGlyphNames=None,
                     baseNames=None,
                     excludeBaseNames=None,
                     suffixes=None,
                     excludeSuffixes=None,
                     ):
        f = self.getFont()

        subset = self.getGlyphSubset(glyphNames=glyphNames, excludeGlyphNames=excludeGlyphNames, baseNames=baseNames, excludeBaseNames=excludeBaseNames, suffixes=suffixes, excludeSuffixes=excludeSuffixes)
        #
        lengthsToLigatures = {}
        #
        for gname in subset:
            gn = GlyphName(gname)
            if len(gn.getBaseNames()) > 1 and 'scrap' not in gn.getSuffixes():
                baseNames = []
                for baseName in gn.getBaseNames():
                    bn = GlyphName(baseName=baseName, suffix=gn.getSuffixes())
                    baseNames.append(bn.getClosestExistingName(f))

                if len(gn.getBaseNames()) in lengthsToLigatures:
                    lengthsToLigatures[len(gn.getBaseNames())].append((gname, baseNames))
                else:
                    lengthsToLigatures[len(gn.getBaseNames())] = [(gname, baseNames)]
        keys = lengthsToLigatures.keys()
        keys.sort()
        keys.reverse()
        #
        ligatures = []
        for length in keys:
            ligs = lengthsToLigatures[length]
            ligatures += sorted(ligs)
        return ligatures


    def getGlyphSubset(self,
                       suffixes=None,
                       excludeSuffixes=None,
                       unicodeCategories=None,
                       excludeUnicodeCategories=None,
                       glyphNames=None,
                       excludeGlyphNames=None,
                       baseNames=None,
                       excludeBaseNames=None,
                       VERBOSE = False
                       ):
        f = self.getFont()
        results = []
        #for gname in f.glyphOrder:
        for g in f:
            go = True
            gn = GlyphName(str(g.name))
            baseName = gn.getBaseName()
            glyphSuffixes = gn.getSuffixes()
            if suffixes and 'scrap' in suffixes:
                go = False
            if suffixes is not None:
                if not glyphSuffixes or glyphSuffixes and not set(suffixes).issubset(set(glyphSuffixes)):
                    go = False
                    if VERBOSE: print('suffixes', suffixes, glyphSuffixes)
                if suffixes == [] and glyphSuffixes != []:
                    go = False
                    if VERBOSE: print('FAIL empty suffixes', suffixes, glyphSuffixes)
            if excludeSuffixes is not None:
                if set(glyphSuffixes) & set(excludeSuffixes):
                    go = False
                    if VERBOSE: print('FAIL excludeSuffixes', suffixes, glyphSuffixes)
            if unicodeCategories is not None and self.getUnicodeData().categoryForGlyphName(g.name) not in unicodeCategories:
                go = False
                if VERBOSE: print('FAIL unicodeCategories', self.getUnicodeData().categoryForGlyphName(g.name), unicodeCategories)
            if excludeUnicodeCategories is not None and self.getUnicodeData().categoryForGlyphName(g.name) in excludeUnicodeCategories:
                go = False
                if VERBOSE: print('excludeUnicodeCategories', self.getUnicodeData().categoryForGlyphName(g.name), unicodeCategories)
            if glyphNames is not None and g.name not in glyphNames:
                go = False
                if VERBOSE: print('glyphNames', glyphNames, g.name)
            if excludeGlyphNames is not None and g.name in excludeGlyphNames:
                go = False
                if VERBOSE: print('excludeGlyphNames', glyphNames, g.name)
            if baseNames is not None and baseName not in baseNames:
                go = False
                if VERBOSE: print('FAIL baseNames', baseName, baseNames)
            if excludeBaseNames is not None and baseName in excludeBaseNames:
                go = False
                if VERBOSE: print('FAIL excludeBaseNames', baseName, excludeBaseNames)
            if go:
                results.append(g.name)
            VERBOSE = False
        return self.sort(results)



class FeatureSub(FeatureBase):
    """
    Substitution statement.
    """
    def __init__(self, source=[], dest=[], joiner='by', tagged=[], groups=[]):
        self.setSource(source)
        self.setDest(dest)
        self.setJoiner(joiner)
        self.setTagged(tagged)
        self.setGroups(groups)

    def getType(self):
        return 'sub'

    #### source ####

    def getSource(self):
        return self.source
    def setSource(self, source):
        if type(source) is not list:
            source = [source]
        self.source = self.makeReferences(source)

    #### dest ####

    def getDest(self):
        return self.dest
    def setDest(self, dest):
        if type(dest) is not list:
            dest = [dest]
        self.dest = self.makeReferences(dest)

    #### tagged ####

    def setTagged(self, tagged=[]):
        self.tagged = tagged
    def getTagged(self):
        return self.tagged

    #### joiner ####

    def setJoiner(self, joiner):
        self.joiner = joiner
    def getJoiner(self):
        return self.joiner

    #### contents ####

    def setContents(self, contents):
        pass
    def getContents(self):
        return self.getSource() + self.getDest()

    #### references ####

    def getReferences(self):
        references = self.getSource() + self.getDest()
        references = self.flattenReferences(references)
        return references

    #### validation ####

    def makeValidSource(self, source, tabs=0):
        if self.VERBOSE: print(self.tabs(tabs) + 'makeValidSource', self)
        subSource = self.getSource()

        newSource = []
        for x, s in enumerate(subSource):
            sv = s.makeValid(source, tabs=tabs+1)
            if sv:
                newSource.append(sv)
            else:
                if self.VERBOSE: print(self.tabs(tabs) + 'removing source item:', s.__repr__(), x, self, source)
        self.setSource(newSource)
        return newSource

    def makeValidDest(self, src, tabs=0):
        if self.VERBOSE: print(self.tabs(tabs) + 'makeValidDest', self)
        dest = self.getDest()
        newDest = []
        for x, d in enumerate(dest):
            dv = d.makeValid(src, tabs=tabs+1)
            if dv:
                newDest.append(dv)
            else:
                if self.VERBOSE: print(self.tabs(tabs) + 'removing dest item', d, x, self, src)
        self.setDest(newDest)
        return dest

    def makeValid(self, source=None, tabs=0):
        if source is None:
            source = self
        if self.VERBOSE: print(self.tabs(tabs) + 'makeValid', self.getType(), self)
        validGroups = self.makeValidGroups(source, tabs=tabs)
        validSource = self.makeValidSource(source, tabs=tabs)
        validDest = self.makeValidDest(source, tabs=tabs)
        if self is source:
            self.clearCache()
        return self.collapse()

    #### collapse ####

    def collapse(self):
        if not self.getSource() or not self.getDest():
            return None
        else:
            return self

    #### write ####

    def writeSource(self):
        return self.writeReferences(self.getSource(), self.getTagged())

    def writeDest(self):
        return self.writeReferences(self.getDest())

    def write(self, tabs=0):
        return self.tabs(tabs) + 'sub %s %s %s;' %(self.writeSource(), self.getJoiner(), self.writeDest())


class FeatureSubstitutionSet(FeatureSub):
    """
    A special kind of substitution.
    """
    def __init__(self,
                 title='',
                 dest=None,
                 removeSuffixes=None,
                 appendSuffixes=None,
                 changeCase=False,
                 f=None,
                 sort=True,
                 joiner='by',
                 tagged=[],
                 groups=[]):
        if dest is None:
            dest = []
        if removeSuffixes is None:
            removeSuffixes = []
        if appendSuffixes is None:
            appendSuffixes = []

        self.setFont(f)
        self.setDestGroup(dest, sort=sort)
        self._source = None
        self.setRemoveSuffixes(removeSuffixes)
        self.setAppendSuffixes(appendSuffixes)
        self.setChangeCase(changeCase)
        self.setJoiner(joiner)
        self.setTagged(tagged)
        self.setTitle(title)
        self.setGroups(groups)

        self.getSourceGroup()

    def getSource(self):
        sourceName = self.getTitle() + '_off'
        return [FeatureGroupRef(sourceName)]

    def getDest(self):
        destName = self.getTitle()
        return [FeatureGroupRef(destName)]

    def getDestGroup(self):
        return FeatureGroup(name=self.getDest()[0], contents=self._dest)

    def setDestGroup(self, dest, sort=True):
        f = self.getFont()
        if sort:
            dest = self.sort(dest)
        self._dest = self.makeReferences(dest)

    def setSourceGroup(self, source):
        self._source = source

    def getRemoveSuffixes(self):
        return self._removeSuffixes
    def setRemoveSuffixes(self, removeSuffixes=[]):
        self._removeSuffixes = removeSuffixes

    def getAppendSuffixes(self):
        return self._appendSuffixes
    def setAppendSuffixes(self, appendSuffixes=[]):
        self._appendSuffixes = appendSuffixes

    def getChangeCase(self):
        return self._changeCase

    def setChangeCase(self, changeCase):
        self._changeCase = changeCase

    def getSourceGroup(self):
        if self._source:
            return self._source
        else:
            f = self.getFont()
            srcGlyphs = []
            for d in self.getDestGroup().contents:
                gn = GlyphName(d, standardizeSuffixOrder=False)
                # do the transformation
                # remove suffixes
                gn.removeSuffixes(self.getRemoveSuffixes())
                # add suffixes
                gn.appendSuffixes(self.getAppendSuffixes())
                # change case
                if self.getChangeCase():
                    baseNames, suffixes = gn.getBaseNames(), gn.getSuffixes()
                    newBaseNames = []
                    for baseName in baseNames:
                        baseNameUni = self.getUnicodeData().unicodeForGlyphName(baseName)
                        if baseNameUni in C.UNICODE_UPPER_TO_SINGLE_LOWER:
                            uni = C.UNICODE_UPPER_TO_SINGLE_LOWER[baseNameUni]
                            baseName = self.getUnicodeData().glyphNameForUnicode(uni)
                        elif baseNameUni in C.UNICODE_LOWER_TO_SINGLE_UPPER:
                            uni = C.UNICODE_LOWER_TO_SINGLE_UPPER[baseNameUni]
                            baseName = self.getUnicodeData().glyphNameForUnicode(uni)
                        if baseName is not None:
                            newBaseNames.append(baseName)
                    gn = GlyphName(baseName=newBaseNames, suffix=suffixes)
                # add source glyphs
                closestExisting = gn.getClosestExistingName(f)
                srcGlyphs.append(closestExisting)
            sourceGroup =  FeatureGroup(name=self.getSource()[0], contents=srcGlyphs)
            self._source = sourceGroup
            return sourceGroup

    def setSourceGroup(self, source):
        pass

    def getGroups(self):
        return self.groups + [self.getSourceGroup()] + [self.getDestGroup()]

    def getGroupNames(self):
        return [group.name for group in self.groups] + self.getSource() + self.getDest()
    """
    def makeValidSource(self, src):
        source = self.getSource()
        for s in source:
            if s != self.getSourceGroup().getName():
                print('removing subSet source', s)
                return None
        return source

    def makeValidDest(self, src):
        dest = self.getDest()
        for d in dest:
            if d != self.getDestGroup().getName():
                print('removing subSet dest', s)
                return None
        return dest
    """
    def makeValid(self, src=None, tabs=0):
        if src is None:
            src = self
        if not self.getSourceGroup().makeValid(src, tabs=tabs+1) or not self.getDestGroup().makeValid(src, tabs=tabs+1):
            self.setDest([])
            if self.VERBOSE: print(self.tabs(tabs) + 'attempting to remove subsetted substitution', self)
            return None
        else:
            return self


    def collapse(self):
        if not self.getSourceGroup() or not self.getDestGroup():
            return None
        else:
            return self



class FeatureSubContextual(FeatureSub):
    """
    Contextual substitution.

    def __init__(self, source=[], dest=[], tagged=[], joiner='by'):
        self.setSource(source)
        self.setDest(dest)
        self.tagged = tagged
        self.joiner = joiner
    """
    pass

class FeatureIgnoreSub(FeatureSub):
    """
    Ignore substitution statement.
    """
    def __init__(self, source=[], tagged=[]):
        self.setSource(source)
        self.setDest([])
        self.tagged = tagged

    def collapse(self):
        if not self.getSource():
            return None
        else:
            return self

    def write(self, tabs=0):
        return self.tabs(tabs) + 'ignore sub %s;' % self.writeSource()


###########
# CONTAINERS
###########

class FeatureContainer(FeatureBase):
    """
    A basic container of statements and other containers.
    """
    def __init__(self, name=None, contents=[], title=None, groups=[]):
        self.setName(name)
        self.setContents(contents)
        self.setTitle(title)
        self.setGroups(groups)

    def getType(self):
        return 'container'

    def write(self, tabs=0):
        lines = []
        titlestr = ''
        if self.getTitle():
            titlestr += '# %s' % str(self.getTitle())
        lines.append(self.tabs(tabs=tabs) + '%s %s { %s' % (self.getType(), self.getName(), titlestr))
        lines += self.writeContents(tabs=tabs)
        lines.append(self.tabs(tabs=tabs) + '} %s;' % self.getName())
        return lines

class FeatureEmptyContainer(FeatureContainer):
    def write(self, tabs):
        lines = []
        lines += self.writeContents(tabs=tabs-1)
        return lines

class FeatureFeature(FeatureContainer):
    """
    A feature container.
    """
    def getType(self):
        return 'feature'
    def write(self, tabs=0):
        lines = FeatureContainer.write(self, tabs=tabs)
        return lines+['']

class FeatureLookup(FeatureContainer):
    """
    A lookup container.
    """
    def getType(self):
        return 'lookup'

class FeatureScript(FeatureContainer):
    """
    Script.
    """
    def getType(self):
        return 'script'

    def getTitleDict(self):
        return C.OPENTYPE_SCRIPT_TAGS

    def getTitle(self):
        if self.getName() in self.getTitleDict():
            return self.getTitleDict()[self.getName()]
        else:
            return 'Unrecognized script'

    def setTitle(self, title):
        pass

    def write(self, tabs=0):
        lines = []
        # figure out title in comments
        titlestr = ''
        if self.getTitle():
            titlestr += '# %s' % str(self.getTitle())
        # append the line
        lines.append(self.tabs(tabs) + '%s %s; %s' % (self.getType(), self.getName(), titlestr))
        # write contents
        lines += self.writeContents(tabs=tabs)
        return lines

class FeatureLanguage(FeatureScript):
    """
    A language container.
    """
    def getType(self):
        return 'language'

    def getTitleDict(self):
        return C.OPENTYPE_LANGUAGE_TAGS

###########
# GROUPS
###########

class FeatureGroup(FeatureBase):
    """
    A group has a list of glyph references.
    """
    def __init__(self, name=None, contents=[], sort=True):
        self.setName(name)
        self.setContents(contents)

    def getGroups(self):
        return []

    def getGroupNames(self):
        return []

    def getType(self):
        return 'group'

    def write(self, tabs=0):
        contents = self.getContents()
        if contents:
            s = ''
            for gname in contents:
                if s == '':
                    s += gname
                else:
                    s += ' ' + gname.write()
            return self.tabs(tabs) + '@%s = [%s];' %(self.getName(), s)
        else:
            return ''

class FeatureGroupLocal(FeatureGroup):
    def getType(self):
        return 'groupLocal'

class FeatureGroupInline(FeatureGroup):
    """
    A nameless group has a list of glyph references.
    """
    def __init__(self, contents=[], sort=True):
        self.setContents(contents)

    def getType(self):
        return 'groupInline'

    def setName(self, name):
        pass

    def getName(self):
        return 'Inline Group'

    def write(self, tabs=0):
        references = self.writeReferences(self.getContents())
        return self.tabs(tabs) + '[%s]' %references

###########
# REFERENCES
###########


class FeatureBaseRef(str, FeatureBase):
    """
    """
    def __init__(self, name=''):
        str.__init__(name)
        self.validatedGroups = []

    def getName(self):
        return self

    def getContents(self):
        return []

    def setFallbacks(self, fallbacks=[]):
        self.fallbacks = self.makeReferences(fallbacks)

    def getFallbacks(self):
        if 'fallbacks' in self.__dict__:
            return self.fallbacks
        else:
            return []

    def write(self, tabs=0):
        return self.tabs(tabs) + str(self.getName())

    def __repr__(self):
        return '<%s:%s>' % (self.getType(), self.getName())

    def getReferences(self):
        return [self]

    def validate(self, source):
        return True

    def makeValid(self, source=None, tabs=0):
        if source is None:
            source = self
        if self.VERBOSE: print(self.tabs(tabs) + 'makeValid', self, self.getType())
        if self.validate(source):
            return self
        else:
            for fallback in self.getFallbacks():
                if fallback.validate(source):
                    return fallback
        return None

class FeatureGlyphRef(FeatureBaseRef):
    """
    Refer to an existing glyph.
    """

    def getType(self):
        return 'glyphRef'

    def validate(self, source):
        cache = source.getCache()
        name = self.getName()
        if name in cache.validGlyphs:
            return True
        elif source.getFont():
            isValid = name in source.getFont()
            if isValid:
                cache.validGlyphs.append(name)
            return isValid
        return False

class FeatureGroupRef(FeatureBaseRef):
    """
    Refer to an existing group.
    """

    def getType(self):
        return 'groupRef'

    def validate(self, source, checkFontGroups=True, checkFeaGroups=True):
        result = False
        cache = source.getCache()
        if checkFontGroups and self.getName() in source.getFont().groups:
            result = True
        if self.getName() in cache.validGroups:
            result = True
        else:
            sourceGroupNames = source.collectGroupNames(source)
            if checkFeaGroups and self.getName() in sourceGroupNames:
                result = True
                cache.validGroups.append(self.getName())
        return result

    def write(self, tabs=0):
        return self.tabs(tabs) + '@%s' % self.getName()

class FeatureLookupRef(FeatureBaseRef):
    """
    Refer to an existing lookup.
    """
    def getType(self):
        return 'lookupRef'

    def write(self, tabs=0):
        return self.tabs(tabs) + 'lookup %s;' %self.getName()

    def validate(self, source):
        result = False
        allLookups = source.getContentsByType(['lookup'])
        if self.getName() in source.getContentNames(allLookups):
            result = True
        return result

###########
# FEATURE BUILDER
###########

class FeatureTemplates(FeatureBase):
    #############
    # templates
    #############

    def getLocl(self):




        trk = FeatureLanguage('TRK', [
                FeatureLookup('lookup_TRK', [
                    FeatureSub('i', 'i.trk'),
                    FeatureSub('I.sc', 'Idotaccent.sc')
                    ])
               ])
        aze = FeatureLanguage('AZE', [
                FeatureLookupRef('lookup_TRK')
                ])
        crt = FeatureLanguage('CRT', [
                FeatureLookupRef('lookup_TRK')
                ])

        locl_ROM_off = FeatureGroupInline(self.getGlyphSubset(baseNames=['Scedilla', 'scedilla']))
        locl_ROM = FeatureGroupInline(self.getGlyphSubset(baseNames=['Scommaaccent', 'scommaaccent']))

        rom = FeatureLanguage('ROM', [
                FeatureLookup('lookup_ROM', [
                    FeatureSub(source=[locl_ROM_off], dest=[locl_ROM])
                    ])
               ])
        cat = FeatureLanguage('CAT', [
               FeatureSubContextual(['L', 'periodcentered', 'L'], ['Ldot'], tagged=[0, 1]),
               FeatureSubContextual(['L.sc', 'periodcentered', 'L.sc'], ['Ldot.sc'], tagged=[0, 1]),
               FeatureSubContextual(['l', 'periodcentered', 'l'], ['ldot'], tagged=[0, 1]),
               ])
        esp = FeatureLanguage('ESP', [
            FeatureSub('emdash', 'emdash.salt_em'),
            FeatureSub('endash', 'endash.salt_en')
            ])
        return FeatureFeature('locl', [
                FeatureScript('latn', [
                                       trk,
                                       aze,
                                       crt,
                                       rom,
                                       cat,
                                       esp
                                ])
                ], title='Localized Forms')

    def getSs18(self):
        return FeatureFeature('ss18', [
        FeatureSub('emdash', 'emdash.salt_em'),
        FeatureSub('endash', 'endash.salt_en')
                                    ], title='Long Dashes')

    def getSs19(self):
        return FeatureFeature('ss19', [
                FeatureSub(FeatureGroupInline(['quotesingle', 'quotedbl']), FeatureGroupInline(['minute', 'second']))
                                    ], title='Primes')

    def getSups(self):
        return FeatureFeature('sups', [
            FeatureSubstitutionSet(title='sups',
                                   dest=self.getGlyphSubset(suffixes=['sups']),
                                   removeSuffixes=['sups'],
                                   f = self.getFont(),
                                   )
                                    ], title='Superiors')

    def getSinf(self):
        return FeatureFeature('sinf', [
            FeatureSubstitutionSet(title='sinf',
                                   dest=self.getGlyphSubset(suffixes=['sinf']),
                                   removeSuffixes=['sinf', 'inferior'],
                                   f = self.getFont(),
                                   )
                                    ], title='Scientific Inferiors')

    def getNumr(self):
        return FeatureFeature('numr', [
            FeatureSubstitutionSet(title='numr',
                                     dest=self.getGlyphSubset(suffixes=['numr']),
                                   removeSuffixes=['numr', 'numerator'],
                                   f = self.getFont(),
                                   ),
            FeatureSub('slash', 'fraction'),
                                    ], title='Numerators')

    def getDnom(self):
        return FeatureFeature('dnom', [
            FeatureSubstitutionSet(title='dnom',
                                     dest=self.getGlyphSubset(suffixes=['dnom']),
                                   removeSuffixes=['dnom', 'denominator'],
                                   f = self.getFont(),
                                   ),
            FeatureSub('slash', 'fraction'),
                                    ], title='Denominators')


    def getOrdn(self):
        ordn_digits = FeatureGroup('ordn_digits', ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'])
        return FeatureFeature('ordn', [
               FeatureSubContextual(['@ordn_digits', 'a'], ['ordfeminine'], tagged=[1]),
               FeatureSubContextual(['@ordn_digits', 'o'], ['ordmasculine'], tagged=[1])
                                       ], title='Ordinals', groups=[ordn_digits])

    def getSimpleFrac(self):
        return FeatureFeature('frac', [
               FeatureSub(['one', 'onesuperior'], ['fraction', 'slash'], ['two', 'twosuperior'], ['onehalf']),
               FeatureSub(['one', 'onesuperior'], ['fraction', 'slash'], ['four'], ['onequarter']),
               FeatureSub(['three', 'threesuperior'], ['fraction', 'slash'], ['four'], ['threequarters']),
                                       ], title='Simple Fraction')

    def getFrac(self):
        figures = FeatureGroup('figures', ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'])

        feature = FeatureFeature('frac', [], title='Fractions', groups=[figures])

        fraction_bar_ignoresubs = []
        for x in range(11, 0, -1):
            dest = ['slash'] + ['@figures'] * x + ['slash']
            fraction_bar_ignoresubs.append(FeatureIgnoreSub(dest, tagged=[0]))
            fraction_bar_ignoresubs.append(FeatureIgnoreSub(dest, tagged=[len(dest)-1]))
        fraction_bar_ignoresubs.append(FeatureSubContextual(['@figures', 'slash', '@figures'], ['fraction'], tagged=[1]))

        fraction_bar = FeatureLookup('FractionBar', fraction_bar_ignoresubs)

        feature.getContents().append(fraction_bar)

        for x in range(0, 10):
            source = ['@figures'] + ['@numr'] * x + ['fraction']
            dest = ['@numr']
            lookup = FeatureLookup('numr'+str(x+1), [FeatureSub(source, dest, tagged=[0])])
            feature.getContents().append(lookup)

        inlineGroup = FeatureGroupInline(['fraction', '@dnom'])
        dnom_sub = FeatureSub([inlineGroup, '@figures'], ['@dnom'], tagged=[1])
        dnom_lookup = FeatureLookup('dnom', [dnom_sub])
        feature.getContents().append(dnom_lookup)

        fractionSpace = FeatureGlyphRef('space.frac')
        fractionSpace.setFallbacks(['space.thin'])
        feature.getContents().append(FeatureSub(['@figures', 'space', '@numr'], [fractionSpace], tagged=[1]))

        return feature

    def getTnum(self):
        sortsAndSpacesCats = C.UNICODE_CATEGORIES_COMBINED['Punctuation'] + C.UNICODE_CATEGORIES_COMBINED['Separator']
        return FeatureFeature('tnum', [
            FeatureSubstitutionSet(title='tnum', dest=self.getGlyphSubset(suffixes=['tab'], excludeUnicodeCategories=sortsAndSpacesCats),
                                   removeSuffixes=['tab'],
                                   f = self.getFont(),
                                   )
                                    ], title='Tabular Figures')

    def getSs20(self):
        sortsAndSpacesCats = C.UNICODE_CATEGORIES_COMBINED['Punctuation'] + C.UNICODE_CATEGORIES_COMBINED['Separator']

        x =  self.getGlyphSubset(suffixes=['tab'], unicodeCategories=sortsAndSpacesCats)
        for z in x:
            print('\t\t', z, type(z))
        return FeatureFeature('ss20', [
            FeatureSubstitutionSet('tnum_sorts', self.getGlyphSubset(suffixes=['tab'], unicodeCategories=sortsAndSpacesCats),
                                   removeSuffixes=['tab'],
                                   f = self.getFont(),
                                   )
                                    ], title='Tabular Sorts & Spaces')

    def getPnum(self):
        return FeatureFeature('pnum', [
            FeatureSub(source=['@tnum'], dest=['@tnum_off']),
            FeatureSub(source=['@tnum_sorts'], dest=['@tnum_sorts_off']),
                                    ], title='Proportional figures')

    def getLnum(self):
        return FeatureFeature('lnum', [
            FeatureSub(source=['@onum'], dest=['@onum_off'])
                                    ], title='Lining figures')

    def getSmcp(self):
        smcpCats = C.UNICODE_CATEGORIES_COMBINED['Letter']
        feature = FeatureFeature('smcp', [
            FeatureSubstitutionSet(title='smcp',
                                   dest=self.getGlyphSubset(suffixes=['sc'],
                                                            unicodeCategories=smcpCats,
                                                            excludeGlyphNames = ['germandbls.sc', 'fi.sc', 'fl.sc', 'Idotaccent.sc']
                                                            ),
                                   removeSuffixes=['sc'],
                                   changeCase=True,
                                   f = self.getFont(),
                                   )
                                    ], title='Small Caps')
        feature.getContents().append(FeatureSub('fi', 'fi.sc'))
        feature.getContents().append(FeatureSub('fl', 'fl.sc'))
        feature.getContents().append(FeatureSub('germandbls', 'germandbls.sc'))
        feature.getContents().append(FeatureSub('i.trk', 'Idotaccent.sc'))
        return feature

    def getC2sc(self):

        featureContents = []

        # Get Small cap letters
        smcpCats = C.UNICODE_CATEGORIES_COMBINED['Letter']
        c2sc_letters_glyphset = self.getGlyphSubset(suffixes=['sc'],
                                                            unicodeCategories=smcpCats,
                                                            excludeGlyphNames = ['germandbls.sc', 'fi.sc', 'fl.sc']
                                                            )
        c2sc_letters = FeatureSubstitutionSet(title='c2sc_letters',
                                   dest=c2sc_letters_glyphset,
                                   removeSuffixes=['sc'],
                                   changeCase=False,
                                   f = self.getFont(),
                                   )
        featureContents.append(c2sc_letters)
        # Get Small cap sorts
        sortsAndSpacesCats = C.UNICODE_CATEGORIES_COMBINED['Punctuation'] + C.UNICODE_CATEGORIES_COMBINED['Separator']
        c2sc_sorts_glyphset = self.getGlyphSubset(suffixes=['sc'],
                                                            unicodeCategories=sortsAndSpacesCats,
                                                            excludeGlyphNames = ['germandbls.sc', 'fi.sc', 'fl.sc'] + c2sc_letters_glyphset
                                                            )
        c2sc_sorts = FeatureSubstitutionSet(title='c2sc_sorts',
                                   dest=c2sc_sorts_glyphset,
                                   removeSuffixes=['sc'],
                                   changeCase=False,
                                   f = self.getFont(),
                                   )
        featureContents.append(c2sc_sorts)
        # Get Other small caps
        c2sc_other_glyphset = self.getGlyphSubset(suffixes=['sc'],
                                                            excludeGlyphNames = ['germandbls.sc', 'fi.sc', 'fl.sc'] + c2sc_letters_glyphset + c2sc_sorts_glyphset
                                                            )
        c2sc_other = FeatureSubstitutionSet(title='c2sc_other',
                                   dest=c2sc_other_glyphset,
                                   removeSuffixes=['sc'],
                                   changeCase=False,
                                   f = self.getFont(),
                                   )
        featureContents.append(c2sc_other)
        # Make feature
        return FeatureFeature('c2sc', featureContents, title='Caps To Small Caps')

    def getOnum(self):
        return FeatureFeature('onum', [
            FeatureSubstitutionSet(title='onum',
                                     dest=self.getGlyphSubset(suffixes=['lc']),
                                   removeSuffixes=['lc'],
                                   f = self.getFont(),
                                   ),
                                    ], title='Lowercase figures')

    def getZero(self):
        return FeatureFeature('zero', [
            FeatureSubstitutionSet(title='zero',
                                     dest=self.getGlyphSubset(suffixes=['salt', 'slash'], baseNames=['zero']),
                                   removeSuffixes=['salt', 'slash'],
                                   f = self.getFont(),
                                   ),
                                    ], title='Slashed zero')

    def getSs17(self):
        return FeatureFeature('ss17', [
            FeatureSubstitutionSet(title='f_calt_nokern',
                                     dest=self.getGlyphSubset(suffixes=['calt', 'nokern'], baseNames=['f']),
                                   removeSuffixes=['calt', 'nokern'],
                                   f = self.getFont(),
                                   ),
                                    ], title='Non-kerning f')

    def getLiga(self):
        ligatures = self.getLigatures(excludeBaseNames=['w_w_w', 'T_h', 's_t', 'c_t', 's_p'])
        subs = []
        for lig, baseNames in ligatures:
            gn = GlyphName(lig)
            sub = FeatureSub(source=baseNames, dest=[lig])
            subs.append(sub)
        return FeatureFeature('liga', subs, title='Standard Ligatures')

    def getDlig(self):
        ligatures = self.getLigatures(baseNames=['w_w_w', 'T_h', 's_t', 'c_t', 's_p'])
        subs = []
        for lig, baseNames in ligatures:
            gn = GlyphName(lig)
            sub = FeatureSub(source=baseNames, dest=[lig])
            subs.append(sub)
        return FeatureFeature('dlig', subs, title='Discretionary Ligatures')


    def getCase(self):
        return FeatureFeature('case', [
            FeatureSubstitutionSet(title='case',
                                     dest=self.getGlyphSubset(suffixes=['uc']),
                                   removeSuffixes=['uc'],
                                   f = self.getFont(),
                                   ),
            FeatureSub(source=['@onum'], dest=['@onum_off'])
                                    ], title='Case-sensitive forms')

    def getOrnm(self):
        ornmGroup = FeatureGroup('ornm', self.getGlyphSubset(baseNames=['apple', 'u2022']))

        return FeatureFeature('ornm', [
                                    FeatureSub(source=['bullet'], dest=['@ornm'], joiner='from')
                                    ],
                              title='Ornaments',
                                groups = [ornmGroup]

                            )

    def getSalt(self, makeSsets=True):
        """
        Tries to divide up all stylistic alternates.
        """

        salts =  self.getGlyphSubset(suffixes=['salt'], excludeSuffixes=['em', 'en', 'slash'])
        saltGroups = OrderedDict()
        for s in salts:
            gn = GlyphName(s, standardizeSuffixOrder=False)
            suffixesAfter = gn.getSuffixesAfter('salt')
            saltLookupName = GlyphTX.name.joinElements(suffixesAfter)
            if saltLookupName in saltGroups:
                saltGroups[saltLookupName].append(s)
            else:
                saltGroups[saltLookupName] = [s]

        # collect the lookups and stylistic set features
        saltLookups = []
        saltFeatures = []
        ssTick = 1
        for saltLookupName, saltGroupGlyphs in saltGroups.items():
            dest = []
            saltSuffixes = GlyphTX.name.splitIntoElements(saltLookupName)[1]

            if saltLookupName == '':
                saltLookupName = 'salt_basic'
                saltSuffixes = ['salt']
            else:
                saltLookupName = 'salt_'+saltLookupName
                saltSuffixes += ['salt']

            lookup = FeatureLookup(name=saltLookupName, contents=[
                                    FeatureSubstitutionSet(title=saltLookupName,
                                                    dest=saltGroupGlyphs,
                                                 removeSuffixes=saltSuffixes,
                                                 f = self.getFont(),
                                                     )]
                                    )
            feature = FeatureFeature('ss'+'%02d' % ssTick, [lookup], title=saltLookupName)
            lookupRef = FeatureLookupRef(saltLookupName)
            saltLookups.append(lookupRef)
            saltFeatures.append(feature)
            ssTick += 1

        return FeatureEmptyContainer('none', contents= saltFeatures + [
                                                   FeatureFeature('salt', saltLookups, title='Stylistic Alternates')]
                                                   )


class FeatureBuilder(FeatureContainer, FeatureTemplates):
    """
    Contains the templates to build features.
    """
    def getType(self):
        return 'builder'

    def __init__(self, font=None):
        self.setFont(font)
        self.setContents([
                          self.getLocl(),
                          self.getSs18(),
                          self.getSs19(),
                          self.getSups(),
                          self.getSinf(),
                          self.getNumr(),
                          self.getDnom(),
                          self.getOrdn(),
                          self.getFrac(),
                          self.getTnum(),
                          self.getSs20(),
                          self.getPnum(),

                          self.getSmcp(),
                          self.getC2sc(),

                          self.getOnum(),
                          self.getLnum(),

                          self.getZero(),
                          self.getSs17(),
                          self.getLiga(),
                          self.getDlig(),
                          self.getSalt(),
                          self.getCase(),
                          self.getOrnm()
                          ])


    # write
    def write(self, tabs=0):
        lines = []
        writeMeta = self.writeMeta(tabs=tabs)
        if writeMeta:
            lines += writeMeta
            lines += ['']
        writeGroups = self.writeGroups(tabs=tabs)
        if writeGroups:
            lines += writeGroups
            lines += ['']
        writeLanguageSystems = self.writeLanguageSystems(tabs=tabs)
        if writeLanguageSystems:
            lines += writeLanguageSystems
            lines += ['']
        writeContents = self.writeContents(tabs=tabs)
        if writeContents:
            lines += writeContents
        return lines

    def _crawl(c, tabs=0):
        for c in c.getContents():
            print('\t'*tabs, c, c.getGroups())
            crawl(c, tabs=tabs+1)

def makeFeatures(f, VERBOSE=True):
    featureBuilder = FeatureBuilder(f)
    featureBuilder.makeValid()
    f.features.text = featureBuilder.writeStr()
    if VERBOSE:
        print('Writing features for %s' %f)

if __name__ == "__main__":
    fonts = AllFonts()
    if fonts:
        for f in fonts:
            makeFeatures(f)
    else:
        paths = File.collect()
        #paths = File.collect(u"/Users/david/Documents/FB/Masters/Font_Bureau")
        for path in paths:
            f = OpenFont(path, showUI=False)
            featureBuilder = FeatureBuilder(f)
            featureBuilder.makeValid()
            File.write(featureBuilder.writeStr(), path.replace('.ufo', '.fea'))
            #File.launch(path.replace('.ufo', '.fea'))
    #Message('Done')
