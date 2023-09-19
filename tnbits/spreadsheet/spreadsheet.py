# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    spreadsheet.py
#

import traceback
from AppKit import NSColor, NSFont, NSFontAttributeName, NSBezierPath, \
    NSForegroundColorAttributeName, NSMakeRect, NSUpArrowFunctionKey, \
    NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSDownArrowFunctionKey, \
    NSCommandKeyMask, NSAlternateKeyMask, NSShiftKeyMask, NSAttributedString, \
    NSControlKeyMask, NSMakePoint
from vanilla import Group, ScrollView

from tnbits.spreadsheet.constants import *
from tnbits.spreadsheet.transformations import *
from tnbits.canvas.canvasview import *
from tnbits.spreadsheet.cell import Cell, EditCell
from tnbits.toolbox.transformer import TX
from  tnbits.base.debug import *
from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *
from tnbits.canvas.kit import CanvasKit
from tnbits.vanillas.contextmenu import ContextMenu

import logging
logger = logging.getLogger(__name__)

class Spreadsheet(Group):
    """Spreadsheet drawing to a canvas.

    TODO:

    * drag column width
    * copy / paste (blocks)
    * mouse drag selection
    * sorting
    """
    def __init__(self, parent, posSize=(0, 0, -0, -0), descriptions=None,
            data=None, menuItems=None, leading=None, textSize=None,
            titleSize=None, cellPadding=2, gridHorizontalLine=0.5,
            gridVerticalLine=0.5, minScale=0.25, maxScale=2.0, delegate=None,
            showRowIndex=True, showColumnTitles=True, backgroundColor=None,
            cellChangedCallback=None, singleClickCallback=None,
            doubleClickCallback=None, orderCallback=None, colors=None):
        """Canvas based spreadsheet."""
        super(Spreadsheet, self).__init__(posSize)
        self.parent = parent
        self.bounds = None
        self.upBounds = None
        self.numberOfRows = 0
        self.numberOfColumns = 0
        self.currentCell = None
        self.canvasSize = 1, 1
        self.origin_x = 0
        self.origin_y = 0
        self.width = 0
        self.originalWidth = 0
        self.minWidth = 0
        self.minHeight = 0
        self.menuIsOn = False
        self.currentMenuItem = None
        self.downMouse = None
        self.draggedMouse = None
        self.upMouse = None

        delegate = self.getDelegate(delegate)
        self.textSize = textSize or DEFAULT_TEXT_SIZE
        self.titleSize = titleSize or DEFAULT_TEXT_SIZE
        self.leading = leading or int(round(self.textSize * DEFAULT_LEADING_FACTOR))
        self.cellPadding = cellPadding
        self.minScale = minScale
        self.maxScale = maxScale
        self.showIndices = showRowIndex
        self.showColumnTitles = showColumnTitles
        self.gridHorizontalLine = gridHorizontalLine
        self.gridVerticalLine = gridVerticalLine
        self.backgroundColor = backgroundColor or lightestGreyColor
        self.menuItems = menuItems
        self.selectedCellX = None
        self.scale = INITIAL_SCALE
        self.cells = {}
        self.draggedY = None
        self.lastRow = 0
        self.lastCol = 0
        self.optionDown = False
        self.cellXValues = {}
        self.cellWidths = {}
        self.originalCellWidths = {}
        self.cellKeys = {}
        self.NSStrings = {}
        self.disabledNSStrings = {}
        self.empasizedNSStrings = {}
        self.selection = []
        self.kit = CanvasKit()
        self.setFontAttributes()
        self.setOrigin()
        self.setDescriptions(descriptions)
        #w, h = parent.getView().getNSView().frame().size
        #self.resizeColumns(w, h)
        self.cellChangedCallback = cellChangedCallback
        self.singleClickCallback = singleClickCallback
        self.doubleClickCallback = doubleClickCallback or self.doubleClickCallback
        self.orderCallback = orderCallback or self.orderCallback
        self.view = CanvasView(self.canvasSize, delegate,
                acceptsMouseMoved=True, liveResize=True)
        self.clipView = CanvasClipView(self)
        self.scrollView = ScrollView((0, 0, -0, -0), self.view,
                backgroundColor=self.backgroundColor, hasHorizontalScroller=True,
                hasVerticalScroller=True, autohidesScrollers=True,
                drawsBackground=True, clipView=self.clipView)
        self.setEditCell()
        self.set(data)

    def __setitem__(self, key, cell):
        """Loads cell data into cell representation matrix with (x, y) tuple
        as key."""
        assert isinstance(cell, Cell)
        x, y = key
        self.numberOfRows = max(self.numberOfRows, y + 1)
        self.numberOfColumns = max(self.numberOfColumns, x + 1)
        self.cells[key] = cell

        if x > self.lastCol:
            self.lastCol = x

        if y > self.lastRow:
            self.lastRow = y

    def __getitem__(self, key):
        return self.cells[key]

    def __iter__(self):
        return iter(self.cells.keys())

    def __len__(self):
        return len(self.cells.keys())

    def set(self, data):
        """Loads the data into cell representation matrix.

        TODO: compare data to keep identical objects?
        """
        if data is None:
            return

        self.reset()

        for y, row in enumerate(data):
            for x, value in enumerate(row):
                self[(x, y)] = value

        self.setCanvasSize()
        self.updateSelection()

    def reset(self):
        """Resets spreadsheet data."""
        self.numberOfRows = 0
        self.numberOfColumns = 0
        self.lastRow = 0
        self.lastCol = 0
        self.cells = {}

    def viewDidEndLiveResize(self):
        size = self.scrollView.getNSScrollView().contentSize()
        w, _ = size
        _, h = self.canvasSize
        #self.view.setSize(w, h)
        #self.canvasSize = w, h
        #self.resizeColumns(w, h)

    def resizeColumns(self, w, h):
        t = 0
        ratio = w / float(self.width)
        x = self.origin_x

        for i, width in self.originalCellWidths.items():
            self.cellXValues[i] = x
            width = width * ratio
            self.cellWidths[i] = width
            x += width

        self.width = x

    def setOrder(self):
        if self.orderCallback:
            order = []
            selectionYs = self.getSelectionYs()

            for cellY in range(0, self.numberOfRows):
                if cellY == self.draggedY:
                    for cellID in self.selection:
                        _, selectionY = cellID
                        order.append(selectionY)

                if not cellY in selectionYs:
                    if cellY <= self.draggedY:
                        order.append(cellY)
                    elif cellY >= self.draggedY:
                        order.append(cellY)

            if self.draggedY == self.numberOfRows:
                for cellID in self.selection:
                    _, selectionY = cellID
                    order.append(selectionY)

            self.draggedY = None
            self.orderCallback(order)

    def asRows(self):
        """Formats cells as dictionary of rows."""
        rows = {}

        for cellID, cell in self.cells.items():
            _, cellY = cellID

            if not cellY in rows:
                rows[cellY] = []

            rows[cellY].append(cell)

        return rows

    # Set.

    def setOrigin(self):
        """Sets the origin offsets in case the header and / or row indices are
        shown."""
        if self.showColumnTitles:
            self.origin_y = self.leading * self.scale
        if self.showIndices:
            self.origin_x = DEFAULT_TEXT_SIZE * 3 * self.scale

    def setDescriptions(self, descriptions):
        """Stores the header descriptions and derives initial dimensions and order."""

        # If missing or too small, get widths from titles.
        for d in descriptions:
            title = TX.asString(d['title'])
            nsTitle = NSAttributedString.alloc().initWithString_attributes_(title, self._attributesTitles)
            width, _ = nsTitle.size()
            width += 2 * PADDING

            if not 'width' in d or width > d['width']:
                d['width'] = width

        self.descriptions = descriptions
        self.order = [(lambda x: x['key'])(x) for x in self.descriptions]
        self.setCellDimensions()

    def setCellDimensions(self):
        """Puts cell x-values in dictionary for faster lookup."""
        x = self.origin_x

        for cellX, column in enumerate(self.descriptions):
            w = column["width"] * self.scale
            self.cellXValues[cellX] = x
            self.cellWidths[cellX] = w
            self.originalCellWidths[cellX] = w
            self.cellKeys[cellX] = column['key']
            x += w

        # TODO: same as canvasSize w?
        self.width = x
        self.originalWidth = x

    def setEditCell(self):
        """Editable cell to be moved to a cell position on enter."""
        self.editCell = EditCell((0, 0, 30, 20), "", callback=self.editCellCallback)
        self.editCell.editCellEnded = self.closeEditCell
        self.editCell.show(False)
        self.editCellIsVisible = False

    def setFontAttributes(self):
        """We don't need to cache this, only happens on scale change."""
        #FIXME: store different types of attributes in dictionary.
        self._attributesCell = {
            NSFontAttributeName: NSFont.systemFontOfSize_(self.textSize*self.scale),
            NSForegroundColorAttributeName: blackColor
        }

        self._attributesDisabledCell = {
            NSFontAttributeName: NSFont.systemFontOfSize_(self.textSize*self.scale),
            NSForegroundColorAttributeName: greyColor
        }

        self._attributesTitles = {
            NSFontAttributeName: NSFont.boldSystemFontOfSize_(self.titleSize*self.scale),
            NSForegroundColorAttributeName: greyColor
        }

    def updateSelection(self):
        """checks if selection cells still exist after data has been updated."""
        for cellID in self.selection:
            x, y = cellID
            if x > self.lastCol or y > self.lastRow:
                i = self.selection.index(cellID)
                del self.selection[i]
                #print('deleted (%d, %d)' % (x, y))

    # Get.

    def getDelegate(self, delegate):
        """Sets application delegate, default is self."""
        if delegate is None:
            delegate = self

        return delegate

    def getCanvasView(self):
        return self.view

    def getCellByEvent(self, event):
        """Transforms the mouse position to flipped and scroll position and
        calculates scaled clicked point, in column measures."""
        p = event2MousePoint(self.getCanvasView(), event)
        return self.getCellByPoint(p)

    def getCellByPoint(self, p):
        cx = 0

        for ix, value in sorted(self.cellXValues.items()):
            if p.x > value:
                cx = ix

        cy = scaledY2CellY(p.y, self.scale, self.origin_y, self.leading, self.numberOfRows)
        return cx, cy

    def getSelection(self):
        return sorted(self.selection)

    def getSelectionYs(self):
        """Returns selection cell y-values."""
        ys = []

        for cellID in self.selection:
            x, y = cellID

            if y not in ys:
                ys.append(y)

        return ys

    def getColumnKey(self, i):
        """Returns the ith key"""
        return self.order[i]

    def getColumnIndex(self, key):
        """Returns the index of a key."""
        assert key in self.order
        return self.order.index(key)

    def getColumnIDs(self, x):
        """Returns all cell identifiers for column x."""
        col = []
        y = 0

        while y <= self.lastRow:
            key = (x, y)
            col.append(key)
            y += 1

        return col

    def getRowIDs(self, y):
        """Returns all cell identifiers for row y."""
        row = []
        x = 0

        while x <= self.lastCol:
            key = (x, y)
            row.append(key)
            x += 1

        return row

    def getSelectionRectangle(self):
        """Floor / ceiling values for selection rectangle."""
        x0, y0 = self.downMouse
        w, h = self.canvasSize

        if x0 < self.origin_x:
            x0 = self.origin_x
        elif x0 > w:
            x0 = w

        if y0 < self.origin_y:
            y0 = self.origin_y
        elif y0 > h:
            y0 = h

        x1, y1 = self.draggedMouse

        if x1 < self.origin_x:
            x1 = self.origin_x
        elif x1 > w:
            x1 = w

        if y1 < self.origin_y:
            y1 = self.origin_y
        elif y1 > h:
            y1 = h

        x2 = x1 - x0
        y2 = y1 - y0

        return x0, y0, x2, y2

    def getNSString(self, value, disabled=False, emphasis=False):
        """Gets an NSString from cache."""
        if disabled:
            cache = self.disabledNSStrings
            attrs = self._attributesDisabledCell
        elif emphasis:
            cache = self.empasizedNSStrings
            attrs = self._attributesTitles
        else:
            cache = self.NSStrings
            attrs = self._attributesCell

        if not value in cache:
            # Double space to position.
            nsString = NSAttributedString.alloc().initWithString_attributes_(value, attrs)
            width, height = nsString.size()
            cache[value] = nsString, width, height
        else:
            nsString, width, height = cache[value]

        return nsString, width, height

    def getMaxCellX(self, mouse):
        """Gets maximum offset (in both directions) a cell `x`-value can
        become."""
        offset = 4 * PADDING * self.scale
        x0 = self.cellXValues[self.selectedCellX]
        w0 = self.cellWidths[self.selectedCellX - 1] - offset
        w1 = self.cellWidths[self.selectedCellX] - offset

        x1, _ = mouse

        if x1 > x0:
            if x1 - x0 > w1:
                x1 = x0 + w1
        elif x1 < x0:
            if x0 - x1 > w0:
                x1 = x0 - w0

        return x1

    # Set.

    def setCanvasSize(self):
        """Adjust canvas to follow the scrollview width and the y position for
        height should happen only when view is resized... with
        viewDidEndLiveResize."""
        # FIXME: change to clipview size if smaller.
        rowHeight = self.origin_y + self.numberOfRows * self.leading * self.scale

        if rowHeight > self.minHeight:
            h = rowHeight
        else:
            h = self.minHeight

        w = self.width
        self.view.setSize(w, h)
        self.canvasSize = w, h
        #print('Spreadsheet width is %d' % w)

    def setScale(self, scale):
        if scale < self.minScale:
            scale = self.minScale
        elif scale > self.maxScale:
            scale = self.maxScale

        self.scale = scale
        self.setOrigin()
        self.setCellDimensions()
        self.setCanvasSize()
        # TODO: scale menuPoint.
        self.clearCache()
        self.setFontAttributes()

    def clearCache(self):
        self.NSStrings = {}
        self.empasizedNSStrings = {}
        self.disabledNSStrings = {}

    # Has.

    def hasData(self):
        if self.numberOfRows == 0 or self.numberOfColumns == 0:
            return False

        return True

    # Update.

    def update(self):
        """Triggers update event(s) for the whole view. It is more efficient
        to use the self.updateRect(rect) if the change rectangle is known."""
        self.getCanvasView().setNeedsDisplay_(True)

    def updateRect(self, rect):
        """Triggers update event for this rect.
        NOTE: Doesn't need self.getCanvasView().setNeedsDisplay_(False)
        """
        x, y, w, h = rect

        try:
            self.getCanvasView().setNeedsDisplayInRect_(((x, y), (w, h)))
        except Exception as e:
            print(traceback.format_exc())

    # Selection.

    def select(self, cellID):
        """Keeps track of selected cells."""
        if cellID is None:
            return

        if not cellID in self.selection:
            self.selection.append(cellID)
            self.selection = sorted(self.selection)

    def deselect(self, cellID):
        """Keeps track of selected cellIDs."""
        if cellID is None:
            return

        if cellID in self.selection:
            self.selection.remove(cellID)

    def selectCellsByRectangle(self, p0, p1):
        if not p0 or not p1:
            return

        x, y = self.getCellByPoint(p0)
        xx, yy = self.getCellByPoint(p1)
        x0 = min(x, xx)
        x1 = max(x, xx)
        y0 = min(y, yy)
        y1 = max(y, yy)

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                self.select((x, y))

    def shiftSelect(self, cellID):
        """
        TODO: keep track of first shift position, use it as the base for
        selection rectangle.
        """
        if cellID is None:
            return

        self.select(cellID)
        min_x = min(self.selection, key=lambda x: x[0])[0]
        max_x = max(self.selection, key=lambda x: x[0])[0]
        min_y = min(self.selection, key=lambda x: x[1])[1]
        max_y = max(self.selection, key=lambda x: x[1])[1]

        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                cellID = (i, j)
                if not cellID in self.selection:
                    self.selection.append(cellID)

    def clearSelection(self):
        """Empties the selection list."""
        self.selection = []

    def selectColumnDivider(self, d=3):
        x, y = self.downMouse
        i = 0

        if y <= self.origin_y:
            for cellX, xCol in self.cellXValues.items():
                if i == 0:
                    i += 1
                    continue

                if xCol - d < int(x) < xCol + d:
                    self.selectedCellX = cellX
                    return True
        return False

    # Cells.

    def _openCell(self):
        cellX, _ = self.currentCell

        if self.descriptions[cellX].get('editable'):
            # FIXME: always succeeds? Open the EditText if editable field. No
            # update necessary, edit box is on top of canvas.
            self.openEditCell(self.currentCell)

    def doubleClickCallback(self, cell):
        self.openEditCell(self.currentCell)

    def orderCallback(self, order):
        logger.warning('Manual order not implement, please pass an orderCallback() function to the spreadsheet constructor.')

    def openEditCell(self, cell):
        """Opens a TextField above cell after edit command."""
        if cell is None:
            return

        cellX, cellY = cell

        if not self.descriptions[cellX].get('editable'):
            return

        column = self.descriptions[cellX]

        if 'editable' in column and column['editable'] is False:
            return

        scrollRect = self.scrollView.getNSScrollView().documentVisibleRect()
        scrollOrigin = scrollRect.origin
        x = self.cellXValues[cellX] - scrollOrigin.x
        y = cellY2ScaledY(cellY, self.scale, self.origin_y, self.leading) - scrollOrigin.y
        w = max(self.cellWidths[cellX] * self.scale, 40)
        h = max(self.leading * self.scale, 20)
        self.editCell.setPosSize((x, y, w, h))
        self.editCell.set(self.cells.get(cell, "").asString())
        self.editCell.show(True)
        self.editCell.getNSTextField().becomeFirstResponder()
        self.editCellIsVisible = True

    def editCellCallback(self, sender):
        """Processes cell contents during edit?"""
        #escapeKey = chr(53)
        pass

    def updateCellValue(self, cell, value):
        """Some preprocessing before writing the pyobjc Unicode string value
        to cell."""
        value = str(value)
        value = value.replace(',', '.')

        try:
            value = float(value)

            if value % 1 == 0:
                value = int(value)
        except:
            # It's a plain string.
            pass

        cell.value = value

    def closeEditCell(self):
        """Processes cell contents after edit, makes the spreadsheet canvas
        become first responder again."""
        # FIXME: current cell disappears after edit.
        # FIXME: check if edited text is a float.
        self.editCell.show(False)
        self.editCellIsVisible = False
        self.getCanvasView().window().makeFirstResponder_(self.getCanvasView())
        value = self.editCell.get()
        cell = self.cells[self.currentCell]
        self.updateCellValue(cell, value)

        if self.cellChangedCallback is not None:
            try:
                self.cellChangedCallback(cell)
            except:
                print(traceback.format_exc())

        # TODO: Should call update by changed rect
        self.update()

    # Drawing.

    def draw(self, rect):
        """Main drawing routine.

        NOTE: errors should be caught or else RoboFont will exit without a
        clear traceback.

        TODO: only update necessary rectangle.
        """
        try:
            self.drawDebug()
            self.drawRows(rect)
            self.drawSelection(rect)
            self.drawCurrentCell(rect)
            self.drawColumnTitles(rect)
            self.drawIndices(rect)
            self.drawCells(rect)
            self.drawGrid(rect)
            if self.downMouse and self.draggedMouse:
                if self.optionDown:
                    self.drawSorting(rect)
                else:
                    self.drawMarquee(rect)
        except Exception as e:
            print(traceback.format_exc())

    def drawDebug(self):
        if SHOWDRAWTILES:
            drawUpdateRect(rect)

    def drawRows(self, rect):
        """Draws background color for rows."""
        for cellY in range(0, self.numberOfRows + 1):
            sy = cellY2ScaledY(cellY, self.scale, 0, self.leading)

            if cellY % 2 == 1:
                fillColor = lightestGreyColor
            else:
                fillColor = whiteColor

            self.kit.drawRectangle(0, sy, self.width, self.leading * self.scale,
                    fillColor=fillColor, strokeColor=None)

    def drawCells(self, rect):
        """Draws the cell contents if they are inside the update rectangle.
        Cache the cell value as (NSString, width, height) for speed, not to
        recreated them in every update. If the scale changes, the
        self.NSStrings is cleared, so new titles will be cached."""
        (rx, ry), (rw, rh) = rect
        scaledLeading = self.leading / self.scale

        for cellID in self.cells:
            self.drawCell(cellID, scaledLeading, rx, ry, rw, rh)

    def drawCell(self, cellID, scaledLeading, rx, ry, rw, rh, offsetX=0, offsetY=0):
        cell = self[cellID]
        cellX, cellY = cellID
        x = self.cellXValues[cellX] + offsetX
        y = cellY2ScaledY(cellY, self.scale, self.origin_y, self.leading) + offsetY
        value = cell.asString()

        if y + scaledLeading < ry or y > ry + rh:
            return

        if cell.enabled:
            nsString, width, height = self.getNSString(value)
        else:
            nsString, width, height = self.getNSString(value, disabled=True)

        # Do right alignment for numbers.
        if isinstance(cell.value, (int, float)):
            w = self.cellWidths[cellX]
            x += (w - self.cellPadding) * self.scale - width

            if x < rx:
                return
        else:
            x += self.cellPadding * self.scale

            if x + width > rx + rw:
                return

        nsString.drawInRect_(NSMakeRect(x, y, width, height))

    def drawCurrentCell(self, rect):
        if not self.hasData():
            return

        if self.currentCell is not None:
            if self.currentCell not in self.selection:
                lightGreenColor.set()
            else:
                UILightBlue.set()
            cellX, cellY = self.currentCell

            if not (cellX is None or cellY is None):
                x = self.cellXValues[cellX]
                y = cellY2ScaledY(cellY, self.scale, self.origin_y, self.leading)
                w = self.cellWidths[cellX]
                h = self.leading * self.scale
                path = NSBezierPath.bezierPathWithRect_(((x, y), (w, h)))
                path.fill()

    def drawSelection(self, rect):
        """Shows selected cells.

        TODO: test on visibility in rectangle.
        """
        if not self.hasData():
            return

        for cellX, cellY in self.selection:
            x = self.cellXValues[cellX]
            #y = cellY * self.leading * self.scale
            if cellY % 2 == 1:
                lightOrangeColor.set()
            else:
                yellowColor.set()
            y = cellY2ScaledY(cellY, self.scale, self.origin_y, self.leading)
            w = self.cellWidths[cellX] * self.scale
            h = self.leading * self.scale
            path = NSBezierPath.bezierPathWithRect_(((x, y), (w, h)))
            path.fill()

    def drawIndices(self, rect):
        """Draws numbers before rows. Keeps them in a dictionary for faster
        lookup (separate from regular dictionary because atrributes differ)."""
        if not self.showIndices:
            return
        elif not self.hasData():
            return

        (rx, ry), (rw, rh) = rect
        sl = self.leading * self.scale

        for cellY in range(0, self.lastRow + 1):
            value = str(cellY + 1)
            nsString, width, height = self.getNSString(value, emphasis=True)

            # We need to draw this row cellY index, because it is inside the
            # update area. Right aligns the number.
            r = NSMakeRect(self.origin_x - width - 3 * self.scale,
                cellY * sl + self.origin_y, width, height)
            nsString.drawInRect_(r)

    def drawColumnTitles(self, rect):
        """Draws the titles of the columns, if they are inside the update
        rectangle.  Caches the title as (NSString, width, height) so they
        don't have to be recreated for every update. If the scale changes, the
        self.NSStrings is cleared, so new titles will be cached."""
        if not self.showColumnTitles:
            return

        greyColor.set()
        (rx, ry), (rw, rh) = rect

        for cellX, column in enumerate(self.descriptions):
            x = self.cellXValues[cellX]
            y = 0
            title = TX.asString(column["title"])
            nsString, width, height = self.getNSString(title, emphasis=True)

            if x + width < rx:
                continue

            if x > rx + rw:
                break

            nsString.drawInRect_(NSMakeRect(x + 2, y, width, height))

    def drawGrid(self, rect):
        """Draws the cell grid."""
        (rx, ry), (rw, rh) = rect
        greyColor.set()

        for cellY in range(0, self.numberOfRows):
            self.drawHorizontalGridLine(cellY)

        for cellX, x in self.cellXValues.items():
            highlighted = False

            if cellX == self.selectedCellX:
                highlighted = True

            self.drawVerticalGridLine(x, highlighted=highlighted)

    def drawHorizontalGridLine(self, cellY, highlighted=False):
        width = self.gridHorizontalLine * self.scale
        color = greyColor
        y = cellY2ScaledY(cellY, self.scale, self.origin_y, self.leading)
        w, _ = self.canvasSize

        if highlighted:
            color = magentaColor

        p0 = (0, y)
        p1 = (w, y)
        self.kit.drawLine(p0, p1, color=color, width=width)

    def drawVerticalGridLine(self, x, highlighted=False):
        width = self.gridVerticalLine * self.scale
        color = greyColor
        _, h = self.canvasSize

        if highlighted:
            color = magentaColor

        p0 = (x, 0)
        p1 = (x, h)
        self.kit.drawLine(p0, p1, color=color, width=width)

    def drawSorting(self, rect):
        dx = self.draggedMouse.x - self.downMouse.x
        dy = self.draggedMouse.y - self.downMouse.y
        (rx, ry), (rw, rh) = rect
        scaledLeading = self.leading / self.scale

        self.draggedY = scaledY2CellY(self.draggedMouse.y, self.scale, self.origin_y,
                self.leading, self.numberOfRows + 1)
        self.drawHorizontalGridLine(self.draggedY, highlighted=True)

        if self.selection:
            ys = self.getSelectionYs()

            for cellY in ys:
                rowIDs = self.getRowIDs(cellY)
                for cellID in rowIDs:
                    self.drawCell(cellID, scaledLeading, rx, ry, rw, rh, offsetY=dy)

        # TODO: highlight nearest horizontal line.

    def drawMarquee(self, rect):
        """Draws the visible representation of a dragged selection."""
        if not self.downMouse or not self.draggedMouse:
            return

        if self.selectedCellX:
            s = 3
            y = self.origin_y / 2
            x0 = self.cellXValues[self.selectedCellX]
            x1 = self.getMaxCellX(self.draggedMouse)
            p0 = (x0, y)
            p1 = (x1, y)
            #TODO: make a single kit.drawArrow.
            self.kit.drawLine(p0, p1, color=magentaColor)

            if abs(x0 - x1) > s:
                ay0 = y - s
                ay1 = y + s

                if x0 < x1:
                    ax = x1 - s
                elif x0 > x1:
                    ax = x1 + s

                ap0 = (ax, ay0)
                ap1 = (ax, ay1)
                self.kit.drawLine(ap0, p1, color=magentaColor)
                self.kit.drawLine(ap1, p1, color=magentaColor)

        else:
            x0, y0, x2, y2 = self.getSelectionRectangle()
            self.kit.drawRectangle(x0, y0, x2, y2, fillColor=None,
                    strokeColor=magentaColor)

    def resizeColumn(self):
        """Updates `x`-value of selected column divider as well as widths of
        columns on both sides."""
        x1 = self.getMaxCellX(self.upMouse)
        x0 = self.cellXValues[self.selectedCellX]
        self.cellXValues[self.selectedCellX] = x1
        diff = x1 - x0
        w = self.cellWidths[self.selectedCellX] - diff
        self.cellWidths[self.selectedCellX] = w
        w0 = self.cellWidths[self.selectedCellX - 1] + diff
        self.cellWidths[self.selectedCellX - 1] = w0
        self.selectedCellX = None

    # Conversions.

    def cell2Rect(self, cw, ch):
        """Answers the cell rectangle for the current cell position."""
        d = 10
        cx = self.currentCell[0]
        cy = self.currentCell[1]

        # Make sure that cellX is withing limits.
        cx1 = min(max(cx, 0), self.numberOfColumns - 1)

        # Clip the cellX + cellW to the number of cols.
        cx2 = min(cx1 + cw, self.numberOfColumns - 1)

        x = self.cellXValues[cx1] * self.scale
        w = self.cellXValues[cx2] * self.scale - x

        # Make sure that cellY is within limits.
        cy1 = min(max(cy, 0), self.numberOfRows)

        # Clip the cellY + cellH to the number of rows.
        cy2 = min(cy1 + ch, self.numberOfRows)
        y = self.origin_y + cy1 * self.leading * self.scale
        h = cy2 * self.leading * self.scale - y

        return x-d, y-d, w+2*d, h+2*d

    # First Responder.

    def becomeFirstResponder(self):
        pass

    def resignFirstResponder(self):
        pass


    # Menu.

    def menu(self, event):
        """Opens a menu on a cell."""

        if len(self.selection) < 2:
            p = event2MousePoint(self.getCanvasView(), event)
            self.clearSelection()
            self.currentCell = self.getCellByPoint(p)

        self.select(self.currentCell)
        self.update()
        contextMenu = ContextMenu(self.menuItems, self.getNSView(), self.parent)
        contextMenu.open(event)
        self.menuIsOn = True

    # Mouse.

    def rightMouseDown(self, event):
        pass

    def mouseDown(self, event):
        """Mouse down event was detected. Handle it, depending on modifier
        keys, current state of selection and clickCount."""
        self.downMouse = event2MousePoint(self.getCanvasView(), event)
        self.draggedMouse = None
        self.upMouse = None

        if not self.menuIsOn:
            self.handleMouse(event)

        self.update()

    def handleMouse(self, event):
        # TODO: find update rectangle for selection.
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        commandDown = modifiers & NSCommandKeyMask
        optionDown = modifiers & NSAlternateKeyMask
        clickCount = event.clickCount()

        if not self.hasData():
            return

        if clickCount == 1 and self.editCellIsVisible:
            self.closeEditCell()

        if not self.selectColumnDivider():
            p = self.getCellByEvent(event)
            self.currentCell = p

            if optionDown:
                self.optionDown = optionDown
                if len(self.selection) == 0:
                    self.clearSelection()
                    self.select(self.currentCell)
            else:
                #p = self.getCellByEvent(event)
                #self.currentCell = p

                if shiftDown:
                    self.shiftSelect(self.currentCell)
                elif commandDown:
                    if not self.currentCell in self.selection:
                        self.select(self.currentCell)
                    else:
                        self.deselect(self.currentCell)
                else:
                    # Click without modifiers clears selection and selects the
                    # current cell.
                    self.clearSelection()
                    self.select(self.currentCell)

                    if clickCount == 1:
                        if not self.singleClickCallback is None:
                            self.singleClickCallback(self.currentCell)

                    if clickCount == 2:
                        if not self.doubleClickCallback is None:
                            self.doubleClickCallback(self.currentCell)

    def mouseDragged(self, event):
        if not self.menuIsOn:
            self.draggedMouse = event2MousePoint(self.getCanvasView(), event)
            self.update()

    def mouseMoved(self, event):
        pass


    def mouseEntered(self, event):
        pass

    def mouseExited(self, event):
        if self.menuIsOn:
            self.menuIsOn = False
            self.update()

    def mouseUp(self, event):
        """Handles mouse up event.

        TODO: add cells to selection.
        """
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        commandDown = modifiers & NSCommandKeyMask
        self.upMouse = event2MousePoint(self.getCanvasView(), event)

        if self.selectedCellX:
            self.resizeColumn()
        elif self.optionDown:
            self.optionDown = False
            self.setOrder()
            self.clearSelection()
            self.currentCell = None
        elif not self.menuIsOn and not commandDown:
            self.selectCellsByRectangle(self.downMouse, self.draggedMouse)

        self.downMouse = None
        self.update()

    # Keys.

    def keyDown(self, event):
        # get the characters
        characters = event.characters()
        modifiers = event.modifierFlags()
        commandDown = modifiers & NSCommandKeyMask
        shiftDown = modifiers & NSShiftKeyMask
        optionDown = modifiers & NSAlternateKeyMask
        controlDown = modifiers & NSControlKeyMask
        self._lastKey = ''

        update = False
        updateRect = None

        #if shiftDown:
        #    stepX = 1 # Always 1

        if characters in "xX" or (commandDown and characters in '-'):
            self.setScale(self.scale / SCALEFACTOR)
        elif characters in "zZ" or (commandDown and characters in '='):
            self.setScale(self.scale * SCALEFACTOR)
        elif commandDown and characters in '0':
            self.setScale(INITIAL_SCALE)
        elif characters == NSUpArrowFunctionKey:
            updateRect = self.moveSelectionUp(shiftDown, commandDown)
        elif characters == NSLeftArrowFunctionKey:
            updateRect = self.moveSelectionLeft(shiftDown, commandDown)
        elif characters == NSRightArrowFunctionKey:
            updateRect = self.moveSelectionRight(shiftDown, commandDown)
        elif characters == NSDownArrowFunctionKey:
            updateRect = self.moveSelectionDown(shiftDown, commandDown)
        elif characters in ' \n\r':
            self.openEditCell(self.currentCell)

        #if updateRect:
        #    self.updateRect(updateRect)
        #elif update:
        self.update()

    def moveSelectionUp(self, shiftDown, commandDown):
        """Moves the cell selection the to cell above. Answers the update
        rectangle. Do not run over the edge of the spreadsheet canvas.  Answers
        None if nothing needs to be updated."""
        if self.currentCell is not None:
            if not shiftDown and not commandDown:
                self.clearSelection()

            cellX, cellY = self.currentCell

            if cellY > 0:
                upCellY = cellY - 1
                self.currentCell = cellX, upCellY

            if shiftDown:
                self.shiftSelect(self.currentCell)
            else:
                self.select(self.currentCell)

            return self.cell2Rect(1, 2)

    def moveSelectionDown(self, shiftDown, commandDown):
        """Moves the cell selection the to cell below. Answer the
        update rectangle. Do not run over the edge of the spreadsheet canvas.
        Answers None if nothing needs to be updated."""
        if self.currentCell is not None:
            if not shiftDown and not commandDown:
                self.clearSelection()

            cellX, cellY = self.currentCell

            if cellY < self.numberOfRows - 1:
                downCellY = cellY + 1
                self.currentCell = cellX, downCellY

            if shiftDown:
                self.shiftSelect(self.currentCell)
            else:
                self.select(self.currentCell)

            return self.cell2Rect(1, 2)

    def moveSelectionLeft(self, shiftDown, commandDown):
        """Moves the cell selection the to cell on the left. Answer the
        update rectangle. Do not run over the edge of the spreadsheet canvas.
        Answers None if nothing needs to be updated."""
        if self.currentCell is not None:
            if not shiftDown and not commandDown:
                self.clearSelection()

            cellX, cellY = self.currentCell

            if cellX > 0:
                leftCellX = cellX - 1
                self.currentCell = leftCellX, cellY

            if shiftDown:
                self.shiftSelect(self.currentCell)
            else:
                self.select(self.currentCell)

            return self.cell2Rect(2, 1)


    def moveSelectionRight(self, shiftDown, commandDown):
        """Moves the cell selection the to cell on the right. Answer
        the update rectangle. Do not run over the edge of the spreadsheet
        canvas. Answer None if nothing needs to be updated."""
        if self.currentCell is not None:
            if not shiftDown and not commandDown:
                self.clearSelection()

            cellX, cellY = self.currentCell

            # Already at last column.
            if cellX < self.numberOfColumns - 1:
                rightCellX = cellX + 1
                self.currentCell = rightCellX, cellY

            if shiftDown:
                self.shiftSelect(self.currentCell)
            else:
                self.select(self.currentCell)

            return self.cell2Rect(2, 1)
