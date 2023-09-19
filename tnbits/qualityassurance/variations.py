# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     variations.py
#
import tnbits.toolbox.transformer as TX

def compareMasters(stylesDict, **kwargs):
    """Checks UFO masters before interpolation.
     * compares lengths
     * compares glyphs

    """
    masterKeys = stylesDict.keys()
    compared = []
    messages = []

    if len(masterKeys) < 2:
        return messages

    for masterKey0 in masterKeys:
        master0 = stylesDict[masterKey0]

        # Cross compare.
        for masterKey1 in masterKeys:
            if masterKey1 == masterKey0:
                continue

            if (masterKey0, masterKey1) in compared or (masterKey1, masterKey0) in compared:
                continue

            master1 = stylesDict[masterKey1]
            m = compareLengths(master0, master1, masterKey0, masterKey1)
            messages.append(m)
            m = compareKeys(master0, master1, masterKey0, masterKey1)
            messages.append(m)
            m = compareAnchors(master0, master1, masterKey0, masterKey1)
            messages.append(m)
            m = compareAnchors(master1, master0, masterKey1, masterKey0)
            messages.append(m)
            compared.append((masterKey0, masterKey1))

    m = compareOrder(stylesDict)
    if len(m) > 0:
        messages.append(m)

    return messages

def compareOrder(stylesDict):
    masterKeys = list(stylesDict.keys())
    messages = []
    masterKey0 = masterKeys[0]
    master0 = stylesDict[masterKey0]
    glyphOrder0 = master0.lib.get("public.glyphOrder", [])

    for masterKey1 in masterKeys[1:]:
        master1 = stylesDict[masterKey1]
        glyphOrder1 = master1.lib.get("public.glyphOrder", [])
        if glyphOrder0 != glyphOrder1:
            msg = '%s has a different order than %s' % (masterKey1[1], masterKey0[1])
            messages.append((msg, 'error'))

    return messages

def compareLengths(master0, master1, masterKey0, masterKey1):
    messages = []

    if len(master1) != len(master0):
        msg = 'Found different lengths while comparing %s to %s' % (masterKey0[1], masterKey1[1])
        messages.append(msg)
        msg = '%d glyphs vs. %d glyphs' % (len(master0), len(master1))
        messages.append((msg, 'error'))

    return messages

def compareKeys(master0, master1, masterKey0, masterKey1):
    messages = []
    # Move to compareKeys.
    s0 = set(master0.keys())
    s1 = set(master1.keys())
    diff0 = s0.difference(s1)
    diff1 = s1.difference(s0)
    diff = diff0 | diff1

    if len(diff) > 0:
        msg = 'Found different glyphs while comparing %s to %s' % (masterKey0[1], masterKey1[1])
        messages.append(msg)
        msg = '%s' % ', '.join(diff)
        messages.append((msg, 'error'))

    return messages

def compareAnchors(master0, master1, masterKey0, masterKey1):
    messages = []
    #msg = 'Comparing %s' % masterKey0[1]
    #messages.append(msg)

    for key in master0.keys():
        g0 = master0[key]

        for a0 in g0.anchors:
            found = False
            g1 = master1[key]

            if not 'name' in a0:
                msg = 'Anchor %s doesn\'t have a name, glyph %s' % (a0, key)
                messages.append((msg, 'error'))
            else:
                for a1 in g1.anchors:
                    if not 'name' in a1:
                        msg = 'Anchor %s in %s doesn\'t have a name' % (a1, masterKey1[1])
                        messages.append((msg, 'warning'))
                        continue
                    elif a0['name'] == a1['name']:
                        found = True
                        break

                if found is False:
                    msg = 'Anchor %s not found in %s, glyph %s' % (a0['name'], masterKey1[1], key)
                    messages.append((msg, 'error'))

    return messages

def fixMasters(stylesDict, **kwargs):
    messages = []
    compared = []
    masterKeys = stylesDict.keys()

    if len(masterKeys) < 2:
        return

    m = fixOrder(stylesDict)
    messages.append(m)

    for masterKey0 in masterKeys:
        master0 = stylesDict[masterKey0]

        # Cross compare.
        for masterKey1 in masterKeys:
            if masterKey1 == masterKey0:
                continue

            if (masterKey0, masterKey1) in compared or (masterKey1, masterKey0) in compared:
                continue

            master1 = stylesDict[masterKey1]
            m = fixAnchors(master0, master1, masterKey0, masterKey1)
            messages.append(m)
            m = fixAnchors(master1, master0, masterKey1, masterKey0)
            messages.append(m)

    return messages

def fixOrder(stylesDict, **wkwargs):
    # TODO: popup dialog to choose which master.
    messages= []
    masterKeys = list(stylesDict.keys())
    masterKey0 = masterKeys[0]
    master0 = stylesDict[masterKey0]
    glyphOrder0 = master0.lib.get("public.glyphOrder", [])

    for masterKey1 in masterKeys[1:]:
        master1 = stylesDict[masterKey1]
        master1.lib["public.glyphOrder"] = glyphOrder0
        master1.save()

    messages.append('Set glyph orders.')
    return messages

def fixAnchors(master0, master1, masterKey0, masterKey1):
    # TODO: decide which master should go first.
    # FIXME: maybe more of a design problem.
    messages= []
    changed = False

    for key in master0.keys():
        g0 = master0[key]

        for a0 in g0.anchors:
            g1 = master1[key]
            found = False

            for a1 in g1.anchors:
                if a0['name'] == a1['name']:
                    found = True
                    break

            if found is False:
                glyph = TX.naked(g1)
                anchor = glyph.anchorClass()
                anchor.name = a0['name']
                anchor.x = a0['x']
                anchor.y = a0['y']
                glyph.appendAnchor(anchor)
                msg = 'Added anchor %s to glyph %s in %s' % (a1['name'], key, masterKey1[1])
                messages.append((msg, 'warning'))
                if changed is False:
                    changed = True

    if changed:
        master1.save()
    else:
        messages.append('No anchor changes.')

    return messages

def deleteOrphans(stylesDict, **kwargs):
    """
    FIXME: currently not in use.
    Deletes glyphs that are missing from some of the masters.

    TODO: Also need to be removed as components, from kernings, features,
    lib.plist.
    """
    messages= []
    orphans = ['onesuperior', 'twosuperior', 'threesuperior', 'i.trk']

    for masterKey0 in masterKeys:
        master0 = stylesDict[masterKey0]
        for o in orphans:
            if o in master0:
                del master0[o]

        master0.save()

    return messages
