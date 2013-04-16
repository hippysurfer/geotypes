
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import string

from _OGLineString import OGLineString
from _OGPoint import OGpointFromSequence

class OGLinearRing(OGLineString):
    def __repr__(self):
        s = string.join([ point.__repr__() for point in self.getPoints() ],',')
        return "(%s)" % (s,)
        

# factory methods

def OGlinearRingFromOGPoints(*points):
    """
    Return a OGLinearRing.

    (arg *points) any number of OGPoints that make up the OGLinearRing.

    """
    linearring = OGLinearRing()
    for point in points:
        linearring.append(point)
        
    return linearring

def OGlinearRingFromSequence(seq):
    """
    Return a OGLinearRing.

    (arg *seq) a sequence of the form ((x,y),...,(x,y)) that make up the OGLinearRing,
    where x and y are floats.

    """

    linearring = OGLinearRing()
    for point in seq:
        linearring.append(OGpointFromSequence(point))
        
    return linearring
