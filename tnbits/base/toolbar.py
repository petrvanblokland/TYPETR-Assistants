# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    toolbar.py
#
class Toolbar(object):
    """Custom toolbar with buttons for most important functions.

    Available OSX wide icons are documented here:

    https://developer.apple.com/documentation/appkit/nsimage/image_template_constants
    """

    def __init__(self, controller, items=None):
        if not items:
            items = []
        controller.tool.w.addToolbar("Toolbar", toolbarItems=items)

