
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGMultiPolygon
    from _OGMultiPolygon import *

from _OGGeometry import OGGeometry
from _OGPolygon import OGPolygon, OGpolygonFromSequence

from CollectionClassTestBase import CollectionClassTestBase

class OGMultiPolygonTest(CollectionClassTestBase):    

    _last_num = 0

    testEqualities = CollectionClassTestBase._testEqualities
    testContainerMethods = CollectionClassTestBase._testContainerMethods

    def getEnumClass(self):
        x1 = float(OGMultiPolygonTest._last_num + 1)
        y1 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2
        x2 = float(OGMultiPolygonTest._last_num + 1)
        y2 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2
        x3 = float(OGMultiPolygonTest._last_num + 1)
        y3 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2
        x4 = float(OGMultiPolygonTest._last_num + 1)
        y4 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2
        x5 = float(OGMultiPolygonTest._last_num + 1)
        y5 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2
        x6 = float(OGMultiPolygonTest._last_num + 1)
        y6 = float(OGMultiPolygonTest._last_num + 2)
        OGMultiPolygonTest._last_num = OGMultiPolygonTest._last_num + 2

        return OGpolygonFromSequence(
            ( # start of Polygon 1
            ((x1,y1),(x2,y2),(x3,y3)),
            ((x4,y4),(x5,y5),(x6,y6))
            ))
                                
    def getCollectionClass(self):
        return OGMultiPolygon()
    
    def testConstructor(self):
        geom = OGMultiPolygon(-1) # with SRID
        assert geom.SRID() == -1

        geom = OGMultiPolygon() # No SRID
        assert geom.SRID() == OGGeometry.default_srid
        assert len(geom) == 0        

    def testFactoryMethods(self):

        polygons = []
        # make a tuple of points.
        for p in xrange(0,10):
            polygons.append(self.getEnumClass())

        geom = OGmultiPolygonFromOGPolygons(*polygons)
        assert len(geom) == 10, str(len(geom)) + " != 10 "

        
        geom1 = OGmultiPolygonFromSequence(
            ( # MultiPolygon
              ( # Polygon
               ( # linearring
                (133.000000, 134.000000),(135.000000, 136.000000),(137.000000, 138.000000)
                ),
                (                
                (139.000000, 140.000000),(141.000000, 142.000000),(143.000000, 144.000000)
                )
               ,) # comma important because it must be a tuple
              ,) # comma important because it must be a tuple
            )
        

    def testReprs(self):
        geom = OGmultiPolygonFromSequence(
            ( # MultiPolygon
              ( # Polygon
               ( # linearring
                (133.000000, 134.000000),(135.000000, 136.000000),(137.000000, 138.000000)
                ),
                (                
                (139.000000, 140.000000),(141.000000, 142.000000),(143.000000, 144.000000)
                )
               ,) # comma important because it must be a tuple
              ,) # comma important because it must be a tuple
            )

        assert str(geom) == "GeometryFromText('MULTIPOLYGON (((133.000000 134.000000,135.000000 136.000000,137.000000 138.000000),(139.000000 140.000000,141.000000 142.000000,143.000000 144.000000)))',128)"
        assert repr(geom) == "(((133.000000 134.000000,135.000000 136.000000,137.000000 138.000000),(139.000000 140.000000,141.000000 142.000000,143.000000 144.000000)))"

        
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGMultiPolygon)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGMultiPolygonTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGMultiPolygon
            from _OGMultiPolygon import *


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
        x = coverage.analysis(_OGMultiPolygon)
        print "\n"
        coverage.report(_OGMultiPolygon)
