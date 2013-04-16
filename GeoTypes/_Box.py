
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of Box.

ChangeLog:
    14 jan 06: Added Box.fromWKT to parse relults from 'extent()' (fredericback@gmail.com)
    17 jan 06: Change constructor to accept several argument types (fredericback@gmail.com)
    13 jun 06: Added joinBoxes() (fredericback@gmail.com)
"""
from _ISQLProtocol import ISQLProtocol
from _Point import Point, pointFromSequence, pointFromValues

class Box(ISQLProtocol):
    """
    Box provides and implementation for a rectangular area in 2d space.

    It has accessor functions for the upper right hand and lower left hand
    corners of the box, which are Points. It supports equallity operations
    with other Box objects.

    The constructor accepts the following argument combinations:
        - Box()                             like Box(Point(0,0), Point(0,0))
        - Box( '((x.y),(x,y))' )            parse from string, x and y are floats
        - Box( 'BOX(x y,x y)' )             parse from string, x and y are floats
        - Box( Point(x,y), Point(x,y) )     set lower left and upper right points

    NOTE: The accessor methods imply that they must recieve the
    coords for the upper_right and lower_left corners. Passing the wrong
    corners into the setXXX methods will result in a ValueError being raised.
    """
    
    def __init__(self,*args):
        """
        The constructor accepts the following argument combinations:
            - Box()                             initalise to ((0.0,0.0),(0.0,0.0))
            - Box( '((x.y),(x,y))' )            parse from string, x and y are floats
            - Box( 'BOX(x y,x y)' )             parse from string, x and y are floats
            - Box( Point(x,y), Point(x,y) )     set lower left and upper right points
        """
        if len(args) == 0:
            self._setUpperRight(Point())
            self._setLowerLeft(Point())
        elif len(args) == 1:

            if args[0] == None: # avoid api breakage, args[0] may still be None 
                self._setUpperRight(Point())
                self._setLowerLeft(Point())
            elif args[0][0] == "B":
                self.fromWKT(args[0]) # if starts with a "B"
            else:
                self.fromString(args[0])

        elif len(args) == 2:
            if args[1].__class__ == Point:
                self._setUpperRight(args[0])
                self._setLowerLeft(args[1])
            else: 
                # Check that second param is a psycopg cursor.
                if args[1].__class__.__name__ != 'cursor':
                    raise ValueError, \
                        """Second param to __init__ is not a %s 
                        or a psycopg cursor."""
                        
                if args[0][0] == "B":
                    self.fromWKT(args[0]) # if starts with a "B"
                else:
                    self.fromString(args[0])
                            
        else: 
            raise ValueError, "wrong number of arguments"

        self._normaliseCornerCoords()
        
    def _normaliseCornerCoords(self):
        #print self._upper_right
        xr = self._upper_right.getX()
        xl = self._lower_left.getX()
        yu = self._upper_right.getY()
        yl = self._lower_left.getY()

        if xl>xr and yl>yu:
            self._upper_right = pointFromValues(xl,yl)
            self._lower_left  = pointFromValues(xr,yu)                        
        elif xl>xr:
            self._upper_right = pointFromValues(xl,yu)
            self._lower_left  = pointFromValues(xr,yl)            
        elif yl>yu:
            self._upper_right = pointFromValues(xr,yl)
            self._lower_left  = pointFromValues(xl,yu)
        #print self
     
    def fromWKT(self, s):
        """ Initialise from a WKT string of the form 'BOX(x y,x y)'
            This syntax is returned by the extent() command in postgis.
        """
    
        try:
            # skip 'BOX(' and ')'
            s = s[4:] 
            s = s[:-1]

            # match
            import re
            f = "[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?"
            e = r"(?P<x1>%s) (?P<y1>%s)\,(?P<x2>%s) (?P<y2>%s)" %(f,f,f,f)
            points = re.match(e,s).groupdict()
            # print points

            # set matching results
            ll = pointFromValues( float(points['x1']),float(points['y1']) )
            ur = pointFromValues( float(points['x2']),float(points['y2']) )
        except:
            raise Exception("Could not parse '%s'" %s) # recast

        self._setUpperRight(ur)
        self._setLowerLeft(ll)
        self._normaliseCornerCoords()

    def fromString(self,s):
        """
        Initialise the Box from a string.        

        (arg s) should be of the form '((x,y),(x,y))' where x and y are floating
        point numbers.
        
        """        
        seq = eval(s,{},{})
        self._setUpperRight(pointFromSequence(seq[0]))
        self._setLowerLeft(pointFromSequence(seq[1]))
        self._normaliseCornerCoords()
       
    def setUpperRight(self,p):
        """
        Set the upper right corner of the Box.

        (arg p) is a Point
        """
        if hasattr(self,'_lower_left'):
            if p.getX() < self._lower_left.getX() \
               or  p.getY() < self._lower_left .getY() :
                raise ValueError, "coord is not upper right of box."
        self._setUpperRight(p)
            
    def _setUpperRight(self,p):
        "Unckecked, private version"
        self._upper_right = p


    def getUpperRight(self):
        """
        Return a Point that represents the uppoer right corner of the Box.
        """
        self._normaliseCornerCoords()
        return self._upper_right

    def setLowerLeft(self,p):
        """
        Set the lower left corner of the Box.

        (arg p) is a Point
        """
        if  hasattr(self,'_upper_right'):
            if p.getX() > self._upper_right.getX() \
                   or  p.getY() > self._upper_right.getY() :
                raise ValueError, "coord is not lower left of box."
        self._setLowerLeft(p)
            
    def _setLowerLeft(self,p):
        "Unckecked, private version"
        self._lower_left = p
             
        
    def getLowerLeft(self):

        """
        Return a Point that represents the lower left corner of the Box.
        """
        self._normaliseCornerCoords()
        return self._lower_left

    def __str__(self):
        """
        Generate a string representation of the Box that is
        suitable to use in a Postgres query.
        """
        self._normaliseCornerCoords()
        return "'(%s,%s)'" % (self.getUpperRight().__repr__(),
                              self.getLowerLeft().__repr__())
    
    def __repr__(self):
        """
        Generate a represention of the Box as a string
        suitable for 'evaling' as a tuple.
        """
        self._normaliseCornerCoords()
        return "(%s,%s)" % (self.getUpperRight().__repr__(),
                            self.getLowerLeft().__repr__())

    def __eq__(self,other):
        """
        The is a simple equallity operator.
        """
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        self._normaliseCornerCoords()
        other._normaliseCornerCoords()
        if self.getUpperRight() == other.getUpperRight() and \
           self.getLowerLeft() == other.getLowerLeft():
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)


# factory methods

def boxFromPoints(upper_right,lower_left):
    """
    Return a Box.

    (arg upper_right) is a Point object.
    (arg lower_left) is a Point object.
    """
    b = Box()
    b._setUpperRight(upper_right)
    b._setLowerLeft(lower_left)
    b._normaliseCornerCoords()
    return b

def boxFromSequence(seq):
    """
    Return a Box.

    (arg seq) is a sequence of the form '((x,y),(x1,y1))' where (x,y) is
    the upper right corner and (x1,y1) is the lower left corner.
    """
    b = Box()
    b._setUpperRight(pointFromSequence(seq[0]))
    b._setLowerLeft(pointFromSequence(seq[1]))
    b._normaliseCornerCoords()
    return b
              
               
def joinBoxes(box_a, box_b):
    """
        Union of two boxes.
        Useful to join geometry extents.
        
        box_a and box_b are instances of Box
        returns a new Box
    """
    a_ll = box_a.getLowerLeft()
    b_ll = box_b.getLowerLeft()
    a_ur = box_a.getUpperRight()
    b_ur = box_b.getUpperRight()
    if a_ll.getX() < b_ll.getX(): mx = a_ll.getX()
    else: mx = b_ll.getX()
    if a_ll.getY() < b_ll.getY(): my = a_ll.getY()
    else: my = b_ll.getY()
    if a_ur.getX() > b_ur.getX(): Mx = a_ur.getX()
    else: Mx = b_ur.getX()
    if a_ur.getY() > b_ur.getY(): My = a_ur.getY()
    else: My = b_ur.getY()
    return Box( Point(mx,my), Point(Mx,My) )
    
