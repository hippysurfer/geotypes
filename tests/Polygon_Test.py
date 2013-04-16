
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    from _Point import *
    from _LineSeg import *
    import _Polygon
    from _Polygon import *

class PolygonTest(unittest.TestCase):

    def testPolygon(self):
        """
        Check basic Polygon class        
        """

        polygon = Polygon()
        assert polygon.isClosed()

        self.assertRaises(RuntimeError, polygon.setOpen)

        assert not polygon.isOpen()
        polygon.setClosed()
        assert not polygon.isOpen()
        assert polygon.isClosed()

        p1 = Point("(1,2)")
        p2 = Point("(2,3)")
        p3 = Point("(4,5)")
        
        polygon = Polygon("((1,2),(2,3),(4,5))")

        assert polygon[0] == p1
        assert polygon[1] == p2
        assert polygon[2] == p3
        assert polygon.isClosed()


        self.assertRaises(RuntimeError, Polygon, "[(1,2),(2,3),(4,5)]")
        self.assertRaises(TypeError,Polygon,"'(1,2),(2,3),(4,5)'")

        polygon = Polygon("((1,2),(2,3),(4,5))")
        assert polygon.__str__() == "'((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))'"
        assert polygon.__repr__() == "((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))"


        polygon1 = Polygon("((1,2),(2,3),(4,5))")
        polygon2 = Polygon("((1,2),(2,3),(4,5))")

        assert polygon1 == polygon2

        polygon2 = Polygon("((1,2),(2,3),(4,5),(6,7))")
        assert polygon1 != polygon2

        polygon2 = Polygon("((4,2),(2,3),(4,5))")
        assert polygon1 != polygon2




            
    def testPolygonContainerBehaviour(self):
        """
        Check that the basic Polygon class works as
        a container of Points
        """

        polygon = Polygon()
        assert len(polygon) == 0

        start = Point("(1.0,2.0)")
        polygon.append(start)

        assert len(polygon) == 1
        assert start in polygon
        assert polygon.index(start) == 0
        assert polygon[polygon.index(start)] == start

        # Check append
        
        p2 = Point("(2.0,3.0)")
        polygon.append(p2)

        assert len(polygon) == 2
        assert start in polygon
        assert polygon.index(start) == 0
        assert polygon[polygon.index(start)] == start
        assert polygon.index(p2) == 1
        assert polygon[polygon.index(p2)] == p2

        # Check __inter__
        
        count = 0
        for point in polygon:
            assert point in polygon
            count = count + 1
            
        assert count == 2


        # Check count

        polygon.append(p2)

        assert polygon.count(start) == 1
        assert polygon.count(p2) == 2


        # Check index - already checked above

        # Check extend

        polygon2 = Polygon()
        polygon2.append(Point("(10,10)"))
        polygon2.append(Point("(11,11)"))
        assert len(polygon2) == 2

        polygon2.extend(polygon)
        assert len(polygon2) == 2 + len(polygon)

        # Check insert

        p3 = Point("(100,100)")
        polygon2.insert(2,p3)
        assert len(polygon2) == 3 + len(polygon)
        assert polygon2.index(p3) == 2
        assert polygon2[2] == p3

        # Check pop

        polygon2.append(p3)
        assert len(polygon2) == 4 + len(polygon)
        assert polygon2.pop() == p3
        assert len(polygon2) == 3 + len(polygon)

        # Check remove

        assert p3 in polygon2
        polygon2.remove(p3)
        assert p3 not in polygon2

        # Check _setitem_
        
        polygon2.append(p3)
        p4 = Point("(200,200)")
        idx = polygon2.index(p3)
        polygon2[idx] = p4
        assert polygon2[idx] == p4
        assert polygon2.index(p4) == idx
        assert p4 in polygon2

        # Check _delitem_
        del polygon2[idx]
        assert p4 not in polygon2
        
        

    def testFactories(self):
        p1 = Point("(1.0,2.0)")
        p2 = Point("(1.0,3.0)")
        p3 = Point("(1.0,4.0)")

        polygon = polygonFromPoints(p1,p2,p3)

        assert polygon[0] == p1
        assert polygon[1] == p2
        assert polygon[2] == p3
        assert polygon.isClosed()        

        polygon = polygonFromSequence(((1.0,2.0),(1.0,3.0),(1.0,4.0)))
        assert polygon[0] == p1
        assert polygon[1] == p2
        assert polygon[2] == p3
        assert polygon.isClosed()

    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(_Polygon)
        assert x[2]==[], "Coverage is less than 100%"

def testSuite():
    return unittest.makeSuite(PolygonTest,'test')

if __name__ == "__main__":
    import os
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            from _Point import *
            from _LineSeg import *
            import _Polygon
            from _Polygon import *

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
        x = coverage.analysis(_Polygon)
        print "\n"
        coverage.report(_Polygon)
