
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest

import os

class CollectionClassTestBase(unittest.TestCase):    
    """
    Base class to contain unittests for the collection
    semantics of all the OpenGIS classess that act as
    python collectioning.
    """

    def getEnumClass(self):
        """
        This method should return a object of the type
        that the container class is meant to hold.
        
        All sub classes should overide this.
        """
        raise NotImplementedError

    def getCollectionClass(self):
        """
        This method returns an instance the class under test.
        All sub classes should overide this.
        """
        raise NotImplementedError
       
    
    def _testEqualities(self):
        
        geom1 = self.getCollectionClass()
        geom2 = self.getEnumClass()
        
        geom1.append(geom2)

        geom3 = self.getCollectionClass()
        geom3.append(geom2)


        assert geom1 == geom3
        
        geom3.append(self.getEnumClass())
        assert geom1 != geom3

        # Equality with a different type should be false.
        assert geom1 != 0

    def _testContainerMethods(self):    
        geom = self.getCollectionClass()

        # append
        a = self.getEnumClass()
        geom.append(a)
        assert len(geom) == 1
        assert geom.count(a) == 1
        assert geom.index(a) == 0
        

        b = self.getEnumClass()
        geom.append(b)
        assert len(geom) == 2

        # index
        assert geom[0] == a
        assert geom[1] == b

        # extend
        geom1 = self.getCollectionClass()
        geom1.append(self.getEnumClass())
        geom1.append(self.getEnumClass())
        assert len(geom1) == 2

        geom.extend(geom1)
        assert len(geom) == 4

        # insert
        c= self.getEnumClass()
        geom.insert(0,c)
        assert geom[0] == c

        # pop
        l = len(geom)
        d = self.getEnumClass()
        geom.append(d)
        assert len(geom) == l+1
        assert geom.pop() == d
        assert len(geom) == l

        # __contains__
        p = self.getEnumClass()
        geom.append(p)
        assert p in geom

        # remove
        geom.remove(p)
        assert p not in geom, str(p)+" should not have been in "+str(geom)

        # __setitem__, __getitem
        p = self.getEnumClass()
        geom[2] = p
        assert geom[2] == p

        # __delitem__
        del geom[2]
        assert geom[2] != p

        # __iter__
        cls = self.getEnumClass().__class__
        for geo in geom:
            assert geo.__class__ == cls
        
