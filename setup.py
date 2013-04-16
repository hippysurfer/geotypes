#!/usr/local/bin/python

################################################################################
# Copyright (c) QinetiQ Plc 2003
#
# Licensed under the LGPL. For full license details see the LICENSE file.
################################################################################


"""

To use this setup script to install GeoTypes:

        cd GeoTypes-version 
        python setup.py install

"""

import sys
import os
import tempfile

from distutils.core import setup
from distutils import sysconfig


if __name__ == '__main__' :
    DOC_FILES = ('LICENSE', 'NEWS', 'INSTALL', 'README', 'VERSION',
                 'KNOWN_BUGS', 'AUTHORS', 'TODO')
    
    LONG_DESCRIPTION = \
"""
GeoTypes 

A package of classes for working with basic 2d geometric types.

These classes were designed for use with the geometric functions
supported by Postgresql (http://www.postgresql.com) although they
do not need Postgresql to be present for them to be used.
"""

    install_dir = sysconfig.get_python_lib() + os.sep + 'GeoTypes'

    setup(name                  = "GeoTypes",
          version               = "0.7.0",
          license               = "LGPL",
          description           = "Classes for working with basic 2d geometric types",
          author                = "Richard Taylor, QinetiQ Plc.",
          author_email          = "r.taylor@eris.qinetiq.com",
          url                   = "http://",
          packages              = [ 'GeoTypes' ],
          data_files            = [ (install_dir, DOC_FILES) ],
          long_description      = LONG_DESCRIPTION
         )


