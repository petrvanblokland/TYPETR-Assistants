
import vanilla
import merz
import weakref
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber

W, H = 600, 150
M = 32

WindowClass = vanilla.Window

class Assistant(Subscriber):

    NAME = 'Base Assistant'

    def __init__(self, glyphEditor):
        Subscriber.__init__(self, glyphEditor)

    def notImplementedKey(self, c):
        print('Not implemented yet', c)

    def keyDown(self, event):
        try:
            characters = event.characters()
        except (AttributeError, TypeError):
            return
        print('... Key:', characters)
        
    def build(self):
        
        w, h = W, H

        #self.mr = MerzRoot(glyph, w, h, fill=(0.9, 0.9, 0.9, 1))
        name = self.getName()
        self.w = WindowClass((w, h), name, minSize=(50, H))
        #self.w.t = CanvasGroup((0, 0, 0, 0), delegate=self)
        self.w.bind('resize', self.windowResized)
        self.w.bind('close', self.windowCloseCallback)

        # Open the window with the sample text pattern
        self.w.open()

    def windowCloseCallback(self, sender):
        """Window is closing, remove the observers"""
        self.destroy()

    def windowResized(self, w):
        """The window resized. Calculate a new Em scale factor, adjust the size of the canvas, 
        and update all Merz components to the new scale."""
        size = self.w._window.frame().size
        #self.mr.w, self.mr.h = size.width, size.height
        #self.mr.updatePosSize() # Update position, size and scale for all child elements
        print('... Window size:', size)
        
    def getName(self):
        glyph = CurrentGlyph()
        if glyph is not None:
            return '%s %s' % (self.mr.glyph.font.info.familyName, self.mr.glyph.font.info.styleName)
        return self.NAME
 
if __name__ == '__main__':
    registerGlyphEditorSubscriber(Assistant)
          