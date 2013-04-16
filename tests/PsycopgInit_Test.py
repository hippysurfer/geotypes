
################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

import unittest
try:
    import psycopg2 as psycopg
    import psycopg2.extensions as psyco_ext
except ImportError:
    import psycopg
    psyco_ext = None
import TestConfig


from _Point import Point

import os
if not os.environ.get('USECOVERAGE') == '1':
    import _PsycopgInit

class PsycopgInitTest(unittest.TestCase):    

    def setUp(self):
        pass
    
    def testPsycopgInit(self):
        _PsycopgInit.initialisePsycopgTypes(psycopg_module=psycopg,psycopg_extensions_module=psyco_ext)
        _PsycopgInit.initialisePsycopgTypes(psycopg_module=psycopg,connect_string="dbname=mq_test user=postgres",
                                            psycopg_extensions_module=psyco_ext)
        _PsycopgInit.initialisePsycopgTypes(psycopg_module=psycopg,connect_string="dbname=mq_test user=postgres",
                                            register_opengis_types=1,psycopg_extensions_module=psyco_ext)

        class MyPoint(Point):
            pass
        
        _PsycopgInit.initialisePsycopgTypes(psycopg_module=psycopg,subclass_map={'point':MyPoint},
                                            psycopg_extensions_module=psyco_ext)


def testSuite():
    return unittest.makeSuite(PsycopgInitTest,'test')

if __name__ == "__main__":
    import os
    if os.environ.get('USECOVERAGE') == '1':
        try:
            import coverage
            coverage.erase()
            coverage.start()
            COVERAGE = 1
            import _PsycopgInit

        except:
            print "Error setting up coverage checking"
            COVERAGE = 0
    else:
        COVERAGE = 0

    if os.environ.get('USEPYCHECK') == '1':
        try:
            import pychecker.checker
        except:
            print "Pychecker not installed on this machine"

    unittest.TextTestRunner().run(testSuite())

    if COVERAGE:
        coverage.stop()
        x = coverage.analysis(_PsycopgInit)
        print "\n"
        coverage.report(_PsycopgInit)
