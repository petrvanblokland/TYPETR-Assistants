from __future__ import division
from AppKit import NSDragOperationMove
from Foundation import NSObject
from Foundation import NSIndexSet, NSMutableIndexSet, NSNumberFormatter
from vanilla import Group, List
from vanilla.vanillaList import VanillaArrayController
from tnbits.tools.toolparts.buildvariations.varglyphcell import VarGlyphCell
from tnbits.vanillas.listitemwrapper import ListItemWrapper
from tnbits.vanillas.classnameincrementer import ClassNameIncrementer


class AxisValue(object):

    def __init__(self, axis, designSpace, sharedLocation, previewGlyphName):
        self.axis = axis
        self.designSpace = designSpace
        self.sharedLocation = sharedLocation
        self.previewGlyphName = previewGlyphName
        self._value = axis.defaultValue

    def __repr__(self):
        return "<%s %r %s>" % (self.__class__.__name__, self.axis.tag, self.value)

    # .axisValue is an alias for .value, so we can use two different keys for the same value
    # in List columns. This could probably be done differently with setting up a table column ID.
    def _get_axisValue(self):
        return self.value
    def _set_axisValue(self, value):
        self.value = value
    axisValue = property(_get_axisValue, _set_axisValue)

    def _get_value(self):
        return self._value
    def _set_value(self, value):
        self._value = min(max(value, self.axis.minValue), self.axis.maxValue)  # clip
        self.sharedLocation[self.axis.tag] = self.value
    value = property(_get_value, _set_value)

    # normalizedValue is between 0 and 1, so it's not the same as a normalized value
    # in a variation font context, where it could also be between -1 and 1 or -1 and 0.
    def _get_normalizedValue(self):
        return (self.value - self.axis.minValue) / (self.axis.maxValue - self.axis.minValue)
    def _set_normalizedValue(self, value):
        value = min(max(value, 0.0), 1.0)  # clip
        self.value = self.axis.minValue + value * (self.axis.maxValue - self.axis.minValue)
    normalizedValue = property(_get_normalizedValue, _set_normalizedValue)

    @property
    def name(self):
        return "%s\n(%s)" % (self.axis.name, self.axis.tag)

    def getOutline(self, value, penFactory):
        location = dict(self.sharedLocation)
        location[self.axis.tag] = value
        return self.designSpace.getOutline(self.previewGlyphName, location, penFactory)


class AxisValueListTableViewDelegate(NSObject):

    __metaclass__ = ClassNameIncrementer

    def tableView_willDisplayCell_forTableColumn_row_(self, view, cell, col, row):
        if col.identifier() == "axisValue":
            arrayController = view.dataSource()
            obj = arrayController.arrangedObjects()[row]
            cell.setRepresentedObject_(obj)


class AxisValueList(Group):

    def __init__(self, posSize, designSpace, location,
            callback=None,
            axisReorderedCallback=None,
            previewGlyphName="e"):
        super(AxisValueList, self).__init__(posSize)
        self._locationChangedCallback = callback
        self._axisReorderedCallback = axisReorderedCallback

        self._sharedLocation = location.copy()  # XXX really share?
        values = [AxisValue(axis, designSpace, self._sharedLocation, previewGlyphName) for axis in designSpace.axes]
        dependencies = {
            "value": ["normalizedValue", "axisValue"],
            "normalizedValue": ["value", "axisValue"],
            "axisValue": ["value", "normalizedValue"],
        }
        listData = [ListItemWrapper(value, dependencies) for value in values]

        formatter = NSNumberFormatter.alloc().init()
        formatter.setMaximumFractionDigits_(1)

        cell = VarGlyphCell.alloc().init()
        cell.setContinuous_(True)
        columnDescriptions = [
            dict(title="Axis name", key="name", width=140, minWidth=140, maxWidth=300, editable=False),
            dict(title="Value", key="value", formatter=formatter, width=60),
            dict(title="Value", key="axisValue", minWidth=140, maxWidth=300, cell=cell),
        ]

        dragSettings = dict(type="myInternalDragType", callback=None)
        selfDropSettings = dict(type="myInternalDragType",
            callback=self.dropRearrangeCallback, operation=NSDragOperationMove)

        self.list = List((0, 0, 0, 0), listData, columnDescriptions=columnDescriptions, rowHeight=80,
            editCallback=self.listEditCallback, drawFocusRing=False, drawVerticalLines=True,
            drawHorizontalLines=True, dragSettings=dragSettings, selfDropSettings=selfDropSettings,
            allowsSorting=False)

        self._delegate = AxisValueListTableViewDelegate.alloc().init()
        self.list.getNSTableView().setDelegate_(self._delegate)

        self.list._tableView.setUsesAlternatingRowBackgroundColors_(False)

    def get(self):
        return self._sharedLocation.copy()

    def set(self, location):
        for wrappedItem in self.list:
            item = wrappedItem.wrappedObject()
            item.value = location[item.axis.tag]
        lst = self.list.getNSTableView()
        lst.reloadData()

    def setPreviewGlyphName(self, previewGlyphName):
        for wrappedItem in self.list:
            item = wrappedItem.wrappedObject()
            item.previewGlyphName = previewGlyphName
        lst = self.list.getNSTableView()
        lst.reloadData()

    def getAxisOrder(self):
        order = []
        arrayController = self.list._arrayController
        for item in arrayController.arrangedObjects():
            order.append(item.wrappedObject().axis.tag)
        return order

    def dropRearrangeCallback(self, sender, dropInfo):
        if not dropInfo["isProposal"]:
            arrayController = sender._arrayController
            arrayController.setSortDescriptors_(())

            rowIndex = dropInfo["rowIndex"]
            draggedItems = dropInfo["data"]

            items = list(arrayController.arrangedObjects())
            draggedObjects = []
            for index, item in enumerate(items):
                if str(item) in draggedItems:
                    draggedObjects.append(item)
                    items[index] = None

            items[rowIndex:rowIndex] = draggedObjects
            items = [item for item in items if item is not None]
            sender.set(items)
            selection = [items.index(item) for item in draggedObjects]
            sender.setSelection(selection)
            if self._axisReorderedCallback is not None:
                self._axisReorderedCallback(self)
        return True

    def listEditCallback(self, sender):
        lst = sender.getNSTableView()
        index = lst.columnWithIdentifier_("axisValue")
        rowIndices = NSMutableIndexSet.indexSetWithIndexesInRange_((0, len(sender)))
        rowIndices.removeIndex_(lst.selectedRow())  # doesn't need redrawing
        colIndices = NSIndexSet.indexSetWithIndex_(index)
        lst.reloadDataForRowIndexes_columnIndexes_(rowIndices, colIndices)
        if self._locationChangedCallback is not None:
            self._locationChangedCallback(self)
