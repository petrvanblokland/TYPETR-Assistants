# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     pack.py
#
from adict import ADict, AList

class Pack(ADict):
    """The *Pack* class is basically identical to the *ADict* (Attribute Dict) class.
    *Pack* instances are used to transfer chunks of data between adapters. The functionality
    can be compared with the tables inside TTF and OTF fonts (an in practice they will
    have a similar architecture), but they are not compatible, since other adapters (e.g. UFO)
    don't have the same division of data."""

    @classmethod
    def _getDictClass(cls):
        return Pack

    @classmethod
    def _getListClass(cls):
        return PackList

class PackList(AList):

    @classmethod
    def _getDictClass(cls):
        return Pack

    @classmethod
    def _getListClass(cls):
        return PackList

