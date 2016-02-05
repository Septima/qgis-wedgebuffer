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

from PyQt4.QtCore import QSettings
from qgis.core import QgsVectorFileWriter, QgsGeometry, QgsPoint, QGis, QgsFeature

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector

import wedge_buffer_implementation

class WedgeBufferAlgorithm(GeoAlgorithm):
    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LAYER = 'INPUT_LAYER'
    AZIMUTH_FIELD = 'AZIMUTH_FIELD'
    WEDGE_ANGLE_FIELD = 'WEDGE_ANGLE_FIELD'
    RADIUS_FIELD = 'RADIUS_FIELD'
    INNER_RADIUS_FIELD = 'INNER_RADIUS_FIELD'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        self.name = 'Wedge Buffer'

        # The branch of the toolbox under which the algorithm will appear
        self.group = 'Wedge Buffer'

        # We add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(ParameterVector(self.INPUT_LAYER,
            self.tr('Input layer'), [ParameterVector.VECTOR_TYPE_POINT], False))

        self.addParameter(ParameterTableField(self.AZIMUTH_FIELD,
                                              self.tr('Azimuth field'), self.INPUT_LAYER))

        self.addParameter(ParameterTableField(self.WEDGE_ANGLE_FIELD,
                                              self.tr('Wedge angle field'), self.INPUT_LAYER))

        self.addParameter(ParameterTableField(self.RADIUS_FIELD,
                                              self.tr('Radius field'), self.INPUT_LAYER))

        self.addParameter(ParameterTableField(self.INNER_RADIUS_FIELD,
                                              self.tr('Inner radius field'), self.INPUT_LAYER, optional=True))

        # We add a vector layer as output
        self.addOutput(OutputVector(self.OUTPUT_LAYER,
            self.tr('Output layer')))

    def processAlgorithm(self, progress):
        """Here is where the processing itself takes place."""

        # The first thing to do is retrieve the values of the parameters
        # entered by the user
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        azimuthField = self.getParameterValue(self.AZIMUTH_FIELD)
        wedgeAngleField = self.getParameterValue(self.WEDGE_ANGLE_FIELD)
        radiusField = self.getParameterValue(self.RADIUS_FIELD)
        innerRadiusField = self.getParameterValue(self.INNER_RADIUS_FIELD)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        # Input layers vales are always a string with its location.
        # That string can be converted into a QGIS object (a
        # QgsVectorLayer in this case) using the
        # processing.getObjectFromUri() method.
        vectorLayer = dataobjects.getObjectFromUri(inputFilename)

        # And now we can process

        # First we create the output layer. The output value entered by
        # the user is a string containing a filename, so we can use it
        # directly
        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        provider = vectorLayer.dataProvider()
        writer = QgsVectorFileWriter(output, systemEncoding,
                                     provider.fields(),
                                     QGis.WKBPolygon, provider.crs())

        # Now we take the features from input layer and add them to the
        # output. Method features() returns an iterator, considering the
        # selection that might exist in layer and the configuration that
        # indicates should algorithm use only selected features or all
        # of them
        features = vector.features(vectorLayer)
        for f in features:
            azimuth = float(f[azimuthField])
            wedgeAngle = float(f[wedgeAngleField])
            radius = float(f[radiusField])
            innerRadius = float( f[innerRadiusField] if innerRadiusField else 0 )

            centre = f.geometry().asPoint()

            wedge = wedge_buffer_implementation.wedge_buffer(centre, radius, azimuth, wedgeAngle, innerRadius)
            qgisPoly = QgsGeometry.fromPolygon( [[QgsPoint(*p) for p in wedge]] )

            outFeat = QgsFeature()
            outFeat.setAttributes( f.attributes() )
            outFeat.setGeometry( qgisPoly )

            writer.addFeature( outFeat )

        # There is nothing more to do here. We do not have to open the
        # layer that we have created. The framework will take care of
        # that, or will handle it if this algorithm is executed within
        # a complex model


