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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Asger Skovbo Petersen, Septima'
__date__ = '2016-02-04'
__copyright__ = '(C) 2016 by Asger Skovbo Petersen, Septima'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load WedgeBuffer class from file WedgeBuffer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .wedge_buffer import WedgeBufferPlugin
    return WedgeBufferPlugin()
