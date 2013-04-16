
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of LineSeg.
"""

from _ISQLProtocol import ISQLProtocol

from _Point import Point, pointFromSequence

class LineSeg(ISQLProtocol):
    """
    LineSeg provides an interface for a line segment in 2d space.

    It has accessor functions for start and end Points, provides a constructor
    that can handle the strings returned from Postgres for the lseg
    type and support equallity operations with other LinSeg objects.
    """

    def __init__(self,s=None,c=None):
        """
        Constructor. Optional (arg s) is a string as returned by postgres.
        It is of the form '((start_x.start_y),(end_x,end_y))' where x and y
        are floating point numbers.

        If (arg s) is None or omitted the LineSeg is initalised to ((0.0,0.0),(0.0,0.0)).
        """

        if s:
            self.fromString(s)
        else:
            self.setStart(Point())
            self.setEnd(Point())

    def fromString(self,s):
        seq = eval(s,{},{})
        self.setStart(pointFromSequence(seq[0]))
        self.setEnd(pointFromSequence(seq[1]))

    def setStart(self,p):
        self._start = p

    def getStart(self):
        return self._start

    def setEnd(self,p):
        self._end = p

    def getEnd(self):
        return self._end

    def __str__(self):
        return "'(%s,%s)'" % (self.getStart().__repr__(),
                              self.getEnd().__repr__())
    
    def __repr__(self):
        return "(%s,%s)" % (self.getStart().__repr__(),
                            self.getEnd().__repr__())

    def __eq__(self,other):
        """
        Two LineSegs are considered equal if thier start and end Points
        are the same.
        """
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        
        if self.getStart() == other.getStart() and \
           self.getEnd() == other.getEnd():
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)


# factory methods

def lineSegFromPoints(start,end):
    """
    Return a LineSeg.

    (arg start) is a Point object.
    (arg end) is a Point object.
    """
    l = LineSeg()
    l.setStart(start)
    l.setEnd(end)
    return l

def lineSegFromSequence(seq):
    """
    Return a LineSeg.

    (arg seq) is a sequence of the form '((start_x.start_y),(end_x,end_y))'.
    """
    l = LineSeg()
    l.setStart(pointFromSequence(seq[0]))
    l.setEnd(pointFromSequence(seq[1]))
    return l
               
