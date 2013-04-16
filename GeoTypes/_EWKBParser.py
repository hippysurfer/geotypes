
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
A parser for the (Extended) Well Formed Text Binary format of OpenGIS types.
"""
#
# 2.5d spec: http://gdal.velocet.ca/projects/opengis/twohalfdsf.html
#

import shlex, StringIO, sys, traceback, xdrlib, struct


# based on xdrlib.Unpacker
class _ExtendedUnPacker:
    """
    A simple binary struct parser, only implements the types that are need for the WKB format.
    """
    
    def __init__(self,data):
        self.reset(data)
        self.setEndianness('XDR')

    def reset(self, data):
        self.__buf = data
        self.__pos = 0

    def get_position(self):
        return self.__pos

    def set_position(self, position):
        self.__pos = position

    def get_buffer(self):
        return self.__buf

    def done(self):
        if self.__pos < len(self.__buf):
            raise Error('unextracted data remains')

    def setEndianness(self,endianness):
        if endianness == 'XDR':
            self._endflag = '>'
        elif endianness == 'NDR':
            self._endflag = '<'
        else:
            raise ExceptionEWKBParser('Attempt to set unknown endianness in ExtendedUnPacker')

    def unpack_byte(self):
        i = self.__pos
        self.__pos = j = i+1
        data = self.__buf[i:j]
        if len(data) < 1:
            raise EOFError
        byte = struct.unpack('%sB' % self._endflag, data)[0]
        return byte

    def unpack_uint32(self):
        i = self.__pos
        self.__pos = j = i+4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        uint32 = struct.unpack('%sI' % self._endflag, data)[0]
        return uint32


    def unpack_short(self):
        i = self.__pos
        self.__pos = j = i+2
        data = self.__buf[i:j]
        if len(data) < 2:
            raise EOFError
        short = struct.unpack('%sH' % self._endflag, data)[0]
        return short

    def unpack_double(self):
        i = self.__pos
        self.__pos = j = i+8
        data = self.__buf[i:j]
        if len(data) < 8:
            raise EOFError
        return struct.unpack('%sd' % self._endflag, data)[0]

class ExceptionEWKBParser(Exception):
    '''This is the EWKB Parser Exception class.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return `self.value`
    
class EWKBParser:

    _count = 0
    
    # these masks are or'd with the type 
    _z_mask = 0x80000000 # to indicate presence of z dimension
    _m_mask = 0x40000000 # to indicate presence of measurement
    _s_mask = 0x20000000 # to indicate presence of SRID

    def __init__(self,factory):
        """
        Initialise a new WKBParser.

        (arg factory) an object that implements the methods of OGAbstractFactory.
        """
        
        self._factory = factory

        self._typemap = {6: self.parseMultiPolygon,
                         1: self.parsePoint,
                         2: self.parseLineString,
                         3: self.parsePolygon,
                         4: self.parseMultiPoint,
                         5: self.parseMultiLineString,
                         7: self.parseGeometryCollection}
        
        
    def parseGeometry(self, geometry):
        

        """
        A factory method for creating objects of the correct OpenGIS type.
        """

        # Used for exception strings
        self._current_string = geometry

        self._factory.beginWork()
        
        reader = _ExtendedUnPacker(geometry)
        
        self._factory.beginUnit(None) # The WKB format does not have the SRID

        # Start the parsing
        self._dispatchNextType(reader)
        
        self._factory.endUnit()
        self._factory.endWork()


    def _dispatchNextType(self,reader):
        """
        Read a type id from the binary stream (reader) and call the correct method to parse it.
        """
        # Need to check endianess here!
        endianness = reader.unpack_byte()
        if endianness == 0:
            reader.setEndianness('XDR')
        elif endianness == 1:
            reader.setEndianness('NDR')
        else:
            raise ExceptionEWKBParser("Invalid endianness in WKB format.\n"\
                                     "The parser can only cope with XDR/big endian WKB format.\n"\
                                     "To force the WKB format to be in XDR use AsBinary(<fieldname>,'XDR'")
                    
        geotype = reader.unpack_uint32()

        if geotype & EWKBParser._z_mask:
            dimensions = 3
            geotype = geotype & (~EWKBParser._z_mask)
        else:
            dimensions = 2
            
        if geotype & EWKBParser._m_mask:
            geotype = geotype & (~EWKBParser._m_mask)
            raise ExceptionEWKBParser('Error: Geometry has M dimension. \n'\
                                      'GeoTypes does not yet support M dimension types. \n'\
                                      'type = %s \n'\
                                     'Invalid geometry in WKB string: %s' % (str(geotype),
                                                                             str(self._current_string),))

            
        if geotype & EWKBParser._s_mask:
            srid = reader.unpack_uint32()
            geotype = geotype & (~EWKBParser._s_mask)
        else:
            srid = None


        # Despatch to a method on the type id.
        if self._typemap.has_key(geotype):
            self._typemap[geotype](reader, dimensions, srid)
        else:
            raise ExceptionEWKBParser('Error type to dispatch with geotype = %s \n'\
                                     'Invalid geometry in WKB string: %s' % (str(geotype),
                                                                             str(self._current_string),))
        
        return True
        
    def parseGeometryCollection(self, reader, dimension, srid):
        self._factory.beginGeometryCollection(srid)
        
                        
        try:
            num_geoms = reader.unpack_uint32()

            for geom in xrange(0,num_geoms):
                self._dispatchNextType(reader)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionEWKBParser("Caught unhandled exception parsing GeometryCollection: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
        
    
        self._factory.endGeometryCollection()
        
    def parseLinearRing(self, reader, dimensions, srid):
        self._factory.beginLinearRing(srid)
        
        try:
            num_points = reader.unpack_uint32()

            for point in xrange(0,num_points):
                self.parsePoint(reader,dimensions,srid)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLinearRing()
            raise ExceptionEWKBParser("Caught unhandled exception parsing LinearRing: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))

        self._factory.endLinearRing()
    
    def parseLineString(self, reader, dimensions, srid):
        # Linestring is broken in the same way as MultiPoint
        
        self._factory.beginLineString(srid)

        try:
            num_points = reader.unpack_uint32()

            for point in xrange(0,num_points):
                self.parsePoint(reader,dimensions,srid)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionEWKBParser("Caught unhandled exception parsing Linestring: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
               
        self._factory.endLineString()
    
    def parseMultiLineString(self, reader, dimensions, srid):
        self._factory.beginMultiLineString(srid)
                
        try:
            num_linestrings = reader.unpack_uint32()

            for linestring in xrange(0,num_linestrings):
                self._dispatchNextType(reader)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionEWKBParser("Caught unhandled exception parsing MultiLineString: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
        

        self._factory.endMultiLineString()
    
    def parseMultiPoint(self, reader, dimensions, srid):
        self._factory.beginMultiPoint(srid)

        try:
            num_points = reader.unpack_uint32()

            for point in xrange(0,num_points):
                self._dispatchNextType(reader)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionEWKBParser("Caught unhandled exception parsing MultiPoint: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
               
        self._factory.endMultiPoint()

    
    def parseMultiPolygon(self, reader, dimensions, srid):
        self._factory.beginMultiPolygon(srid)
                
        try:
            num_polygons = reader.unpack_uint32()

            for polygon in xrange(0,num_polygons):
                self._dispatchNextType(reader)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionEWKBParser("Caught unhandled exception parsing MultiPolygon: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
        
        
        self._factory.endMultiPolygon()
    
    def parsePoint(self, reader, dimensions, srid):
        self._factory.beginPoint(srid)
                
        x = reader.unpack_double()
        y = reader.unpack_double()
        if dimensions == 3:
            z = reader.unpack_double()
        else:
            z = None

        if z != None:
            self._factory.addPoints3D(x,y,z)
        else:
            self._factory.addPoints(x,y)

        self._factory.endPoint()
    
    def parsePolygon(self, reader, dimensions, srid):
        self._factory.beginPolygon(srid)

        try:
            num_points = reader.unpack_uint32()

            for point in xrange(0,num_points):
                self.parseLinearRing(reader,dimensions, srid)

        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortPolygon()
            raise ExceptionEWKBParser("Caught unhandled exception parsing Polygon: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))

        self._factory.endPolygon()

class HEXEWKBParser(EWKBParser):

    def __init__(self,factory):
        """
        Initialise a new WKBParser.

        (arg factory) an object that implements the methods of OGAbstractFactory.
        """
        EWKBParser.__init__(self,factory)
        
        
    def parseGeometry(self, geometry):
        

        """
        A factory method for creating objects of the correct OpenGIS type.
        """

        EWKBParser.parseGeometry(self,geometry.decode('hex'))
