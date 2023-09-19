# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     transformer.py
#

import json, re, math, hashlib
import os
from time import time
import datetime
from random import randint
from tnbits.constants import Constants as C
from tnbits.tools.constantsparts.smartsets import SS_ACCENTS, SS_TOPACCENTS
from tnbits.base.constants.tool import EXTENSION_FAM
from tnbits.base.future import chr

class TX: # Transformer

    WHITESPACE = ' \t\r\n'

    # N U M B E R S

    @classmethod
    def asNumber(cls, v):
        try:
            fv = float(v)
            iv = int(v)
            if fv == iv:
                return iv
            return fv
        except (ValueError, TypeError):
            pass
        return 0

    @classmethod
    def asNumberOrNone(cls, value):
        try:
            if value == int(value):
                return cls.asIntOrNone(value)
            return cls.asFloatOrNone(value)
        except (ValueError, TypeError):
            pass
        return None

    @classmethod
    def asFloatOrNone(cls, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def asId(cls, value, default=0):
        """The *asId* method transforms the *value* attribute either to an
        instance of @int@ or to @None@, so it can be used as *id* field in a
        @Record@ instance. If the value cannot be converted, then the optional
        *default* (default value is @0 @) is answered.<br/>"""
        try:
            value = int(value)
            if value <= 0:
                return default
            return value
        except (ValueError, TypeError):
            return default

    @classmethod
    def asIntOrNone(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def asIntOrDefault(cls, value, default):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @classmethod
    def asInt(cls, value, default=None):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default or 0

    @classmethod
    def isInt(cls, value):
        return cls.asIntOrNone(value) is not None

    @classmethod
    def asIntOrValue(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    @classmethod
    def asRoundedInt(cls, value, default=None):
        value = cls.asIntOrNone(value)
        if value is None:
            value = default
        try:
            return int(round(value))
        except (ValueError, TypeError):
            return int(round(default or 0))

    @classmethod
    def asFloat(cls, value, default=None):
        value = cls.asFloatOrNone(value)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @classmethod
    def asBool(cls, value, default=None):
        if value is None:
            return default
        return bool(value)

    @classmethod
    def asFormatted(cls, value, default=None, format=None):
        if value is None:
            return default
        if isinstance(value, (int, float)):
            if int(round(value)) == value: # Same as rounded whole number
                return '%d' % value
            return (format or '%0.2f') % value # Otherwise show as float with 2 digits.
        return value # Unchanged, cannot format.

    @classmethod
    def asTuple(cls, value):
        if isinstance(value, list):
            value = tuple(value)
        elif not isinstance(value, tuple):
            value = (value,)
        return value

    @classmethod
    def asSet(cls, value):
        if isinstance(value, (list, tuple)):
            value = set(value)
        if not isinstance(value, set):
            value = set((value,))
        return value

    @classmethod
    def interpolate(cls, a, b, v, doRound=False):
        """Answer the interpolated value of factor v between a and b. If
        doRound is True (default is False), then round the result before
        answering it."""
        i = a + (b-a) * v
        if doRound:
            i = int(round(i))
        return i

    # S T R I N G

    @classmethod
    def commaString2List(cls, s):
        return cls.stringList2StrippedList(s.split(','))

    @classmethod
    def stringList2StrippedList(cls, strings):
        l = []
        for string in strings:
            l.append(string.strip())
        return l

    @classmethod
    def filterValue2Int(cls, s):
        """Filter all numeric characters from the string and answer the
        resulting integer.  Answer 0 if no digits are found. If s is already a
        number, then answer it as rounded int."""
        if isinstance(s, (int, float)):
            return int(round(s))
        digits = '0'
        for c in s:
            if c in '0123456789':
                digits += c
        return cls.asInt(digits)

    # B O O L E A N

    @classmethod
    def bool2Marker(cls, value):
        if value:
            return C.POINTMARKER_TRUE
        return C.POINTMARKER_FALSE

    @classmethod
    def bool2Int(cls, value):
        if value:
            return 1
        return 0

    @classmethod
    def int2Bool(cls, value):
        if value:
            return True
        else:
            return False

    @classmethod
    def start2Marker(cls, start):
        return {
            C.POINTTYPE_START:C.POINTMARKER_TRUE,
            C.POINTTYPE_NOTSTART:C.POINTMARKER_EMPTY,
        }[bool(start)]

    @classmethod
    def index2PointId(self, index):
        return '*Pid%d' % index

    @classmethod
    def none2Empty(cls, value):
        """Answers an empty string if value is None, otherwise pass it through
        To make sure that 0 empty objects show as result."""
        if value is None:
            return ''
        return value

    @classmethod
    def asDict(cls, value, isRoot=True):
        """Answers the value as dict as root. If the value itself is not a
        dict, answer it as dict(value=value). For lower levels than root,
        answer the plain value if is it a string or a number. Basic classed
        don't get translated when not called as root. All other objects are
        called by value.asDict() If the object cannot handle that method, then
        convert it to string."""
        d = {}
        if isinstance(value, dict):
            for key, v in value.items():
                d[key] = cls.asDict(v, False)
        elif isinstance(value, (int, float, str)):
            if isRoot:
                d = dict(value=value)
            else:
                d = value # On lower levels than root, just copy the value, instead of making dict.
        elif isinstance(value, (list, tuple)):
            l = []
            if isRoot:
                d = dict(value=l) # Always answer a dict as root
            else:
                d = l # Otherwise answer the plain value.
            for v in value:
                l.append(cls.asDict(v, False))
        elif hasattr(value, 'asDict'):
            d = value.asDict()
        else:
            d = dict(value=repr(value))
        return d

    # ---------------------------------------------------------------------------------------------------------
    #    F I X E D

    @classmethod
    def value2Fixed(cls, value):
        if isinstance(value, str):
            if value.endswith('u'):
                value = cls.float2Fixed(cls.asFloat(value[:-1]))
            else:
                value = cls.asIntOrNone(value)
        return value

    @classmethod
    def float2Fixed(cls, value):
        """The @float2Fixed@ method translates a float into a 1/64 pixel
        unit-value."""
        return int(round(value * 64))

    @classmethod
    def fixed2Float(cls, value):
        """The @fixed2Float@ method translates a fixed 1/64 pixel-unit value
        to float."""
        return float(value) / 64

    # ---------------------------------------------------------------------------------------------------------
    #    S T R I N G

    @classmethod
    def asString(cls, value, default=None):
        if value is None:
            value = default
        return u'%s' % value

    @classmethod
    def asStringOrEmpty(cls, s):
        if s is None:
            return ''
        return cls.asString(s)

    @classmethod
    def asRoundedOrZeroString(cls, s):
        return '%d' % round(cls.asFloat(s) or 0)

    @classmethod
    def shrink(cls, s):
        return (s or '').strip().replace(' ', '').replace('\t', '')

    @classmethod
    def removeWhiteSpace(cls, s):
        """Vacuum s by removing all white space."""
        for c in cls.WHITESPACE:
            s = s.replace(c, '')
        return s

    @classmethod
    def strippedString(cls, s):
        return (s or '').strip()

    @classmethod
    def list2SpacedString(cls, l):
        return cls.list2String(l, ' ')

    @classmethod
    def list2StringList(cls, l):
        strings = []
        for element in l:
            if not isinstance(element, str):
                element = '%s' % element
            strings.append(element)
        return strings

    @classmethod
    def list2CommaString(cls, l):
        return cls.list2String(l, ',')

    @classmethod
    def value2IdCommaString(cls, value):
        """Transforms a list with numbers into a comma separated string. This
        can be used to convert a list of record ids into a SQL compatible list
        of ids, without integers showing up as @1234L@."""
        t = []
        if not isinstance(value, (set, list, tuple)):
            value = str(value).split(',')
        for item in value:
            if cls.isInt(item):
                t.append('%s' % item) # Avoid longs show up as 1234L, deprecated in py3?
        return ', '.join(t)

    @classmethod
    def idCommaString2IdSet(cls, s):
        """Transforms a string with comma separated items into a set of id
        integers."""
        t = set()
        if s is not None:
            for value in s.split(','):
                value = cls.asInt(value)
                if value is not None:
                    t.add(value)
        return t

    @classmethod
    def commaString2IntegerList(cls, s):
        l = []
        for word in cls.commaString2List(s):
            number = cls.asInt(word)
            if number is not None:
                l.append(number)
        return l

    @classmethod
    def list2String(cls, l, separator=''):
        return separator.join([cls.asString(ll) for ll in l])

    @classmethod
    def errors2String(cls, errors):
        print(errors)
        return C.LABEL_ERRORSEPARATOR.join(errors or [])

    PLAINWORDS = re.compile('([a-z0-9_\<\>]*)')

    @classmethod
    def string2PlainWords(cls, s):
        return cls.PLAINWORDS.findall(s.lower())

    @classmethod
    def string2WordsKey(cls, s):
        words = cls.string2PlainWords(s)
        return cls.words2WordsKey(words)

    @classmethod
    def words2WordsKey(cls, words):
        k = []
        words.sort()
        for word in words:
            if word:
                k.append(word)
        return '_'.join(k)

    # ---------------------------------------------------------------------------------------------------------
    #    S Q L  C O N V E R S I O N S

    PATHCHARS = re.compile('([a-zA-Z0-9_/\.]*)')

    @classmethod
    def path2StyleKey(cls, path):
        """Answers the style key as tuple of format (familyPath, fileName)."""
        return cls.path2FamilyPath(path), cls.path2FileName(path)

    @classmethod
    def path2FamilyPath(cls, path):
        """Answers the family path of a font path /aaa/bbb/FamilyName-Bold.ufo makes
        /aaa/bbb/FamilyName"""
        return cls.path2FamilyDir(path) + '/' + cls.path2FamilyName(path) + '.fam'

    @classmethod
    def path2FamilyName(cls, path):
        """Answers the family name of a font path

        - /aaa/bbb/FamilyName.fam
        - /aaa/FamilyName/
        - /aaa/bbb/FamilyName-Bold.ufo
        - /aaa/bbb/FamilyNameRegular.ttf (*)

        - /aaa/bbb/FamilyName.designspace

        makes FamilyName. If the direct .plist family path is given, then the
        extension is stripped.

        (*) TODO: compare files that don't have a hyphen.
        """
        name = None

        if path and '/' in path:
            name = path.split('/')[-1]

            if '.' in name:
                extension = cls.extensionOf(name).lower()

                if extension == EXTENSION_FAM:
                    name = name.split('.')[0]
                elif extension in ('ufo', 'ttf', 'otf', 'designspace') and '-' in path:
                    # TODO: compare all relevant files in the folder.
                    name = name.split('-')[0]

        if name is None:
            name = 'Untitled'

        return name

    @classmethod
    def path2FamilyDir(cls, path):
        # If it is a relative path, then expand on current directory.
        if path.startswith('.'):
            path = os.path.abspath(path)
        return '/'.join(path.split('/')[:-1])

    @classmethod
    def path2FileName(cls, path):
        """
        TODO: To be changed by Nobu: enc = sys.getfilesystemencoding()
        """
        # If it is a relative path, then expand on current directory.
        if path.startswith('.'):
            path = os.path.abspath(path)
        return path.split('/')[-1]

    @classmethod
    def path2ScriptsDir(cls, path):
        return TX.path2FamilyDir(path) + '/scripts'

    @classmethod
    def string2Path(cls, s):
        # Construct a valid (url) path name from letters, figures and _/.
        return ''.join(cls.PATHCHARS.findall(s))

    @classmethod
    def path2StyleName(cls, path):
        """Transform /aa/bb/Family-Bold-Italic.ufo into Bold-Italic."""
        return '.'.join('-'.join(cls.path2FileName(path).split('-')[1:]).split('.')[:-1])

    @classmethod
    def extensionOf(cls, path):
        assert isinstance(path, str)
        return path.split('.')[-1].lower()

    # ---------------------------------------------------------------------------------------------------------
    #    S Q L  C O N V E R S I O N S

    @classmethod
    def name2UrlName(self, name, pattern=None, usehyphen=True):
        """The @name2UrlName@ method converts the *name* attribute to a name
        that is safe to be used in an URL. This method is used for uploaded
        images with unknown (and probably wrong) filenames. Also it is used to
        derive the @self.FIELD_IDNAME@ content from @self.FIELD_NAME@. The
        processing also takes care that not multiple hyphen exist in a
        row.<br/>

        The optional *pattern* (default set to
        @'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-1234567890'@)
        allows the use of other patterns.<br/>

        If there is a period in the name, then it might be part of the
        extension. Split the name into a @name.extension@ and recursively solve
        the parts.<br/>

        If the *usehyphen* attribute is set (default value is @True@), then
        allow the use of hyphens (divider between parameter and value in Xierpa
        syntax), otherwise all hyphens are replaced by underscores.
        """
        if not name:
            return ''
        if name.startswith('/'):
            name = name[1:]
        if isinstance(name, str):
            # Convert to Unicode.
            name = name.decode('utf-8')
        if '.' in name:
            # Test if there still is an extension, split otherwise.
            parts = name.split('.')
            newname = self.name2UrlName('.'.join(parts[:-1]), pattern, usehyphen)
            newext = self.name2UrlName(parts[-1], pattern, usehyphen).lower()
            return newname + '.' + newext

        if pattern is None:
            pattern = u'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_1234567890'

        urlname = []
        hadHyphen = True

        for c in name:
            if c in ' /':
                c = '-'
            elif not c in pattern:
                if c in self.ACCENT2ASCII:
                    c = self.ACCENT2ASCII[c]
                else:
                    c = ''

            if c != '-' or not hadHyphen:
                urlname.append(c)

            hadHyphen = c == '-'

        urlname = ''.join(urlname)
        if not usehyphen:
            urlname = urlname.replace('-', '_')
        while urlname and urlname[-1] in '-_':
            urlname = urlname[:-1]
        return urlname

    # ---------------------------------------------------------------------------------------------------------
    #    S Q L  C O N V E R S I O N S

    @classmethod
    def escapeSqlQuotes(cls, s):
        """Prevents hacking: escape single quote in SQL string, change every
        single quote to @''@.  PostgreSQL interprets and inserts only a single
        quote in the database."""
        if s is not None and isinstance(s, str):
            s = s.replace("'", "''").replace('\\', '\\\\')
        return s

    # ---------------------------------------------------------------------------------------------------------
    #    M N E M O N I C

    @classmethod
    def mnemonic2Upper(cls, mnemonic):
        name = (mnemonic.vtt).split(' ')[0]
        return cls.mnemonicName2Upper(name)

    SELECTIVEUPPER = (
        ('gr', 'Gr'), ('gR', 'Gr'), ('GR', 'Gr'),
        ('wh', 'Wh'), ('wH', 'Wh'), ('WH', 'Wh'),
        ('bl', 'Bl'), ('bL', 'Bl'), ('Bl', 'Bl'),
        ('x', 'X'), ('y', 'Y')
    )
    @classmethod
    def mnemonicName2Upper(cls, name):
        """This is tricky. We want to make [x] and [X] behave identical,
        because there is no difference in the meaning of the cases, but we need
        to keep the difference on [m....] and [M....] and [..r..] and [..R..]
        and force the color names to the proper casing, no matter what the
        origin is. We just make the x and y upper case in the bracket field and
        set the color to Cap+lowercase."""
        parts = name.split('[')
        parts[0] = parts[0].upper()

        if len(parts) > 1:
            params = parts[1]

            for s1, s2 in cls.SELECTIVEUPPER:
                params = params.replace(s1, s2)

            parts[1] = params

        return '['.join(parts)

    @classmethod
    def mnemonic2NamePart(cls, mnemonic):
        return (mnemonic.vtt or '').split('[')[0].upper()

    # ---------------------------------------------------------------------------------------------------------
    #    P A T H

    @classmethod
    def module2Path(cls, module):
        return '/'.join((module.__file__).split('/')[:-1])

    @classmethod
    def path2ParentPath(cls, path):
        return '/'.join(path.split('/')[:-1])

    @classmethod
    def path2FormatPath(cls, path, format=None):
        """Answers the path where the extension is changed to format If format
        is None, then the extension is removed."""
        if path is not None:
            path = '.'.join(path.split('.')[:-1])
            if format is not None:
                path += '.' + format
            return path
        return None

    @classmethod
    def path2Name(cls, path):
        """Answers the file name part of the path."""
        if path is None:
            return None
        if not path:
            return 'Untitled'
        return path.split('/')[-1]

    @classmethod
    def path2FontName(cls, path):
        """Takes that file part of the path, and get the chunk until the first
        period to remove the extension, version
        numbers and the database download ID.

        /xxx/yyy/zzz/Agency_FB-Compressed.ufo becomes Agency_FB-Compressed
        /xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo becomes Agency_FB-Compressed
        #xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo becomes Agency_FB-Bold
        """
        name = cls.path2Name(path)
        if name is not None:
            return name.split('.')[0]
        return 'Untitled'

    path2GlyphIdName = path2FontName

    @classmethod
    def path2HintPath(cls, path):
        return cls.path2FormatPath(path, 'autohint.ttf')

    @classmethod
    def path2FontId(cls, path):
        """Answers the font ID for the font associated with this path. If the
        path does not exist, or if the font name is invalid, then answer
        None."""
        if path is not None:
            name = cls.path2Name(path)
            return name
        return None

    # ---------------------------------------------------------------------------------------------------------
    #    F O N T

    @classmethod
    def font2Name(cls, font):
        name = None

        if font is not None:
            name = cls.path2Name(cls.font2Path(font))

            if name is None and font.info: # The font may not have been saved yet, then there is no filename.
                if (font.info.styleMapFamilyName or font.info.familyName):
                    name = (font.info.styleMapFamilyName or font.info.familyName)
                    if name and font.info.styleName:
                        name += '-' + font.info.styleName
        if name is None:
            name = 'Untitled'
        return name

    @classmethod
    def font2FileName(cls, font):
        """Answer the font file name. In case of a new unsaved font,
        answer *"Untitled"*."""
        return (font.path or 'Untitled').split('/')[-1]

    @classmethod
    def font2Naked(cls, font):
        if font is not None and hasattr(font, 'naked'):
            font = font.naked()
        return font

    @classmethod
    def font2Path(cls, font):
        if cls.font2Naked(font) is None:
            return None
        return font.path

    @classmethod
    def font2ID(cls, font):
        """Answer the unique record/adapter ID of the font/style. This can be
        the unique database record id or the unique file path. For now we just
        answer the file path."""
        return cls.font2Path(font)

    @classmethod
    def font2FamilyID(cls, font):
        """Answer the unique record/adapter ID of the family of *font*. This
        can be the unique database record id of the font parent or the unique
        directory path of the font. For now we just answer the the location of
        the family plist file.

        Special situation is if the font is not saved yet. In that case it does
        not have a path."""
        fontPath = cls.font2Path(font)
        if fontPath is not None:
            return cls.path2ParentPath(fontPath) + '/' + cls.font2FamilyName(font) + '.plist'
        return None

    @classmethod
    def font2FamilyName(cls, font):
        return cls.fontName2FamilyName(cls.font2Name(font))

    @classmethod
    def font2StyleName(cls, font):
        return cls.fontName2StyleName(cls.font2Name(font))

    @classmethod
    def fontName2FamilyName(cls, name):
        """For now take the chunk up till "-" in the filename and ignore the
        family name as set in the font.info Also make sure that the extension
        is removed, if the font has no "-" it isn't name.
        Relay-Medium_Italic.ufo becomes Relay. ThisFont.ufo becomes ThisFont.
        """
        return name.split('.')[0].split('-')[0]

    @classmethod
    def fontName2StyleName(cls, name):
        return '-'.join(name.split('.')[0].split('-')[1:])

    @classmethod
    def font2UfoQueryName(cls, font):
        key = 'com.typenetwork.ufoqueryname'
        name = font.lib.get(key)
        if name is None:
            name = font.lib[key] = cls.font2Name(font)
        return name

    @classmethod
    def family2UfoQueryName(cls, font):
        key = 'com.typenetwork.ufoqueryfamilyname'
        name = font.lib.get(key)
        if name is None:
            name = font.lib[key] = cls.font2FamilyName(font)
        return name

    # ---------------------------------------------------------------------------------------------------------
    #    G E N E R A T O R

    @classmethod
    def uniqueID(cls):
        return '%x' % (int(time()) * 100000 + randint(0, 100000))

    # ---------------------------------------------------------------------------------------------------------
    #   T I M E

    @classmethod
    def seconds2Date(cls, seconds, year=1904):
        """Answers TTF seconds converted to a datetime instance."""
        return datetime.datetime(year, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=seconds)

    @classmethod
    def date2Seconds(cls, dt, year=1904):
        """Answers the datetime converted to TTF seconds."""
        return int((dt - datetime.datetime(year, 1, 1, 0, 0, 0)).total_seconds())

    # ---------------------------------------------------------------------------------------------------------
    #    T E S T I N G

    @classmethod
    def isUniqueID(cls, uid):
        if uid == 0: # None is not allowed in lib
            return True
        # In case it is a special SpacePoint unique uid
        if isinstance(uid, int) and uid in range(C.UNIQUEID_SPACE, C.UNIQUEID_SPACE + 4):
            return True
        return uid is not None and isinstance(uid, str) and uid.startswith('*')

    # ---------------------------------------------------------------------------------------------------------
    #    J S O N
    #
    #    Note that Status now has its own json conversion.

    @classmethod
    def json2Dict(cls, src):
        try:
            return json.loads(src)
        except TypeError:
            return None

    @classmethod
    def dict2Json(cls, d):
        return json.dumps(d, indent=4)

    @classmethod
    def json2List(cls, src):
        try:
            return json.loads(src)
        except TypeError:
            return None

    @classmethod
    def list2Json(cls, d):
        return json.dumps(d, indent=4)


    # ---------------------------------------------------------------------------------------------------------
    #    H I N T  P R O G R A M

    @classmethod
    def program2Source(cls, ttxprogram):
        """Transforms the TTX program into a text source, where the line
        breaks are before evert mnemonic. Blank lines are removed."""
        source = []
        for line in list(ttxprogram):
            if not line:
                continue
            if line and line[0].upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                source += '\n' + line
            else:
                source += ' ' + line
        return ''.join(source)

    # ---------------------------------------------------------------------------------------------------------
    #    C V T  D I C T  C O N V E R S I O N

    @classmethod
    def stringKeyDict2IntKeyDict(cls, stringkeydict):
        """Used for converting RoboFont font.lib CVT dict (with string keys)
        to the CVT dict (with int keys) as needed for TTX."""
        intkeydict = {}
        for stringkey, item in stringkeydict.items():
            intkey = cls.asInt(stringkey)
            if intkey is not None:
                intkeydict[intkey] = item
        return intkeydict

    # ---------------------------------------------------------------------------------------------------------
    #    P O I N T  &  C O N T O U R

    @classmethod
    def labels2LabelList(cls, labels):
        if labels is None:
            labelList = []
        elif isinstance(labels, str):
            labelList = cls.commaString2List(labels)
        elif isinstance(labels, (list, tuple)):
            labelList = cls.stringList2StrippedList(labels)
        else:
            labelList = [repr(labels)]
        return labelList

    # ---------------------------------------------------------------------------------------------------------
    #    R O M A N  N U M E R A L S

    @classmethod
    def arabic2RomanNumerals(cls, arabic):
        """Return the roman numeral representing n. Should work for n in (1,
        4999). Borrowed from Nick Montfort."""
        numerals = [(value, numeral) for numeral, value in C.ROMAN_NUMERAL_VALUES.items()]
        numerals.sort()
        numerals.reverse()
        smaller = {1000: (100, 'C'), 500: (100, 'C'),
                   100: (10, 'X'), 50: (10, 'X'), 10: (1, 'I'),
                   5: (1, 'I')}
        roman = ''
        for (value, numeral) in numerals:
            roman += (arabic / value) * numeral
            arabic -= (arabic / value) * value
            if value in smaller and arabic >= value - smaller[value][0]:
                roman += smaller[value][1] + numeral
                arabic -= (value - smaller[value][0])
        return roman

    """ -- "values" is error here
    @classmethod
    def romanNumeral2Arabic(cls, roman, VERBOSE=False):
        letters = list(roman)
        letters.reverse()
        arabic = 0
        place = 0
        for letter in letters:
            if VERBOSE: print(letter, place)
            value = values[letter]
            if value >= place:
                arabic += value
                if VERBOSE: print('\t+', value)
            else:
                arabic -= value
                if VERBOSE: print('\t-', value)
            place = value
        return arabic
    """

    # ---------------------------------------------------------------------------------------------------------
    #    U N I C O D E

    @classmethod
    def dec2hex(cls, n, uni=1):
        hex = "%X" % n

        if uni == 1:
            while len(hex) <= 3:
                hex = '0' + str(hex)
        return hex

    @classmethod
    def hex2dec(cls, s):
        try:
            return int(s, 16)
        except:
            pass

    @classmethod
    def hex2char(cls, hex):
        try:
            return chr(cls.hex2dec(hex))
        except:
            pass

    @classmethod
    def writeUnicode(cls, unicodeString):
        """Takes a unicode string and returns a decimal integer."""
        if type(unicodeString) is str:
            return cls.hex2dec(unicodeString)
        else:
            return int(unicodeString)

    @classmethod
    def readUnicode(cls, unicodeInteger):
        """Takes a decimal integer and returns a unicode string."""
        if type(unicodeInteger) is int:
            return cls.dec2hex(unicodeInteger)
        else:
            return str(unicodeInteger)

    @classmethod
    def writeUnicodes(cls, uniStringList):
        """Takes a list of unicode strings and returns a list of
        ufoLib-friendly (?) integers."""
        intList = []
        for u in uniStringList:
            intList.append(cls.writeUnicode(u))
        return intList

    @classmethod
    def readUnicodes(cls, uniIntList):
        """Takes a list of ufoLib friendly (?) integers and returns a string of
        unicodes."""
        stringList = []
        for u in uniIntList:
            stringList.append(cls.readUnicode(u))
        return stringList

    # ---------------------------------------------------------------------------------------------------------
    # G L Y P H  N A M E

    @classmethod
    def _getDecomposedBaseName(cls, name, result=None):
        """Deconstructs the name, starting from the right side, recognizing
        chunks that are diacritics names. Recursively adds as many as possible.
        Once there is no match, the remaining left part must be the base name
        of the glyph. Recursively answers the baseName and the list of found
        diacritics. In the "altBaseName" result attribute. The caller gets
        translated "i" and "j" into "dotlessi" and "dotlessj" info."""
        if result is None:
            result = []

        for index in range(1, len(name)):
            diacritics = name[-index:]
            if diacritics in SS_ACCENTS:
                result = [diacritics] + result
                return cls._getDecomposedBaseName(name[:-index], result)

        return name, result

    @classmethod
    def name2DecomposedName(cls, name):
        """Decomposes the glyph name into a dict, holding name, baseName, a
        list of diacritics and a list of extensions, by splitting on
        glyph/accent name patterns. Exceptions to this method are ('Thorn',
        'thorn', 'slash' and 'ascii')."""

        exceptions = ('Thorn', 'thorn', 'slash', 'ascii')
        if any(exception in name for exception in exceptions):
            decomposedName = dict(name=name, baseName=name, altBaseName=name, diacritics=[], extensions=[])
        elif name.startswith('.'):
            decomposedName = dict(name=name, baseName=name, altBaseName=name, diacritics=[], extensions=[])
        else:
            parts = name.split('.') # ['Agrave', 'sc']
            extensions = parts[1:]
            baseName, diacritics = cls._getDecomposedBaseName(parts[0])

            # If the baseName is "i" or "j" make altBaseName into
            # "dotlessi" or "dotlessj" of it is combined with a top accent.
            # Otherwise altBaseName is equal to baseName
            if baseName in ('i', 'j') and SS_TOPACCENTS.intersection(set(diacritics)):
                altBaseName = 'dotless'+baseName # Make alternative baseName
            else:
                altBaseName = baseName
            if extensions: # Put them back on the base name
                baseName += '.' + '.'.join(extensions)
            decomposedName = dict(name=name, baseName=baseName,
                altBaseName=altBaseName, diacritics=diacritics, extensions=extensions)
        return decomposedName


    # ---------------------------------------------------------------------------------------------------------
    # Floq field name conversion between Floq attributes and database fields

    @classmethod
    def floq2Field(cls, floqName):
        if floqName.endswith('ID'):
            return floqName[:-2]+'_id'
        return floqName

    @classmethod
    def field2Floq(cls, fieldName):
        if fieldName.endswith('_id'):
            return fieldName[:-3]+'ID'
        return fieldName

    # ---------------------------------------------------------------------------------------------------------
    #    T T X

    @classmethod
    def formatBinaryForTTX(cls, b, length=32, segments=8):
        import string
        s = str(b)[2:]
        prefix = '0' * (length - len(s))
        s = prefix + s
        sWithSpaces = "".join(s[i:i + segments] + " " for i in xrange(0, len(s), segments))
        return sWithSpaces.strip()

    # ----------------------------------------------------------------------------------------------------------
    # Python Objects

    @classmethod
    def isUniqueList(cls, l):
        try:
            if len(l) == len(set(l)):
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def makeUniqueList(cls, seq, idfun=None):
        # order preserving
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            # in old Python versions:
            # if marker in seen
            # but in new ones:
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result

    @classmethod
    def isUniqueDict(cls, d):
        if cls.isUniqueList(d.values()):
            return True
        else:
            return False

    @classmethod
    def reverseDict(cls, d):
        if not cls.isUniqueDict(d):
            usedValues = []
            duplicateValues = []
            for v in d.values():
                if v in usedValues:
                    duplicateValues.append(v)
                usedValues.append(v)

            print('Warning: duplicate values found %s' % str(duplicateValues))

        newDict = {}
        keys = d.keys()
        keys.sort()
        for k in keys:
            v = d[k]
            if isinstance(v, list):
                v = tuple(v)
            newDict[v] = k
        return newDict

    @classmethod
    def bash(cls, cmd, cwd=None):
        """Runs a command in the bash shell."""
        import subprocess
        retVal = subprocess.Popen(cmd, shell=True, \
            stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
        if retVal == ['']:
            return(0)
        else:
            return(retVal)

    # ------------------------------------------------------------------------------------------------------------------
    #    M A G I C  K E Y  P R O T E C T I O N

    @classmethod
    def getMagicKey(cls, uid=1):
        """To be calculated in the calling application identically.

        @@@ Add this conditionally to the URL when going live and secure, to be
        checked on the server side."""
        return int(round(math.pi * 123234545645) + uid * id * 223344)

    @classmethod
    def validMagicKey(cls, key, uid=1):
        return key == cls.getMagicKey(uid or 1)

    @classmethod
    def encryptPassword(cls, password):
        return hashlib.md5(password).hexdigest()

    #  T N F O N T

    @classmethod
    def naked(cls, p):
        if hasattr(p, 'naked'):
            p = p.naked()
        return p

    # ---------------------------------------------------------------------------------------------------------
    #     X M L  C O N V E R S I O N S

    @classmethod
    def dataAttribute2Html5Attribute(cls, key):
        """The @dataAttribute2Html5Attribute@ method converts an *key*
        attribute that starts with @'data_'@ to the HTML5 attribute that starts
        with @'data-'@. Otherwise the *key* attribute is answered unchanged.
        """
        if key.startswith(u'data_'):
            return 'data-' + key[5:]
        return key

    @classmethod
    def pyAttrName2XmlAttrName(cls, key):
        """
        The @pyAttrName2XmlAttrName@ converts the Python XML attribute name @key@ to an
        appropriate XML attribute identifier.<br/>.
        If the *key* is @'class_'@ then it is translated into @'class'@.
        If there is an HTML5 attribute *data_xxxx* used, then change that to *data-xxxx*.
        """
        if key == 'class_':
            key = 'class'
        if key.startswith('data'):
            key = key.replace('_', '-')
        return key

    @classmethod
    def xmlAttrName2PyAttrName(cls, key):
        """The @xmlAttrName2PyAttrName@ method converts the XML attribute name
        *key* to an appropriate Python attribute identifier.<br/>

        If the *key* is @'class'@ then it is translated into @'class_'@. If a
        namespace is defined (to be recognized on {...}, then replace that by
        prefix @'ns_'@.<br/> If there is an HTML5 attribute *data-xxxx* used,
        then change that to *data_xxxx*."""
        if key == 'class':
            key = 'class_'
        elif key.startswith('{'):
            key = 'ns_' + key.split('}')[-1]
        elif '-' in key:
            # In case of new HTML5 data-xxxx attributes.
            key = key.replace('-', '_')
        return key

    @classmethod
    def xmlValue2PyValue(cls, value, conversions):
        """The @xmlValue2PyValue@ method converts the XML string attribute to
        the appropriate Python object type, if the class is defined in the list
        *conversions*. If the *value* is not a string, it must have been
        converted before (e.g. by self.EXPR), the answer it untouched."""
        if not isinstance(value, str):
            return value

        strippedvalue = value.strip()

        if int in conversions:
            try:
                return int(strippedvalue)
            except ValueError:
                pass

        if float in conversions:
            try:
                return float(strippedvalue)
            except ValueError:
                pass

        if bool in conversions:
            if strippedvalue.lower() in ['true', 'false']:
                return strippedvalue.lower() == 'true'

        if dict in conversions or list in conversions or tuple in conversions:
            if ((strippedvalue.startswith('{') and strippedvalue.endswith('}')) or
                (strippedvalue.startswith('[') and strippedvalue.endswith(']')) or
                (strippedvalue.startswith('(') and strippedvalue.endswith(')'))):
                try:
                    # In theory this is a security leak, since there maybe
                    # "strange" objects inside the dictionary. Problem to be
                    # solved in the future?
                    return eval(strippedvalue)
                except (SyntaxError, NameError):
                    pass

        # Can't do anything with this value. Return unstripped and untouched.
        return value

    # Remove all tags from the string
    REMOVETAGS = re.compile(r'<.*?>')

    @classmethod
    def stripTags(cls, xml):
        return cls.REMOVETAGS.sub('', xml)

    REMOVEMULTIPLEWHITESPACE = re.compile(r'\n\s+')

    @classmethod
    def stripMultipleWhiteLines(cls, s):
        return cls.REMOVEMULTIPLEWHITESPACE.sub('\n\n', s)

    # support single or double quotes while ignoring quotes preceded by \
    XMLATTRS = re.compile(r'''([A-Z][A-Z0-9_]*)\s*=\s*(?P<quote>["'])(.*?)(?<!\\)(?P=quote)''', re.IGNORECASE)

    @classmethod
    def xmlAttrString2PyAttr(cls, s, conversions):
        attrs = {}
        for key, _, value in cls.XMLATTRS.findall(s):
            attrs[key] = value
        return cls.xmlAttr2PyAttr(attrs, conversions)

    @classmethod
    def xmlAttr2PyAttr(cls, par_dict, conversions):
        """Transforms an XML attribute dictionary to a Python attribute
        dictionary. The *class* attribute name is translated into *class_* and
        all values are tested to convert into either @int@, @float@ or
        boolean as represented by one of @'TRUE'@, @True@, @true@, @FALSE@,
        @False@, @false@. If the conversion fails, then pass the value
        unchanged. If there the attribute name is of format

        @'{http://www.w3.org/XML/1998/namespace}space'@

        e.g. as generated by Xopus XML Schema, then just remove the name space
        prefix. If there is an HTML5 attribute *data-xxxx* used, then change
        that to *data_xxxx*."""
        pydict = {}

        for key, value in par_dict.items():
            key = cls.xmlAttrName2PyAttrName(key)
            value = cls.xmlValue2PyValue(value, conversions)
            pydict[key] = value
        return pydict

    @classmethod
    def tableField2JoinedField(cls, table, field):
        if field.startswith(table):
            return field
        return '%s_%s' % (table, field)

    @classmethod
    def value2TagName(cls, value):
        """
        The @value2TagName@ class method converts the *value* object into a value XML tag name.
        """
        tagname = []
        if not isinstance(value, str):
            value = repr(value)
        if value.lower().startswith('xml'):
            tagname.append('_')
        for c in value:
            if c in ' !?@#$%^&*()[]\t\r\n/\\':
                pass
            elif c.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890:.':
                tagname.append(c)
            else:
                tagname.append('_')
        return ''.join(tagname)
