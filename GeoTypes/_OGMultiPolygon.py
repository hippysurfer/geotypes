
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string

from _OGMultiSurface import OGMultiSurface
from _OGPolygon import OGpolygonFromSequence

class OGMultiPolygon(OGMultiSurface):

    def _og_str(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
        return 'MULTIPOLYGON (%s)' % (s,)
    
    def __repr__(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
            
        return "(%s)" % (s,)


# factory methods

def OGmultiPolygonFromOGPolygons(*polygons):
    """
    Return a OGMultipolygon.

    (arg *points) any number of OGPolygons that make up the OGMultiPolygon.

    """
    multipolygon = OGMultiPolygon()
    for polygon in polygons:
        multipolygon.append(polygon)
        
    return multipolygon

def OGmultiPolygonFromSequence(seq):
    """
    Return a OGMultiPolygon.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the OGMultiPolygon,
    where x and y are floats.

    """

    multipolygon = OGMultiPolygon()
    for polygon in seq:
        multipolygon.append(OGpolygonFromSequence(polygon))
        
    return multipolygon
