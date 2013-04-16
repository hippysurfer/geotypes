
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGMultiPoint
    from _OGMultiPoint import *

from _OGGeometry import OGGeometry
from _OGPolygon import OGPolygon, OGpolygonFromSequence

from CollectionClassTestBase import CollectionClassTestBase

class OGMultiPointTest(CollectionClassTestBase):    

    _last_num = 0

    testEqualities = CollectionClassTestBase._testEqualities
    testContainerMethods = CollectionClassTestBase._testContainerMethods

    def getEnumClass(self):
        x1 = float(OGMultiPointTest._last_num + 1)
        y1 = float(OGMultiPointTest._last_num + 2)
        OGMultiPointTest._last_num = OGMultiPointTest._last_num + 2

        return OGpointFromSequence((x1,y1))
                                
    def getCollectionClass(self):
        return OGMultiPoint()
    
    def testConstructor(self):
        geom = OGMultiPoint(-1) # with SRID
        assert geom.SRID() == -1

        geom = OGMultiPoint() # No SRID
        assert geom.SRID() == OGGeometry.default_srid
        assert len(geom) == 0        

    def testFactoryMethods(self):

        points = []
        # make a tuple of points.
        for p in xrange(0,10):
            points.append(self.getEnumClass())

        geom = OGmultiPointFromOGPoints(*points)
        assert len(geom) == 10, str(len(geom)) + " != 10 "

        
        geom1 = OGmultiPointFromSequence(
                ((133.000000, 134.000000),(135.000000, 136.000000),(137.000000, 138.000000))
                )
        

    def testReprs(self):
        geom = OGmultiPointFromSequence(
                ((133.000000, 134.000000),(135.000000, 136.000000),(137.000000, 138.000000))
                )

        assert str(geom) == "GeometryFromText('MULTIPOINT (133.000000 134.000000,135.000000 136.000000,137.000000 138.000000)',128)"
        assert repr(geom) == "(133.000000 134.000000,135.000000 136.000000,137.000000 138.000000)"

        
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGMultiPoint)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGMultiPointTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGMultiPoint
            from _OGMultiPoint import *


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
        x = coverage.analysis(_OGMultiPoint)
        print "\n"
        coverage.report(_OGMultiPoint)
