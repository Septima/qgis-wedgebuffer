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

import math

RAD2DEGREE = 180 / math.pi
DEGREE2RAD = math.pi / 180

def polar_to_cartesian(centre, angle, radius):
    x = math.cos(angle) * radius + centre[0]
    y = math.sin(angle) * radius + centre[1]
    return (x,y)

def make_arc(centre, radius, rad_from_azimuth, rad_to_azimuth, rad_angle_resolution):
    cartesian = []
    rad_az = rad_from_azimuth
    if rad_from_azimuth < rad_to_azimuth:
        while rad_az < rad_to_azimuth:
            cartesian.append(polar_to_cartesian(centre, rad_az, radius))
            rad_az = rad_az + rad_angle_resolution
    else:
        while rad_az > rad_to_azimuth:
            cartesian.append(polar_to_cartesian(centre, rad_az, radius))
            rad_az = rad_az - rad_angle_resolution
    cartesian.append(polar_to_cartesian(centre, rad_to_azimuth, radius))
    return cartesian


def wedge_buffer(centre, radius, azimuth, opening_angle, inner_radius = 0, angle_resolution = 10):
    # make Azimuth 0 north and positive clockwise
    azimuth = -1 * azimuth + 90
    rad_from_azimuth = (azimuth - opening_angle * 0.5) * DEGREE2RAD
    rad_to_azimuth = (azimuth + opening_angle * 0.5) * DEGREE2RAD
    rad_angle_res = angle_resolution * DEGREE2RAD

    cartesian_coords = make_arc(centre, radius, rad_from_azimuth, rad_to_azimuth, rad_angle_res)

    if inner_radius <= 0:
        cartesian_coords.append(centre)
    else:
        # Reverse arc at inner radius
        cartesian_coords += make_arc(centre, inner_radius, rad_to_azimuth, rad_from_azimuth, rad_angle_res)

    # Close ring
    cartesian_coords.append(cartesian_coords[0])
    return cartesian_coords