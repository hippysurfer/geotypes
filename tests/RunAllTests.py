################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest

import sys
sys.path = sys.path + ['../GeoTypes']

test_modules = ['Box_Test',
                'Circle_Test',
                'LineSeg_Test',
                'Path_Test',
                'Point_Test',
                'Polygon_Test',
                'OGPoint_Test',
                'OGLineString_Test',
                'OGLinearRing_Test',
                'OGGeometryCollection_Test',
		'OGMultiPoint_Test',
		'OGMultiLineString_Test',
		'OGMultiPolygon_Test',
                'GeoTypes_Test',
                'OGGeoTypes_Test',
                'PsycopgInit_Test']

testloader = unittest.TestLoader()
testsuite = unittest.TestSuite()

for test in test_modules:
    module = __import__(test)
    testsuite.addTest(testloader.loadTestsFromModule(module))



unittest.TextTestRunner().run(testsuite)
