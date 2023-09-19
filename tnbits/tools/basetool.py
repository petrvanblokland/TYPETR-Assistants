# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    basetool.py
#
#   DEPRECATED: see tnbits.base.tool.

from AppKit import NSApp, NSLog, NSApplication, NSLeftMouseDragged, \
    NSRightMouseDragged, NSLeftMouseUp, NSRightMouseUp, NSShiftKeyMask, \
    NSAlternateKeyMask, NSCommandKeyMask, NSUpArrowFunctionKey, \
    NSDownArrowFunctionKey, NSLeftArrowFunctionKey, NSRightArrowFunctionKey
import traceback

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver
except:
    print('basetool.py (DEPRECATED): not in RoboFont, stand alone mode.')

from defconAppKit.windows.baseWindow import BaseWindowController
import tnbits
from tnbits.base.screens import ScreenConfiguration
from tnbits.constants import Constants
from tnbits.tools.window import FloatingScreenWindow, ScreenWindow
from tnbits.tools.basetoolbits.progressbits import ProgressBits
from tnbits.tools.basetoolbits.updaterbits import UpdaterBits
from tnbits.tools.basetoolbits.interpolatorbits import InterpolatorBits
from tnbits.tools.basetoolbits.preferencebits import PreferenceBits
from tnbits.tools.basetoolbits.toolbits import ToolBits
from tnbits.model import model

#   R O B O F O N T

# FIXME: test RFont.
#
def getRoboFontFont(style):
    """Answers the corresponding RoboFont wrapper font for this style. The
    assumption is that the RF font and style share the same naked font
    instance. Style can be another wrapper or a naked instance. This does the
    reverse of nakedStyle(f)"""
    # TODO: Should not be here? Move to RF BaseTool.
    from mojo.roboFont import AllFonts

    for font in AllFonts():
        if font and font.path == style.path:
            return font

    return None

def closeStyle(style):
    font = getRoboFontFont(style)
    if font is not None:
        font.close()

def updateStyle(style):
    """If the parent style of glyph is an open RoboFont font, then broadcast
    the update."""
    # TODO: Should not be here? Move to RF BaseTool.
    font = getRoboFontFont(style)
    if font is not None:
        print('updating %s' % style.path)
        font.update()

def style2Front(style):
    """Make style the front window and set to current font.

    NOTE: see also self.style2Front().

    """
    # TODO: Should not be here? Move to RF BaseTool.
    font = getRoboFontFont(style)
    if font is not None:
        font.document().getMainWindow().getNSWindow().makeKeyAndOrderFront_(None)

'''
Keep hard links to open tool instances of type BaseTool in the TOOLS dictionary to avoid
opening multiple instances; key is toolId.

{toolId: toolInstance, ...}
'''
TOOLS = {}
DEBUG = False
# Calculate the root of tnTools in our application.
ROOT_TNTOOLS =  '/'.join(tnbits.__file__.split('/')[:-2]) + '/tntools'

class BaseTool(ToolBits, InterpolatorBits, PreferenceBits, ProgressBits, \
    UpdaterBits, BaseWindowController):
    """The BaseTool class combines functionality for all tools that want to be found
    by the fbProject."""
    C = Constants # Access to constants through self.C, allowing changes by inheriting classes.
    TOOLID = None # To be redefined by the inheriting tool class
    NAME = None # To be redefined by the inheriting class

    '''
    Default observers. Open and close callbacks are necessary for
    updateStyles() to work correctly. Optionally redefined by tool.
    Consists of tuples:

     (Callback, eventName)

    NOTE: callback name has to be different from event name.
    '''
    TOOLOBSERVERS = (
        ('_fontDidOpen', C.EVENT_FONTDIDOPEN),
        ('_fontDidClose', C.EVENT_FONTDIDCLOSE),
    )

    CATEGORY = '' # Inheriting classes should replace by original category label of this tool.
    ISBADGERTOOL = True # By default all tools go into the badger list, except badger itself.

    USEFLOATINGWINDOW = False # Force the use of floating tools, regardless of RF single window mode.
    WINDOWCLASS = ScreenWindow # In case in multiple window mode., unless redefined.
    FLOATINGWINDOWCLASS = FloatingScreenWindow # In case in single window mode.

    VIEWX = VIEWY = 50 # Default position of a new tool.
    VIEWWIDTH = 360 # Default tool width, unless redefined by inheriting class.
    VIEWHEIGHT = 100 # Default tool height, unless redefined by inheriting class.

    # Flag to indicate if multiple windows of the tool are allowed, e.g. per
    # style or family.  In that case the tool doesn't show in the badger
    # selection.
    ALLOWMULTIPLE = False

    '''
    Default model of the central set of preference values model for a tool.
    The preferences values dictionary is stored in the RoboFont preferences,
    under the tool ID. If it does not exist, it will be initialized from the
    PREFERENCE_MODEL dictionary. The one below offers default behavior.
    Inheriting tool classes are likely to redefine the content of the
    PREFERENCE_MODEL dictionary.

    self.preferences is queried by the central DisplayItems tool, to offer a
    generic interface to all preferences of a tool, including color selection.
    The DisplayItems tool tries to guess the type of UI required for a certain
    value, but the target value behavior can be redefined by implementing a
    method.
    '''
    PREFERENCE_MODEL = dict(
        # Label in RF preferences. Sort key is to define the automatic ordering
        # of groups of parameters.
        useFloatingWindow=dict(label=u'Tool as floating window', sort=100,
            type=C.PREFTYPE_BOOL, default=USEFLOATINGWINDOW),
        windowPosSize=dict(label=u'Window size', sort=110,
            type=C.PREFTYPE_RECT, default=(VIEWX, VIEWY, VIEWWIDTH,
                VIEWHEIGHT),
        allowMultiple=False),
    )

    def __init__(self, badger=None):
        self.windowClass = self.getWindowClass()
        self.badger = badger # Set a weak reference to badger. Can be None, as with the Badger tool itself.
        self._active = True # Boolean flag if the tool is active or not.
        self.w = None
        self.path = None # Can be filled by the project to know original source path.
        self.name = self.NAME or 'Untitled Tool'
        self._progress = None # Optional storage for progress bar when running.
        self._pendingUpdateData = {} # Request ids, connected to optional data to distract the rect from.
        self._pendingUpdates = []
        self._updating = False # We can reset, because we know that we started the update.

    def getRoot(self):
        """Answers the root *ROOT_TNTOOLS* as defined on initialization."""
        return ROOT_TNTOOLS

    def build(self):
        print('### Redefine the self.build method for inheriting tool classes.')

    def getWindowToFront(self):
        """Bring the window of this tool to front."""
        self.w.show()

    @classmethod
    def open(cls, toolID=None):
        """Open a new tool window of this class if it doesn't exist yet, or if
        multiple windows of the same tool are allowed. Optional custom tool ID to
        enable separate tools for multiple families."""
        if toolID is not None:
            cls.TOOLID = toolID

        try:
            tool = cls.getTool()
        except:
            print(traceback.format_exc())

        if tool.ALLOWMULTIPLE or not tool.isOpen():
            try:
                tool.build()
            except:
                print(traceback.format_exc())
        else:
            # Bring the existing tool window to the front.
            tool.getWindowToFront()

        return tool # Answer the new instance as convenience for the caller.

    @classmethod
    def addTool(cls, tool):
        """Add the `tool` to `TOOLS`."""
        if tool.__class__ == BaseTool:
            return

        toolID = tool.getId()

        if toolID is None:
            print('No tool ID for tool %s' % tool)
            return
        else:
            try:
                assert not toolID in TOOLS
            except Exception as e:
                print(e)
                print('%s already in TOOLS!' % toolID)
                return

            TOOLS[toolID] = tool
            return tool

    @classmethod
    def getTool(cls):
        """Answer the tool of `cls`. If it does not exist, create an instance first."""
        if not cls.exists():
            return cls.addTool(cls())

        return TOOLS[cls.getId()]

    @classmethod
    def getToolById(cls, toolId):
        """Answer the tool instance indicated by `toolId`. If the tool does not exist,
        or the weakref is dead, then answer `None`."""
        return TOOLS.get(toolId)

    @classmethod
    def exists(cls):
        """Answer is an instance of the `cls` tool already exists."""
        return cls.getId() in TOOLS

    @classmethod
    def getTools(cls):
        """Answer the dictionary with tools that are not dead. Clean up `TOOLS`
        during iteration."""
        return TOOLS

    @classmethod
    def getId(cls):
        """Unique tool id. Must be refined by inheriting class. Otherwise None,
        to prevent base tool classes to add themselves."""
        return cls.TOOLID

    @classmethod
    def getName(cls):
        """Answer the tool name, as defined by the inheriting class."""
        return cls.NAME

    @classmethod
    def screenConfiguration(cls):
        """Answers the `ScreenConfiguration` instance for the current
        composition of screens. Note that this instance is dynamically
        generated, always representing the current screen composition. This
        means that if the screen change while RoboFont is open, then the window
        positions are saved in the preferences under the new configuration
        ID."""
        return ScreenConfiguration()

    def getTitle(self, family):
        """Returns window title that displays family name and number of
        styles."""
        return '%s - %s (%d styles)' % (self.NAME, family.name, len(family.getStyleKeys()))

    def isOpen(self):
        """Answers if the tool has an open window."""
        return self.w is not None

    def isActive(self):
        """Answers if the tool is currently active and has an open window,"""
        return self._active and self.isOpen()

    def activate(self, active=True):
        self._active = active

    #   W I N D O W  S T U F F

    def getWindowClass(self):
        """Answers the class for the tool windows, depending on the settings of
        the preference."""
        try:
            if self.getPreference(self.C.PREF_FLOATINGWINDOW):
                return self.FLOATINGWINDOWCLASS
        except:
            return self.WINDOWCLASS

        return self.WINDOWCLASS

    def getView(self):
        """Assume for now that we have one window per tool."""
        return self.w

    getWindow = getView

    def hide(self):
        """Hides the window(s) of the tools if they exist."""
        if self.isActive():
            self.w.hide()
        self.activate(False)

    def show(self):
        """Show the window(s) of the tool. If there are no open window yet, then
        call *self.build* to open the window."""
        if not self.isActive():
            self.build()
        else:
            self.w.show()
        self.activate()

    def openWindow(self):
        self.setUpBaseWindowBehavior()
        self.addObservers()
        self.w.bind('move', self.toolWindowMoved) # Store the position in tool preferences
        self.w.bind('resize', self.toolWindowResized) # Store the position in tool preferences
        self.w.open()
        self.activate() # Mark that the tool is active, when the window open.

    def windowCloseCallback(self, sender):
        BaseWindowController.windowCloseCallback(self, sender)
        if self.w is not None:
            self.w.unbind('move', self.toolWindowMoved)
            self.w.unbind('resize', self.toolWindowResized)
        self.w = None
        self.activate(False)
        self.terminate()

    def getWindowTitle(self):
        """Answer the title of the window, as @self.NAME@."""
        return self.NAME

    def __del__(self):
        """Make sure all observers are released and the window is closed by calling @self.terminate()@."""
        self.terminate()

    def terminate(self):
        """Gets called by the project manager, if the tool is deleted. To be redefined by
        inheriting classes. The default behavior is to close the window, if it exists."""
        # Still exists in the tools? Delete self from the tools set.
        self.removeObservers()
        toolId = self.getId()

        if toolId in TOOLS:
            del TOOLS[toolId]

        badger = self.badger # Is there an overall badger tool (to select categories, etc.)

        if badger is not None: # Then make sure to notify it that we are terminating.
            badger.toolIsTerminating(self)

        if hasattr(self, 'w') and self.w is not None: # Make sure it is closed.
            self.w.close()
            self.w = None # Avoid duplicate closing on termination

    # ---------------------------------------------------------------------------------------------------------
    #   E V E N T / N O T I F I C A T I O N  O B S E R V E R S

    def getCurrentStyle(self):
        from mojo.roboFont import CurrentFont
        try:
            return CurrentFont()
        except NotImplementedError:
            return None

    getCurrentFont = getCurrentStyle

    def currentGlyphChanged(self, event):
        """Gets called if the tool sets the tool observer

        @('currentGlyphChanged', C.EVENT_CURRENTGLYPHCHANGED),@

        DO NOT REDEFINE IN INHERITING CLASS, or otherwise add the line below to
        remove/add the glyph observers."""
        # Default behavior of this is to add an observer for "glyphChanged", which is called if
        # the outline or the width of the glyph changed in the editor.
        self.setCurrentGlyphObserver(event['glyph'])

    def setCurrentGlyphObserver(self, glyph=None):
        """This method is a construction to remove the "Glyph.Changed"
        and "Glyph.WidthChanged" observers from the current "self._glyph"
        (if it is set) and then set observers on the new current glyph
        (if it exists). If there is no current glyph, then @self._glyph"
        is set to @None@."""
        # TODO: This needs to be fixed in a more generalized way. Not store current glyph
        # TODO: and get it from the event?

        if not hasattr(self, '_glyph'):  # Make sure it exists
            self._glyph = None
        '''
        # FIXME: doesn't exist (yet) in floqmodel4.
        if self._glyph is not None:
            self._glyph.removeObserver(self, "Glyph.Changed")
            self._glyph.removeObserver(self, "Glyph.WidthChanged")
        '''
        if glyph is None:
            glyph = self.getCurrentGlyph()
        self._glyph = glyph

        if self._glyph is not None:
            try:
                # Due to (yet) unknown bug, it happens that observers are added multiple times.
                # For now, just catch the exception and ignore.
                self._glyph.addObserver(self, "glyphChanged", "Glyph.Changed")
                self._glyph.addObserver(self, "glyphChanged", "Glyph.WidthChanged")
            except:
                pass
                # print('[### ERROR glyphbits.setCurrentGlyphObserver] Cannot add observer "Glyph.Changed"')

    def glyphChanged(self, event):
        """Adds notification to the current glyph, so we know when it changes.
        This method gets called if points or width of the current glyph have
        changed, and if the tool has set

        @('currentGlyphChanged', C.EVENT_CURRENTGLYPHCHANGED),@

        This method should be redefined by inheriting tool classes. Default
        behavior is to do nothing.
        """
        if DEBUG: print('''[%s] Implement self.glyphChanged(event) to see changes in glyph outline or width. This message should never happen.''' % self.getId())

    @classmethod
    def getCurrentGlyph(cls):
        """Gets the current glyph in the front RF editor window."""
        from mojo.roboFont import CurrentGlyph
        try:
            return CurrentGlyph()
        except NotImplementedError:
            return None

    @classmethod
    def isCurrentGlyph(cls, glyph):
        """
        Tests if the parameter glyph and the currently selected one are the same.
        """
        current = cls.getCurrentGlyph()
        return bool(glyph is not None and current is not None and glyph._object is current._object)

    # ---------------------------------------------------------------------------------------------------------
    #   E V E N T  S T U F F

    def isShiftKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        return modifiers & NSShiftKeyMask

    def isOptionKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        #commandDown = modifiers & NSCommandKeyMask
        return modifiers & NSAlternateKeyMask

    def isCommandKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        return  modifiers & NSCommandKeyMask

    def isDoubleClickEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        return event.clickCount() == 2

    def isMouseDownEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        return not event.type() in (NSLeftMouseUp, NSRightMouseUp)

    def isMouseDraggedEvent(self):
        """Answer if the mouse is currently dragging.
        If there is no event, then answer False."""
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        if event is None:
            return False
        return event.type() in (NSLeftMouseDragged, NSRightMouseDragged)

    def isCursorKeyEvent(self):
        """Answer if the current event was a cursor key. This
        way tools can decide not to update, as the change is minor there is a
        frequent call, such as dragging or cursor keys. Answer false if
        option+shift is down, because then it is better to update."""
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        #return not modifiers & NSShiftKeyMask and \
        return not modifiers & NSShiftKeyMask and \
            event.keyCode in (NSUpArrowFunctionKey, NSDownArrowFunctionKey,NSLeftArrowFunctionKey,NSRightArrowFunctionKey)

    # ---------------------------------------------------------------------------------------------------------
    #   S T Y L E

    @classmethod
    def updateStyles(cls):
        """Update the open family/styles, to match the naked fonts with what
        is already open in the model. If RF has another naked style,
        then change the reference of the model to the RF naked font."""
        model.updateStyles()

    def style2Front(self, style):
        """Make _font_ the front window and set to current font."""
        style.document().getMainWindow().getNSWindow().makeKeyAndOrderFront_(None)

    @classmethod
    def getAllStyles(cls):
        return AllFonts()

    @classmethod
    def getOpenStyleFromPath(cls, path):
        for font in cls.getAllStyles():
            if font.path == path:
                return font
        return None

    def updateRoboFont(self, style):
        """Update the style in RoboFont, if it is open."""
        roboFontFont = getRoboFontFont(style)
        if roboFontFont is not None:
            roboFontFont.update()

    def updateRoboFontGlyph(self, style, glyphName, layerName=None):
        """Update the RoboFont glyph, if it exists."""
        roboFontFont = getRoboFontFont(style)
        if roboFontFont is not None and glyphName in roboFontFont:
            glyph = roboFontFont[glyphName]
            if layerName is not None:
                glyph = glyph.getLayer(layerName)
            if glyph is not None:
                glyph.update()

    def saveRoboFont(self, style):
        """Save the style in RoboFont, if it is open, to avoid confusion of
        "saving by external application". """
        roboFontFont = getRoboFontFont(style)
        if roboFontFont is not None: # It is open in RoboFont. Let RF do the saving.
            roboFontFont.save()
        else: # Otherwise save the style directly.
            style.save()

    @classmethod
    def openRoboFontGlyphWindow(cls, style, glyphName):
        from mojo.UI import OpenGlyphWindow
        font = getRoboFontFont(style)
        if font is None:
            from fontParts.nonelab import RFont
            font = RFont(naked=style)
        if glyphName in font:
            return OpenGlyphWindow(font[glyphName])
        return None

    @classmethod
    def openRoboFontWindow(cls, style,):
        from mojo.UI import OpenFontWindow
        font = getRoboFontFont(style)
        if font is not None:
            style2Front(font)
        #elif font is not None and font.path:
        #    OpenFont(font.path) #  Open FontWindow if it does not exist of bring to front

    # ---------------------------------------------------------------------------------------------------------
    #     E V E N T / N O T I F I C A T I O N  O B S E R V E R S

    def addObservers(self):
        """The tool defines the observer it wants to have. Note that this is
        additional to the normal notifications, and observer is required to
        get notifications if the tool is not active."""
        for callbackName, eventName in self.getToolObservers():
            self.addObserver(self, callbackName, eventName)

    def _fontDidClose(self, sender):
        model.fontDidClose(sender)

    def _fontDidOpen(self, sender):
        model.fontDidOpen(sender)

    def _fontDidSave(self, sender):
        pass

    def addObserver(self, model, callbackName, eventName):
        """Add the observer."""
        addObserver(model, callbackName, eventName)

    def getToolObservers(self):
        """Answer the tool observers to be installed for this tool. Typically
        this is @self.TOOLOBSERVERS@."""
        if DEBUG: print(self.TOOLOBSERVERS)
        return self.TOOLOBSERVERS

    def removeObservers(self):
        """Remove all current observers for this tool."""
        for _, eventName in self.getToolObservers(): #  callbackName, eventName
            removeObserver(self, eventName)

    def preferencesChanged(self):
        """Get called by tools that changed the preferences of this tool (such
        as the DisplayItems.  To be redefined by tools who want to cache their
        preferences in local values."""
        pass
