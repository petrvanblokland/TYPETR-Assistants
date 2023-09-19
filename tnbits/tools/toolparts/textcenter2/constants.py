
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    constants.py
#

from AppKit import NSUpArrowFunctionKey, NSDownArrowFunctionKey, \
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSColor,\
        NSBackspaceCharacter, NSDeleteFunctionKey, NSDeleteCharacter
from tnbits.tools.basetool import BaseTool
from tnbits.tools.toolparts.textcenter2.textsamples import PAGES
from tnbits.base.future import chr

# TODO: should be globals.

class Constants:
    C = BaseTool.C

    TOOLID = 'tnTextCenter2'
    NAME = 'Text Center 2'
    CATEGORY = C.CATEGORY_GENERALIZE

    USEFLOATINGWINDOW = False

    # 5 seconds for UI-mode elements to show.
    DISPLAY_TIME  = 5

    # Default window position.
    VIEWX = VIEWY = 50
    VIEWWIDTH = 600
    VIEWHEIGHT = 400
    VIEWMINSIZE = 200, 100
    VIEWMAXSIZE = 8000, 4000

    CHAR_SINGLEGLYPHKERNLEFT = '1' # Toggle force left of kerning pair under glyph name instead of group.
    CHAR_SINGLEGLYPHKERNRIGHT = '2' # Toggle force right of kerning pair under glyph name instead of group.
    #CHAR_CREATERIGHT = '1' # Create a new right group with the current glyph
    #CHAR_ADDRIGHT = '2' # Add the cyurent glyph to the right space group
    #CHAR_REMOVERIGHT = '3' # Remove the current glyph from the right space group
    #CHAR_CREATELEFT = '5' # Create a new left group with the current glyph
    #CHAR_ADDLEFT = '6' # Add the cyrrent glyph to the left space group
    #CHAR_REMOVELEFT = '7' # Remove the current glyph from the left space group

    CHAR_ZOOMIN = 'zZ' # z: zoom in by factor 2. Z: zoom in by factor 10 OR cmd-Z = undo
    CHAR_ZOOMOUT = 'xX' # x: zoom out by factor 2. X: zoom out by factor 10 OR cmd-X = cut
    CHAR_LEADINGINC = 'cC' # c: increment leading by 1%. C: Increment leading by 10% OR cmd-C = copy
    CHAR_LEADINGDEC = 'vV' # v: decrement leading by 1%, V: Decrement leading by 10% OR cmd-V = paste
    CHAR_METRICS = 'mM' # Toggle showing of metrics lines.
    CHAR_SHOWBASE = 'bB' # Toggle showing of base markers.
    CHAR_SHOWVALUES = 'nN' # Show the labels with spacing and kerning values.
    CHAR_EDITKERNING = 'kK' # True: Edit kerning, stop spacing. False: Don't edit kerning
    CHAR_EDITSPACING = 'sS' # True: Edit spacing, stop kerning. False: Don't edit spacing
    CHAR_CLEANPROFILES = 'qQ' # Execute cleanProfiles() to validate and clean the profiles, e.g. no double references.
    CHAR_REFLOW = 'rR' # Reflow the text, in case spacing is not reliable. OR cmd-R = redo
    CHAR_LOCKANCHOR = 'tT' # Toggle lock/unlock to position accents according to anchor positions.
    CHAR_UPDATEACCENT = 'yY' # "Y": all glyphs. "y": current glyph. Needs  shift key. Update the accent positions of a all glyphs in the style from anchors in base glyphs.
    #CHAR_REPROFILE = 'tT' # Clear the current profile and try to fit all glyph into existing profiles
    CHAR_LEFTDEC = 'uU' # u: decrement left margin by 5. U: decrement left margin by 1
    CHAR_LEFTINC = 'iI' # i: increment left margin by 5. I: increment left margin by 1
    CHAR_RIGHTDEC = 'oO' # o: decrement right margin by 5. O: decrement right margin by 1
    CHAR_RIGHTINC = 'pP' # p: increment right margin by 5. P: increment right margin by 1.
    CHAR_KERNDEC = 'hH' # h: decrement kerning by 5. H: decrement kerning by 1
    CHAR_KERNINC = 'jJ' # j: increment kerning by 5. J: increment kerning by 1
    CHAR_SHOWMARKERS = 'wW' # Show markers
    CHAR_SHOWKERNING = 'qQ' # Show kerning, otherwise just make lines from spacing.
    CHAR_SHOWMISSING = '?' # Toggle the showMissing checkbox.
    CHAR_RECALCMARGINS = '=' # Recalculate the margins, based on if the glyphs are part of a group and which is the base glyph.
    CHAR_REMOVEFROMLEFTGROUP = '(' # Remove the current glyph from it's current left group
    CHAR_REMOVEFROMRIGHTGROUP = ')' # Remove the current glyph from it's current right group
    CHAR_PREVPROOF = 63276 # Next proof
    CHAR_NEXTPROOF = 63277 # Previous proof
    CHAR_PREVPROOF_K = u'<' # Previous sample.
    CHAR_PREVPAGE_K = u'≤' # If there is paging in the sample, go to the previous page.
    CHAR_NEXTPROOF_K = u'>' # Next sample.
    CHAR_NEXTPAGE_K = u'≥' # If there is paging in the sample, go to the next page.

    ARROWCHARACTERS = [
        NSUpArrowFunctionKey,
        NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey,
        NSRightArrowFunctionKey
    ]
    DELETECHARACTERS = [
        NSBackspaceCharacter,
        NSDeleteFunctionKey,
        NSDeleteCharacter,
        chr(0x007F),
    ]
    PPEM_MIN = 6
    PPEM_MAX = 400
    PPEM_DEFAULT = 100
    LEADING_DEFAULT = 110

    M = 36 # Page margin in the canvas.

    FUN_LEFTRIGHT = 'leftright'
    FUN_RIGHTLEFT = 'rightleft'
    FUN_LEFT = 'left'
    FUN_RIGHT = 'right'
    FUN_CENTER = 'center'
    FUN_WIDTH = 'width'

    LABEL_EXISTS = u'•'
    LABEL_CHR = 'Ch'
    LABEL_NAME = 'Name'
    LABEL_HEX = '#'

    RIGHTARROW = u'→'

    METRICSW = 300 # Minimal width of metrics info area.
    METRICSH = 180 # Height of metrics info area.
    LABEL_SIZE = 11 # Point size of metrics value labels.
    KEY_SIZE = 12

    REDCOLOR = NSColor.redColor() # Color indicator for kerning
    BLACKCOLOR = NSColor.blackColor() # Key indicator
    WHITECOLOR = NSColor.whiteColor() # Key indicator
    DARKGREENCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0.5, 0, 1)
    DARKBLUECOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0.7, 1)
    BASEMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.3, 0.3, 0.3, 0.9)
    METRICSBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.7, 0.7, 0.7, 0.7)
    SPACINGBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.8, 0.8, 0.9, 0.9)
    KERNINGBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.9, 0.8, 0.8, 0.9)
    MISSINGGLYPHMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.5, 0.6, 0.9, 0.8)
    LOCKMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1)

    EDIT_MODES = {0:'spacing', 1:'kerning'} # Order fits radio buttons in GUI

    # SmartSet glyph sets and other standard sample page content.
    PROOFPAGES = [] # SmartSet names for popup
    PROOFPAGENAMES = [] # Construct small set from glyph names. None means all glyphs.
    for name, t in PAGES:
        PROOFPAGENAMES.append(name)
        PROOFPAGES.append(t)

    WILDCARDS = ('', 'acute','grave','hungarumlaut','macron','tilde','breve','ogonek',
        'circumflex','dieresis','caron','dotaccent','dot','slash','ring','cedilla','bar',
        'commaaccent', 'tonos', 'dieresistonos', 'commaturnedabove', 'cyrillicbreve',
        'brevecyrillic', 'kreska', 'ringacute',
         )

    UPDATE_WINDOWTITLE = 'windowTitle'
    UPDATE_SPACEGROUPS = 'spaceGroups'
    UPDATE_STYLELIST = 'styleList'
    UPDATE_KERNINGGROUPS = 'kerningGroups'
    UPDATE_MARGINS = 'margins' # Update the margins of all glyphs from groups and base glyph in the groups.
    UPDATE_TEXT = 'text'
    UPDATE_TEXTHEIGHT = 'textHeight' # In case leading changed, we just need to recalculate the height of the canvas.
    UPDATE_LINE = 'line' # Update the current line only.
    UPDATE_LINES = 'lines' # Update the spacing of all lines, not the content of the items.
    UPDATE_TOGGLELOCKANCHOR = 'toggleLockAnchor'
    UPDATE_ACCENTPOSITIONS = 'updateAccentsFromBase'
    UPDATE_ACCENTSTYLEPOSITIONS = 'updateStyleAccentsFromBase' # Update entire style for accent positions.

    UPDATERS = (
        # Update action name,   method name.
        (UPDATE_WINDOWTITLE, 'updateWindowTitle'),
        (UPDATE_STYLELIST, 'updateStyleList'),
        (UPDATE_SPACEGROUPS, 'updateSpaceGroups'),
        (UPDATE_KERNINGGROUPS, 'updateKerningGroups'),
        (UPDATE_MARGINS, 'updateMarginGroups'),
        (UPDATE_TEXT, 'updateText'),
        (UPDATE_TEXTHEIGHT, 'updateTextHeight'),
        (UPDATE_LINE, 'updateLine'),
        (UPDATE_LINES, 'updateLines'),
        (UPDATE_TOGGLELOCKANCHOR, 'updateToggleLockAnchor'),
        (UPDATE_ACCENTPOSITIONS, 'updateAccents'),
        (UPDATE_ACCENTSTYLEPOSITIONS, 'updateStyleAccents'),
    )

    # Same key compatible with accentBuilder tool.
    EXTKEY = "com.typenetwork.accentbuilder"
    EXTKEY_LOCK = "%s.locked" % EXTKEY

    # Batch tasks

    T_SPACING = 'Spacing'
    T_KERNING = 'Kerning'
    T_EXPORT = 'Export'

    TASKS = (
        T_SPACING, T_KERNING, T_EXPORT
    )

    PREFERENCE_MODEL = dict(
        # Dimensioneer doesn't have a window on it's own. Use the DisplayItems
        # tools to set the preferences. Label in RF preferences. Sort key is
        # to define the automatic ordering of groups of parameters. Drawing
        # switches.
        metricsColor=dict(label=u'Metrics color', sort=10, type=C.PREFTYPE_COLOR, default=(0.6, 0.6, 0.6, 1)),
        labelColor=dict(label=u'Labels color', sort=20, type=C.PREFTYPE_COLOR, default=(0.1, 0.1, 0.1, 1)),
        textColor=dict(label=u'Text color', sort=30, type=C.PREFTYPE_COLOR, default=(0, 0, 0, 1)),
        selectedGlyphColor=dict(label=u'Hover glyph color', sort=50, type=C.PREFTYPE_COLOR, default=(0.8, 0, 0, 1)),
        nonExistingGlyphColor=dict(label=u'Non-existing glyph color', sort=60, type=C.PREFTYPE_COLOR, default=(0, 0.8, 0, 1)),
        canvasColor=dict(label=u'Canvas color', sort=70, type=C.PREFTYPE_COLOR, default=(1, 1, 1, 1)),

        #saveKerning=dict(label=u'Save kerning', sort=100, type=C.PREFTYPE_BOOL, default=True), # If set, save the envelop kerning into the self._style.kernings.
        #kernByEnvelop=dict(label=u'Kerning by envelop', sort=110, type=C.PREFTYPE_BOOL, default=True), # If set, get kerning from touching envelops.
        #drawEnvelop=dict(label=u'Draw kerning envelop', sort=120, type=C.PREFTYPE_BOOL, default=True), # If set draw the kerning envelop.
        #envelopColor=dict(label=u'Kerning envelop color', sort=130, type=C.PREFTYPE_COLOR, default=(.5, 0, .5, .2)),
        #drawMarginProfiles=dict(label=u'Draw margin profile bars', sort=140, type=C.PREFTYPE_BOOL, default=False), # If set draw margin profile bars.
        #drawGaussProfiles=dict(label=u'Draw Gauss profile pixels', sort=140, type=C.PREFTYPE_BOOL, default=True), # If set draw margin profile Gauss pixels.
        #marginProfileColor=dict(label=u'Margin profile color', sort=150, type=C.PREFTYPE_COLOR, default=(1, 0, .5, .5)),
        #profileTolerance=dict(label=u'Profile group tolerance', sort=160, type=C.PREFTYPE_INT, default=30), # Tolerance for profile to compare if glyph in same group
        #xHeightProfileSteps=dict(label=u'xHeight profile steps', sort=170, type=C.PREFTYPE_INT, default=32), # Number or steps/scanbars on xHeight for a profile.

        # Install plugins
        #installEnvelopEditor=dict(label=u'Install EnvelopEditor', sort=300, type=C.PREFTYPE_BOOL, default=True),
        # Window stuff
        useFloatingWindow=dict(label=u'Tool as floating window', sort=400, type=C.PREFTYPE_BOOL, default=USEFLOATINGWINDOW),
        windowPosSize=dict(label=u'Window size', sort=410, type=C.PREFTYPE_RECT, default=(VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)),
    )

    # Flag to indicate if multiple windows of the tool are allowed, e.g. per
    # style or family. In that case the tool doesn't show in the badger
    # selection.
    ALLOWMULTIPLE = True

    TOOLOBSERVERS = (
        # Callback, eventName
        ('drawProfiles', C.EVENT_DRAWBACKGROUND),
        # Detect changes in the glyph and font master selection
        ('currentGlyphChanged', C.EVENT_CURRENTGLYPHCHANGED), # Implement as self.glyphChanged(event)
        ('fontIsClosing', C.EVENT_FONTWILLCLOSE),
        ('fontWillSave', C.EVENT_FONTWILLSAVE),
        ('viewChangedGlyph', C.EVENT_VIEWDIDCHANGEGLYPH),
        ('currentFontChanged', C.EVENT_CURRENTFONTCHANGED),
        ('featuresChanged', C.EVENT_FEATURESCHANGED),
    )
