
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of Circle.
"""

from _ISQLProtocol import ISQLProtocol
from _Point import Point, pointFromSequence

class Circle(ISQLProtocol):
    """
    Circle provides an implementation for a circle in 2d space.

    It has accessor functions for a centre Point and radius size,
    provides a constructor that can handle the strings returned from
    Postgres for the circle type and support equallity operations
    with other Circle objects.
    """
    
    def __init__(self,s=None,c=None):
        """
        Constructor. Optional (arg s) is a string as returned by postgres.
        It is of the form '<(x.y),r>' where x,y and r are floating point numbers.

        If (arg s) is None or omitted the Circle is initalised to <(0.0,0.0),0>.
        """
        if s:
            self.fromString(s)
        else:
            self.setCentre(Point())
            self.setRadius(0.0)

    def fromString(self,s):
        """
        Initalise the Circle from a string.

        (arg s) should be of the form '<(x,y),r>' although this
        method will also work with the form '((x,y),r)'.
        """
        # circles come out of the db as '<(x,y),r>'
        # so we must first convert them to '((x,y),r'
        s = s.replace('<','(')
        s = s.replace('>',')')        
        seq = eval(s,{},{})
        self.setCentre(pointFromSequence(seq[0]))
        self.setRadius(seq[1])

    def setCentre(self,p):
        """
        Set the centre Point of the circle.

        (arg p) is a Point.
        """
        self._centre = p

    def getCentre(self):
        """
        Return the centre Point of the circle.
        """
        return self._centre

    def setRadius(self,r):
        """
        Set the radius of the circle.

        (arg r) is a float.
        """
        self._radius = r

    def getRadius(self):
        """
        Return the radius of the circle.
        """
        return self._radius

    def __str__(self):
        """
        Generate a string representation of the Circle that is
        suitable to use in a Postgres query.
        """
        return "'<%s,%f>'" % (self.getCentre().__repr__(),
                              self.getRadius())
    
    def __repr__(self):
        """
        Generate a represention of the Circle as a string
        suitable for 'evaling' as a tuple.
        """
        return "(%s,%f)" % (self.getCentre().__repr__(),
                            self.getRadius())

    def __eq__(self,other):
        """
        Support for equality operations.

        A Circle is equal to another Circle if the centre Points are equal
        and the radius is equal.
        """
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        
        if self.getCentre() == other.getCentre() and \
               self.getRadius() == other.getRadius():
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)


# factory methods

def circleFromCentreAndRadius(centre,radius):
    """
    Return a Circle.

    (arg centre) is a Point.
    (arg radius) is a float.
    """
    c = Circle()
    c.setCentre(centre)
    c.setRadius(radius)
    return c

def circelFromSequence(seq):
    """
    Return a Circle.

    (arg seq) is a sequence of the form ((x,y),r) where x,y and r
    are floats.
    """
    c = Circle()
    c.setCentre(pointFromSequence(seq[0]))
    c.setRadius(seq[1])
    return c
               
