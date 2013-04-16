
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

from _OGMultiPolygon import OGMultiPolygon
from _OGPoint import OGPoint
from _OGLineString import OGLineString
from _OGLinearRing import OGLinearRing
from _OGPolygon import OGPolygon
from _OGMultiPoint import OGMultiPoint
from _OGMultiLineString import OGMultiLineString
from _OGGeometryCollection import OGGeometryCollection

from _OGLoggingFactory import OGLoggingFactory
from _OGAbstractFactory import OGAbstractFactory

#class OGGeoTypeFactory(OGLoggingFactory):
class OGGeoTypeFactory(OGAbstractFactory):

    def __init__(self):
        self._top = None
        self._current_node = None

    def getGeometry(self):
        return self._top
    
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
    
##    def abortUnit(self):
##        pass
    
##    def abortWork(self):
##        pass
    
    def addPoints(self,x,y):
##        print "addPoint"
        self._current_node.setX(x)
        self._current_node.setY(y)        
    
    def addPoints3D(self,x,y,z):
##        print "addPoint3D"
        self._current_node.setX(x)
        self._current_node.setY(y)        
        self._current_node.setZ(z)        

    def beginGeometryCollection(self, srid=None):
        self._beginNode(OGGeometryCollection, srid)

    def _beginNode(self, node_type, srid=None):
        self._printState()

        parent = self._current_node
        self._current_node = node_type(srid=srid or self._srid)
        self._current_node.setParent(parent)

        if self._top == None:
            self._top = self._current_node

        self._printState()
        
    def beginLinearRing(self, srid=None):
        self._beginNode(OGLinearRing, srid)
    
    def beginLineString(self, srid=None):
        self._beginNode(OGLineString, srid)
    
    def beginMultiLineString(self, srid=None):
        self._beginNode(OGMultiLineString, srid)
    
    def beginMultiPoint(self, srid=None):
        self._beginNode(OGMultiPoint, srid)
    
    def beginMultiPolygon(self, srid=None):
        self._beginNode(OGMultiPolygon, srid)
    
    def beginPoint(self,srid=None):
        self._beginNode(OGPoint, srid)
    
    def beginPolygon(self, srid=None):
        self._beginNode(OGPolygon, srid)

    def beginUnit(self, srid):
        self._srid = srid
    
##    def beginUnit(java.lang.String[] words, int[] values):
##        pass
    
##    def beginWork(self):
##        pass

    def endGeometryCollection(self):
        self._endNode()

    def _endNode(self):
        self._printState()

        parent = self._current_node.getParent()
        if parent != None:
            parent.append(self._current_node)
        self._current_node = parent
        
    def endLinearRing(self):
        self._endNode()
        
    def endLineString(self):
        self._endNode()
    
    def endMultiLineString(self):
        self._endNode()
        
    def endMultiPoint(self):
        self._endNode()
    
    def endMultiPolygon(self):
        self._endNode()
    
    def endPoint(self):
        self._endNode()
    
    def endPolygon(self):
        self._endNode()
    
##    def endUnit(self):
##        pass
    
##    def endWork(self):
##        pass

##    def reset(self):
##        pass

    def _printState(self):
        #print "_current_node = ", self._current_node, " _top = ", self._top
        pass
