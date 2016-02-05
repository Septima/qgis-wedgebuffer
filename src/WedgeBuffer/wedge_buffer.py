# -*- coding: utf-8 -*-

"""
/***************************************************************************
 WedgeBuffer
                                 A QGIS plugin
 Makes wedge shaped buffers on points
                              -------------------
        begin                : 2016-02-04
        copyright            : (C) 2016 by Asger Skovbo Petersen, Septima
        email                : asger@septima.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Asger Skovbo Petersen, Septima'
__date__ = '2016-02-04'
__copyright__ = '(C) 2016 by Asger Skovbo Petersen, Septima'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from processing.core.Processing import Processing
from wedge_buffer_provider import WedgeBufferProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class WedgeBufferPlugin:

    def __init__(self):
        self.provider = WedgeBufferProvider()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)
