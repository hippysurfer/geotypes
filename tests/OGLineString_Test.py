
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGLineString
    from _OGLineString import *

from _OGGeometry import OGGeometry
from _OGPoint import OGPoint, OGpointFromValues

class OGLineStringTest(unittest.TestCase):    

    def testConstructor(self):
        linestring = OGLineString(-1) # with SRID
        assert linestring.SRID() == -1

        linestring = OGLineString() # No SRID
        assert linestring.SRID() == OGGeometry.default_srid
        assert len(linestring) == 0
        
    def testEqualities(self):
        linestring1 = OGLineString()
        linestring1.append(OGPoint())
        
        linestring2 = OGLineString()
        linestring2.append(OGPoint())

        assert linestring1 == linestring2
        
        linestring2.append(OGpointFromValues(1.0,2.0))
        assert linestring1 != linestring2        

    def testContainerMethods(self):    
        linestring = OGLineString()

        # append
        linestring.append(OGpointFromValues(1.0,2.0))
        assert len(linestring) == 1
        
        linestring.append(OGpointFromValues(3.0,4.0))
        assert len(linestring) == 2

        # index
        assert linestring[0] == OGpointFromValues(1.0,2.0)
        assert linestring[1] == OGpointFromValues(3.0,4.0)

        # extend
        linestring1 = OGLineString()
        linestring1.append(OGpointFromValues(2.0,3.0))
        linestring1.append(OGpointFromValues(4.0,5.0))
        assert len(linestring1) == 2

        linestring.extend(linestring1)
        assert len(linestring) == 4

        # insert
        linestring.insert(0,OGpointFromValues(6.0,7.0))
        assert linestring[0] == OGpointFromValues(6.0,7.0)

        # pop
        l = len(linestring)
        linestring.append(OGpointFromValues(1.0,2.0))
        assert len(linestring) == l+1
        assert linestring.pop() == OGpointFromValues(1.0,2.0)
        assert len(linestring) == l

        # __contains__
        p = OGpointFromValues(100.0,200.0)
        linestring.append(p)
        assert p in linestring

        # remove
        linestring.remove(p)
        assert p not in linestring

        # __setitem__, __getitem
        p = OGpointFromValues(100.0,200.0)
        linestring[2] = p
        assert linestring[2] == p

        # __delitem__
        del linestring[2]
        assert linestring[2] != p

        # __iter__
        for geo in linestring:
            assert geo.__class__ == OGPoint
        
    def testFactoryMethods(self):
        linestring = OGlineStringFromOGPoints(OGpointFromValues(1.0,2.0),
                                              OGpointFromValues(2.0,3.0))
        assert len(linestring) == 2
                
        linestring = OGlineStringFromSequence(((1.0,2.0),(2.0,3.0)))
        assert len(linestring) == 2

    def test_count(self):
        linestring1 = OGLineString()
        linestring1.append(OGpointFromValues(2.0,3.0))

        assert linestring1.count(OGpointFromValues(2.0,3.0)) == 1
        assert linestring1.count(OGpointFromValues(2.0,4.0)) == 0
       
    def test_index(self):
        linestring1 = OGLineString()
        linestring1.append(OGpointFromValues(2.0,3.0))

        assert linestring1.index(OGpointFromValues(2.0,3.0)) == 0
        try:
            linestring1.index(OGpointFromValues(2.0,4.0))
            assert 0, "Should have raised an exception"
        except ValueError:
            pass
            
    def test_og_str(self):
        linestring1 = OGLineString()
        linestring1.append(OGpointFromValues(2.0,3.0))
        assert linestring1._og_str() == "LINESTRING (2.000000 3.000000)", linestring1._og_str()
       
    def test_repr(self):
        linestring1 = OGLineString()
        linestring1.append(OGpointFromValues(2.0,3.0))
        assert repr(linestring1) == "(2.000000 3.000000)", repr(linestring1)

    def test_bad_eq(self):
        linestring1 = OGLineString()
        assert not linestring1 == 1
       
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGLineString)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGLineStringTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGLineString
            from _OGLineString import *

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
        x = coverage.analysis(_OGLineString)
        print "\n"
        coverage.report(_OGLineString)
