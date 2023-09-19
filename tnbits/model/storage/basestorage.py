# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   basestorage.py
#
import os
from fontTools.ttLib import TTFont
from tnbits.toolbox.transformer import TX

class BaseStorage(object):
    """Defines the storage API."""

    #
    # Reading
    #

    # Reading top level info

    def readInfoPack(self):
        """Format
            dict(infoKey: value, ...}
        """
        pack = self._readInfoPack()
        self._validateInfoPack(pack)
        return pack

    def _readInfoPack(self):
        raise NotImplementedError(self)

    def readKerningPack(self):
        """Format
            dict(horizontal: {'A': {'V': -12, ...}, ...}, # kern or GPOS
                 vertical: {'AA': {'BB': 50, ...}, ...), # GPOS, vhea, etc.
            }
        """
        raise NotImplementedError

    def readLibPack(self):
        """Format
            dict(key1: value1, ...}
        """
        raise NotImplementedError

    def readGroupPack(self):
        raise NotImplementedError

    def readFeaturePack(self):
        raise NotImplementedError

    def readHintPack(self):
        raise NotImplementedError

    def readPacks(self):
        """In case the caller wants to read all style packs at once."""
        return dict(
            info=self.readInfoPack(),
            kerning=self.readKerningPack(),
            lib=self.readLibPack(),
            group=self.readGroupPack(),
            feature=self.readFeaturePack(),
            hintPack=self.readHintPack(),
        )

    # Reading glyphs

    def readGlyphPack(self, glyphName):
        raise NotImplementedError

    '''
    def getRepresentation(self, glyphName, location, bezierPath):
        raise NotImplementedError
    '''

    # Introspection

    def getGlyphNames(self):
        """Return the list of glyph names in the font (in order)."""
        raise NotImplementedError

    def getNumberOfGlyphs(self):
        return len(self.getGlyphNames())

    #TODO: use __contains__()?

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    #
    # Writing
    #

    # Writing top level info

    def writeInfoPack(self, pack):
        self._validateInfoPack(pack)
        self._writeInfoPack(pack)

    def _writeInfoPack(self, pack):
        raise NotImplementedError

    def writeKerningPack(self, pack):
        raise NotImplementedError

    def writeLibPack(self, pack):
        raise NotImplementedError

    def writeGroupPack(self, pack):
        raise NotImplementedError

    def writeFeaturePack(self, pack):
        raise NotImplementedError

    def writeHintPack(self, pack):
        raise NotImplementedError

    # Writing glyphs

    def writeGlyphPack(self, glyphName, glyphPack):
        raise NotImplementedError

    def deleteGlyph(self, glyphName):
        raise NotImplementedError

    # Syncing/saving/flushing

    def sync(self):
        """Ensures all changes are written to the storage medium."""
        raise NotImplementedError

    # Validation

    def _validateInfoPack(self, infoPack):
        pass
        # raise errors or issue warnings?
        # checkPack(infoPack)

    def getId(self):
        raise NotImplementedError

def getStorageClass(data):
    """Answers the storage class that connects to the given data in the best
    way. This can be a font instance (with data.path attribute) or a plain path
    string."""
    storageClass = None

    if isinstance(data, TTFont):
        from tnbits.model.storage.otfstorage import OTFStorage
        storageClass = OTFStorage
    else:
        extension = TX.extensionOf(data).lower()

        if extension in ("ttf", "otf"):
            # Must be a TTF or OTF binary font file.
            from tnbits.model.storage.otfstorage import OTFStorage
            storageClass = OTFStorage
        elif extension == "ufo":
            # Must be a normal UFO file.
            from tnbits.model.storage.ufostorage import UFOStorage
            storageClass = UFOStorage
        elif extension == 'fam' or os.path.isdir(data):
            # Must be a family file reference.
            from tnbits.model.storage.familystorage import FamilyStorage
            storageClass = FamilyStorage

    # Not found, this style has not been saved yet -- no storage class yet.
    # Assume the type is a UFO.
    if storageClass is None:
        from tnbits.model.storage.ufostorage import UFOStorage
        storageClass = UFOStorage

    return storageClass

def getStorage(data):
    """Answer the storage instance that connects best to the given data. This
    can be a font instance (with data.path attribute) or a plain path string.

    In case the storage class cannot be found (e.g. with an unsaved new style),
    then answer None."""
    assert data
    cls = getStorageClass(data)

    # No storage class known, this is an unsaved new style or opened from
    # OTF/TTF.
    if cls in ('', None):
        return None

    return cls(data)
