#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   hasOverlap.py
#
from shapely.geometry import LineString

def bezier(t, *points):
    """General De Casteljau evaluation of any-degree Bézier"""
    if len(points) == 1:
        return points[0]
    next_set = []
    for i in range(1, len(points)):
        x = points[i-1][0] + t*(points[i][0] - points[i-1][0])
        y = points[i-1][1] + t*(points[i][1] - points[i-1][1])
        next_set.append((x, y))
    return bezier(t, *next_set)

def flatten_contour_to_segments(contour, steps=30):
    """Return a list of LineString segments along the contour"""
    pts = [(p.x, p.y, p.type) for p in contour.points]
    if not pts:
        return []

    segments = []
    seg = []

    for x, y, t in pts:
        seg.append((x, y))
        if t is not None:
            # Flatten segment
            if len(seg) == 2 and t == "line":
                segments.append(LineString(seg))
            else:
                points = [bezier(i/steps, *seg) for i in range(steps+1)]
                for i in range(len(points)-1):
                    segments.append(LineString([points[i], points[i+1]]))
            seg = [seg[-1]]

    return segments

def hasOverlap(glyph, steps=30):
    """Return True if any flattened segment in the glyph intersects another contour"""
    contour_segments = []
    for contour in glyph.contours:
        contour_segments.append(flatten_contour_to_segments(contour, steps))

    # Compare segments from different contours only
    for i in range(len(contour_segments)):
        for j in range(i+1, len(contour_segments)):
            for seg1 in contour_segments[i]:
                for seg2 in contour_segments[j]:
                    if seg1.intersects(seg2):
                        return True
    return False
