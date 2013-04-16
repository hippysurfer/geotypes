
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

class OGAbstractFactory:

    def __init__(self):
        pass

    def getGeometry(self):
        pass
    
    def abortGeometryCollection(self):
        pass
    
    def abortLinearRing(self):
        pass

    def abortLineString(self):
        pass
    
    def abortMultiLineString(self):
        pass
    
    def abortMultiPoint(self):
        pass
    
    def abortMultiPolygon(self):
        pass
    
    def abortPoint(self):
        pass
    
    def abortPolygon(self):
        pass
    
    def abortUnit(self):
        pass
    
    def abortWork(self):
        pass
    
    def addPoints(self,x,y):
        pass
    
    def addPoints3D(self,x,y,z):
        pass

    def beginGeometryCollection(self):
        pass
    
    def beginLinearRing(self):
        pass
    
    def beginLineString(self):
        pass
    
    def beginMultiLineString(self):
        pass
    
    def beginMultiPoint(self):
        pass
    
    def beginMultiPolygon(self):
        pass
    
    def beginPoint(self):
        pass
    
    def beginPolygon(self):
        pass
    
    def beginUnit(self, srid):
        pass
        
    def beginWork(self):
        pass

    def endGeometryCollection(self):
        pass
    
    def endLinearRing(self):
        pass
    
    def endLineString(self):
        pass
    
    def endMultiLineString(self):
        pass
    
    def endMultiPoint(self):
        pass
    
    def endMultiPolygon(self):
        pass
    
    def endPoint(self):
        pass
    
    def endPolygon(self):
        pass
    
    def endUnit(self):
        pass
    
    def endWork(self):
        pass

    def reset(self):
        pass
