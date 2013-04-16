
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string
from _OGMultiCurve import OGMultiCurve
from _OGLineString import OGlineStringFromSequence

class OGMultiLineString(OGMultiCurve):
    
    def _og_str(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
            
        return "MULTILINESTRING (%s)" % (s,)
    
    def __repr__(self):
        s = string.join([ point.__repr__() for point in self.getGeometries() ],',')
            
        return "(%s)" % (s,)


# factory methods

def OGmultiLineStringFromOGLineStrings(*linestrings):
    """
    Return a OGMultiLineString.

    (arg *points) any number of OGLineStrings that make up the OGMultiLineString.

    """
    multilinestring = OGMultiLineString()
    for linestring in linestrings:
        multilinestring.append(linestring)
        
    return multilinestring

def OGmultiLineStringFromSequence(seq):
    """
    Return a OGMultiLineString.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the OGMultiLineString,
    where x and y are floats.

    """

    multilinestring = OGMultiLineString()
    for linestring in seq:
        multilinestring.append(OGlineStringFromSequence(linestring))
        
    return multilinestring
