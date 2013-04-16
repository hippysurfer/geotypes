
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
    import _LineSeg
    from _LineSeg import *


class LineSegTest(unittest.TestCase):    
    def testEqualities(self):
        p = LineSeg()
        q = LineSeg()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q

    def testLineSeg(self):
        """
        Check that the basic LineSeg class works
        """

        start = Point("(1.0,2.0)")
        end = Point("(1.0,3.0)")

        l = LineSeg()
        l.setStart(start)
        l.setEnd(end)

        assert l.getStart() == start
        assert l.getEnd() == end
        assert l.__str__() == "'(%s,%s)'" % (start.__repr__(),
                                             end.__repr__())
        assert l.__repr__() == "(%s,%s)" % (start.__repr__(),
                                            end.__repr__())

        l = LineSeg("((1.0,2.0),(1.0,3.0))")
        assert l.getStart() == start
        assert l.getEnd() == end
        assert l.__str__() == "'(%s,%s)'" % (start.__repr__(),
                                             end.__repr__())
        
        l1 = LineSeg("((1.0,2.0),(1.0,3.0))")
        l2 = LineSeg("((1.0,2.0),(1.0,3.0))")

        assert l1 == l2

        l1 = LineSeg("((1.0,2.0),(1.0,3.0))")
        l2 = LineSeg("((1.1,2.0),(1.0,3.0))")

        assert l1 != l2

        l1 = LineSeg("((1.0,2.0),(1.0,3.0))")
        l2 = LineSeg("((1.0,2.0),(1.1,3.0))")

        assert l1 != l2

        l1 = LineSeg("((1.0,2.0),(1.0,3.0))")
        l2 = LineSeg("((1.0,2.1),(1.1,3.0))")

        assert l1 != l2

        

    def testFactories(self):
        start = Point("(1.0,2.0)")
        end = Point("(1.0,3.0)")
        
        l = lineSegFromPoints(start,end)
        assert l.getStart() == start
        assert l.getEnd() == end
        assert l.__str__() == "'(%s,%s)'" % (start.__repr__(),
                                             end.__repr__())
        assert l.__repr__() == "(%s,%s)" % (start.__repr__(),
                                            end.__repr__())
        

        l = lineSegFromSequence(((1.0,2.0),(1.0,3.0)))
        assert l.getStart() == start
        assert l.getEnd() == end
        assert l.__str__() == "'(%s,%s)'" % (start.__repr__(),
                                             end.__repr__())
        assert l.__repr__() == "(%s,%s)" % (start.__repr__(),
                                            end.__repr__())

    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(_LineSeg)
        assert x[2]==[], "Coverage is less than 100%"

def testSuite():
    return unittest.makeSuite(LineSegTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1        
            import _Point
            from _Point import *
            import _LineSeg
            from _LineSeg import *

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
        x = coverage.analysis(_LineSeg)
        print "\n"
        coverage.report(_LineSeg)
