from AppKit import NSDocumentController
from lib.doodleDocument import CreateDoodleFont

def openUI(font):
    documentController = NSDocumentController.sharedDocumentController()

    document, error = document, error = documentController.makeUntitledDocumentOfType_error_("Unified Font Object", None)

    document.font = font
    document.font.disableNotifications()

    documentController.addDocument_(document)
    document.makeWindowControllers()
    document.showWindows()



myFont = CreateDoodleFont()


myFont.newGlyph("a")

pen = myFont["a"].getPen()

pen.moveTo((100, 100))
pen.lineTo((200, 100))
pen.lineTo((200, 200))
pen.lineTo((100, 200))
pen.closePath()

openUI(myFont)
