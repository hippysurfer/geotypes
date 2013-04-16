
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string

from _OGGeometry import OGGeometry

class OGGeometryCollection(OGGeometry):

    """
    OGGeometryCollection.

    It implements most of the methods of a container class so that any
    OpenGIS Collection class should be usable as if it were a list of
    OGGeometry objects.
    """
    
    def __init__(self,srid=None):
        OGGeometry.__init__(self,srid)
        self.emptyGeomList()

    def emptyGeomList(self):
        """
        Reset the Collection to have no Points.
        """
        self._geoms = []

    def getGeometries(self):
        """
        Return a list of all the Geometries in the Collection.
        """
        return self._geoms

    def append(self, p):
        self.getGeometries().append(p)
        
    def count(self, p):
        return self.getGeometries().count(p)
        
    def index(self, p):
        return self.getGeometries().index(p)
        
    def extend(self, path):
        self.getGeometries().extend(path._geoms)
        
    def insert(self,pos,p):
        self.getGeometries().insert(pos,p)
        
    def pop(self):
        return self.getGeometries().pop()
    
    def remove(self,p):
        self.getGeometries().remove(p)

    def __len__(self):
        return len(self.getGeometries())
    
    def __getitem__(self, key):
        return self.getGeometries()[key]
    
    def __setitem__(self, key, value):
        # check that value is a Geometry!
        self.getGeometries()[key] = value
        
    def __delitem__(self, key):
        del self.getGeometries()[key]
    
    def __iter__(self):

        class __iter__:
            def __init__(self,geoms):
                self._geoms = geoms
                self.pos = 0

            def __iter__(self): return self

            def next(self):
                if self.pos == len(self._geoms):
                    raise StopIteration
                
                geom = self._geoms[self.pos]
                self.pos = self.pos + 1
                return geom

        return __iter__(self.getGeometries())
        
    def __contains__(self, p):
        return p in self.getGeometries()

    def _og_str(self):
        s = string.join([ geom._og_str() for geom in self.getGeometries() ],',')

        return 'GEOMETRYCOLLECTION (%s)' % (s,)
        
    def __repr__(self):
        s = string.join([ geom.__repr__() for geom in self.getGeometries() ],',')
            
        return "(%s)" % (s,)

    def __eq__(self,other):
        """
        Equality for GeometryCollections means that:
             both Collections have the same number of geoms
             all geoms are equal
        
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

    # Methods defined by the OpenGIS standard
    def NumGeometries(self):
        return len(self)

    def GeometryN(self,index):
        return self[index]

def OGgeometryCollectionFromOGGeometries(*geometries):
    """
    Return a OGGeometryCollection.

    (arg *geometries) any number of OGGeometries that make up the OGGeometryCollection.

    """
    geomcollection = OGGeometryCollection()
    for geom in geometries:
        geomcollection.append(geom)
        
    return geomcollection
