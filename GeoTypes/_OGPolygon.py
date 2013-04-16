
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string

from _OGSurface import OGSurface
from _OGLinearRing import OGlinearRingFromSequence

class OGPolygon(OGSurface):
    """
    OGPloygon provides an implementation of a sequence of OGLinearRing in 2 or 3d space.

    It implements most of the methods of a container class and should be usable as if
    it were a list of OGLinearRings.
    """
    
    def __init__(self,srid=None):
        OGSurface.__init__(self,srid)
        self.emptyLineList()

    def emptyLineList(self):
        """
        Reset the Ploygon to have no Lines.
        """
        self._lines = []

    def getLines(self):
        """
        Return a list of all the points on the Polygon.
        """
        return self._lines

    def append(self, p):
        self.getLines().append(p)
        
    def count(self, p):
        return self.getLines().count(p)
        
    def index(self, p):
        return self.getLines().index(p)
        
    def extend(self, path):
        self.getLines().extend(path._lines)
        
    def insert(self,pos,p):
        self.getLines().insert(pos,p)
        
    def pop(self):
        return self.getLines().pop()
    
    def remove(self,p):
        self.getLines().remove(p)

    def __len__(self):
        return len(self.getLines())
    
    def __getitem__(self, key):
        return self.getLines()[key]
    
    def __setitem__(self, key, value):
        # check that value is a Line!        
        self.getLines()[key] = value
        
    def __delitem__(self, key):
        del self.getLines()[key]
    
    def __iter__(self):

        class __iter__:
            def __init__(self,lines):
                self._lines = lines
                self.pos = 0

            def __iter__(self): return self

            def next(self):
                if self.pos == len(self._lines):
                    raise StopIteration
                
                line = self._lines[self.pos]
                self.pos = self.pos + 1
                return line

        return __iter__(self.getLines())
        
    def __contains__(self, p):
        return l in self.getLines()
      
    def _og_str(self):
        s = string.join([ line.__repr__() for line in self.getLines() ],',')
            
        return "POLYGON (%s)" % (s,)
    
    def __repr__(self):
        s = string.join([ line.__repr__() for line in self.getLines() ],',')
            
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

def OGpolygonFromOGLines(*linearrings):
    """
    Return a OGPolygon.

    (arg *linearrings) any number of OGLinearRings that make up the OGPolygon.

    """
    polygon = OGPolygon()
    for line in linearrings:
        polygon.append(line)
        
    return polygon

def OGpolygonFromSequence(seq):
    """
    Return a OGPolygon.

    (arg *seq) a sequence of the form (((x,y),...,(x,y)),((x,y),...,(x,y))) that make up the OGPolygon,
    where x and y are floats.

    """

    polygon = OGPolygon()
    for line in seq:
        polygon.append(OGlinearRingFromSequence(line))
        
    return polygon

