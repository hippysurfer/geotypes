
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Initialisation support for hooking the GeoTypes into the psycopg typecast machinery.
"""
import sys, traceback,re

from _Point import Point
from _LineSeg import LineSeg
from _Path import Path
from _Polygon import Polygon
from _Circle import Circle
from _Box import Box

_class_map = {'point':   {'class': Point, 'oid': 600, 'name': 'POINT'},
              'lseg':    {'class': LineSeg, 'oid': 601, 'name': 'LINESEG'},
              'path':    {'class': Path,  'oid': 602, 'name': 'PATH'},
              'polygon': {'class': Polygon, 'oid': 604, 'name': 'POLYGON'},
              'circle':  {'class': Circle, 'oid': 718, 'name': 'CIRCLE'},
              'box':     {'class': Box, 'oid': 603, 'name': 'BOX'}}

from _OGMultiPolygon import OGMultiPolygon
from _OGPoint import OGPoint
from _OGLineString import OGLineString
from _OGPolygon import OGPolygon
from _OGMultiPoint import OGMultiPoint
from _OGMultiLineString import OGMultiLineString
from _OGGeometryCollection import OGGeometryCollection
from _OGGeoTypeFactory import OGGeoTypeFactory
from _WKTParser import WKTParser
from _WKBParser import WKBParser
from _EWKBParser import EWKBParser, HEXEWKBParser

class _PostWKTGISClassFactory:
    """
    Private class used as a factory for OpenGID types.
    """
    def __init__(self):
        pass
    
    def __call__(self,s=None):
        """
        A factory method for creating objects of the correct OpenGIS type.
        """
        factory = OGGeoTypeFactory()
        parser = WKTParser(factory)
        parser.parseGeometry(s)

        return factory.getGeometry()

class _PostWKBGISClassFactory:
    """
    Private class used as a factory for OpenGID types.
    """
    def __init__(self):
        pass
    
    def __call__(self,s=None):
        """
        A factory method for creating objects of the correct OpenGIS type.
        """
        factory = OGGeoTypeFactory()
        parser = WKBParser(factory)
        parser.parseGeometry(s)

        return factory.getGeometry()

class _PostHEXEWKBGISClassFactory:
    """
    Private class used as a factory for OpenGID types.
    """
    def __init__(self):
        pass
    
    def __call__(self,s=None,c=None):
        """
        A factory method for creating objects of the correct OpenGIS type.
        """
        factory = OGGeoTypeFactory()

        # We need to know whether the format of the s is EWKB or HEXEWKB
        # there is no full proof way of doing this so we take a guess
        # In all the cases I have seen the ord of the byte word of an
        # EWKB string is below 32. Because HEXEWKB is a text string it
        # is not possible for the ord of the first character to be below
        # 32. So this is the best way I have.
        try:
            if ord(s[0]) < 32:
                parser = EWKBParser(factory)
            else:
                parser = HEXEWKBParser(factory)
        except:
            # catch the very rare case where s[0] would fail because of the
            # size of the string
            parser = HEXEWKBParser(factory)

        parser.parseGeometry(s)
        return factory.getGeometry()


def _getPostgisVersion(conn,curs):
    """returns the postgis version as (major,minor,patch)"""
    curs.execute("select postgis_full_version()")    
    conn.commit()
    m = re.compile('POSTGIS="([^"]*)"').match(curs.fetchall()[0][0])
    return m.group(1).split('.')
    
def _getTypeOid(conn,curs,typename):
    curs.execute("select oid from pg_type where typname='%s'" % (typename,))
    conn.commit()
    return curs.fetchall()[0][0]

def initialisePsycopgTypes(psycopg_module, subclass_map={}, connect_string=None, 
                           register_opengis_types=None, psycopg_extensions_module=None):
    """
    Inform psycopg about the GeoType types.

    This ensures that when the 'bound' variable method of query generation is used
    the GeoTypes are automatically coverted into the right format for use in postgres
    queries.

    It also ensures that any results columns from queries that are of a geometric
    type are returned as instances of the GeoType classes.

    (arg psycopg_module) is the psycopg module itself. This is passes in as a parameter
    to ensure that the GeoTypes package can be used with or without psycopg. If it
    were imported in the module directly it would reduce the flexibility of the package.

    (arg subclass_map) is a dictionary of 'postgres_type':'GeoType class' pairs. It allows
    a caller to subclass the GeoType classes and ensure that the subclasses get hooked into
    the psycopg type machinery rather the plain GeoType classes. See the PsycopgInit_Test.py
    file for an example of its use. Default {}.

    (arg connect_string) is a postgres connection string of the form
    'dbname=schema_test user=postgres. If this is not None an attempt it made to create a
    test table from which to dynamically workout the type OIDS for the geometric types. If this
    is None as list of OID values that where correct when I tested it are used. I am not sure
    how oftern these OIDs change but if you have problems with typecast registration try
    passing a connect_string and see if it fixes it. Default None.

    (arg register_opengis_types) is a flag to control whether the OpenGIS types are registered.
    The the flag is not None the OpenGIS types are registered with Psycopg. If this is not None
    a (arg connect_string) must be provided as the type oids for the OpenGIS types differ
    between databases and the correct oid must be calculated dynamically. Default None.
    
    (arg psycopg_extensions_module) is the psycopg2.extensions module. This is required if
    psycopg2 is being used. Default None.
    
    """
    if int(psycopg_module.__version__[0]) > 1:
        if psycopg_extensions_module == None:
            raise RuntimeError, \
                """
                You are using Psycopg2 but you have not provided the psycopg_extensions_module
                to initialisePsycopgTypes. You need to pass the psycopg2.extensions module
                as the 'psycopg_extensions_module' parameter to initialisePsycopgTypes.
                """
        connect=psycopg_module.connect
        register_type=psycopg_extensions_module.register_type
        new_type=psycopg_extensions_module.new_type
    else:
        connect=psycopg_module.connect
        register_type=psycopg_module.register_type
        new_type=psycopg_module.new_type
                
    if subclass_map != {}:
        for override in subclass_map.keys():
            _class_map[override]['class'] = subclass_map[override]

    if connect_string != None:
        conn = connect(connect_string)

        # Start by working out the oids for the standard Postgres geo types
        curs = conn.cursor()

        # check the postgis version number
        (major,minor,patch) = _getPostgisVersion(conn,curs)

        if int(major) < 1:
            print ("This version of GeoTypes is only tested with PostGis-1.X. \n"\
                   "Your PostGis is version %s.%s.%s. \n"\
                   "GeoTypes will continue but it is likely that you will have "\
                   "some problems." % (major,minor,patch))
            
        for typename in _class_map.keys():
            _class_map[typename]['oid'] = _getTypeOid(conn,curs,typename)
            
        if register_opengis_types:
            # Now calculate the type oid for the OpenGIS Geometry type.
            # This one is different for every database.
            # At some point in its development Postgis changed the oids that
            # are used, so we need to try a couple of combinations.

            # sentinals
            geometry_type_oid = -1

            try:
                geometry_type_oid = _getTypeOid(conn,curs,'geometry')
            except:
                # We failed to find a working combination of oids.
                type, value, tb = sys.exc_info()[:3]
                error = ("%s , %s \n" % (type, value))
                for bits in traceback.format_exception(type,value,tb):
                    error = error + bits + '\n'
                del tb

                raise RuntimeError, \
                      "Failed to get the type oid for the 'geometry' type from the database:\n\n"\
                      "                   connection_string = '%s' \n\n"\
                      "This is probably because you have not initialised the OpenGIS types\n"\
                      "for this database. Look at http://postgis.refractions.net/docs/x83.html\n"\
                      "for instructions on how to do this.\n\n"\
                      "The actual exception raised was:\n\n"\
                      "%s" % (connect_string, error)
            

            if int(major) < 1 :
                wkb_type_oid = -1

                try:
                    wkb_type_oid = _getTypeOid(conn,curs,'wkb')
                except IndexError:
                    # raised if the typename is not present
                    pass

            # Register the type factory for the OpenGIS types.
            if int(major) < 1 :
                register_type(new_type((geometry_type_oid,), 'Geometry', _PostWKTGISClassFactory()))
                register_type(new_type((wkb_type_oid,), 'WKB', _PostWKBGISClassFactory()))
            else:
                register_type(new_type((geometry_type_oid,), 'Geometry', _PostHEXEWKBGISClassFactory()))

    # Finally, register the standard Postgres GIS types.
    # If no connect_string is given these use a default set of type oids that were
    # correct for the database I tested it on.
    for new_class in _class_map.values():
        register_type(new_type((new_class['oid'],), new_class['name'], new_class['class']))

