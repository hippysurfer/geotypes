
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import os

import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import _OGLinearRing
    from _OGLinearRing import *

from _OGGeometry import OGGeometry
from _OGPoint import OGPoint, OGpointFromValues

class OGLinearRingTest(unittest.TestCase):    
    def testFactoryMethods(self):
        linearring = OGlinearRingFromOGPoints(OGpointFromValues(1.0,2.0),
                                              OGpointFromValues(2.0,3.0))
        assert len(linearring) == 2
                
        linearring = OGlinearRingFromSequence(((1.0,2.0),(2.0,3.0)))
        assert len(linearring) == 2

        assert repr(linearring) == '(1.000000 2.000000,2.000000 3.000000)', repr(linearring)
        
    def testzzz_CoverageAssertion(self):
            try:
                coverage.stop()
            except:
                return 1

            x = coverage.analysis(_OGLinearRing)
            assert x[2]==[], "Coverage is less than 100%"


def testSuite():
    return unittest.makeSuite(OGLinearRingTest,'test')

if __name__ == "__main__":
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _OGLinearRing
            from _OGLinearRing import *

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
        x = coverage.analysis(_OGLinearRing)
        print "\n"
        coverage.report(_OGLinearRing)
