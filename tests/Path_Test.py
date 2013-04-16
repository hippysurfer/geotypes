
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
    import _Path
    from _Path import *

class PathTest(unittest.TestCase):
    def testEqualities(self):
        p = Path()
        q = Path()
        assert p != None
        assert None != p
        assert p != 0
        assert p != {}
        assert p != []
        assert p == q

    def testPath(self):
        """
        Check basic Path class        
        """

        path = Path()
        assert path.isClosed()
        path.setOpen()
        assert path.isOpen()
        assert not path.isClosed()
        path.setClosed()
        assert not path.isOpen()
        assert path.isClosed()

        p1 = Point("(1,2)")
        p2 = Point("(2,3)")
        p3 = Point("(4,5)")
        
        path = Path("((1,2),(2,3),(4,5))")

        assert path[0] == p1
        assert path[1] == p2
        assert path[2] == p3
        assert path.isClosed()

        path = Path("[(1,2),(2,3),(4,5)]")

        assert path[0] == p1
        assert path[1] == p2
        assert path[2] == p3
        assert path.isOpen()

        self.assertRaises(TypeError,Path,"'(1,2),(2,3),(4,5)'")

        path = Path("((1,2),(2,3),(4,5))")
        assert path.__str__() == "'((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))'"
        assert path.__repr__() == "((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))"

        path = Path("[(1,2),(2,3),(4,5)]")
        assert path.__str__() == "'[(1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000)]'"
        assert path.__repr__() == "[(1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000)]"


        path.setClosed()
        assert path.__str__() == "'((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))'"
        assert path.__repr__() == "((1.000000,2.000000),(2.000000,3.000000),(4.000000,5.000000))"

        path1 = Path("((1,2),(2,3),(4,5))")
        path2 = Path("((1,2),(2,3),(4,5))")

        assert path1 == path2

        path2 = Path("((1,2),(2,3),(4,5),(6,7))")
        assert path1 != path2

        path2 = Path("((4,2),(2,3),(4,5))")
        assert path1 != path2

        path1 = Path("((1,2),(2,3),(4,5))")
        path2 = Path("[(1,2),(2,3),(4,5)]")
        assert path1 != path2



            
    def testPathContainerBehaviour(self):
        """
        Check that the basic Path class works as
        a container of Points
        """

        path = Path()
        assert len(path) == 0

        start = Point("(1.0,2.0)")
        path.append(start)

        assert len(path) == 1
        assert start in path
        assert path.index(start) == 0
        assert path[path.index(start)] == start

        # Check append
        
        p2 = Point("(2.0,3.0)")
        path.append(p2)

        assert len(path) == 2
        assert start in path
        assert path.index(start) == 0
        assert path[path.index(start)] == start
        assert path.index(p2) == 1
        assert path[path.index(p2)] == p2

        # Check __inter__
        
        count = 0
        for point in path:
            assert point in path
            count = count + 1
            
        assert count == 2


        # Check count

        path.append(p2)

        assert path.count(start) == 1
        assert path.count(p2) == 2


        # Check index - already checked above

        # Check extend

        path2 = Path()
        path2.append(Point("(10,10)"))
        path2.append(Point("(11,11)"))
        assert len(path2) == 2

        path2.extend(path)
        assert len(path2) == 2 + len(path)

        # Check insert

        p3 = Point("(100,100)")
        path2.insert(2,p3)
        assert len(path2) == 3 + len(path)
        assert path2.index(p3) == 2
        assert path2[2] == p3

        # Check pop

        path2.append(p3)
        assert len(path2) == 4 + len(path)
        assert path2.pop() == p3
        assert len(path2) == 3 + len(path)

        # Check remove

        assert p3 in path2
        path2.remove(p3)
        assert p3 not in path2

        # Check _setitem_
        
        path2.append(p3)
        p4 = Point("(200,200)")
        idx = path2.index(p3)
        path2[idx] = p4
        assert path2[idx] == p4
        assert path2.index(p4) == idx
        assert p4 in path2

        # Check _delitem_
        del path2[idx]
        assert p4 not in path2
        
        

    def testFactories(self):
        p1 = Point("(1.0,2.0)")
        p2 = Point("(1.0,3.0)")
        p3 = Point("(1.0,4.0)")

        path = pathFromPoints(p1,p2,p3)

        assert path[0] == p1
        assert path[1] == p2
        assert path[2] == p3
        assert path.isClosed()        

        path = pathFromSequence(((1.0,2.0),(1.0,3.0),(1.0,4.0)))
        assert path[0] == p1
        assert path[1] == p2
        assert path[2] == p3
        assert path.isClosed()
        
    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(_Path)
        assert x[2]==[], "Coverage is less than 100%"

def testSuite():
    return unittest.makeSuite(PathTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            from _Point import *
            from _LineSeg import *
            import _Path
            from _Path import *

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
        x = coverage.analysis(_Path)
        print "\n"
        coverage.report(_Path)
