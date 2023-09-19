# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    static.py

import tnbits
ROOT_TNBITS = '/'.join(tnbits.__file__.split('/')[:-1])
ROOT_TNTOOLS =  '/'.join(ROOT_TNBITS.split('/')[:-1]) + '/tntools'

'''
Keep hard links to open tool instances of type BaseTool in the TOOLS dictionary to avoid
opening multiple instances; key is toolId.

{toolId: toolInstance, ...}
'''
TOOLS = {}

def getRoot():
    """Answers the root *ROOT_TNTOOLS* as defined on initialization."""
    return ROOT_TNTOOLS

def open(cls, toolID=None):
    """Opens a new tool window of this class if it doesn't exist yet, or if
    multiple windows of the same tool are allowed. Optional custom tool ID to
    enable separate tools for multiple families."""
    if toolID is not None:
        cls.TOOLID = toolID

    tool = cls.getTool()

    if tool.ALLOWMULTIPLE or not tool.isOpen():
        tool.build()
    else:
        # Bring the existing tool window to the front.
        tool.getWindowToFront()

    return tool # Answer the new instance as convenience for the caller.

def addTool(tool):
    """Adds the `tool` to `TOOLS`."""
    TOOLS[tool.getId()] = tool

def getTool(cls):
    """Answer the tool of `cls`. If it does not exist, create an instance first."""
    if not cls.exists():
        cls.addTool(cls())
    return TOOLS[cls.getId()]

def getToolById(cls, toolId):
    """Answer the tool instance indicated by `toolId`. If the tool does not exist,
    or the weakref is dead, then answer `None`."""
    return TOOLS.get(toolId)

def exists(cls):
    """Answer is an instance of the `cls` tool already exists."""
    return cls.getId() in TOOLS

def getTools(cls):
    """Answer the dictionary with tools that are not dead. Clean up `TOOLS`
    during iteration."""
    return TOOLS

def getId(cls):
    """Unique tool id. Must be refined by inheriting class. Otherwise None,
    to prevent base tool classes to add themselves."""
    return cls.TOOLID

def getName(cls):
    """Answer the tool name, as defined by the inheriting class."""
    return cls.NAME

def isCurrentGlyph(cls, glyph):
    """
    Tests if the parameter glyph and the currently selected one are the same.
    """
    current = cls.getCurrentGlyph()
    return bool(glyph is not None and current is not None and glyph._object is current._object)

# RoboFab.

def getCurrentStyle():
    from mojo.roboFont import CurrentFont
    return CurrentFont()

def getCurrentGlyph():
    """Gets the current glyph in the front RF editor window."""
    from mojo.roboFont import CurrentGlyph
    return CurrentGlyph()

