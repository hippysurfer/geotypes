
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
    import _Box
    from _Box import *


class BoxTest(unittest.TestCase):    
    def testEqualities(self):
        p = Box()
        q = Box()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q
        
    def testBox(self):
        """
        Check that the basic Box class works
        """

        upper_right = Point("(2.0,2.0)")
        lower_left = Point("(1.0,1.0)")

        b = Box()
        b.setUpperRight(upper_right)
        b.setLowerLeft(lower_left)

        assert b.getUpperRight() == upper_right
        assert b.getLowerLeft() == lower_left
        assert b.__str__() == "'(%s,%s)'" % (upper_right.__repr__(),
                                             lower_left.__repr__())
        assert b.__repr__() == "(%s,%s)" % (upper_right.__repr__(),
                                            lower_left.__repr__())

        b = Box("((2.0,2.0),(1.0,1.0))")
        assert b.getUpperRight() == upper_right
        assert b.getLowerLeft() == lower_left
        assert b.__str__() == "'(%s,%s)'" % (upper_right.__repr__(),
                                             lower_left.__repr__())
        
        b1 = Box("((2.0,2.0),(1.0,1.0))")
        b2 = Box("((2.0,2.0),(1.0,1.0))")

        assert b1 == b2

        b1 = Box("((2.0,2.0),(1.0,1.0))")
        b2 = Box("((2.1,2.0),(1.0,1.0))")

        assert b1 != b2

        b1 = Box("((2.0,2.0),(1.0,1.0))")
        b2 = Box("((2.0,2.0),(1.1,1.0))")

        assert b1 != b2

        b1 = Box("((2.0,2.0),(1.0,1.0))")
        b2 = Box("((2.0,2.1),(1.1,1.0))")

        assert b1 != b2


    def testNormalise(self):
        """
        Check that the normalise methods work.
        """

        upper_right = Point("(2.0,2.0)")
        lower_left = Point("(1.0,1.0)")
        upper_left = Point("(1.0,2.0)")
        lower_right = Point("(2.0,1.0)")

        b = boxFromPoints(upper_left,lower_right)
        assert b.getUpperRight() == upper_right
        assert b.getLowerLeft() == lower_left

        b = boxFromPoints(lower_left,upper_right)
        assert b.getUpperRight() == upper_right
        assert b.getLowerLeft() == lower_left

        b = boxFromPoints(lower_right,upper_left)
        assert b.getUpperRight() == upper_right
        assert b.getLowerLeft() == lower_left

        b = Box()
        b.setUpperRight(lower_left)
        self.assertRaises(ValueError, b.setLowerLeft, upper_right)

        b = Box()
        b._setLowerLeft(upper_right)
        self.assertRaises(ValueError, b.setUpperRight, lower_left)


    def testFactories(self):
        upper_right = Point("(2.0,2.0)")
        lower_left = Point("(1.0,1.0)")
        
        b = boxFromPoints(upper_right,lower_left)
        assert b.getUpperRight() == upper_right, "boxFromPoints failed"
        assert b.getLowerLeft() == lower_left, "boxFromPoints failed"
        assert b.__str__() == "'(%s,%s)'" % (upper_right.__repr__(),
                                             lower_left.__repr__()), "boxFromPoints failed"
        assert b.__repr__() == "(%s,%s)" % (upper_right.__repr__(),
                                            lower_left.__repr__()), "boxFromPoints failed"
        

        b = boxFromSequence(((2.0,2.0),(1.0,1.0)))
        assert b.getUpperRight() == upper_right, "boxFromSequence failed"
        assert b.getLowerLeft() == lower_left, "boxFromSequence failed"
        assert b.__str__() == "'(%s,%s)'" % (upper_right.__repr__(),
                                             lower_left.__repr__()), "boxFromSequence failed"
        assert b.__repr__() == "(%s,%s)" % (upper_right.__repr__(),
                                            lower_left.__repr__()), "boxFromSequence failed"

    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(_Box)
        assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(BoxTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _Point
            from _Point import *
            import _Box
            from _Box import *
            
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
        x = coverage.analysis(_Box)
        print "\n"
        coverage.report(_Box)
