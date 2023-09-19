# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttxwriter.py
#
import os
from fontTools import ttx

from tnbits.constants import Constants
from tnbits.toolbox.transformer import TX
from fontTools.ttLib import TTLibError

from AppKit import NSLog

class TTXWriter(object):
    """
    """

    C = Constants

    @classmethod
    def decompile(cls, path):
        """
        Decompiles the path into a TTX file. If the path is another format than TTF
        then converts it to TTF. Test if the file exists, else answers None.
        """
        ttfPath = TX.path2FormatPath(path, cls.C.EXTENSION_TTF)
        ttxPath = TX.path2FormatPath(path, cls.C.EXTENSION_TTX)

        if os.path.exists(ttfPath):
            try:
                ttx.ttDump(ttfPath, ttxPath, ttx.Options({}, 1))
            except TTLibError as e:
                NSLog(str(e))

            return ttxPath

        return None

    @classmethod
    def compile(cls, path):
        """
        Compiles the path into TTF format. If the path is another format than TTX
        then converts it to TTX. Tests if the file exists then converts and answers
        the TTX path. Otherwise answers None.
        """
        ttxPath = TX.path2FormatPath(path, cls.C.EXTENSION_TTX)
        ttfPath = TX.path2FormatPath(path, cls.C.EXTENSION_TTF)

        if os.path.exists(ttfPath):
            try:
                ttx.ttCompile(ttxPath, ttfPath, ttx.Options({}, 1))
            except Exception as e:
                NSLog(str(e))

            return ttfPath
        return None

    @classmethod
    def delete(cls, path):
        """If it exists, removes the TTX file that is related to path."""
        ttxPath = TX.path2FormatPath(path, cls.C.EXTENSION_TTX)
        if os.path.exists(ttxPath):
            os.remove(ttxPath)
