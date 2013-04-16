
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
import sys


try:
    import psycopg2 as psycopg
    import psycopg2.extensions as psyco_ext
except ImportError:
    import psycopg
    psyco_ext = None
import os
import TestConfig

if not os.environ.get('USECOVERAGE') == '1':
##    from _Point import *
##    from _LineSeg import *
##    from _Box import *
##    from _Path import *
##    from _Polygon import *
##    from _Circle import *
    import GeoTypes

            
from _PsycopgInit import initialisePsycopgTypes

initialisePsycopgTypes(psycopg_module=psycopg,
                       psycopg_extensions_module=psyco_ext)

conn = psycopg.connect('dbname=mq_test user=postgres')
curs = conn.cursor()


class GeoTypesPointTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_point_type"
        try:
            self.curs.execute("CREATE TABLE %s (p1 point, p2 point)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (p1 point, p2 point)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

        
    def testPoint(self):


        p1 = GeoTypes.pointFromValues(1.0,2.0)
        p2 = GeoTypes.pointFromValues(3.0,4.0)

        self.curs.execute("INSERT INTO %s VALUES (%%(p1)s, %%(p2)s)"  % (self.tbl_name,),
                          {'p1':p1, 'p2':p2})

        self.curs.execute("SELECT p1,p2 FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "Point"
        assert p4.__class__.__name__ == "Point"
        assert p3.getX() == 1.0
        assert p3.getY() == 2.0
        assert p4.getX() == 3.0
        assert p4.getY() == 4.0

class GeoTypesLineSegTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_lineseg_type"
        try:
            self.curs.execute("CREATE TABLE %s (l lseg)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (l lseg)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

    def testLineSeg(self):

        start = GeoTypes.pointFromValues(1.0,2.0)
        end = GeoTypes.pointFromValues(3.0,4.0)
        l = GeoTypes.lineSegFromPoints(start,end)

        self.curs.execute("INSERT INTO %s VALUES (%%(l)s)" % (self.tbl_name,),
                          {'l':l})

        self.curs.execute("SELECT l FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        ol = ret[0]
        assert ol.__class__.__name__ == "LineSeg"
        assert ol.getStart() == start
        assert ol.getEnd() == end
        assert ol == l

class GeoTypesBoxTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_box_type"
        try:
            self.curs.execute("CREATE TABLE %s (b box)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (b box)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

    def testBox(self):

        upper_right = GeoTypes.pointFromValues(2.0,2.0)
        lower_left = GeoTypes.pointFromValues(1.0,1.0)
        b = GeoTypes.boxFromPoints(upper_right,lower_left)

        self.curs.execute("INSERT INTO %s VALUES (%%(b)s)" % (self.tbl_name,),
                          {'b':b})

        self.curs.execute("SELECT b FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        ol = ret[0]
        assert ol.__class__.__name__ == "Box"
        assert ol.getUpperRight() == upper_right, "%s != %s" % (repr(ol.getUpperRight()),repr(upper_right))
        assert ol.getLowerLeft() == lower_left
        assert ol == b

    def testWrongCorners(self):
        """
        Check what happens if the upper_left and lower_right corner are
        specified.

        Postgres ourght to return the upper_right and lower_left anyway.
        """

        upper_right = GeoTypes.pointFromValues(2.0,2.0)
        lower_left = GeoTypes.pointFromValues(1.0,1.0)
        upper_left = GeoTypes.pointFromValues(1.0,2.0)
        lower_right = GeoTypes.pointFromValues(2.0,1.0)
        b = GeoTypes.boxFromPoints(upper_left,lower_right)
                

        self.curs.execute("INSERT INTO %s VALUES (%%(b)s)" % (self.tbl_name,),
                              {'b':b})

        self.curs.execute("SELECT b FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        ol = ret[0]

        assert ol.__class__.__name__ == "Box"
        assert ol.getUpperRight() == upper_right
        assert ol.getLowerLeft() == lower_left
        assert ol == b, ("Broken box equallity", ol, b)


class GeoTypesPathTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_path_type"
        try:
            self.curs.execute("CREATE TABLE %s (p path)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (p path)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

    def testPath(self):

        p1 = GeoTypes.pointFromValues(1.0,2.0)
        p2 = GeoTypes.pointFromValues(3.0,4.0)
        p3 = GeoTypes.pointFromValues(5.0,6.0)
        path = GeoTypes.pathFromPoints(p1,p2,p3)

        self.curs.execute("INSERT INTO %s VALUES (%%(p)s)" % (self.tbl_name,),
                          {'p':path})

        self.curs.execute("SELECT p FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        op = ret[0]
        assert op.__class__.__name__ == "Path"
        assert op == path

class GeoTypesPolygonTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_polygon_type"
        try:
            self.curs.execute("CREATE TABLE %s (p polygon)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (p polygon)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

    def testPath(self):

        p1 = GeoTypes.pointFromValues(1.0,2.0)
        p2 = GeoTypes.pointFromValues(3.0,4.0)
        p3 = GeoTypes.pointFromValues(5.0,6.0)
        polygon = GeoTypes.polygonFromPoints(p1,p2,p3)

        self.curs.execute("INSERT INTO %s VALUES (%%(p)s)" % (self.tbl_name,),
                          {'p':polygon})

        self.curs.execute("SELECT p FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        op = ret[0]
        assert op.__class__.__name__ == "Polygon"
        assert op == polygon


class GeoTypesCircleTest(unittest.TestCase):    

    def setUp(self):
        self.curs = curs
        self.tbl_name = "test_circle_type"
        try:
            self.curs.execute("CREATE TABLE %s (c circle)" % (self.tbl_name,))
        except:
            conn.rollback()
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))
            self.curs.execute("CREATE TABLE %s (c circle)" % (self.tbl_name,))
        conn.commit()

    def tearDown(self):
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name,))

    def testCircle(self):

        centre = GeoTypes.pointFromValues(1.0,1.0)
        radius = 5
        c = GeoTypes.circleFromCentreAndRadius(centre,radius)

        self.curs.execute("INSERT INTO %s VALUES (%%(c)s)" % (self.tbl_name,),
                          {'c':c})

        self.curs.execute("SELECT c FROM %s" % (self.tbl_name,))

        ret = self.curs.fetchall()[0]

        oc = ret[0]
        assert oc.__class__.__name__ == "Circle"
        assert oc.getCentre() == centre
        assert oc.getRadius() == radius
        assert oc == c

    def testzzz_CoverageAssertion(self):
        try:
            coverage.stop()
        except:
            return 1
        
        x = coverage.analysis(GeoTypes)
        assert x[2]==[], "Coverage is less than 100%"

def testSuite():
    return unittest.TestSuite((
        unittest.makeSuite(GeoTypesPointTest,'test'),
        unittest.makeSuite(GeoTypesLineSegTest,'test'),
        unittest.makeSuite(GeoTypesBoxTest,'test'),
        unittest.makeSuite(GeoTypesPathTest,'test'),
        unittest.makeSuite(GeoTypesPolygonTest,'test'),
        unittest.makeSuite(GeoTypesCircleTest,'test')
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


