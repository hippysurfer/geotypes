
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import sys, traceback

try:
    import psycopg2 as psycopg
    import psycopg2.extensions as psyco_ext
except ImportError:
    import psycopg
    psyco_ext = None
import os

import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
    import GeoTypes

            
from _PsycopgInit import initialisePsycopgTypes

dbname='mq_test'

initialisePsycopgTypes(psycopg_module=psycopg,connect_string='dbname=%s user=postgres' % (dbname,),
                       register_opengis_types=None,psycopg_extensions_module=psyco_ext)

conn = psycopg.connect('dbname=%s user=postgres' % (dbname,))
curs = conn.cursor()

class EWKBParserTestBase(unittest.TestCase):

      
    def _testPoint2d(self):
        geo = self._getGeom('SRID=4;POINT(0 0)')
        
        assert geo.__class__.__name__ == "OGPoint"
        assert geo.SRID() == 4

    def _testPoint3d(self):
        geo = self._getGeom('SRID=4;POINT(1.0 2.0 3.0)')
        
        assert geo.__class__.__name__ == "OGPoint"
        assert geo.getZ() == 3.0
        assert geo.SRID() == 4

    def _testLineString(self):
        geo = self._getGeom('SRID=4;LINESTRING(0 0,1 1,1 2)')
        
        assert geo.__class__.__name__ == "OGLineString"
        assert geo.SRID() == 4

    def _testLineString3d(self):
        geo = self._getGeom('SRID=4;LINESTRING(0 0 3.0,1 1 1,1 2 3)')
        
        assert geo.__class__.__name__ == "OGLineString"
        assert geo[0].getZ() == 3.0
        assert geo.SRID() == 4

    def _testPolygon(self):
        geo = self._getGeom('SRID=4;POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1, 2 1, 2 2, 1 2,1 1))')
        
        assert geo.__class__.__name__ == "OGPolygon"
        assert geo.SRID() == 4

    def _testPolygon3d(self):
        geo = self._getGeom('SRID=4;POLYGON((0 0 3.0,4 0 4,4 4 4,0 4 4,0 0 3.0),(1 1 4, 2 1 4, 2 2 4, 1 2 4,1 1 4))')
        
        assert geo.__class__.__name__ == "OGPolygon"
        assert geo.SRID() == 4

    def _testMultiPoint(self):
        geo = self._getGeom('SRID=4;MULTIPOINT(0 0,1 2)')
        
        assert geo.__class__.__name__ == "OGMultiPoint"
        assert geo.SRID() == 4

    def _testMultiPoint3d(self):
        geo = self._getGeom('SRID=4;MULTIPOINT(0 0 3.0,1 2 3.0)')
        
        assert geo.__class__.__name__ == "OGMultiPoint"
        assert geo.SRID() == 4

    def _testMultiLineString(self):
        geo = self._getGeom('SRID=4;MULTILINESTRING((0 0,1 1,1 2),(2 3,3 2,5 4))')
        
        assert geo.__class__.__name__ == "OGMultiLineString"
        assert geo.SRID() == 4

    def _testMultiLineString3d(self):
        geo = self._getGeom('SRID=4;MULTILINESTRING((0 0 0,1 1 1,1 2 2),(2 3 3,3 2 4,5 4 5))')
        
        assert geo.__class__.__name__ == "OGMultiLineString"
        assert geo.SRID() == 4

    def _testMultiPolygon(self):
        geo = self._getGeom('SRID=4;MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))')
        
        assert geo.__class__.__name__ == "OGMultiPolygon"
        assert geo.SRID() == 4

    def _testMultiPolygon3d(self):
        geo = self._getGeom('SRID=4;MULTIPOLYGON(((0 0 0,4 0 4,4 4 4,0 4 4,0 0 0),(1 1 1,2 1 1,2 2 1,1 2 3,1 1 1)), ((-1 -1 -1,-1 -2 -1,-2 -2 -2,-2 -1 -2,-1 -1 -1)))')
        
        assert geo.__class__.__name__ == "OGMultiPolygon"
        assert geo.SRID() == 4

    def _testGeometryCollection(self):
        geo = self._getGeom('SRID=4;GEOMETRYCOLLECTION(POINT(2 3))')
        
        assert geo.__class__.__name__ == "OGGeometryCollection"
        assert geo.SRID() == 4


class EWKBParserTest(EWKBParserTestBase):

    def setUp(self):
        self.factory = GeoTypes.OGGeoTypeFactory()
        self.parser = GeoTypes.EWKBParser(self.factory)
    
    def _tearDown(self):
        pass
    

    def _getGeom(self,query):
        try:
            curs.execute("""DECLARE zot BINARY CURSOR FOR SELECT '%s'::geometry FOR READ ONLY""" \
                         % (query,))
            curs.execute("""FETCH ALL FROM zot""")
            f = curs.fetchall()
            self.parser.parseGeometry(f[0][0])
        finally:
            conn.commit()

        return self.factory.getGeometry()

    testPoint2d = EWKBParserTestBase._testPoint2d

    testPoint3d = EWKBParserTestBase._testPoint3d

    testLineString = EWKBParserTestBase._testLineString

    testLineString3d = EWKBParserTestBase._testLineString3d

    testPolygon = EWKBParserTestBase._testPolygon

    testPolygon3d = EWKBParserTestBase._testPolygon3d

    testMultiPoint = EWKBParserTestBase._testMultiPoint

    testMultiPoint3d = EWKBParserTestBase._testMultiPoint3d

    testMultiLineString = EWKBParserTestBase._testMultiLineString

    testMultiLineString3d = EWKBParserTestBase._testMultiLineString3d

    testMultiPolygon = EWKBParserTestBase._testMultiPolygon

    testMultiPolygon3d = EWKBParserTestBase._testMultiPolygon3d

    testGeometryCollection = EWKBParserTestBase._testGeometryCollection

class HEXEWKBParserTest(EWKBParserTestBase):

    def setUp(self):
        self.factory = GeoTypes.OGGeoTypeFactory()
        self.parser = GeoTypes.HEXEWKBParser(self.factory)
    
    def _tearDown(self):
        pass
    

    def _getGeom(self,query):
        try:
            curs.execute("""SELECT '%s'::geometry""" \
                         % (query,))
            f = curs.fetchall()
            self.parser.parseGeometry(f[0][0])
        finally:
            conn.commit()

        return self.factory.getGeometry()

    testPoint2d = EWKBParserTestBase._testPoint2d

    testPoint3d = EWKBParserTestBase._testPoint3d

    testLineString = EWKBParserTestBase._testLineString

    testLineString3d = EWKBParserTestBase._testLineString3d

    testPolygon = EWKBParserTestBase._testPolygon

    testPolygon3d = EWKBParserTestBase._testPolygon3d

    testMultiPoint = EWKBParserTestBase._testMultiPoint

    testMultiPoint3d = EWKBParserTestBase._testMultiPoint3d

    testMultiLineString = EWKBParserTestBase._testMultiLineString

    testMultiLineString3d = EWKBParserTestBase._testMultiLineString3d

    testMultiPolygon = EWKBParserTestBase._testMultiPolygon

    testMultiPolygon3d = EWKBParserTestBase._testMultiPolygon3d

    testGeometryCollection = EWKBParserTestBase._testGeometryCollection

def testSuite():
    return unittest.TestSuite((
        unittest.makeSuite(EWKBParserTest,'test'),
        unittest.makeSuite(HEXEWKBParserTest,'test'),
        ))

if __name__ == "__main__":
    import os
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import GeoTypes          

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
        x = coverage.analysis(GeoTypes)
        print "\n"
        coverage.report(GeoTypes)


