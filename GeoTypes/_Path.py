
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of Path.
"""

import types, string

from _ISQLProtocol import ISQLProtocol
from _Point import Point, pointFromSequence

class Path(ISQLProtocol):
    """
    Path provides and implementation of a sequence of connected Points in 2d space.

    It implements most of the methods of a container class and should be usable as if
    it were a list of Points.

    Both 'open' and 'closed' paths are supported and a path can be toggled between
    open and closed using the setOpen() and setClosed() methods.
    """
    
    def __init__(self,s=None,c=None):
        """
        Constructor. Optional (arg s) is a string as returned by postgres.

        Its form is a bit of a pain because postgres does not have seperate types for
        open and closed paths. See http://www.postgresql.org/docs/7.3/static/datatype-geometric.html
        for a description of its represenation.

        If (arg s) is None or omitted the Path is initialised to have no Points.


        """
        if s:
            self.fromString(s)
        else:
            self.emptyPointList()

    def emptyPointList(self):
        """
        Reset the Path to have no Points.
        """
        self._points = []
        self.setClosed()

    def getPoints(self):
        """
        Return a list of all the points on the Path.
        """
        return self._points

    def setClosed(self):
        """
        Make the Path an closed Path.
        """
        self._closed = 1
        
    def setOpen(self):
        """
        Make the Path an open Path.
        """

        self._closed = 0


    def isClosed(self):
        return self._closed

    def isOpen(self):
        return not self._closed
        
    def fromString(self,s):
        """
        Initialse the Path from a string.

        (arg s) is of the form described in
        http://www.postgresql.org/docs/7.3/static/datatype-geometric.html
        
        """
        seq = eval(s,{},{})
        self.emptyPointList()

        # If it is a tuple PG defines it as closed
        # If it is a list PG defines it as open
        # not nice but what can you do ?
        if type(seq) == types.TupleType:
            self.setClosed()
        elif type(seq) == types.ListType:
            self.setOpen()
        else:
            raise TypeError, 'Bad initalise string must be a Tuple or a List'
        for p in seq:
            self.append(pointFromSequence(p))

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
    
    def __str__(self):
        if self.isClosed(): envolope = "'(%s)'"
        else: envolope = "'[%s]'"

        s = string.join([ point.__repr__() for point in self.getPoints() ],',')
            
        return envolope % (s,)
    
    def __repr__(self):
        if self.isClosed(): envolope = "(%s)"
        else: envolope = "[%s]"

        s = string.join([ point.__repr__() for point in self.getPoints() ],',')
            
        return envolope % (s,)

    def __eq__(self,other):
        """
        Equality for paths means that:
             both paths are either open or closed.
             both paths have the same number of points
             all points are equal
        
        """
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        
        if not ((self.isClosed() and other.isClosed() ) or \
                (self.isOpen() and other.isOpen())):
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

def pathFromPoints(*points):
    """
    Return a Path.

    (arg *points) any number of Points that make up the Path.

    NOTE: The Path will be closed by default.
    """
    path = Path()
    for point in points:
        path.append(point)
        
    return path

def pathFromSequence(seq):
    """
    Return a Path.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the Path,
    where x and y are floats.

    NOTE: The Path will be closed by default.
    """

    path = Path()
    for point in seq:
        path.append(pointFromSequence(point))
        
    return path
               
