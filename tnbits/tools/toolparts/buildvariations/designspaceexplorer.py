from __future__ import division
import math
from fontTools.pens.cocoaPen import CocoaPen
from vanilla import Group, SplitView, EditText, TextBox
from tnbits.tools.toolparts.buildvariations.axisvaluelist import AxisValueList
from tnbits.tools.toolparts.buildvariations.canvas3d import Item3D, Canvas3D


class CachingDesignSpaceWrapper(object):

    def __init__(self, designSpace):
        self._designSpace = designSpace
        self.axes = designSpace.axes
        self._lowerCacheSize = 100
        self._upperCacheSize = 200
        self.clearCache()

    def clearCache(self):
        self._cache = {}
        self._counter = 0
        self._hits = 0
        self._misses = 0
        assert self._upperCacheSize > self._lowerCacheSize

    @staticmethod
    def _getCacheKey(glyphName, location):
        return tuple([glyphName] + sorted(location.items()))

    def _purgeCache(self):
        def _sorter(item):
            return item[1][1]
        items = sorted(self._cache.items(), key=_sorter, reverse=True)
        items = items[:self._lowerCacheSize]
        self._cache = {k: v for k, v in items}

    def getGlyphName(self, charCode):
        return self._designSpace.getGlyphName(charCode)

    def getOutline(self, glyphName, location, penFactory):
        cacheKey = self._getCacheKey(glyphName, location)
        if cacheKey not in self._cache:
            if len(self._cache) > self._upperCacheSize:
                self._purgeCache()
            cachedObject = self._designSpace.getOutline(glyphName, location, penFactory)
            self._cache[cacheKey] = (cachedObject, self._counter, 0)
            self._counter += 1
            self._misses += 1
        else:
            self._hits += 1
            cachedObject, counter, numRetrieved = self._cache[cacheKey]
            self._cache[cacheKey] = (cachedObject, self._counter, numRetrieved + 1) # update counter
            self._counter += 1
        return cachedObject


class DesignSpaceExplorer(Group):

    def __init__(self, posSize, designSpace, location=None, callback=None,
            previewCharacter="e"):
        super(DesignSpaceExplorer, self).__init__(posSize)
        self._designSpace = CachingDesignSpaceWrapper(designSpace)
        self._callback = callback
        self._sortedAxes = designSpace.axes
        self._previewGlyphName = designSpace.getGlyphName(ord(previewCharacter))
        # Prepare outlines for 3d view
        self._staticOutlines = self._getStaticOutlineList()

        if location is None:
            location = {}
            for a in designSpace.axes:
                location[a.tag] = a.defaultValue
            outlines = self._staticOutlines + [self._getLocationOutline(location)]

        if len(designSpace.axes) >= 3:
            angleX = math.radians(-10)
            angleY = math.radians(-20)
        else:
            angleX = angleY = 0
        self._cubeView = Canvas3D((0, 0, 0, 0), outlines, angleX, angleY)
        self._cubeView.individualZoom = 0.85
        self._cubeView.doStroke = False
        self._cubeView.backgroundColor = (1,)

        self._axisList = AxisValueList((0, 44, 0, 0), designSpace,
                location, callback=self._locationChangedCallback,
                axisReorderedCallback=self._axisReorderedCallback,
                previewGlyphName=self._previewGlyphName)

        cubeGroup = Group((0, 0, 0, 0))
        cubeGroup.cubeView = self._cubeView

        listGroup = Group((0, 0, 0, 0))
        listGroup.previewCharLabel = TextBox((10, 13, 130, 34), "Preview character:")
        listGroup.previewChar = EditText((134, 10, 60, 24), previewCharacter, callback=self._previewCharChanged)
        listGroup.axisList = self._axisList

        paneDescriptors = [
            dict(view=listGroup, identifier="pane2", minSize=250),
            dict(view=cubeGroup, identifier="pane1", minSize=150),
        ]
        self.splitView = SplitView((0, 0, -0, -0), paneDescriptors)

    def get(self):
        return self._axisList.get()

    def set(self, location):
        self._axisList.set(location)
        self._locationChangedCallback(self._axisList)

    def setPreviewGlyphName(self, previewGlyphName):
        self._previewGlyphName = previewGlyphName
        self._axisList.setPreviewGlyphName(previewGlyphName)
        self._staticOutlines = self._getStaticOutlineList()
        self._locationChangedCallback(self._axisList)

    def _getLocationOutline(self, location):
        coord = []
        for axis in self._sortedAxes[:3]:
            coord.append(axis.normalizeValue(location[axis.tag]))
        coord.extend([0.5] * (3 - len(coord)))
        x, y, z = coord
        path, center, size = self._designSpace.getOutline(self._previewGlyphName, location, CocoaPen)
        path = path.path
        item = Item3D((x-0.5, y-0.5, z-0.5), path, center, size, (0,))
        return item

    def _getStaticOutlineList(self, location=None):
        designSpace = self._designSpace
        if location is None:
            location = {}
        else:
            location = location.copy()
        for axis in self._sortedAxes[:3]:
            location[axis.tag] = axis.defaultValue
        locations = [location]

        for axis in self._sortedAxes[:3]:
            newLocations = []
            for loc in locations:
                for value in set([axis.minValue, axis.defaultValue, axis.maxValue]):
                    localDup = loc.copy()
                    localDup[axis.tag] = value
                    newLocations.append(localDup)
            locations = newLocations

        outlines = []
        for location in locations:
            coord = []
            for axis in self._sortedAxes[:3]:
                val = location.get(axis.tag, axis.defaultValue)
                coord.append(axis.normalizeValue(val))
            coord.extend([0.5] * (3 - len(coord)))
            x, y, z = coord
            path, center, size = designSpace.getOutline(self._previewGlyphName, location, CocoaPen)
            path = path.path
            item = Item3D((x-0.5, y-0.5, z-0.5), path, center, size, (0.6, 0.5))
            outlines.append(item)

        return outlines

    def _previewCharChanged(self, sender):
        s = sender.get()
        if len(s) > 1:
            s = s[-1]
        sender.set(s)
        if s:
            charCode = ord(s)
        else:
            charCode = ord("a")
        self.setPreviewGlyphName(self._designSpace.getGlyphName(charCode))

    def _locationChangedCallback(self, sender):
        tableView = self._axisList.list.getNSTableView()
        selectedIndices = tableView.selectedRowIndexes()
        if selectedIndices.firstIndex() > 2 or selectedIndices.lastIndex() > 2:
            location = sender.get()
            self._staticOutlines = self._getStaticOutlineList(location)
            outlines = self._staticOutlines + [self._getLocationOutline(location)]
        else:
            outlines = self._staticOutlines + [self._getLocationOutline(sender.get())]
        self._cubeView.set(outlines)
        if self._callback is not None:
            self._callback(self)

    def _axisReorderedCallback(self, sender):
        axisOrderMap = {tag: i for i, tag in enumerate(self._axisList.getAxisOrder())}
        def _sorter(item):
            return axisOrderMap.get(item.tag, 100000)
        self._sortedAxes = sorted(self._designSpace.axes, key=_sorter)
        self._staticOutlines = self._getStaticOutlineList()
        self._locationChangedCallback(sender)
