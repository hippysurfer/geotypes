################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################

"""
Implementation of ISQLProtocol.
"""

class ExceptionISQLProtocol(Exception):
    '''This is the ISQLProtocol Exception class.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    
class ISQLProtocol(object):
    """
    This class provides a default implementation of the ISQLProtocol used
    by the psycopg2 adapt system.
    """

    def __conform__(self, proto):
	    # The import is nested here so that the module will import 
	    # cleanly even if psycopg is not available. This is required
	    # because the basic geographic types are designed to be used
	    # idepentantly from postgis.
        import psycopg2.extensions
        if proto == psycopg2.extensions.ISQLQuote:
            return self
        raise ExceptionISQLProtocol, \
            """Failed to conform to requested protocol. The psycopg adapt
            machinery asked the instance of: %s to conform to the protocol: %s 
            but %s does not know how.""" % (self.__class__.__name__,
                                            repr(proto.__class__.__name__),
                                            self.__class__.__name__)
    
    def getquoted(self):
        return str(self)

    def prepare(self, conn):
        pass
