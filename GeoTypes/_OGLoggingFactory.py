
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import _OGAbstractFactory

class OGLoggingFactory(_OGAbstractFactory.OGAbstractFactory):

    def __init__(self):
        print "__init__"
    
    def abortGeometryCollection(self):
        print "abortGeometryCollection"
    
    def abortLinearRing(self):
        print "abortLinearRing"

    def abortLineString(self):
        print "abortLineString"
    
    def abortMultiLineString(self):
        print "abortMultiLineString"
    
    def abortMultiPoint(self):
        print "abortMultiPoint"
    
    def abortMultiPolygon(self):
        print "abortMultiPolygon"
    
    def abortPoint(self):
        print "abortPoint"
    
    def abortPolygon(self):
        print "abortPolygon"
    
    def abortUnit(self):
        print "abortUnit"
    
    def abortWork(self):
        print "abortWork"
    
    def addPoints(self,x,y):
        print "addPoints x=%f, y=%f" % (x,y)
    
    def addPoints3D(self,x,y,z):
        print "addPoints3D  x=%f, y=%f, z=%f" % (x,y,z)

    def beginGeometryCollection(self):
        print "beginGeometryCollection"
    
    def beginLinearRing(self):
        print "beginLinearRing"
    
    def beginLineString(self):
        print "beginLineString"
    
    def beginMultiLineString(self):
        print "beginMultiLineString"
    
    def beginMultiPoint(self):
        print "beginMultiPoint"
    
    def beginMultiPolygon(self):
        print "beginMultiPolygon"
    
    def beginPoint(self):
        print "beginPoint"
    
    def beginPolygon(self):
        print "beginPolygon"
    
    def beginUnit(self, srid):
        print "beginUnit"
    
##    def beginUnit(java.lang.String[] words, int[] values):
##        print ""
    
    def beginWork(self):
        print "beginWork"

    def endGeometryCollection(self):
        print "endGeometryCollection"
    
    def endLinearRing(self):
        print "endLinearRing"
    
    def endLineString(self):
        print "endLineString"
    
    def endMultiLineString(self):
        print "endMultiLineString"
    
    def endMultiPoint(self):
        print "endMultiPoint"
    
    def endMultiPolygon(self):
        print "endMultiPolygon"
    
    def endPoint(self):
        print "endPoint"
    
    def endPolygon(self):
        print "endPolygon"
    
    def endUnit(self):
        print "endUnit"
    
    def endWork(self):
        print "endWork"

    def reset(self):
        print "reset"


