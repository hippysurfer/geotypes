
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os

import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _Point
    from _Point import *
    import _Circle
    from _Circle import *

class CircleTest(unittest.TestCase):    
    def testEqualities(self):
        p = Circle()
        q = Circle()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q
        
    def testCircle(self):
        """
        Check that the basic Circle class works
        """

        centre = Point("(1.0,1.0)")
        radius = 5

        c = Circle()
        c.setCentre(centre)
        c.setRadius(radius)

        assert c.getCentre() == centre
        assert c.getRadius() == radius
        assert c.__str__() == "'<%s,%f>'" % (centre.__repr__(),
                                               radius)
        assert c.__repr__() == "(%s,%f)" % (centre.__repr__(),
                                               radius)

        c = Circle("<(1.0,1.0),5)")
        assert c.getCentre() == centre
        assert c.getRadius() == radius
        assert c.__str__() == "'<%s,%f>'" % (centre.__repr__(),
                                                radius)
        
        c1 = Circle("<(1.0,1.0),5>")
        c2 = Circle("<(1.0,1.0),5>")

        assert c1 == c2

        c1 = Circle("<(1.0,1.0),5>")
        c2 = Circle("<(1.0,2.0),5>")

        assert c1 != c2

        c1 = Circle("<(1.0,1.0),5>")
        c2 = Circle("<(1.0,1.0),6>")

        assert c1 != c2

        

    def testFactories(self):

        centre = Point("(1.0,1.0)")
        radius = 5

        
        c = circleFromCentreAndRadius(centre,radius)
        assert c.getCentre() == centre
        assert c.getRadius() == radius
        assert c.__str__() == "'<%s,%f>'" % (centre.__repr__(),
                                               radius)
        assert c.__repr__() == "(%s,%f)" % (centre.__repr__(),
                                               radius)


        c = circelFromSequence(((1.0,1.0),5))
        assert c.getCentre() == centre
        assert c.getRadius() == radius
        assert c.__str__() == "'<%s,%f>'" % (centre.__repr__(),
                                               radius)
        assert c.__repr__() == "(%s,%f)" % (centre.__repr__(),
                                               radius)

    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(_Circle)
        assert x[2]==[], "Coverage is less than 100%"
        
def testSuite():
    return unittest.makeSuite(CircleTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _Point
            from _Point import *
            import _Circle
            from _Circle import *

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
        x = coverage.analysis(_Circle)
        print "\n"
        coverage.report(_Circle)
