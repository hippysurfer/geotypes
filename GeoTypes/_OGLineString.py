
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import types, string

from _OGCurve import OGCurve
from _OGPoint import OGPoint, OGpointFromSequence

class OGLineString(OGCurve):
    """
    OGLineString provides and implementation of a sequence of connected OGPoints in 2 or 3d space.

    It implements most of the methods of a container class and should be usable as if
    it were a list of OGPoints.
    """
    
    def __init__(self,srid=None):
        OGCurve.__init__(self,srid)
        self.emptyPointList()

    def emptyPointList(self):
        """
        Reset the LineString to have no Points.
        """
        self._points = []

    def getPoints(self):
        """
        Return a list of all the points on the LineString.
        """
        return self._points

    def append(self, p):
        self.getPoints().append(p)
        
    def count(self, p):
        return self.getPoints().count(p)
        
    def index(self, p):
        return self.getPoints().index(p)
        
    def extend(self, path):
        self.getPoints().extend(path._points)
        
    def insert(self,pos,p):
        self.getPoints().insert(pos,p)
        
    def pop(self):
        return self.getPoints().pop()
    
    def remove(self,p):
        self.getPoints().remove(p)

    def __len__(self):
        return len(self.getPoints())
    
    def __getitem__(self, key):
        return self.getPoints()[key]
    
    def __setitem__(self, key, value):
        # check that value is a Point!        
        self.getPoints()[key] = value
        
    def __delitem__(self, key):
        del self.getPoints()[key]
    
    def __iter__(self):

        class __iter__:
            def __init__(self,points):
                self._points = points
                self.pos = 0

            def __iter__(self): return self

            def next(self):
                if self.pos == len(self._points):
                    raise StopIteration
                
                point = self._points[self.pos]
                self.pos = self.pos + 1
                return point

        return __iter__(self.getPoints())
        
    def __contains__(self, p):
        return p in self.getPoints()
      
    def _og_str(self):
        s = string.join([ point.__repr__() for point in self.getPoints() ],',')
            
        return "LINESTRING (%s)" % (s,)
    
    def __repr__(self):
        s = string.join([ point.__repr__() for point in self.getPoints() ],',')
            
        return "(%s)" % (s,)

    def __eq__(self,other):
        """
        Equality for paths means that:
             both paths are either open or closed.
             both paths have the same number of points
             all points are equal
        
        """
        if (type(self) != type(other)):
            return False

        if not len(self) == len(other):
            return False

        count = 0
        while count < len(self):
            if self[count] != other[count]: return False
            count = count + 1

        return True
            
    def __ne__(self,other):
        return not self.__eq__(other)


# factory methods

def OGlineStringFromOGPoints(*points):
    """
    Return a OGLineString.

    (arg *points) any number of OGPoints that make up the OGLineString.

    """
    linestring = OGLineString()
    for point in points:
        linestring.append(point)
        
    return linestring

def OGlineStringFromSequence(seq):
    """
    Return a OGLineString.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the OGLineString,
    where x and y are floats.

    """

    linestring = OGLineString()
    for point in seq:
        linestring.append(OGpointFromSequence(point))
        
    return linestring
