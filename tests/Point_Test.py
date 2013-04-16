
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest

import TestConfig

import os
if not os.environ.get('USECOVERAGE') == '1':
    import _Point
    from _Point import *


class PointTest(unittest.TestCase):    

    def testEqualities(self):
        p = Point()
        q = Point()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q
        
    def testPoint(self):
        """
        Check that the basic Point class works
        """

        p = Point()
        assert p.getX() == 0.0
        assert p.getY() == 0.0
        assert p.__str__() == "'(0.000000,0.000000)'"

        p = Point("(1.0,2.0)")
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "'(1.000000,2.000000)'"

        p.fromString("(3.0,4.0)")
        assert p.getX() == 3.0
        assert p.getY() == 4.0
        assert p.__str__() == "'(3.000000,4.000000)'"

        p.setX(5.0)
        assert p.__str__() == "'(5.000000,4.000000)'"
        
        p.setY(6.0)
        assert p.__str__() == "'(5.000000,6.000000)'"        

        assert p.__repr__() == "(5.000000,6.000000)"

        p1 = Point("(1.0,2.0)")
        p2 = Point("(1.0,2.0)")

        assert p1 == p2

        p1 = Point("(1.0,2.0)")
        p2 = Point("(1.0,3.0)")
        
        assert p1 != p2


    def testFactories(self):

        p = pointFromValues(1.0,2.0)
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "'(1.000000,2.000000)'"

        p = pointFromSequence((1.0,2.0))
        assert p.getX() == 1.0
        assert p.getY() == 2.0
        assert p.__str__() == "'(1.000000,2.000000)'"
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_Point)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(PointTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _Point
            from _Point import *

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
        x = coverage.analysis(_Point)
        print "\n"
        coverage.report(_Point)
