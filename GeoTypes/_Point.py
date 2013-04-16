
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of Point.

ChangeLog:
    17 jan 06: Change constructor to accept several argument types (fredericback@gmail.com)
"""

from _ISQLProtocol import ISQLProtocol

class Point(ISQLProtocol):
    """
    Point provides an interface for a single point in 2d space.

    The constructor accepts the following argument combinations:
        - Point()                           initalised to (0.0,0.0)
        - Point( '((x,y),(x,y))' )          parse from string, x and y are floats
        - Box( 'BOX(x y,x y)' )             parse from string, x and y are floats
        - Box( Point(x,y), Point(x,y) )     set lower left and upper right points

    It has accessor functions for X and Y coords and support equallity operations
    with other Point objects.
    """
    
    def __init__(self,*args):
        """
        The constructor accepts the following argument combinations:
            - Point()                           initalised to (0.0,0.0)
            - Point( '((x,y),(x,y))' )          parse from string, x and y are floats
            - Box( 'BOX(x y,x y)' )             parse from string, x and y are floats
            - Box( Point(x,y), Point(x,y) )     set lower left and upper right points

        Constructor. Optional (arg s) is a string as returned by postgres.
        It is of the form '(x,y)' where x and y are floating point numbers.
        """

        if len(args) == 0:
            self.setX(0.0)
            self.setY(0.0)
        elif len(args) == 1:

             # avoid api breakage, args[0] may still be None 
            if args[0] == None:
                self.setX(0.0)
                self.setY(0.0)
            else:
                self.fromString(args[0])

        elif len(args) == 2:
            if args[1].__class__ == self.__class__:
                self.setX(args[0])
                self.setY(args[1])
            else: 
                # Check that second param is a psycopg cursor.
                if args[1].__class__.__name__ != 'cursor':
                    raise ValueError, \
                        """Second param to __init__ is not a %s 
                        or a psycopg cursor."""
                
                self.fromString(args[0])
        else:
            raise ValueError, "wrong number of arguments"


    def fromString(self,s):
        """
        Initialise the Point from a string.

        (arg s) should be of the form '(x,y)' where x and y are floating
        point numbers.
        """
        seq = eval(s,{},{})
        self.setX(seq[0])
        self.setY(seq[1])
        
    def setX(self,x):
        """
        Set the X coord of the Point.

        (arg x) is a float.
        """
        self._x = x

    def getX(self):
        """
        Return the X coord of the Point.
        """
        return self._x

    def setY(self,y):
        """
        Set the Y coord of the Point.

        (arg x) is a float.
        """

        self._y = y

    def getY(self):
        """
        Return the X coord of the Point.
        """

        return self._y

    def __str__(self):
        """
        Generate a string representation of the Point that is
        suitable to use in a Postgres query.
        """
        return "'(%f,%f)'" % (self.getX(), self.getY())

    def __repr__(self):
        """
        Generate a represention of the Point as a string
        suitable for 'evaling' as a tuple.
        """
        if self._x is None or self._y is None:
            return "(%s,%s)" % (self._x,self._y)
        return "(%f,%f)" % (self.getX(), self.getY())

    def __eq__(self,other):
        """
        Support equality operations.

        A Point is equal to another point is X == other.X and Y = other.Y.
        """
        if (self.__class__.__name__ != other.__class__.__name__):
            return False

        if self.getX() == other.getX() and \
           self.getY() == other.getY():
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

# Some helpful factory methods

def pointFromValues(x,y):
    """
    Return a Point object.

    (arg x) is the X coord as a float
    (arg y) is the Y coord as a float
    """
    
    p = Point()
    p.setX(x)
    p.setY(y)
    return p

def pointFromSequence(seq):
    """
    Return a Point object.

    (arg seq) is a sequence of the form (x,y) where x is the X coord as a float
    and y is the Y coord as a float.
    """

    p = Point()
    p.setX(seq[0])
    p.setY(seq[1])
    return p
