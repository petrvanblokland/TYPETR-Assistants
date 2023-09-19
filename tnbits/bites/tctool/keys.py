# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    keys.py
#
KEY_SPACE = ' '
KEY_NEWLINE = '\n'
KEY_RETURN = '\r'

# Toggle force left of kerning pair under glyph name instead of group.
# Toggle force right of kerning pair under glyph name instead of group.
#KEY_SINGLEGLYPHKERNLEFT = '1'
#KEY_SINGLEGLYPHKERNRIGHT = '2'

# z: zoom in by factor 2. Z: zoom in by factor 10 OR cmd-Z = undo.
# x: zoom out by factor 2. X: zoom out by factor 10 OR cmd-X = cut.
KEY_ZOOMIN = 'zZ'
KEY_ZOOMOUT = 'xX'

KEY_FIND = 'fF'
# Show the labels with spacing and kerning values.
KEY_SHOWVALUES = 'nN'

# True: Edit spacing, stop kerning. False: Don't edit spacing.
# True: Edit kerning, stop spacing. False: Don't edit kerning.
KEY_EDITKERNING = 'kK'
KEY_EDITSPACING = 'sS'

# Execute cleanProfiles() to validate and clean the profiles, e.g. no double
# references.
KEY_CLEANPROFILES = 'qQ'

# Reflow the text, in case spacing is not reliable. OR cmd-R = redo.
#KEY_REFLOW = 'rR'

# Toggle lock/unlock to position accents according to anchor positions.
KEY_LOCKANCHOR = 'tT'

# "Y": all glyphs. "y": current glyph. Needs  shift key. Update the accent
# positions of a all glyphs in the style from anchors in base glyphs.
#KEY_UPDATEACCENT = 'yY'

# Clear the current profile and try to fit all glyph into existing profiles.
#KEY_REPROFILE = 'tT'

KEY_EQUALSPACING = '='

# u: decrease left margin by 5. U: decrease left margin by 1.
# i: increase left margin by 5. I: increase left margin by 1.
# o: decrease right margin by 5. O: decrease right margin by 1.
# p: increase right margin by 5. P: increase right margin by 1.
KEY_LEFTDEC = 'uU'
KEY_LEFTINC = 'iI'
KEY_RIGHTDEC = 'oO'
KEY_RIGHTINC = 'pP'

# h: decrease kerning by 5. H: decrease kerning by 1.
# j: increase kerning by 5. J: increase kerning by 1.
KEY_KERNDEC = 'hH'
KEY_KERNINC = 'jJ'

# c: increase leading by 1%. C: Increment leading by 10% OR cmd-C = copy.
# v: decrease leading by 1%, V: Decrement leading by 10% OR cmd-V = paste.
KEY_LEADINGINC = 'cC'
KEY_LEADINGDEC = 'vV'

# Show markers.
# Show kerning, otherwise just make lines from spacing.
# Toggle the showMissing checkbox.
# Toggle showing of metrics lines.
# Toggle showing of base markers.
KEY_SHOWMARKERS = 'wW'
KEY_SHOWKERNING = 'qQ'
KEY_SHOWMISSING = '?'
KEY_SHOWMETRICS = 'mM'
KEY_SHOWBASE = 'bB' # FIXME

'''
# Remove the current glyph from it's current left group.
KEY_REMOVEFROMLEFTGROUP = '('

# Remove the current glyph from it's current right group.
KEY_REMOVEFROMRIGHTGROUP = ')'

# Next proof.
KEY_PREVPROOF = 63276

# Previous proof.
KEY_NEXTPROOF = 63277

# Previous sample.
KEY_PREVPROOF_K = u'<'

# If there is paging in the sample, go to the previous page.
KEY_PREVPAGE_K = u'≤'

# Next sample.
KEY_NEXTPROOF_K = u'>'

# If there is paging in the sample, go to the next page.
KEY_NEXTPAGE_K = u'≥'
'''
