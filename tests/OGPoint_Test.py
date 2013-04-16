
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGPoint
    from _OGPoint import *

from _OGGeometry import OGGeometry

class OGPointTest(unittest.TestCase):    

    def testEqualities(self):
        p = OGPoint()
        q = OGPoint()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q
        
    def testPoint2d(self):
        """
        Check that the basic Point class works
        """

        p = OGPoint()
        assert p.getX() == 0.0
        assert p.getY() == 0.0
        assert p.__str__() == "GeometryFromText('POINT(0.000000 0.000000)',%d)" % (OGGeometry.default_srid,)

        p = OGPoint()
        p.fromString("1.0 2.0")
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000)',%d)" % (OGGeometry.default_srid,)

        p.fromString("3.0 4.0")
        assert p.getX() == 3.0
        assert p.getY() == 4.0
        assert p.__str__() == "GeometryFromText('POINT(3.000000 4.000000)',%d)" % (OGGeometry.default_srid,)

        p.setX(5.0)
        assert p.__str__() == "GeometryFromText('POINT(5.000000 4.000000)',%d)" % (OGGeometry.default_srid,)
        
        p.setY(6.0)
        assert p.__str__() == "GeometryFromText('POINT(5.000000 6.000000)',%d)" % (OGGeometry.default_srid,)

        assert p.__repr__() == "5.000000 6.000000"

        p1 = OGPoint()
        p1.fromString("1.0 2.0")

        p2 = OGPoint()
        p2.fromString("1.0 2.0")

        assert p1 == p2

        p1 = OGPoint()
        p1.fromString("1.0 2.0")

        p2 = OGPoint()
        p2.fromString("1.0 3.0")

        
        assert p1 != p2

    def testPoint3d(self):
        """
        Check that the basic Point class works
        """

        p = OGPoint()
        assert p.getX() == 0.0
        assert p.getY() == 0.0
        assert p.getZ() == None
        assert p.__str__() == "GeometryFromText('POINT(0.000000 0.000000)',%d)" % (OGGeometry.default_srid,)

        p = OGPoint()
        p.fromString("1.0 2.0 3.0")
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.getZ() == 3.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000 3.000000)',%d)" % (OGGeometry.default_srid,)

        p.fromString("3.0 4.0 5.0")
        assert p.getX() == 3.0
        assert p.getY() == 4.0
        assert p.getZ() == 5.0
        assert p.__str__() == "GeometryFromText('POINT(3.000000 4.000000 5.000000)',%d)" % (OGGeometry.default_srid,)

        p.setX(5.0)
        assert p.__str__() == "GeometryFromText('POINT(5.000000 4.000000 5.000000)',%d)" % (OGGeometry.default_srid,)
        
        p.setY(6.0)
        assert p.__str__() == "GeometryFromText('POINT(5.000000 6.000000 5.000000)',%d)" % (OGGeometry.default_srid,)

        p.setZ(7.0)
        assert p.__str__() == "GeometryFromText('POINT(5.000000 6.000000 7.000000)',%d)" % (OGGeometry.default_srid,)

        assert p.__repr__() == "5.000000 6.000000 7.000000"

        p1 = OGPoint()
        p1.fromString("1.0 2.0 3.0")

        p2 = OGPoint()
        p2.fromString("1.0 2.0 3.0")

        assert p1 == p2

        p1 = OGPoint()
        p1.fromString("1.0 2.0 3.0")

        p2 = OGPoint()
        p2.fromString("1.0 3.0 3.0")

        
        assert p1 != p2


    def testFactories(self):

        p = OGpointFromValues(1.0,2.0)
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000)',%d)" % (OGGeometry.default_srid,)

        p = OGpointFromSequence((1.0,2.0))
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000)',%d)" % (OGGeometry.default_srid,)

        p = OGpointFromValues(1.0,2.0,3.0)
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.getZ() == 3.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000 3.000000)',%d)" % (OGGeometry.default_srid,)

        p = OGpointFromSequence((1.0,2.0,3.0))
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.getZ() == 3.0
        assert p.__str__() == "GeometryFromText('POINT(1.000000 2.000000 3.000000)',%d)" % (OGGeometry.default_srid,)
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGPoint)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGPointTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGPoint
            from _OGPoint import *

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
        x = coverage.analysis(_OGPoint)
        print "\n"
        coverage.report(_OGPoint)
