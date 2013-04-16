
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
A parser for the Well Known Text Format of OpenGIS types.

Changelog:
    06 jan 06: made SRID optional in WKTParser.parseGeometry (fredericback@gmail.com)
    
"""

import shlex, StringIO, sys, traceback

class ExceptionWKTParser(Exception):
    '''This is the WKT Parser Exception class.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return `self.value`
    
class WKTParser:

    def __init__(self,factory):
        self._factory = factory

        self._typemap = {'MULTIPOLYGON': self.parseMultiPolygon,
                         'POINT': self.parsePoint,
                         'LINESTRING': self.parseLineString,
                         'POLYGON': self.parsePolygon,
                         'MULTIPOINT': self.parseMultiPoint,
                         'MULTILINESTRING': self.parseMultiLineString,
                         'GEOMETRYCOLLECTION': self.parseGeometryCollection,
                        }
        
    
    def parseGeometry(self, geometry):
        """
        A factory method for creating objects of the correct OpenGIS type.
        """

        # Used for exception strings
        self._current_string = geometry

        self._factory.beginWork()
        
        # tokenize the string
        tok_stream = shlex.shlex(StringIO.StringIO(geometry))
        tok_stream.wordchars = tok_stream.wordchars + '.-'

        # Avoid some extra lookups
        next_tok = tok_stream.get_token

        # Check if first token contains an SRID. If it does not, assume an SRID of -1.
        token = next_tok()
        if token == 'SRID':
            try:
                if next_tok() != '=': raise
                srid = int(next_tok())
                if next_tok() != ';': raise
            except: raise ExceptionWKTParser('Invalid SRID in WKT string: %s' % (str(self._current_string),))
            token = next_tok()
        else: 
            srid = -1

        self._factory.beginUnit(srid)

        # Start the parsing proper. 
        if self._typemap.has_key(token):
            self._typemap[token](next_tok)
        else:
            raise ExceptionWKTParser('Invalid geometry in WKT string: %s' % (str(self._current_string),))

        self._factory.endUnit()
        self._factory.endWork()
        
    def parseGeometryCollection(self, next_tok):
        self._factory.beginGeometryCollection()

        if next_tok() != "(":
            self._factory.abortGeometryCollection()
            raise ExceptionWKTParser('Invalid GeometryCollection in WKT string: %s' % (str(self._current_string),))

        last_geom = None
        
        while not last_geom:
            geotype = next_tok()
            if self._typemap.has_key(geotype):
                self._typemap[geotype](next_tok)
            else:
                self._factory.abortGeometryCollection()
                raise ExceptionWKTParser('Invalid geometry in WKT string: %s' % (str(self._current_string),))
            
            terminal_tok = next_tok()

            # If we have reached the closing ')' then there are no more geoms in this collection.
            if terminal_tok == ')':
                last_geom = 1
            else:
                if terminal_tok != ',': 
                    self._factory.abortGeometryCollection()
                    raise ExceptionWKTParser('Invalid terminal on GeometryCollection in WKT string: %s' % (str(self._current_string),))
        
            
        self._factory.endGeometryCollection()
        
##    def parseLinearRing(self, next_tok):
##        self._factory.begin()
##        self._factory.end()
    
    def parseLineString(self, next_tok):
        # Linestring is broken in the same way as MultiPoint
        
        self._factory.beginLineString()

        try:
            if next_tok() != "(":
                self._factory.abortLineString()
                raise ExceptionWKTParser('Invalid Linestring in WKT string: %s' % (str(self._current_string),))

            broken_form = None
            last_point = None
            while not last_point:

                self._factory.beginPoint()

                x = next_tok()
                if x != '(':
                    broken_form = 1
                else:
                    x = next_tok()
                    
                y = next_tok()
                z = next_tok()

                if z == ',' or z == ')':
                    terminal_tok = z
                    z = None
                else:
                    terminal_tok = next_tok()

                if z:
                    self._factory.addPoints3D(float(x),float(y),float(z))
                else:
                    self._factory.addPoints(float(x),float(y))

                self._factory.endPoint()

                # If we have reached the closing ')' then there are no more linestring in this collection.
                if terminal_tok == ')' and broken_form:
                    last_point = 1
                elif terminal_tok == ')' and not broken_form:
                    terminal_tok = next_tok()
                    if terminal_tok ==')':
                        last_point = 1                    
                    else:
                        if terminal_tok != ',': 
                            self._factory.abortLineString()
                            raise ExceptionWKTParser('Invalid terminal on LineString in WKT string: %s' % (str(self._current_string),))
                else:
                    if terminal_tok != ',': 
                        self._factory.abortLineString()
                        raise ExceptionWKTParser('Invalid terminal on LineString in WKT string: %s' % (str(self._current_string),))                       
        except:
            type, value, tb = sys.exc_info()[:3]
            error = ("%s , %s \n" % (type, value))
            for bits in traceback.format_exception(type,value,tb):
                error = error + bits + '\n'
            del tb
            self._factory.abortLineString()
            raise ExceptionWKTParser("Caught unhandled exception parsing Linestring: %s \n"\
                                     "Traceback: %s\n" % (str(self._current_string),error))
               
        self._factory.endLineString()
    
    def parseMultiLineString(self, next_tok):
        self._factory.beginMultiLineString()
                
        if next_tok() != "(":
            self._factory.abortMultiLineString()
            raise ExceptionWKTParser('Invalid MultiLinestring in WKT string: %s' % (str(self._current_string),))

        last_linestring = None
        while not last_linestring:

            try:
                self.parseLineString(next_tok)
            except ExceptionWKTParser, x:
                self._factory.abortMultiLineString()
                raise ExceptionWKTParser(x.value)

            terminal_tok = next_tok()

            # If we have reached the closing ')' then there are no more linestring in this collection.
            if terminal_tok == ')':
                last_linestring = 1
            else:
                if terminal_tok != ',': 
                    self._factory.abortMultiLineString()
                    raise ExceptionWKTParser('Invalid terminal on MultiLineString in WKT string: %s' % (str(self._current_string),))
        

        self._factory.endMultiLineString()
    
    def parseMultiPoint(self, next_tok):

        # Multipoint syntax if broken, the spec says it should be.
        # MULTIPOINT(<Point Text> { , <Point Text> }* )
        # <Point Text> = ( <Point> )
        #
        # But PG does not include the brackets e.g.
        # correct = MULTIPOINT((0 0 0),(1 2 1))
        # pg      = MULTIPOINT(0 0 0,1 2 1)
        # So we have to special handling for both forms, bummer!
        self._factory.beginMultiPoint()
        
        if next_tok() != "(":
            self._factory.abortMultiPoint()
            raise ExceptionWKTParser('Invalid MultiPoint in WKT string: %s' % (str(self._current_string),))

        broken_form = None
        last_point = None
        while not last_point:

            self._factory.beginPoint()
            
            x = next_tok()
            if x != '(':
                broken_form = 1
            else:
                x = next_tok()

            y = next_tok()
            z = next_tok()
                    
            if z == ')' or z == ',':
                terminal_tok = z
                z = None
            else:
                terminal_tok = next_tok()

            if z:
                self._factory.addPoints3D(float(x),float(y),float(z))
            else:
                self._factory.addPoints(float(x),float(y))
            
            self._factory.endPoint()

            # If we have reached the closing ')' then there are no more linestring in this collection.
            if terminal_tok == ')' and broken_form:
                last_point = 1
            elif terminal_tok == ')' and not broken_form:
                terminal_tok = next_tok()
                if terminal_tok ==')':
                    last_point = 1                    
                else:
                    if terminal_tok != ',': 
                        self._factory.abortMultiPoint()
                        raise ExceptionWKTParser('Invalid terminal on MultiPoint in WKT string: %s' % (str(self._current_string),))
            else:
                if terminal_tok != ',': 
                    self._factory.abortMultiPoint()
                    raise ExceptionWKTParser('Invalid terminal on MultiPoint in WKT string: %s' % (str(self._current_string),))                        
        
        self._factory.endMultiPoint()
    
    def parseMultiPolygon(self, next_tok):
        self._factory.beginMultiPolygon()
        
        if next_tok() != "(":
            self._factory.abortMultiPolygon()
            raise ExceptionWKTParser('Invalid MultiPolygon in WKT string: %s' % (str(self._current_string),))

        last_polygon = None
        while not last_polygon:

            try:
                self.parsePolygon(next_tok)
            except ExceptionWKTParser, x:
                self._factory.abortMultiPolygon()
                raise ExceptionWKTParser(x.value)

            terminal_tok = next_tok()

            # If we have reached the closing ')' then there are no more polygons in this collection.
            if terminal_tok == ')':
                last_polygon = 1
            else:
                if terminal_tok != ',': 
                    self._factory.abortMultiPolygon()
                    raise ExceptionWKTParser('Invalid terminal on MultiPolygon in WKT string: %s' % (str(self._current_string),))
        
        self._factory.endMultiPolygon()

    def parsePoint(self, next_tok):
        self._factory.beginPoint()
                
        if next_tok() != "(":
            self._factory.abortPoint()
            raise ExceptionWKTParser('Invalid Linestring in WKT string: %s' % (str(self._current_string),))


        x = next_tok()
        y = next_tok()
        z = next_tok()

        if z == ')':
            terminal_tok = z
            z = None
        else:
            terminal_tok = next_tok()

        if z:
            self._factory.addPoints3D(float(x),float(y),float(z))
        else:
            self._factory.addPoints(float(x),float(y))

        if terminal_tok != ')':
            self._factory.abortPoint()
            raise ExceptionWKTParser('Invalid terminal on Linestring in WKT string: %s' % (str(self._current_string),))
                
        self._factory.endPoint()
    
    def parsePolygon(self, next_tok):
        self._factory.beginPolygon()
                        
        if next_tok() != "(":
            self._factory.abortPolygon()
            raise ExceptionWKTParser('Invalid Polygon in WKT string: %s' % (str(self._current_string),))

        last_linestring = None
        while not last_linestring:

            try:
                self.parseLineString(next_tok)
            except ExceptionWKTParser, x:
                self._factory.abortPolygon()
                raise ExceptionWKTParser(x.value)

            terminal_tok = next_tok()

            # If we have reached the closing ')' then there are no more linestring in this collection.
            if terminal_tok == ')':
                last_linestring = 1
            else:
                if terminal_tok != ',': 
                    self._factory.abortPolygon()
                    raise ExceptionWKTParser('Invalid terminal on Polygon in WKT string: %s' % (str(self._current_string),))
        

        self._factory.endPolygon()
