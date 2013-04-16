
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################


from _ISQLProtocol import ISQLProtocol

class OGGeometry(ISQLProtocol):

    default_srid = 128
    
    def __init__(self, srid):
        if srid == None:
            self._srid = OGGeometry.default_srid
        else:
            self._srid = srid
        
    def SRID(self):
        return self._srid

    def setParent(self,geometry):
        self._parent = geometry

    def getParent(self):
        return self._parent

    def __str__(self):            
        return "GeometryFromText('%s',%d)" % (self._og_str(),self.SRID())
