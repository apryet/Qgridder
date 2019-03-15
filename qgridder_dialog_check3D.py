# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_dialog_check3D.py
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


from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *

from .qgridder_dialog_base import QGridderDialog
from .ui_qgridder_check3D import Ui_QGridderCheck3D

from . import qgridder_utils
from .qgridder_utils import ftools_utils

import numpy as np


class QGridderDialogCheck3D(QGridderDialog, Ui_QGridderCheck3D):
    """
    Grid creation dialog
    """
    def __init__(self,iface, settings):

        # Set up the user interface from Designer.
        QDialog.__init__(self)
        self.iface = iface
        self.settings = settings
        self.setupUi(self)


        # Connect buttons
        self.buttonLayer3DUp.clicked.connect(self.layer3D_up)
        self.buttonLayer3DDown.clicked.connect(self.layer3D_down)
        self.buttonLayer3DRemove.clicked.connect(self.remove_layer3D)
        self.buttonAddNewLayer3D.clicked.connect(self.add_new_layer3D)
        self.buttonAddExistingLayer3D.clicked.connect(self.add_existing_layer3D)
        self.buttonCheck3D.clicked.connect(self.run_check3D)
        
        # Populate model name list
        self.populate_layer_list(self.listReferenceGrid)
        self.populate_layer_list(self.listExistingLayer)

        # Set encoding 
        self.encoding = 'System'
        

    # ========== update listLayers3D
    def update_listLayers3D(self) :
        NamesofLayersInMapCanvas =  []
        # load list of every layers in map canvas
        for layer in self.iface.mapCanvas().layers() :
            NamesofLayersInMapCanvas.append(layer.name())
        # check whether each layer of the listLayers3D list is loaded
        itemRemoved = True
        while( itemRemoved == True ) :
            itemRemoved = False
            for row in range(self.listLayers3D.count()) :
                if self.listLayers3D.item(row) != None :
                    if self.listLayers3D.item(row).text() not in NamesofLayersInMapCanvas :
                        self.listLayers3D.takeItem(row)
                        itemRemoved = True
                        break

    # ---------- Pseudo 3D grid management --------------------------------

    def layer3D_up(self):
        itemRow = self.listLayers3D.currentRow()
        if itemRow > 0 :
            item = self.listLayers3D.takeItem(itemRow)
            self.listLayers3D.insertItem(itemRow-1,item)
            self.listLayers3D.setCurrentRow(itemRow-1)

    def layer3D_down(self):
        itemRow = self.listLayers3D.currentRow()
        if itemRow < self.listLayers3D.count() - 1 :
            item = self.listLayers3D.takeItem(itemRow)
            self.listLayers3D.insertItem(itemRow+1,item)
            self.listLayers3D.setCurrentRow(itemRow+1)

    def remove_layer3D(self):
        itemRow = self.listLayers3D.currentRow()
        removedItem = self.listLayers3D.takeItem(itemRow)

    def add_new_layer3D(self):
        # fetch reference grid from listReferenceGrid
        ReferenceGridLayerName = self.listReferenceGrid.currentText()
        if not ReferenceGridLayerName == "":
            ReferenceGridLayer = ftools_utils.getMapLayerByName( unicode( ReferenceGridLayerName ) )

        # Copy reference grid to shapefile to user defined location
        OutFileName, Encoding = ftools_utils.saveDialog( self )
        if OutFileName == None :
            return()

        # write new layer to shapefile
        ftools_utils.writeVectorLayerToShape( ReferenceGridLayer, OutFileName, Encoding )

        # get new layer name
        file_info = QFileInfo( OutFileName )
        if file_info.exists():
            newLayerName = file_info.completeBaseName()
        else :
            newLayerName = OutFileName

        # check whether this layer name is already in the 3D list
        if len(self.listLayers3D.findItems(newLayerName,Qt.MatchFixedString)) != 0 :
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("This layer is already in the list."))
            return()

        # Load new layer into map canvas ...
        for (name,layer) in QgsProject.instance().mapLayers().items():
            # Note : reload() doesn't work.
            if layer.source()== OutFileName:
                QgsMapLayerRegistry.instance().removeMapLayers( layer.id() )
        ftools_utils.addShapeToCanvas( OutFileName )

        # add new layer to listLayers3D
        self.listLayers3D.addItem(newLayerName)

    def add_existing_layer3D(self):
        # get layer name
        existingGridLayerName = self.listExistingLayer.currentText()
        # check whether current layer is not already in the list
        if len(self.listLayers3D.findItems(existingGridLayerName,Qt.MatchFixedString)) == 0 :
            # add new layer
            self.listLayers3D.addItem(existingGridLayerName)
        else :
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("This layer is already in the list.")
                    )

    def run_check3D(self):
        allLayers = []
        topoRules = {'model':'nested', 'nmax':2,'pmax':4}
        for row in range( self.listLayers3D.count() ) :
            vLayerName = self.listLayers3D.item(row).text()
            vLayer  = ftools_utils.getMapLayerByName( unicode( vLayerName ) )
            allLayers.append(vLayer)
        qgridder_utils.correct_pseudo3D_grid(allLayers, topoRules)
        QMessageBox.information(self, self.tr("Qgridder"),
            self.tr('pseudo-3D grid topology successfully checked and corrected')
        )
        # Refresh map canvas
        self.iface.mapCanvas().refresh()
        return()


