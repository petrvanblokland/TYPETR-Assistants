# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     localproof.py
#
DEBUG = False

import os
import httplib
import socket
from urllib import urlencode

from tnbits.constants import Constants
C = Constants
from tnbits.toolbox.transformer import TX
from tnbits.proofing import webproof

class WebProof(object):
    u"""
    <doc>The <code>WebProof</code> class implements the generation, uploading and proofing of webfonts. If <code>
    self.error</code> is not <code>None</code> then there was an error connecting.

    http://webtype.chrissam42.com:8013/testfont

    Send a POST with the form variables encoded like the form on that page. The upload file is a TTF and will get
    converted to EOT and WOFF for the specimen. You can use the default specimen or provide your own. If there is an
    error, it will return HTTP 400 and the error will be in the X-Content header. On success, it will HTTP 302 redirect
    you to the specimen URL. This uses temporary files, so the results will only be guaranteed to be good as long as the
    files exist. This should be hours or days, so it should be fine. When you are done, you can request

    http://webtype.chrissam42.com:8013/testfont/delete-XXXXXXXX

    using the "token" from the specimen URL, and it will delete the temporary files.</doc>
    """
    HOST = 'webtype.chrissam42.com'
    PORT = 8013
    PATH = '/qa'

    TEMPLATE_GLYPHS = 'glyphs.html'
    TEMPLATE_INDEX = 'index.html'
    TEMPLATE_SIZEDCOLUMNS = 'sizedcolumns.html'
    TEMPLATE_DEFAULT = TEMPLATE_GLYPHS

    """HTML
    <form method="POST" action="/testfont" enctype="multipart/form-data"  accept-charset="utf-8">
    <p>Upload a TTF file, and we will create EOT and WOFF versions of it, then output an HTML template showing a
    specimen of the webfont in action. Optionally provide your own CSS and HTML below, otherwise we will use a default
    waterfall and paragraph setting.</p><label>Upload TTF:

    <input type="hidden" name="upload.testfont_filename" alt="+" />
    <input name="upload.testfont_data" onchange="this.form['upload.testfont_filename'].value=this.value;" type="file"
    size="36" alt="+" /></label>
    <label>Optional CSS for specimen template:<br /><textarea name="testcss"></textarea></label>
    <label>Optional HTML for specimen template: (will be wrapped in a container that sets the font-family automatically)
    <br/>

    <textarea name="testhtml"></textarea></label>
    <button type="submit">Submit</button>
    </form>
    """
    def __init__(self, html=None):
        self.error = None
        self.token = None
        self.setTemplateHtml(html)

    def getServerRoot(self):
        u"""
        <doc>Answer the standard path for the localroot of the web pages. If different, this method can be defined by
        the inheriting application class.</doc>
        """
        return C.PATH_SERVERROOT

    def setTemplateHtml(self, html=None, template=None):
        if html is None:
            # Get the template data
            templatepath = TX.module2Path(webproof) + '/templates/' +  (template or self.TEMPLATE_DEFAULT)
            f = open(templatepath, 'rb')
            self.html = f.read()
            f.close()
        else:
            self.html = html

    def getHtml(self, fontPath, fontface=None):
        html = self.html
        fontName = TX.path2Name(fontPath)
        PATTERNS = (
            ('title', 'FBFlight Preview'),
            ('fontname', fontName),
            ('fontface', fontface or ''),
        )
        for pattern, replace in PATTERNS:
            try:
                html = html.replace('{{' + pattern + '}}', replace)
            except UnicodeDecodeError:
                html = html.replace('{{' + pattern + '}}', '### Cannot replace %s' % pattern)
        return html

    def upload(self, fontPath):
        # Get the font data.
        fontfile = open(fontPath, 'rb')
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="upload.testfont_filename"')
        L.append('')
        L.append("testfont.ttf")
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="testhtml"')
        L.append('Content-Type: text/html; charset=utf-8')
        L.append('')
        L.append(self.getHtml(fontPath))
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="upload.testfont_data"; filename="testfont.ttf"')
        L.append('Content-Type: application/octet-stream')
        L.append('')
        L.append(fontfile.read())
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)

        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

        fontfile.close()

        headers = {
            'Content-type': content_type,
        }
        h = httplib.HTTPConnection(self.HOST, self.PORT)
        h.follow_redirects = False

        url = self.getUrl()
        h.request(url=url, method="POST", body=body, headers=headers)

        if self.error is None:
            response = h.getresponse()
            location = response.getheader("Location")
            print('%s %s' % (response, response.__dict__))
            print(location)
            if location is not None:
                self.token = location.split('-')[-1]
            print(response.getheader('X-Content'))
        return self.error is None # Success?

    def uploadS3(self, fontPath):
        # Upload to Amazon S3
        pass

    PATH_QA = '/qa/typenetwork'
    PATH_ROBOFLIGHT = '/fbflight' + PATH_QA

    def save(self, fontPath):
        u"""
        <doc>Will save to local host. The HOST, PORT and PATH get changed here. We just have to write the HTML file, as
        the font non-obfuscated TTF fonts (and EOT and WOFF) are assumed to be already there already. It just needs the
        proper URL inside the HTML page to find it with @font-face.</doc>
        """
        if fontPath is None:
            self.error = 'Undefined font path'
        else:
            self.setLocal()
            self.token = TX.path2Name(fontPath) + '.html'
            rootPath = self.getServerRoot() + self.PATH_QA + '/' + self.token[0].lower()
            try:
                os.makedirs(rootPath)
            except OSError:
                pass
            htmlPath = rootPath + '/token-' + self.token
            partName = '/'.join(fontPath.split('/')[-2:])
            partName = '.'.join(partName.split('.')[:-1])
            fontFace = """ --><style>
            @font-face {
                font-family: "TestFont";
                src: url("%(url)s.eot?#iefix") format("embedded-opentype"),
                url("%(url)s.woff") format("woff"),
                url("%(url)s.ttf") format("truetype");
                font-style: normal;
                font-weight: normal;
                }
            </style><!-- """ % {'url': '/fbflight/fonts/typenetwork/%s' % partName}
            f = open(htmlPath, 'wb')
            f.write(self.getHtml(fontPath, fontFace))
            f.close()
        return self.error is None

    def setLocal(self):
        # Bit of a hack, to set the parameters for saving to local file
        self.HOST = C.HOST # Set in local config.py that is not in git
        self.PORT = C.PORT
        self.PATH = self.PATH_ROBOFLIGHT

    def getHttpBaseUrl(self):
        url = 'http://%s' % C.HOST
        if C.PORT is not None:
            url += ':%s' % C.PORT
        return url

    def openBrowser(self, url=None):
        if url is None:
            url = self.getHttpBaseUrl() + self.PATH_ROBOFLIGHT + '/' + self.token[0].lower() + '/token-%s' % self.token
        os.system('open "%s"' % url)

    def getHtmlPaths(self, rootPath, paths=None):
        if paths is None:
            paths = []
        for path in os.listdir(rootPath):
            if path.startswith('.'):
                continue
            filePath = rootPath + '/' + path
            if os.path.isdir(filePath):
                self.getHtmlPaths(filePath, paths)
            else:
                paths.append(filePath)
        return paths

    def buildProofIndex(self):
        self.setLocal() # Bit of hack, change  later when index needs to be uploaded too.
        self.setTemplateHtml(template=self.TEMPLATE_INDEX) # Get the HTML template
        rootPath = self.getServerRoot() + self.PATH_QA
        htmlPath = rootPath + '/' + self.TEMPLATE_INDEX
        links = []
        for path in sorted(self.getHtmlPaths(rootPath)):
            path = '/fbflight' + path.replace(self.getServerRoot(), '')
            label = TX.path2Name(path).replace('token-', '').replace('.ttf.html', '')
            links.append('<a href="%s" target="specimen">%s</a><br/>' % (path, label))
        html = self.html.replace('{{indexlist}}', '\n'.join(links))
        f = open(htmlPath, 'wb')
        f.write(html)
        f.close()
        self.openBrowser(self.getHttpBaseUrl() + self.PATH_ROBOFLIGHT + '/' + self.TEMPLATE_INDEX)

if __name__ == "__main__":
    # Test imports
    wp = WebProof()
    fontPath = '/FontDevelopment/Monocode/2012-10-02/2012-10-05/FontSquirrel/webfontkit-20121007-151951/monocoderegular-webfont.ttf'
    wp.upload(fontPath)
    if wp.error is None:
        wp.openBrowser()
