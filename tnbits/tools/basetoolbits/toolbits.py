# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    toolbits.py
#
from AppKit import NSLog
import weakref
import os, imp, inspect
import traceback

# Folders to ignore in searching for tools.
WHITELIST = ('Dimensioneer.py', 'OverlayUFOs.py', 'LayerManager.py', \
        'CurvePalet.py', 'OutlineManager.py', 'Nudge.py', 'GlyphsMover.py', \
        'TextCenter.py', 'TrueTypeSubsetter.py', 'LegalBuilder.py')
BLACKLIST = ('Badger.py', 'DisplayItems.py')

class ToolBits:
    """Bits and pieces to find other tools. This allows tools to start other tools.

    TODO: also implement as global functions in tnbits.base.badger.
    """


    def findTools(self, force=False, path=None, paths=None, badger=None, verbose=False):
        """Recursively finds all tool classes in the script area, that have a
        valid value for *self.TOOLID* and then store an instance of that tool
        if it does not already exists. If the `force` flag is set, then always
        replace the tool instance after calling `tool.terminate()` for the
        existing tool. Tools and folders that start with a "_" are ignored.
        The *badger* is defined if this method is called by the main badger
        tool. Other tools will use their internal defined badger weakref
        attribute.

        TODO: should badger really execute all the tools first?
        """
        if paths is None:
            paths = {}
            path = self.getRoot()
            print(path)

        if badger is None:
            badger = self.badger

        errorPath = path + '.tnError.txt'

        for fileName in os.listdir(path):
            ignore = False
            # Filter the names of files that cannot be valid tools.

            if fileName[0] in '_.': # Ignore these files and folders
                continue

            filePath = path + '/' + fileName

            if os.path.isdir(filePath):
                self.findTools(force, filePath, paths, badger)


            # Must be Python source.
            if not fileName.endswith('.py'):
                ignore = True
            elif fileName in BLACKLIST: # Don't list self.
                ignore = True
            elif fileName not in WHITELIST:
                ignore = True

            if ignore:
                #if verbose:
                #    print('findTools(): ignoring %s' % filePath)
                continue

            try:
                # FIXME: is this really necessary?
                # WARNING: Scripts in the Tool-area should NOT use any direct
                # executable code because the interpretation by the badger will
                # then execute them. E.g. opening font dialogs and such. Use if
                # __name__ == '__main__' instead.
                tool = self.loadToolFromFile(filePath)
                print('findTools(): executing %s' % filePath)

                for cls in tool.__dict__.values():
                    # Try instantiate tool from cls
                    self.makeTool(cls, force, filePath, badger)

            except Exception as e:
                errorFile = open(errorPath, 'w')
                errorFile.write('Badger: error loading tool %s\n%s' % (filePath, str(e)))
                errorFile.write(traceback.format_exc())
                errorFile.close()

        return self.getTools()

    def loadToolFromFile(self, filepath):
        """Loads (read and compiler) the module indicated by `filePath`.
        """
        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            return imp.load_source(mod_name, filepath)

    def makeToolByToolId(self, toolId):
        """Finds the class related to `toolId` and build the tool, if it fits the requirement of
        a `BaseTool`: support `tool.getId()`, supports `tool.buid()` and does not
        exist already."""
        tools = self.findTools() # Read tree from file, it may have changed.
        if toolId in tools:
            tools[toolId].build()
            return tools[toolId] # Answer the tool for convenience of the caller.
        return None

    def makeTool(self, cls, force, filePath, badger=None):
        """Adds an instance of cls to `self.tools` if it has a valid
        `self.TOOLID` and if it doesn’t exists yet, or of the _force_ flag is
        set. If an existing tool instance is deleted then call the
        `tool.terminate()` first. """
        # FIXME: do we really want to execute all tools beforehand?
        if badger is None:
            badger = self.badger

        if hasattr(cls, "__name__") and hasattr(cls, "__module__") and cls.__name__ == "Object" and cls.__module__ == "objc":
            # objc.Object can crash hard on a hasattr(cls, ...)
            return None

        #from tnbits.tools.basetool import BaseTool
        from tnbits.base.tool import Tool

        '''
        If the tools can have multiple windows, then the selection should
        be through the opening of a family or style. The tool will not
        show up in the badger selection. If there is tool class id
        defined the tool will add itself to the global tool set. Just
        instantiate. If badger is None, we are collecting for
        preferences.
        '''
        if inspect.isclass(cls) and cls != Tool and \
            hasattr(cls, 'getId') and hasattr(cls, 'build'):
            if not cls.ALLOWMULTIPLE and cls.exists():
                print('Unique tool %s already exists' % cls.TOOLID)
                return

            # Not a base tool or disabled tool.
            if (badger is None or not cls.ALLOWMULTIPLE):# and cls.getId():
                tool = cls()

                if tool is None:
                    print('No tool with class %s' % cls)
                    return
                elif isinstance(tool, Tool):
                    print('Skipping new style tool %s for now...' % cls)
                    return
                else:
                    # Keep original file path of this tool.
                    tool.path = filePath
                    # Set tool.badger as weakref. Typically this is the
                    # main badger tool.
                    tool.badger = badger
                    # Store in the global TOOLS pool as weak ref with
                    # toolId as key.
                    self.addTool(tool)
                    return tool

    # self.badger  # Answer the main badger tool, who does category selection.

    def _get_badger(self):
        if hasattr(self, '_badger') and self._badger is not None:
            return self._badger()
        return None

    def _set_badger(self, badger):
        if badger is not None:
            self._badger = weakref.ref(badger)
        else:
            self._badger = None

    badger = property(_get_badger, _set_badger)

    # self.category # Answer the current category selections of the badger tool.
    # Can be None if the badger is not available.

    def _get_category(self):
        badger = self.badger
        if badger is not None:
            return badger.getSelectedCategory()
        return None

    category = property(_get_category)
