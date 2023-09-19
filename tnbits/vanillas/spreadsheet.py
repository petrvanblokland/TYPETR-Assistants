# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    spreadsheet.py
#
from objc import YES
from AppKit import (NSSize, NSRightTextAlignment, NSCenterTextAlignment,
    NSLeftTextAlignment)
from vanilla import List
from tnbits.tools.basetool import BaseTool
from tnbits.vanillas.window import ScreenWindow
from tnbits.vanillas.listcell import SmallRightAlignTextListCell

class Spreadsheet(List):
    """Implements spreadsheet behavior, using the standard *List* class. Much is
    possible, except easy adding of columns. So we initialize a lot and keep
    the, hidden. This allows to expand adding columns to that max amount.

    DEPRECATED. Too limited, see tnbits.spreadsheet for canvas based version.
    Keeping this for style reference.

    TableView
    https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/nstableview_Class/Reference/Reference.html

    Column
    https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSTableColumn_Class/Reference/Reference.html#//apple_ref/occ/instm/NSTableColumn/headerCell

    Creating Views to Display
    – makeViewWithIdentifier:owner:
    – rowViewAtRow:makeIfNecessary:
    – viewAtColumn:row:makeIfNecessary:
    Setting the Data Source
    – setDataSource:
    – dataSource
    Loading Data
    – reloadData
    – reloadDataForRowIndexes:columnIndexes:
    Using Views for Row and Column Content
    – beginUpdates
    – endUpdates
    – columnForView:
    – moveRowAtIndex:toIndex:
    – insertRowsAtIndexes:withAnimation:
    – removeRowsAtIndexes:withAnimation:
    – rowForView:
    NSView-based Table Nib Registration
    – registerNib:forIdentifier:
    – registeredNibsByIdentifier
    Target-action Behavior
    – setDoubleAction:
    – doubleAction
    – clickedColumn
    – clickedRow
    Configuring Behavior
    – setAllowsColumnReordering:
    – allowsColumnReordering
    – setAllowsColumnResizing:
    – allowsColumnResizing
    – setAllowsMultipleSelection:
    – allowsMultipleSelection
    – setAllowsEmptySelection:
    – allowsEmptySelection
    – setAllowsColumnSelection:
    – allowsColumnSelection
    Setting Display Attributes
    XXX setIntercellSpacing:
    – intercellSpacing
    – setRowHeight:
    – rowHeight
    – setBackgroundColor:
    – backgroundColor
    – setUsesAlternatingRowBackgroundColors:
    – usesAlternatingRowBackgroundColors
    – selectionHighlightStyle
    – setSelectionHighlightStyle:
    – setGridColor:
    – gridColor
    – setGridStyleMask:
    – gridStyleMask
    – indicatorImageInTableColumn:
    – setIndicatorImage:inTableColumn:
    Getting and Setting Row Size Styles
    – effectiveRowSizeStyle
    – rowSizeStyle
    – setRowSizeStyle:
    Column Management
    – addTableColumn:
    – removeTableColumn:
    – moveColumn:toColumn:
    – tableColumns
    – columnWithIdentifier:
    – tableColumnWithIdentifier:
    Selecting Columns and Rows
    – selectColumnIndexes:byExtendingSelection:
    – selectedColumn
    – selectedColumnIndexes
    – deselectColumn:
    – numberOfSelectedColumns
    – isColumnSelected:
    – selectRowIndexes:byExtendingSelection:
    – selectedRow
    – selectedRowIndexes
    – deselectRow:
    – numberOfSelectedRows
    – isRowSelected:
    – selectAll:
    – deselectAll:
    Enumerating Table Rows
    – enumerateAvailableRowViewsUsingBlock:
    Managing Type Select
    – allowsTypeSelect
    – setAllowsTypeSelect:
    Getting and Setting Column Focus
    – focusedColumn
    – setFocusedColumn:
    – shouldFocusCell:atColumn:row:
    Table Dimensions
    – numberOfColumns
    – numberOfRows
    Displaying Cell
    – preparedCellAtColumn:row:
    Getting and Setting Floating Rows
    – floatsGroupRows
    – setFloatsGroupRows:
    Editing Cells
    – editColumn:row:withEvent:select:
    – editedColumn
    – editedRow
    – performClickOnCellAtColumn:row:
    Adding and Deleting Row Views
    – didAddRowView:forRow:
    – didRemoveRowView:forRow:
    Setting Auxiliary Views
    – setHeaderView:
    – headerView
    – setCornerView:
    – cornerView
    Layout Support
    – rectOfColumn:
    – rectOfRow:
    – rowsInRect:
    – columnIndexesInRect:
    – columnAtPoint:
    – rowAtPoint:
    – frameOfCellAtColumn:row:
    – columnAutoresizingStyle
    – setColumnAutoresizingStyle:
    – sizeLastColumnToFit
    – noteNumberOfRowsChanged
    – tile
    – sizeToFit
    – noteHeightOfRowsWithIndexesChanged:
    – columnsInRect: Deprecated in OS X v10.5
    Drawing
    – drawRow:clipRect:
    – drawGridInClipRect:
    – highlightSelectionInClipRect:
    – drawBackgroundInClipRect:
    Scrolling
    – scrollRowToVisible:
    – scrollColumnToVisible:
    Table Column State Persistence
    – setAutosaveName:
    – autosaveName
    – setAutosaveTableColumns:
    – autosaveTableColumns
    Setting the Delegate
    – setDelegate:
    – delegate
    Highlightable Column Headers
    – highlightedTableColumn
    – setHighlightedTableColumn:
    Dragging
    – dragImageForRowsWithIndexes:tableColumns:event:offset:
    – canDragRowsWithIndexes:atPoint:
    – setDraggingSourceOperationMask:forLocal:
    – setVerticalMotionCanBeginDrag:
    – verticalMotionCanBeginDrag
    – draggingDestinationFeedbackStyle
    – setDraggingDestinationFeedbackStyle:
    – setDropRow:dropOperation:
    Sorting
    – setSortDescriptors:
    – sortDescriptors
    Text Delegate Methods
    – textShouldBeginEditing:
    – textDidBeginEditing:
    – textDidChange:
    – textShouldEndEditing:
    – textDidEndEditing:
    Deprecated Methods
    – drawsGrid Deprecated in OS X v10.3
    – selectColumn:byExtendingSelection: Deprecated in OS X v10.3
    – selectedColumnEnumerator Deprecated in OS X v10.3
    – selectedRowEnumerator Deprecated in OS X v10.3
    – selectRow:byExtendingSelection: Deprecated in OS X v10.3
    – setDrawsGrid: Deprecated in OS X v10.3
    – autoresizesAllColumnsToFit Deprecated in OS X v10.4
    – dragImageForRows:event:dragImageOffset: Deprecated in OS X v10.4
    – setAutoresizesAllColumnsToFit: Deprecated in OS X v10.4
    – tableView:writeRows:toPasteboard:  delegate method Deprecated in OS X v10.4
    """

    MAXCOLUMNS = 50

    def __init__(self, posSize, rows=None, maxColumns=None, autoUpdate=True,
        drawVerticalLines=False, drawHorizontalLines=False, **kwargs):

        self.maxColumns = maxColumns or self.MAXCOLUMNS
        if not 'columnDescriptions' in kwargs:
            kwargs['columnDescriptions'] = self.getDescription()
        if rows is None:
            rows = []
        self.rows = rows
        self.autoUpdate = autoUpdate
        List.__init__(self, posSize, rows, drawVerticalLines=drawVerticalLines,
            drawHorizontalLines=drawHorizontalLines, **kwargs)

    def getDescription(self):
        description = [dict(title='index', width=36, cell=SmallRightAlignTextListCell(editable=False),
            editable=False)]
        for colId in range(self.maxColumns):
            row = dict(title=self.col2ColId(colId), width=48,
                cell=SmallRightAlignTextListCell(editable=True), editable=True)
            description.append(row)
        return description

    # Cell stuff

    def setCell(self, colIndex, rowIndex, value, update=True):
        """Sets item value of @(colIndex, rowIndex). If update is false, then
        don't update the presented list.  This is used if multiple cell are
        updated in a single session. In that the caller should call
        @self.update()@ to make sure that the internal rows are synchronized
        with the vanilla list."""
        row = self.getRow(rowIndex)
        colId = self.col2ColId(colIndex)
        assert colId in row
        row[colId] = value
        if update and self.autoUpdate:
            self.updateRow(rowIndex)

    def getItem(self, colIndex, rowIndex):
        """Get item value of cell @(cellIndex)@."""
        row = self.getRow(rowIndex)
        colId = self.col2ColId(colIndex)
        return row.get(colId)

    # self[index] = row    works as in the regular list.

    def _getNSColumn(self, colId):
        return self.getNSTableView().tableColumnWithIdentifier_('%s' % colId)

    def getIndexOfColumn(self, colId):
        """Answer the current index in the view of the col that originally had
        *colIndex*."""
        return self.getNSTableView().columnWithIdentifier_(colId)

    def col2ColId(self, colIndex):
        if not isinstance(colIndex, str):
            return 'C%s' % colIndex
        return colIndex

    def update(self):
        """Called by application if @self.autoUpate@ is @False@."""
        self.set(self.rows)

    def updateRow(self, rowIndex):
        """Update only this row."""
        self[rowIndex] = self.rows[rowIndex]

    def disableSorting(self):
        """Rough method for now to disable all sorting by the headers."""
        self.getNSTableView().unbind_('sortDescriptors')

    # Row stuff

    def newRow(self, rowIndex, value=None):
        row = dict(index=rowIndex)
        if value is None:
            value = ''
        for colId in range(self.maxColumns):
            row[self.col2ColId(colId)] = value
        return row

    def getRow(self, rowIndex):
        """Answer dictionary of row values. Keys are the column identifiers.
        If the current set of row in the page is not big enough, then expand
        the sheet to this *rowIndex*."""
        for ri in range(len(self.rows), rowIndex+1):
            self.rows.append(self.newRow(ri))
        return self.rows[rowIndex]

    def deleteRowsBelow(self, rowIndex):
        """Delete all rows below *rowIndex* (with higher index)."""
        self.rows = self.rows[0:rowIndex]

    def deleteColumnsAfter(self, colIndex):
        """Clear all content to the right of *colIndex*."""
        for col in range(colIndex, self.maxColumns):
            for row in self.rows:
                row[col] = '' # We cannot delete. Just clear.

    # Cell attributes

    def setCellLeftAlign(self, colId, rowIndex):
        self.setCellAlign(colId, rowIndex, 'left')

    def setCellRightAlign(self, colId, rowIndex):
        self.setCellAlign(colId, rowIndex, 'right')

    def setCellCenter(self, colId, rowIndex):
        self.setCellAlign(colId, rowIndex, 'center')

    def setCellAlign(self, colId, rowIndex, align):
        align = {
            'center': NSCenterTextAlignment,
            'right': NSRightTextAlignment,
        }.get(align, NSLeftTextAlignment)
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        cell = nsColumn.dataCellForRow_(rowIndex)
        cell.setAlignment_(align)

    # Column attributes

    #def setColumnSortable(self, colId, value):
    #    nsColumn = self._getNSColumn(self.col2ColId(colId))
    #    nsColumn.setSortDescriptorPrototype_(value)

    def hideColumn(self, colId, hide=True):
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setHidden_(hide)

    def hideColumns(self, colIds, hide=True):
        for colId in colIds:
            self.hideColumn(colId, hide)

    def showColumn(self, colId):
        self.hideColumn(colId, False)

    def setColumnTitle(self, colId, title):
        """Set the title of the column. This does not affect its identifier."""
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.headerCell().setStringValue_(title)
        self.getNSTableView().headerView().setNeedsDisplay_(YES)

    def setColumnEditable(self, colId, flag):
        """Set the editable flag of the column."""
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setEditable_(flag)

    def setColumnWidth(self, colId, width):
        """Set the width of the column in the current view. Done by selecting a
        page."""
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setWidth_(width)

    def getColumnWidth(self, colId):
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        return nsColumn.width()

    def setColumnMinWidth(self, colId, width):
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setMinWidth_(width)

    def setColumnMaxWidth(self, colId, width):
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setMaxWidth_(width)

    def setColumnToolTip(self, colId, toolTipString):
        nsColumn = self._getNSColumn(self.col2ColId(colId))
        nsColumn.setHeaderToolTip_(toolTipString)

    # self.intercellSpacing

    def _set_intercellSpacing(self, size):
        if isinstance(size, (tuple, list)):
            w, h = size
        else:
            w = h = size
        self.getNSTableView().setIntercellSpacing_(NSSize(w, h))

    def _get_intercellSpacing(self):
        size = self.getNSTableView().intercellSpacing()
        return size.width, size.height

    intercellSpacing = property(_get_intercellSpacing, _set_intercellSpacing)

    # self.columnReordering

    def _get_columnReordering(self):
        return self.getNSTableView().allowsColumnReordering()

    def _set_columnReordering(self, flag):
        self.getNSTableView().setAllowsColumnReordering_(flag)

    columnReordering = property(_get_columnReordering, _set_columnReordering)

    # self.columnResizing

    def _get_columnResizing(self):
        return self.getNSTableView().allowsColumnResizing()

    def _set_columnResizing(self, flag):
        self.getNSTableView().setAllowsColumnResizing_(flag)

    columnResizing = property(_get_columnResizing, _set_columnResizing)

class SpreadsheetTester(BaseTool):

    TOOLID = 'tnSpreadsheetTester'
    NAME = 'Spreadsheet Tester'

    VIEWWIDTH = VIEWHEIGHT = 300
    VIEWMINSIZE = 200, 200
    VIEWMAXSIZE = 2000, 2000

    WINDOWCLASS = ScreenWindow # Window type for all tool/module windows, unless redefined.

    def build(self):
        screen, posSize = self.getWindowScreenPosSize() # Defaults comes from PREFERENCES_MODEL
        self.w = self.WINDOWCLASS(posSize=posSize, title=self.getWindowTitle(), screen=screen,
            minSize=self.VIEWMINSIZE, maxSize=self.VIEWMAXSIZE)
        self.populateView()
        self.openWindow() # Set bindings of window events and open window.
        self.test1()

    def populateView(self):
        view = self.getView()
        # Cache the family-name related with the open fonts.
        view.spreadsheet = Spreadsheet((0, 0, -0, -0),
            drawVerticalLines=True, drawHorizontalLines=True)

    def test1(self):
        ss = self.w.spreadsheet
        ss[(0, 0)] = 5
        ss[(1, 0)] = 5
        ss[(1, 4)] = 10
        ss[(8, 11)] = 1000
        ss[(1, 12)] = 'Text'
        ss.intercellSpacing = (0,0)
        print(ss.intercellSpacing)
        print(ss.columnReordering)
        print(ss.columnResizing)
        print(ss[4, 12])
        ss.setColumnWidth(4, 100)
        ss.setColumnWidth(5, 20)
        #ss.setColumnTitle(4, 'aaa')
        #ss.setColumnTitle(5, 'AAA')
        print(ss[4, 12])
        ss.setColumnMinWidth(4, 30)
        ss.setColumnMaxWidth(4, 80)
        ss.hideColumn(6)
        ss.setColumnToolTip(4, 'Tooltip of the column. ' * 10)
        ss[(8, 12)] = 200

if __name__ == '__main__':
    SpreadsheetTester().build()
