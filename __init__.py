# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Gridder
                                 A QGIS plugin
 Builds 2D grids for finite difference
                             -------------------
        begin                : 2013-04-08
        copyright            : (C) 2013 by Pryet
        email                : alexandre.pryet@ensegid.fr
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
def name():
    return "Qgridder"
def description():
    return "Builds 2D grids for finite difference"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "2.0"
def classFactory(iface):
    # load Gridder class from file Gridder
    from qgridder import QGridder
    return QGridder(iface)
