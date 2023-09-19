# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#         glyphio.py
#
from tnbits.constants import Constants as C

class UfoIO(object):
    """
    The `UfoIO` class implements all knowledge of how to get lib data in a UFO font or UFO glyph
    (fontorglyph).
    """

    @classmethod
    def getLib(cls, fontorglyph, path=None, default=None):
        """
        The `getLib` answers the dictionary as stored in the lib of <attr>fontorglyph</attr> under
        <attr>path</attr> This allows every editor private space in the <attr>fontorglyph</attr>. If the lib of editor
        dictionary do not exist and <attr>default</attr> is defined, then the entry created and stored before answering.

        """
        if fontorglyph is not None:
            rootlib = fontorglyph.lib.get(C.FONTLIB_ROBOHINT)
            if rootlib is None:
                rootlib = fontorglyph.lib[C.FONTLIB_ROBOHINT] = {}
            if path is None:
                # No path defined, answer the entire lib.
                item = rootlib
            else:
                item = rootlib.get(path)
                if item is None and default is not None:
                    item = cls.setLib(fontorglyph, path, default)
            return item
        return None

    @classmethod
    def setLib(cls, fontorglyph, path, item):
        """
        The `setLibItem` method sets the <parh>key</attr> to <attr>item</attr> to be stored in the lib
        of <attr>fontorglyph</attr>. Make sure that the <attr>item</attr> is something that can be transformed into
        JSON source code.<br/>
        For convenience the <attr>item</attr> is answered.

        """
        if fontorglyph is not None:
            assert isinstance(item, (str, float, int, tuple, list, dict))
            rootlib = fontorglyph.lib.get(C.FONTLIB_ROBOHINT)
            if rootlib is None:
                rootlib = fontorglyph.lib[C.FONTLIB_ROBOHINT] = {}
            rootlib[path] = item
            return item
        return None

    @classmethod
    def clearLib(cls, fontorglyph):
        fontorglyph.lib[C.FONTLIB_ROBOHINT] = {}
