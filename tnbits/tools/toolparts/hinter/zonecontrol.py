# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010 buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    zonecontrol.py
#

from vanilla import Group, List, PopUpButton
from AppKit import NSView, NSBezierPath, NSColor
from tnbits.constants import Constants

class ZoneControl(Group):
    """Shows graphic state zone points."""

    C = Constants
    zones = [C.ZONE0, C.ZONE1]
    zone = []

    C0 = 2
    C1 = 304
    C2 = 456

    def __init__(self, posSize, delegate):
        super(ZoneControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        self.zonesBox = PopUpButton((self.C0, 2, 150, 30), map(str, self.zones), callback=self.zonesCallback)
        descriptions = [{"title": "index"}, {"title": "value"}]
        self.zoneList = List((self.C0, 30, -0, -0), self.zone, columnDescriptions=descriptions, selectionCallback=self.zoneCallback)
        self.update()

    def update(self):
        self.zone = []

        if not self.delegate.simulator.gstate is None:
            if self.delegate.zoneId is None:
                self.delegate.zoneId = self.C.ZONE1
            zoneId = self.delegate.zoneId

            self.zonesBox.set(self.zones.index(zoneId))
            l = self.setZone(zoneId)
            selection = []
            for p in self.delegate.simulator.gstate.referencePoints:
                if not p is None and p < l:
                    selection.append(p - 1)

            self.zoneList.setSelection(selection)

    def setZone(self, zoneId):
        """
        Gets the zones instructions from the graphics state and shows them
        in an enumerated list.
        """
        zone = self.delegate.simulator.gstate.zones[zoneId]
        self.zone = []

        for i, value in enumerate(zone):
            self.zone.append({'index': str(i+1), 'value': str(value)})

        self.zoneList.set(self.zone)
        return len(zone)

    def zonesCallback(self, sender):
        """
        """
        i = sender.get()
        zoneId = self.zones[int(i)]
        self.delegate.zoneId = zoneId
        self.setZone(zoneId)

    def zoneCallback(self, sender):
        pass
