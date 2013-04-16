
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string

from _OGGeometryCollection import OGGeometryCollection
from _OGPoint import OGPoint, OGpointFromSequence


class OGMultiPoint(OGGeometryCollection):
    
    def _og_str(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
            
        return "MULTIPOINT (%s)" % (s,)
    
    def __repr__(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
            
        return "(%s)" % (s,)


# factory methods

def OGmultiPointFromOGPoints(*points):
    """
    Return a OGMultipoint.

    (arg *points) any number of OGPoints that make up the OGMultiPoint.

    """
    multipoint = OGMultiPoint()
    for point in points:
        multipoint.append(point)
        
    return multipoint

def OGmultiPointFromSequence(seq):
    """
    Return a OGMultiPoint.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the OGMultiPoint,
    where x and y are floats.

    """

    multipoint = OGMultiPoint()
    for point in seq:
        multipoint.append(OGpointFromSequence(point))
        
    return multipoint
