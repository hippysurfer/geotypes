
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of Polygon.
"""
import types, string


from _Path import Path
from _Point import Point, pointFromSequence

class Polygon(Path):
    """
    Point provides an interface for a closed path in 2d space.

    It is a sub class of the Path class with the enforced limitation
    that the Path can not be set to 'open'.

    It implements most of the methods of a container class and should be usable as if
    it were a list of Points.

    The Polygon class is provided in addition to the closed Path class because
    Postgres has distinct types for these two objects.

    """

    def __init__(self,s=None,c=None):
        Path.__init__(self,s)

    def setOpen(self):
        raise RuntimeError, "Path cannot be open for a polygon"

    def isClosed(self):
        return 1

    def isOpen(self):
        return 0
        


# factory methods

def polygonFromPoints(*points):
    """
    Return a Polygon.

    (arg *points) any number of Points that make up the Polygon.
    """
    poly = Polygon()
    for point in points:
        poly.append(point)
        
    return poly

def polygonFromSequence(seq):
    """
    Return a Polygon.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the Polygon,
    where x and y are floats.
    """
    poly = Polygon()
    for point in seq:
        poly.append(pointFromSequence(point))
        
    return poly
               
