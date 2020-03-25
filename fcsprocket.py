from math import cos, sin, pi, acos, asin, atan, sqrt

import FreeCAD, Part
from FreeCAD import Base, Console
from . import involute
rotate = involute.rotate


def makeSprocket(P, N, Dr):
    if FreeCAD.ActiveDocument is None:
        FreeCAD.newDocument("Sprocket")
    doc = FreeCAD.ActiveDocument
    w = FCWireBuilder()
    sprocket.CreateSprocket(w, P, N, Dr)
    sprocketw = Part.Wire([o.toShape() for o in w.wire])
    sprocket = doc.addObject("Part::Feature", "Sprocket")
    sprocket.Shape = sprocketw
    return sprocket

class FCWireBuilder(object):
    """A helper class to prepare a Part.Wire object"""
    def __init__(self):
        self.pos = None
        self.theta = 0.0
        self.wire = []

    def move(self, p):
        """set current position"""
        self.pos = Base.Vector(*p)

    def line(self, p):
        """Add a segment between self.pos and p"""
        p = rotate(p, self.theta)
        end = Base.Vector(*p)
        self.wire.append(Part.LineSegment(self.pos, end))
        self.pos = end

    def arc(self, p, r, sweep):
        """"Add an arc from self.pos to p which radius is r
        sweep (0 or 1) determine the orientation of the arc
        """
        p = rotate(p, self.theta)
        end = Base.Vector(*p)
        mid = Base.Vector(*(midpoints(p, self.pos, r)[sweep]))
        self.wire.append(Part.Arc(self.pos, mid, end))
        self.pos = end

    def curve(self, *points):
        """Add a Bezier curve from self.pos to points[-1]
        every other points are the control points of the Bezier curve (which
        will thus be of degree len(points) )
        """
        points = [Base.Vector(*rotate(p, self.theta)) for p in points]
        bz = Part.BezierCurve()
        bz.setPoles([self.pos] + points)
        self.wire.append(bz)
        self.pos = points[-1]

    def close(self):
        pass

def midpoints(p1, p2, r):
    """A very ugly function that returns the midpoint of a p1 and p2
    on the circle which radius is r and which pass through p1 and
    p2

    Return the 2 possible solutions
    """
    vx, vy = p2[0]-p1[0], p2[1]-p1[1]
    b = (vx**2 + vy**2)**.5
    v = (vx/b, vy/b)
    cosA = b**2 / (2*b*r)
    A = acos(cosA)

    vx, vy = rotate(v, A)
    c1 = (p1[0]+r*vx, p1[1]+r*vy)
    m1x, m1y = ((p1[0]+p2[0])/2 - c1[0], (p1[1]+p2[1])/2 - c1[1])
    dm1 = (m1x**2+m1y**2)**.5
    m1x, m1y = (c1[0] + r*m1x/dm1, c1[1] + r*m1y/dm1)
    m1 = (m1x, m1y)

    vx, vy = rotate(v, -A)
    c2 = (p1[0]+r*vx, p1[1]+r*vy)
    m2x, m2y = ((p1[0]+p2[0])/2 - c2[0], (p1[1]+p2[1])/2 - c2[1])
    dm2 = (m2x**2+m2y**2)**.5
    m2x, m2y = (c2[0] + r*m2x/dm2, c2[1] + r*m2y/dm2)
    m2 = (m2x, m2y)

    return m1, m2
