# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tools.py
#

"""
Keeps hard links to open tool instances of type Tool in the TOOLS dictionary to
avoid opening multiple instances; key is toolId + family name.

{key: toolInstance, ...}

NOTE: doesn't look at BaseTool instances.
"""
import logging
import os
from tnbits.base.log import Log
from tnbits.base.handler import BitsHandler

TOOLS = {}
BLACKLIST = ('Badger.py', 'DisplayItems.py', 'SwitchBoard.py')
PREFTOOLS = {'Tool': ['Proof', 'QualityAssurance', 'TextCenter'], 'BaseTool': ['Dimensioneer']}

LOG = None

def openTool(toolClass, family=None):
    """Open a new tool window of this class if it doesn't exist yet, or if
    multiple windows of the same tool are allowed. Adds family name to tool ID
    to enable a separate tool for each family."""
    if family is None:
        return

    toolIdentifier = '%s_%s' % (toolClass.TOOLID, family.name)
    tool = getTool(toolIdentifier)
    openLog()

    if tool is None:
        tool = toolClass()
        tool.TOOLID = toolIdentifier # Necessary?
        addTool(toolIdentifier, tool)
        tool.build()

        if not family is None and hasattr(tool, 'setFamily'):
            tool.setFamily(family)
    else:
        tool.getWindowToFront()

    return tool

def addTool(toolIdentifier, tool):
    """Add the **tool** to **TOOLS**."""
    TOOLS[tool.getID()] = tool

def removeTool(tool):
    toolId = tool.getID()

    if toolId in TOOLS:
        del TOOLS[toolId]

def getTool(toolID):
    """Answer the tool of **toolClass**. If it does not exist, create an
    instance first."""
    if toolID in TOOLS:
        return TOOLS[toolID]

def showOutputWindow():
    """Shows RoboFont output window."""
    from mojo.UI import OutputWindow
    o = OutputWindow()
    o.show()

def getToolById(toolId):
    """Answer the tool instance indicated by **toolId**. If the tool
    does not exist, or the weakref is dead, then answer **None**."""
    return TOOLS.get(toolId)

def exists(toolClass):
    """Answer is an instance of the **toolClass** tool
    already exists."""
    return getID(toolClass) in TOOLS

def getTools(toolClass):
    """Answer the dictionary with tools that are not dead. Clean up
    **TOOLS** during iteration."""
    return TOOLS

def getID(toolClass):
    """Unique tool ID. Must be refined by inheriting class. Otherwise None, to
    prevent base tool classes to add themselves."""
    return toolClass.TOOLID

def getPrefTools():
    """Fixed list of tool names that have their own preference settings.
    NOTE: Should eventually include (almost) all tools.
    """
    return PREFTOOLS

def findTools(path, verbose=False):
    """Recursively looks for all tools in the script area."""
    toolIdentifiers = []

    for fileName in os.listdir(path):
        ignore = False

        # Filter the names of files that cannot be valid tools
        if fileName[0] in '_.': # Ignore these files and folders
            continue

        # Now we found a valid file
        filePath = path + '/' + fileName

        if os.path.isdir(filePath):
            tn = findTools(filePath, verbose=verbose)
            toolIdentifiers.extend(tn)
        else:
            # Must be a file. Is it a Python source?
            if not fileName.endswith('.py'):
                ignore = True

            if fileName in BLACKLIST:
                ignore = True

            if ignore:
                if verbose:
                    print('findTools(): ignoring %s' % filePath)
                continue
            else:
                toolIdentifiers.append(fileName)

    return toolIdentifiers

def loadToolFromFile(self, filepath):
    """Loads (read and compiler) the module indicated by `filePath`.

    NOTE: disabling for now, but might be useful in some cases.
    """
    import os, imp

    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    py_mod = None

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    return py_mod

# Logging.

def addLogger(moduleName, h):
    logger = logging.getLogger(moduleName)
    logger.addHandler(h)

def openLog():
    global LOG

    if LOG is None:
        LOG = Log()
        h = BitsHandler(LOG.console)
        addLogger('tnbits', h)

def getLog():
    if LOG is None:
        openLog()
    return LOG

def setLog():
    log = getLog()
    log.set()

def showLog():
    log = getLog()
    log.show()
