
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

from _OGGeometry import OGGeometry

class OGPoint(OGGeometry):

    def __init__(self, srid=None):
        OGGeometry.__init__(self,srid)
        self.setX(0.0)
        self.setY(0.0)
        self.setZ(None)

    
    def fromString(self,s):
        """
        Initialise the Point from a string.

        (arg s) should be of the form '(x y z)' where x and y are floating
        point numbers.
        """
        seq = s.split(' ')
        self.setX(float(seq[0]))
        self.setY(float(seq[1]))
        if len(seq) == 3:
            self.setZ(float(seq[2]))
        else:
            self.setZ(None)
        

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

    def setZ(self,z):
        """
        Set the Z coord of the Point.

        (arg x) is a float.or None. If (arg x) is None the Point becomes 2d.
        """

        self._z = z

    def getZ(self):
        """
        Return the Z coord of the Point.
        """

        return self._z

    def _og_str(self):
        """
        Generate a string representation of the Point that is
        suitable to use in a Postgres query.
        """
        if self.getZ():            
            ret = "POINT(%f %f %f)" % (self.getX(),
                                       self.getY(),
                                       self.getZ())
        else:
            ret = "POINT(%f %f)" % (self.getX(),
                                    self.getY())
                                    
        return ret

    def __repr__(self):
        """
        Generate a represention of the Point as a string
        suitable for 'evaling' as a tuple.
        """
        if self.getZ():            
            ret = "%f %f %f" % (self.getX(), self.getY(), self.getZ())
        else:
            ret = "%f %f" % (self.getX(), self.getY())

        return ret

    def __eq__(self,other):
        """
        Support equality operations.

        A Point is equal to another point is X == other.X and Y = other.Y.
        """
        if (type(self) != type(other)):
            return False

        if self.getX() == other.getX() and \
           self.getY() == other.getY() and \
           self.getZ() == other.getZ():
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

# Some helpful factory methods

def OGpointFromValues(x,y,z=None):
    """
    Return a Point object.

    (arg x) is the X coord as a float
    (arg y) is the Y coord as a float
    """
    
    p = OGPoint()
    p.setX(x)
    p.setY(y)
    p.setZ(z)
    return p

def OGpointFromSequence(seq):
    """
    Return a Point object.

    (arg seq) is a sequence of the form (x,y) where x is the X coord as a float
    and y is the Y coord as a float.
    """

    
    p = OGPoint()
    p.setX(seq[0])
    p.setY(seq[1])
    if len(seq) == 3:
        p.setZ(seq[2])
        
    return p
