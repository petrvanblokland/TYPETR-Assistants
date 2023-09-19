# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    crossbrowsertesting.py
#
#    http://crossbrowsertesting.com/apidocs/v2
#
#    Requires: http://code.google.com/p/httplib2/
#

import httplib2
import json

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.storage.state import State

class Browser(State):
    pass

class CrossBrowserTesting(object):
    """

    The `CrossBrowserTesting` class uploads a TTF font and gets the images
    downloaded of the font samples, using http://crossbrowsertesting.com.

    """
    @classmethod
    def getBrowsers(cls):
        # Answer a dictionary or supported browsers
        url = 'http://crossbrowsertesting.com/api/v2/screenshots/browsers?format=json'
        resp, content = httplib2.Http().request(url)
        browsers = {}
        for browserdata in json.loads(content)['response']['oss']:
            browser = Browser.fromDict(browserdata)
            print(browser.name, browser)
        return browsers

    @classmethod
    def getScreen(cls):
        pass

if __name__ == "__main__":
    # Test imports
    cbt = CrossBrowserTesting
    for key, item in cbt.getBrowsers().items():
        print(key)
        print(item.keys())
        print(item['message'])
        print(item['oss'])
        print(item['error'])

