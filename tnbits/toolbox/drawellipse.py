"""drawellipse.py -- This module contains functions to draw an ellipse or a circle onto a pen.

There are native cuadratic versions as well, that will generate more optimal shapes when
dealing with qudratic curves.
"""

__all__ = ["drawCircle", "drawEllipse", "drawCircleQuadratic", "drawEllipseQuadratic"]


bezierArcMagic = 0.5522847498     # constant for drawing circular arcs w/ Beziers

def drawEllipse(pen, cx, cy, rx, ry, tension=bezierArcMagic):
    # to reverse contour, just use negative rx or ry
    h1x, h1y = (1, tension)
    h2x, h2y = (tension, 1)
    x, y = (0, 1)
    pen.moveTo((cx + rx, cy))
    for i in range(4):
        pen.curveTo(
            (cx + rx * h1x, cy + ry * h1y),
            (cx + rx * h2x, cy + ry * h2y),
            (cx + rx * x, cy + ry * y))
        h1x, h1y = -h1y, h1x
        h2x, h2y = -h2y, h2x
        x, y = -y, x
    pen.closePath()


quadBezierArcMagic = 0.414213562373  # constant for drawing circular arcs w/ quadratic Beziers

def drawEllipseQuadratic(pen, cx, cy, rx, ry, tension=quadBezierArcMagic):
    # to reverse contour, just use negative rx or ry
    x = rx * tension
    y = ry * tension
    pen.qCurveTo((cx+x, cy+ry), (cx+rx, cy+y),
                 (cx+rx, cy-y), (cx+x, cy-ry),
                 (cx-x, cy-ry), (cx-rx, cy-y),
                 (cx-rx, cy+y), (cx-x, cy+ry), None)
    pen.closePath()


# Two convenience functions

def drawCircle(pen, cx, cy, radius, reverse=False):
    rx = ry = radius
    if reverse:
        ry = -ry
    drawEllipse(pen, cx, cy, rx, ry)


def drawCircleQuadratic(pen, cx, cy, radius, reverse=False):
    rx = ry = radius
    if reverse:
        ry = -ry
    drawEllipseQuadratic(pen, cx, cy, rx, ry)


if __name__ == "__main__":
    # DrawBot test
    bez = BezierPath()
    drawEllipse(bez, 500, 500, 480, 400)
    drawEllipse(bez, 500, 500, 460, -300)
    drawEllipseQuadratic(bez, 500, 500, 440, 200)
    drawEllipseQuadratic(bez, 500, 500, 420, -100)
    drawPath(bez)
