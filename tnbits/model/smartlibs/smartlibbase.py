# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    smartlibbase.py
#
from tnbits.model import model

def getStyle(styleKey):
    return model.getStyle(styleKey)

class SmartLibBase(object):
    """SmartLibBase is the base class for instance that need to read/write into
    style.lib, with the need for hidden data conversion, e.g. data sets that
    are using non-standard Python object which are not supported in style.lib
    UFO storage.

    Inheriting SmartLib classes should redefine self.getLib() and
    self.asDict().  Note that the family.updateStyles is checking on the
    validity of the open naken font/style instance.  If RoboFont opens a font
    that is already open in the model, then this is replace by the new
    RoboFont instance.  That that moment also the piggy-backed
    style._tnSmartLibs is copied as reference to the new font instance."""

    SLKEY = '_tnSmartLibs' # Collection of SmartLib data in style.lib

    def __init__(self, styleKey):
        """The style is found through the unique styleKey, which has format
        (familyPath, styleFileName)."""
        self.styleKey = styleKey
        # Get the dict from style.lib and allow self to convert it into self.d
        self.d = self.fromDict(self._fromLib())

    @classmethod
    def getId(cls):
        return cls.__name__

    @classmethod
    def isSmartLib(cls):
        return True

    @classmethod
    def clearLibs(cls, styleKey):
        style = getStyle(styleKey)
        if style is not None:
            try:
                del style._tnSmartLibs
            except AttributeError:
                pass # Ignore if it does not exist.
            try:
                del style.lib['_tnSmartLibs']
            except KeyError:
                pass # Ignore if it does not exist.

    @classmethod
    def getLib(cls, styleKey):
        """The actual "cls" is defined by the caller, likely to be inheriting
        from SmartLibBase. Class should support __init__(self, styleKey), where
        d is the dict coming from style.lib['_tnSmartLibs'][cls.getId()], if is
        already stored in the style. Otherwise a new dict is created.

        cls.asDict() answers the style.lib[key] compatible dictionary. If there
        is no data in the style._tnSmartLibs yet, an empty instance is created
        and stored in the style before answering.  If
        style._tnSmartLibs[cls.getId()] already exists, then answer it without
        reading from style.lib."""
        style = getStyle(styleKey) # Make sure to talk to the existing naked styleKey instance.
        if style is None: # Double check, the style may not exist anymore.
            return None
        try:
            smartLibs = style._tnSmartLibs
        except AttributeError:
            smartLibs = style._tnSmartLibs = {}
        name = cls.getId()
        if not name in smartLibs:
            smartLibs[name] = cls(styleKey) # Up to the calling smartLib class to collect and convert the data from style.lib.
        return smartLibs.get(name)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.d)

    def get(self, key, default=None):
        return self.d.get(key, default)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    # self.style   Answer style from the model by styleKey
    def _get_style(self):
        return getStyle(self.styleKey)
    style = property(_get_style)

    def _fromLib(self):
        """Answer the dict from style.lib. Create an empty dict if it does not
        exist there."""
        try:
            return self.style.lib[self.SLKEY][self.getId()]
        except KeyError:
            return {}

    def save(self):
        """Save the self.d in the style.lib as safe converted data."""
        style = self.style
        if style is not None:
            if not self.SLKEY in style.lib.keys(): # No smartLibs in this style yet. Prepare the overall dict.
                style.lib[self.SLKEY] = {}
            # Store the converted data into style.lib['_tnSmartLibs'][self.getId()]
            style.lib[self.SLKEY][self.getId()] = self.asDict()

    # Redefined by inheriting classes to convert data from/to style.lib

    def fromDict(self, d):
        """Main method to answer the style.lib collected data and answer as
        dict. To be redefined by inheriting classes. Default behavior is to
        answer the unmodified dict."""
        return d

    def asDict(self):
        """Answer the data of self as dict to ba saved in
        self.style.lib['_tnSmartLibs'].  To be redefined by inheriting classed.
        Default behavior is to store the unmodified self.d."""
        return self.d

def saveSmartLibs(styleKey):
    """Save all the smart lib instances in the naked style into the style.lib.
    Note that this way tools can initialize their own smart sets (without using
    the get(style, cls) function) in the style.  This method will save all
    instances that pass the isSmartSet() test into style.lib.  Answer the dirty
    flag if the styleOrGlyph.lib actually changed."""
    style = getStyle(styleKey)
    dirty = False
    try:
        smartLibs = style._tnSmartLibs
        for name, smartLib in smartLibs.items():
            if smartLib.isSmartLib():
                smartLib.save()
                dirty = True
    except AttributeError:
        pass # No smart libs in the indicated style. Ignore save.
    return dirty # Answer the flag if the styleOrGlyph actually changed.

if __file__ == '__main__':
    class MySmartLib(SmartLibBase):
        # Redefine getLib to convert style.lib data into local data. E.g. by create set from list.
        def getLib(self):
            try:
                d = self.obj.lib[self.SLKEY][self.getId()]
                d['XYZ'] = set(d.get('XYZ', []))
            except KeyError:
                return dict(XYZ=set())

        # Prepere the data to be saved: answer dict with only Python base data types, to be saved into style.lib
        def asDict(self):
            return dict(XYZ=list(self.get('XYZ', [])))

    f = CurrentFont()
    mySmartLib = MySmartLib.getLib(f)
    mySmartLib['XYZ'] = set((1234, 2345)) # Non style.lib savvy data.
    mySmartLib.save()
    print(f.lib['_tnSmartLibs'])
    print(f.naked()._tnSmartLibs[MySmartLib.getId()].d)
