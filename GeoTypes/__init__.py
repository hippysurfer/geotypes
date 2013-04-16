
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
#
# 2005, dec 5: corrected typo (Fred, fredericback@gmail.com)
#
################################################################################

"""
Package of classes for working with OpenGIS classes in PostGIS and
basic postgres 2d geometric types.

These classes were designed for use with the geometric functions
supported by Postgresql (http://www.postgresql.com) although they
do not need Postgresql to be present for the classes to be used.

The basic 2d types implemented are those listed in the Postgresql documentation
at http://www.postgresql.org/docs/7.3/static/datatype-geometric.html with
the exception of 'line' which, as the documentation is says, is 'not fully
implemented yet'.

The package exports the following classes:

    (class Point)
    (class LineSeg)
    (class Path)
    (class Polygon)
    (class Circle)
    (class box)

In addition the following factory methods are provided to make construction
of these classes easier:

    (func pointFromValues)
    (func pointFromSequence)
    (func lineSegFromPoints)
    (func lineSegFromSequence)
    (func pathFromPoints)
    (func pathFromSequence)
    (func boxFromPoints)
    (func boxFromSequence)
    (func circleFromCentreAndRadius)
    (func circelFromSequence)
    (func polygonFromPoints)
    (func polygonFromSequence)

The OpenGIS classes implemented are documented at
http://postgis.refractions.net/docs/ch04.html#RefObject

Supported OpenGIS classes are:

    (class OGMultiPolygon)
    (class OGPoint)
    (class OGLineString)
    (class OGLinearRing)
    (class OGPolygon)
    (class OGMultiPoint)
    (class OGMultiLineString)
    (class OGGeometryCollection)

    * these classes support SRID, (x,y) and (x,y,z) variants but there
    is currently no support for (x,y,m) or (x,y,z,m) variants.
    
Factory methods for OpenGIS classes

    (func OGpointFromValues)
    (func OGpointFromSequence)
    (func OGlineStringFromOGPoints)
    (func OGlineStringFromSequence)
    (func OGlinearRingFromOGPoints)
    (func OGlinearRingFromSequence)
    (func OGpolygonFromOGLines)
    (func OGpolygonFromSequence)
    (func OGmultiPointFromOGPoints)
    (func OGmultiPointFromSequence)
    (func OGmultiLineStringFromOGLineStrings)
    (func OGmultiLineStringFromSequence)
    (func OGmultiPolygonFromOGPolygons)
    (func OGmultiPolygonFromSequence)
    (func OGgeometryCollectionFromOGGeometries)

The OpenGIS format parsers are available as:

    (class OGGeoTypeFactory)
    (class EWKBParser)
    (class HEXEWKBParer)
    (class WKTParser)
    (class WKBParser)
    
One final method is provided to help with linking these classes into psycopg
(http://initd.org/software/initd/psycopg) database wrapper:

    (func initialisePsycopgTypes)

Example usage:

    import psycopg
    import GeoTypes

    connect_string='dbname=schema_test user=postgres'
    GeoTypes.initialisePsycopgTypes(psycopg_module=psycopg,
                                    connect_string=connect_string,
                                    register_opengis_types=True)

    conn = psycopg.connect(connect_string)
    curs = conn.cursor()

    curs.execute("CREATE TABLE table_name (p1 point, b box)")

    p = GeoTypes.pointFromValues(5.0,7.0)
    b = GeoTypes.boxFromPoints(p,GeoTypes.pointFromValues(1.0,1.0))

    curs.execute("INSERT INTO table_name VALUES (%(p)s,%(b)s)", {'p':p, 'b':b})


    curs.execute("SELECT p1, b FROM table_name WHERE (p1 ~= %(p)s)", {'p':p})

    ret = curs.fetchall()[0]

    new_point = ret[0]
    new_box   = ret[1]

    if new_box == b:
        print "We have the same box!"


To use a binary cursor:

    curs.execute("DECLARE zot BINARY CURSOR FOR SELECT p1,b FROM table_name
                                           FOR READ ONLY")
    curs.execute("FETCH ALL FROM zot")

    raw = curs.fetchall()

    conn.commit()

Using the parser without hooking in to psycopg.

You can parse the EWKT or EWKB formats manually if you do not want to use
the psycopg implicit casting machinery.

Example:

    import GeoTypes
    import psycopg
    
    conn = psycopg.connect('dbname=mq_test')
    curs = conn.cursor()
    
    factory = GeoTypes.OGGeoTypeFactory()
    parser = GeoTypes.WKTParser(factory)
    
    curs.execute("select AsEWKT(p1) from test");
    f = curs.fetchall()
    
    parser.parseGeometry(f[0][0])
    geom = factory.getGeometry()

"""

# Main (default) Postgres classes

from _Point import Point
from _LineSeg import LineSeg
from _Path import Path
from _Polygon import Polygon
from _Circle import Circle
from _Box import Box


# Useful factory methods


from _Point   import pointFromValues,           pointFromSequence
from _LineSeg import lineSegFromPoints,         lineSegFromSequence
from _Path    import pathFromPoints,            pathFromSequence
from _Box     import boxFromPoints,             boxFromSequence
from _Circle  import circleFromCentreAndRadius, circelFromSequence
from _Polygon import polygonFromPoints,         polygonFromSequence


# Psycopg initialisation support

from _PsycopgInit import initialisePsycopgTypes

# OpenGIS classes

from _OGGeometry import OGGeometry
from _OGMultiPolygon import OGMultiPolygon
from _OGPoint import OGPoint
from _OGLineString import OGLineString
from _OGLinearRing import OGLinearRing
from _OGPolygon import OGPolygon
from _OGMultiPoint import OGMultiPoint
from _OGMultiLineString import OGMultiLineString
from _OGGeometryCollection import OGGeometryCollection

# OpenGIS factory methods
from _OGPoint       import OGpointFromValues,        OGpointFromSequence
from _OGLineString import  OGlineStringFromOGPoints, OGlineStringFromSequence
from _OGLinearRing import  OGlinearRingFromOGPoints, OGlinearRingFromSequence
from _OGPolygon    import  OGpolygonFromOGLines,     OGpolygonFromSequence
from _OGMultiPoint import  OGmultiPointFromOGPoints, OGmultiPointFromSequence
from _OGMultiLineString import  OGmultiLineStringFromOGLineStrings, OGmultiLineStringFromSequence
from _OGMultiPolygon import  OGmultiPolygonFromOGPolygons, OGmultiPolygonFromSequence
from _OGGeometryCollection import OGgeometryCollectionFromOGGeometries

# Direct access to parsers
from _OGGeoTypeFactory import OGGeoTypeFactory
from _EWKBParser import EWKBParser, HEXEWKBParser
from _WKTParser import WKTParser
from _WKBParser import WKBParser
