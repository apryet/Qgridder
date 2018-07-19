# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridderdialog_base.py
                                 Qgridder - A QGIS plugin

 This file handles Qgridder graphical user interface                           

 Qgridder Builds 2D regular and unstructured grids and comes together with 
 pre- and post-processing capabilities for spatially distributed modeling.

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
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class QGridderDialog(QDialog):
    """
    Qgridder base dialog
    """
    def __init__(self,iface):

        # Set up the user interface from Designer.
        self.iface = iface

        #  ======= Populate input layer list
    def populate_layer_list(self,listOfLayers):
        listOfLayers.clear()
        layermap = QgsMapLayerRegistry.instance().mapLayers()

        if type(layermap)==dict :
            if len(layermap) > 0:
                listOfLayers.setEnabled(True)
                for name, layer in layermap.iteritems():
                    listOfLayers.addItem( unicode( layer.name() ) )
                    if layer == self.iface.activeLayer():
                        listOfLayers.setCurrentIndex( listOfLayers.count() -1 )
            else :
                listOfLayers.setEnabled(False)
        else :
            listOfLayers.setEnabled(False)



