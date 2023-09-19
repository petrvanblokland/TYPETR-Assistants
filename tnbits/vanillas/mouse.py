# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

class Mouse(object):

    def __init__(self):
        self.p = None
        self.xy = None
        self.dragging = False
        self.modifiers = None

    def __repr__(self):
        return 'Mouse[%s %s %s %s]' % (self.p, self.xy, self.dragging, self.modifiers)
