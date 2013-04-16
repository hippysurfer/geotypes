
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os

import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGGeometryCollection
    from _OGGeometryCollection import *

from _OGGeometry import OGGeometry
from _OGPoint import OGPoint, OGpointFromValues

from CollectionClassTestBase import CollectionClassTestBase

class OGGeometryCollectionTest(CollectionClassTestBase):    

    _last_num = 0
    
    def getEnumClass(self):
        x = float(OGGeometryCollectionTest._last_num + 1)
        y = float(OGGeometryCollectionTest._last_num + 2)
        OGGeometryCollectionTest._last_num = OGGeometryCollectionTest._last_num + 2
        
        return OGpointFromValues(x,y)
        
    def getCollectionClass(self):
        return OGGeometryCollection()

    testEqualities = CollectionClassTestBase._testEqualities
    testContainerMethods = CollectionClassTestBase._testContainerMethods
    
    def testConstructor(self):
        geom = OGGeometryCollection(-1) # with SRID
        assert geom.SRID() == -1

        geom = OGGeometryCollection() # No SRID
        assert geom.SRID() == OGGeometry.default_srid
        assert len(geom) == 0        

    def testFactoryMethods(self):

        points = []
        # make a tuple of points.
        for p in xrange(0,10):
            points.append(self.getEnumClass())

        geom = OGgeometryCollectionFromOGGeometries(*points)
        assert len(geom) == 10, str(len(geom)) + " != 10 "
        
    def testOpenGISMethods(self):
        geom = OGGeometryCollection()
        geom.append(OGpointFromValues(1.0,2.0))        
        geom.append(OGpointFromValues(3.0,4.0))

        assert geom.NumGeometries() == 2
        assert geom.GeometryN(0) == OGpointFromValues(1.0,2.0)

    def testReprs(self):
        geom = OGGeometryCollection()
        geom.append(OGpointFromValues(1.0,2.0))        
        geom.append(OGpointFromValues(3.0,4.0))

        assert str(geom) == "GeometryFromText('GEOMETRYCOLLECTION (POINT(1.000000 2.000000),POINT(3.000000 4.000000))',128)"
        assert repr(geom) == "(1.000000 2.000000,3.000000 4.000000)"
        
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGGeometryCollection)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGGeometryCollectionTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGGeometryCollection
            from _OGGeometryCollection import *


        except:
            print "Error setting up coverage checking"
            COVERAGE = 0
    else:
        COVERAGE = 0

    if os.environ.get('USEPYCHECK') == '1':
        try:
            import pychecker.checker
        except:
            print "Pychecker not installed on this machine"

    unittest.TextTestRunner().run(testSuite())

    if COVERAGE:
        coverage.stop()
        x = coverage.analysis(_OGGeometryCollection)
        print "\n"
        coverage.report(_OGGeometryCollection)
