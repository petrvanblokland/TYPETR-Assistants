# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    updaterbits.py
#

class UpdaterBits:
    """The UpdaterBits of a tool separates the request for an update (e.g.
    vanilla fills, redraws, etc.) from the actual execution. In practice the
    development of tools collects the calls for update methods, where in
    practice these only should be executed once for a certain event.

    Callbacks that are part of an event (e.g. setting a list content will cause
    the update callback for that list be called), should only set the request,
    not actually execute the update."""

    def registerUpdaters(self, registeredUpdates):
        """Register the list of update request name and the methods to be
        called.  registeredUpdates has format [('updateList', 'updateList'),
        ...]"""
        self._registeredUpdateMethods = {} # Make dictionary for fast access
        self._registeredUpdateIds = [] # Keep the defined order

        for updateName, updateMethodName in registeredUpdates:
            assert hasattr(self, updateMethodName), 'Missing method name "%s"' % updateMethodName
            self._registeredUpdateMethods[updateName] = getattr(self, updateMethodName)
            self._registeredUpdateIds.append(updateName)
        self.clearPendingUpdates()

    def clearPendingUpdates(self):
        self._pendingUpdateData = {} # Request ids, connected to optional data to distract the rect from.
        self._pendingUpdates = []
        self._updating = False # We can reset, because we know that we started the update.

    def requestUpdate(self, names, updateInfo=None):
        """Add the name-type of update to be added to the pending list. Names
        can be a single update name or a list/tuple with update names. If we
        are already in updating mode, no more requests can be added.  They will
        be ignored. This happens if updating callbacks are happening during the
        execution of the pending updates. It's "too late" to add new ones. Call
        update first before new requests will be stored.  In case info is
        defined, request an update of the rect defined by the data. This can be
        a rectangle, but also the glyph/name the changed, so the calling
        application needs to figure out later how to distract the rect from
        this data.

        The optional updateInfo can contain the rectangle that must be
        updated."""
        if self._updating:
            return
        if not isinstance(names, (tuple, list)):
            names = [names]
        for name in names:
            assert name in self._registeredUpdateIds, 'Unregistered method name "%s"' % name
            # Make sure the request is only added once to the pending update list.
            if not name in self._pendingUpdateData: # Just add once, ignore other requests with the same name.
                self._pendingUpdateData[name] = updateInfo # Can be None if the update doesn't not need info for update rect.
                self._pendingUpdates.append(name) # Collect update names, so we can find the ordered methods while updating.

    def update(self):
        """Run through the aggregated update requests, execute the methods in
        the order of registered methods."""
        from time import time
        if not self._updating: # If already in updating mode, then ignore.
            for name in self._pendingUpdates: # Run through the list of pending updater names.
                info = self._pendingUpdateData[name] # If there is any info supplied to determine the update rect, then pass it on.
                # Execute the method with the intended data as resource for the
                # calling tools to decide on which part to update.  Info can be
                # None if the request was made without additional info.
                #
                if name in self._registeredUpdateMethods:
                    self._registeredUpdateMethods[name](info)
                else:
                    print('### [Error] TRYING TO UPDATE', name, info, 'Missing updater method.')
            # We updated, now clear the pending list for next set of requests.
            # Also clears the self._updating flag.
            self.clearPendingUpdates()
