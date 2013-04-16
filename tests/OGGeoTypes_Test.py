
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
                       register_opengis_types=1,psycopg_extensions_module=psyco_ext)

conn = psycopg.connect('dbname=%s user=postgres' % (dbname,))
curs = conn.cursor()

class OGGeoTypesTestBase(unittest.TestCase):

    def _setUp(self,type):
        self.curs = curs
        self.tbl_name_2d = "test_og_point_type2d"
        self.tbl_name_3d = "test_og_point_type3d"
        
        try:
            conn.rollback()
            self.curs.execute("CREATE TABLE %s (dummy int)" % (self.tbl_name_2d,))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p1', 128, '%s', 2 )" % (dbname,self.tbl_name_2d,type))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p2', 128, '%s', 2 )" % (dbname,self.tbl_name_2d,type))
            self.curs.execute("CREATE TABLE %s (dummy int)" % (self.tbl_name_3d,))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p1', 128, '%s', 3 )" % (dbname,self.tbl_name_3d,type))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p2', 128, '%s', 3 )" % (dbname,self.tbl_name_3d,type))
        except:
##            print "Exception in setUp code1:"
##            print '-'*60
##            traceback.print_exc(file=sys.stdout)
##            print '-'*60
            conn.rollback()
            try:
                self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p1' )" % (dbname,self.tbl_name_2d,))
                self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p2' )" % (dbname,self.tbl_name_2d,))
                self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p1' )" % (dbname,self.tbl_name_3d,))
                self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p2' )" % (dbname,self.tbl_name_3d,))
            except:
                print "Exception in setUp code2:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                conn.rollback()
                
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name_2d,))
            self.curs.execute("DROP TABLE %s"  % (self.tbl_name_3d,))
            conn.commit()
            self.curs.execute("CREATE TABLE %s (dummy int)" % (self.tbl_name_2d,))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p1', 128, '%s', 2 )" % (dbname,self.tbl_name_2d,type))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p2', 128, '%s', 2 )" % (dbname,self.tbl_name_2d,type))
            self.curs.execute("CREATE TABLE %s (dummy int)" % (self.tbl_name_3d,))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p1', 128, '%s', 3 )" % (dbname,self.tbl_name_3d,type))
            self.curs.execute("SELECT AddGeometryColumn('%s', '%s', 'p2', 128, '%s', 3 )" % (dbname,self.tbl_name_3d,type))
        conn.commit()

    def _tearDown(self):
        conn.rollback()
        try:
            self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p1' )" % (dbname,self.tbl_name_2d,))
            self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p2' )" % (dbname,self.tbl_name_2d,))
            self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p1' )" % (dbname,self.tbl_name_3d,))
            self.curs.execute("SELECT DropGeometryColumn('%s', '%s', 'p2' )" % (dbname,self.tbl_name_3d,))
        except:
            print "Exception in tearDown code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            conn.rollback()
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name_2d,))
        self.curs.execute("DROP TABLE %s"  % (self.tbl_name_3d,))
        conn.commit()

    def _sub_test2dWKB(self,p1,p2):
        self.curs.execute("INSERT INTO %s (p1,p2) VALUES (%%(p1)s, %%(p2)s)"  % (self.tbl_name_2d,),
                          {'p1':p1, 'p2':p2})


        self.curs.execute("""DECLARE zot BINARY CURSOR FOR SELECT p1,p2 FROM %s
                                           FOR READ ONLY""" % (self.tbl_name_2d,))
        self.curs.execute("""FETCH ALL FROM zot""")

        raw = self.curs.fetchall()

        conn.commit()

        return raw


    def _sub_test3dWKB(self,p1,p2):
        self.curs.execute("INSERT INTO %s (p1,p2) VALUES (%%(p1)s, %%(p2)s)"  % (self.tbl_name_3d,),
                          {'p1':p1, 'p2':p2})

        self.curs.execute("""DECLARE zot BINARY CURSOR FOR SELECT p1,p2 FROM %s
                                           FOR READ ONLY""" % (self.tbl_name_3d,))
        self.curs.execute("""FETCH ALL FROM zot""")
        raw = self.curs.fetchall()
        conn.commit()
                
        return raw

    def _sub_test2dWKT(self,p1,p2):
        self.curs.execute("INSERT INTO %s (p1,p2) VALUES (%%(p1)s, %%(p2)s)"  % (self.tbl_name_2d,),
                          {'p1':p1, 'p2':p2})

        self.curs.execute("SELECT p1,p2 FROM %s" % (self.tbl_name_2d,))

        return  self.curs.fetchall()

    def _sub_test3dWKT(self,p1,p2):

        self.curs.execute("INSERT INTO %s (p1,p2) VALUES (%%(p1)s, %%(p2)s)"  % (self.tbl_name_3d,),
                          {'p1':p1, 'p2':p2})

        self.curs.execute("SELECT p1,p2 FROM %s" % (self.tbl_name_3d,))

        return self.curs.fetchall()


###########################  Point #############################################
        
class OGGeoTypesPointTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('POINT')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):

        p1 = GeoTypes.OGpointFromValues(1.0,2.0)
        p2 = GeoTypes.OGpointFromValues(3.0,4.0)

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]
        
        assert p3.__class__.__name__ == "OGPoint"
        assert p4.__class__.__name__ == "OGPoint"
        assert p3.getX() == 1.0
        assert p3.getY() == 2.0
        assert p4.getX() == 3.0
        assert p4.getY() == 4.0

    def run3d(self,test_func):

        p1 = GeoTypes.OGpointFromValues(1.0,2.0,3.0)
        p2 = GeoTypes.OGpointFromValues(4.0,5.0,6.0)

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGPoint"
        assert p4.__class__.__name__ == "OGPoint"
        assert p3.getX() == 1.0
        assert p3.getY() == 2.0
        assert p3.getZ() == 3.0
        assert p4.getX() == 4.0
        assert p4.getY() == 5.0
        assert p4.getZ() == 6.0
  
    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)
    
      

################################# LineString ######################################################
    
class OGGeoTypesLineStringTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('LINESTRING')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):

        p1 = GeoTypes.OGlineStringFromSequence(((1.0,2.0),(3.0,4.0)))
        p2 = GeoTypes.OGlineStringFromSequence(((5.0,6.0),(7.0,8.0)))

        raw = test_func(self,p1,p2)
        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGLineString"
        assert p4.__class__.__name__ == "OGLineString"
        assert p3[0].getX() == 1.0
        assert p3[0].getY() == 2.0
        assert p3[1].getX() == 3.0
        assert p3[1].getY() == 4.0
        assert p4[0].getX() == 5.0
        assert p4[0].getY() == 6.0

    def run3d(self,test_func):

        p1 = GeoTypes.OGlineStringFromSequence(((1.0,2.0,9.0),(3.0,4.0,10.0)))
        p2 = GeoTypes.OGlineStringFromSequence(((5.0,6.0,11.0),(7.0,8.0,12.0)))

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGLineString"
        assert p4.__class__.__name__ == "OGLineString"
        assert p3[0].getX() == 1.0
        assert p3[0].getY() == 2.0
        assert p3[0].getZ() == 9.0
        assert p4[0].getX() == 5.0
        assert p4[0].getY() == 6.0
        assert p4[0].getZ() == 11.0

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)
    

        

############################### Polygon ######################################################
    
class OGGeoTypesPolygonTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('POLYGON')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):

        p1 = GeoTypes.OGpolygonFromOGLines(
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2),
                    GeoTypes.OGpointFromValues(2,2),
                    GeoTypes.OGpointFromValues(2,1),
                    GeoTypes.OGpointFromValues(1,2),
                    ),
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2),
                    GeoTypes.OGpointFromValues(2,2),
                    GeoTypes.OGpointFromValues(2,1),
                    GeoTypes.OGpointFromValues(1,2),
                    )
            )

        p2 = GeoTypes.OGpolygonFromOGLines(
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    ),
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    )
            )
        
        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGPolygon"
        assert p4.__class__.__name__ == "OGPolygon"

    def run3d(self,test_func):

        p1 = GeoTypes.OGpolygonFromOGLines(
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    ),
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    )
            )

        p2 = GeoTypes.OGpolygonFromOGLines(
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4,3),
                    GeoTypes.OGpointFromValues(4,4,3),
                    GeoTypes.OGpointFromValues(4,3,3),
                    GeoTypes.OGpointFromValues(3,4,3),
                    ),
            GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4,3),
                    GeoTypes.OGpointFromValues(4,4,3),
                    GeoTypes.OGpointFromValues(4,3,3),
                    GeoTypes.OGpointFromValues(3,4,3),
                    )
            )

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGPolygon"
        assert p4.__class__.__name__ == "OGPolygon"

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)
    




########################## MultiPoint ##################################################
    

class OGGeoTypesMultiPointTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('MULTIPOINT')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):

        p1 = GeoTypes.OGmultiPointFromSequence(((1.0,2.0),(3.0,4.0)))
        p2 = GeoTypes.OGmultiPointFromSequence(((5.0,6.0),(7.0,8.0)))

        raw = test_func(self,p1,p2)
        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiPoint"
        assert p4.__class__.__name__ == "OGMultiPoint"
    
        assert p3[0].getX() == 1.0, "failed p3[0].getX() != %s" % str(p3[0].getX())
        assert p3[0].getY() == 2.0
        assert p3[1].getX() == 3.0
        assert p3[1].getY() == 4.0
        assert p4[0].getX() == 5.0
        assert p4[0].getY() == 6.0

    def run3d(self,test_func):

        p1 = GeoTypes.OGmultiPointFromSequence(((1.0,2.0,9.0),(3.0,4.0,10.0)))
        p2 = GeoTypes.OGmultiPointFromSequence(((5.0,6.0,11.0),(7.0,8.0,12.0)))

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiPoint"
        assert p4.__class__.__name__ == "OGMultiPoint"
        assert p3[0].getX() == 1.0
        assert p3[0].getY() == 2.0
        assert p3[0].getZ() == 9.0
        assert p4[0].getX() == 5.0
        assert p4[0].getY() == 6.0
        assert p4[0].getZ() == 11.0

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)
    

    

################### MultiLineString ###########################################

class OGGeoTypesMultiLineStringTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('MULTILINESTRING')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):
        
        p1 = GeoTypes.OGmultiLineStringFromOGLineStrings(
            GeoTypes.OGlineStringFromSequence(((1.0,2.0),(3.0,4.0))),
            GeoTypes.OGlineStringFromSequence(((5.0,6.0),(7.0,8.0))))
        p2 = GeoTypes.OGmultiLineStringFromOGLineStrings(
            GeoTypes.OGlineStringFromSequence(((1.0,2.0),(3.0,4.0))),
            GeoTypes.OGlineStringFromSequence(((5.0,6.0),(7.0,8.0))))

        raw = test_func(self,p1,p2)
        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiLineString"
        assert p4.__class__.__name__ == "OGMultiLineString"

    def run3d(self,test_func):
        
        p1 = GeoTypes.OGmultiLineStringFromOGLineStrings(
            GeoTypes.OGlineStringFromSequence(((1.0,2.0,9.0),(3.0,4.0,10.0))),
            GeoTypes.OGlineStringFromSequence(((5.0,6.0,11.0),(7.0,8.0,12.0))))
        p2 = GeoTypes.OGmultiLineStringFromOGLineStrings(
            GeoTypes.OGlineStringFromSequence(((1.0,2.0,9.0),(3.0,4.0,10.0))),
            GeoTypes.OGlineStringFromSequence(((5.0,6.0,11.0),(7.0,8.0,12.0))))

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiLineString"
        assert p4.__class__.__name__ == "OGMultiLineString"

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)
    
################### MultiPolygon ###############################################

class OGGeoTypesMultiPolygonTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('MULTIPOLYGON')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):
        
        p1 = GeoTypes.OGmultiPolygonFromOGPolygons(
              GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    )
                 ),
               GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    )
                 )
               )

        p2 = p1

        raw = test_func(self,p1,p2)
        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiPolygon"
        assert p4.__class__.__name__ == "OGMultiPolygon"

    def run3d(self,test_func):

        p1 = GeoTypes.OGmultiPolygonFromOGPolygons(
               GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    )
                 ),
              GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4,3),
                    GeoTypes.OGpointFromValues(4,4,3),
                    GeoTypes.OGpointFromValues(4,3,3),
                    GeoTypes.OGpointFromValues(3,4,3),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4,3),
                    GeoTypes.OGpointFromValues(4,4,3),
                    GeoTypes.OGpointFromValues(4,3,3),
                    GeoTypes.OGpointFromValues(3,4,3),
                    )
                 )
               )
               
        p2 = p1

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGMultiPolygon"
        assert p4.__class__.__name__ == "OGMultiPolygon"

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)


##################### GeometryCollection ##########################################

class OGGeoTypesGeometryCollectionTestBase(OGGeoTypesTestBase):    

    def setUp(self):
        self._setUp('GEOMETRYCOLLECTION')
        
    def tearDown(self):
        self._tearDown
        
    def run2d(self,test_func):
        
        p1 = GeoTypes.OGgeometryCollectionFromOGGeometries(

              #  A Polyon
            
              GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(3,4),
                    GeoTypes.OGpointFromValues(4,4),
                    GeoTypes.OGpointFromValues(4,3),
                    GeoTypes.OGpointFromValues(3,4),
                    )
                 ),

                # A Linearing
              
              GeoTypes.OGlinearRingFromOGPoints(
                 GeoTypes.OGpointFromValues(3,4),
                 GeoTypes.OGpointFromValues(4,4),
                 GeoTypes.OGpointFromValues(4,3),
                 GeoTypes.OGpointFromValues(3,4),
                 ),

               )

        p2 = p1

        raw = test_func(self,p1,p2)
        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGGeometryCollection"
        assert p4.__class__.__name__ == "OGGeometryCollection"

    def run3d(self,test_func):

        p1 = GeoTypes.OGgeometryCollectionFromOGGeometries(
            
               # A Polygon
            
               GeoTypes.OGpolygonFromOGLines(
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    ),
                 GeoTypes.OGlinearRingFromOGPoints(
                    GeoTypes.OGpointFromValues(1,2,3),
                    GeoTypes.OGpointFromValues(2,2,3),
                    GeoTypes.OGpointFromValues(2,1,3),
                    GeoTypes.OGpointFromValues(1,2,3),
                    )
                 ),

               # A Linear Ring
               GeoTypes.OGlinearRingFromOGPoints(
                 GeoTypes.OGpointFromValues(3,4,3),
                 GeoTypes.OGpointFromValues(4,4,3),
                 GeoTypes.OGpointFromValues(4,3,3),
                 GeoTypes.OGpointFromValues(3,4,3),
                 ),
               )
               
        p2 = p1

        raw = test_func(self,p1,p2)

        ret = raw[0]

        p3 = ret[0]
        p4 = ret[1]

        assert p3.__class__.__name__ == "OGGeometryCollection"
        assert p4.__class__.__name__ == "OGGeometryCollection"

    def test3dWKB(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKB)

    def test3dWKT(self):
        self.run3d(OGGeoTypesTestBase._sub_test3dWKT)

    def test2dWKB(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKB)

    def test2dWKT(self):
        self.run2d(OGGeoTypesTestBase._sub_test2dWKT)


def testSuite():
    return unittest.TestSuite((
        unittest.makeSuite(OGGeoTypesPointTestBase,'test'),
        unittest.makeSuite(OGGeoTypesLineStringTestBase,'test'),
        unittest.makeSuite(OGGeoTypesPolygonTestBase,'test'),
        unittest.makeSuite(OGGeoTypesMultiPointTestBase,'test'),
        unittest.makeSuite(OGGeoTypesMultiLineStringTestBase,'test'),
        unittest.makeSuite(OGGeoTypesMultiPolygonTestBase,'test'),
        unittest.makeSuite(OGGeoTypesGeometryCollectionTestBase,'test'),
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


