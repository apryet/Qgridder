# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridderdialog.py
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
from qgis.gui import *

from .qgridder_dialog_base import QGridderDialog
from .ui_qgridder_new import Ui_QGridderNew

from . import qgridder_utils
from .qgridder_utils import ftools_utils

import numpy as np


class QGridderDialogNew(QGridderDialog, Ui_QGridderNew):
    """
    Grid creation dialog class
    """
    def __init__(self,iface, settings):

        # Set up the user interface from Designer.
        QDialog.__init__(self)
        self.iface = iface
        self.settings = settings
        self.setupUi(self)

        # Set up widgets
        self.checkRatio.setChecked(True)
        self.checkLoadLayer.setChecked(True)

        # Connect buttons
        self.buttonUpdateFromLayer.clicked.connect(self.update_from_layer)
        self.buttonUpdateFromCanvas.clicked.connect(self.update_from_canvas)
        self.buttonBrowse.clicked.connect(self.out_file)
        self.buttonWriteGrid.clicked.connect(self.run_write_grid)

        # Connect actions
        self.sboxXres.valueChanged.connect(self.set_Yres)
        self.textXmin.textChanged.connect(self.estim_number_grid_cells)
        self.textXmax.textChanged.connect(self.estim_number_grid_cells)
        self.textYmin.textChanged.connect(self.estim_number_grid_cells)
        self.textYmax.textChanged.connect(self.estim_number_grid_cells)
        self.sboxXres.valueChanged.connect(self.estim_number_grid_cells)
        self.sboxYres.valueChanged.connect(self.estim_number_grid_cells)
        self.textOutFilename.textChanged.connect(self.set_out_file)
        
        # Populate model name list
        self.populate_layer_list(self.listSourceLayer)

        # Get update extents from map canvas
        self.update_from_canvas()

        # Set up validators
        self.textXmin.setValidator(QDoubleValidator(self.textXmin))
        self.textXmax.setValidator(QDoubleValidator(self.textXmax))
        self.textYmin.setValidator(QDoubleValidator(self.textYmin))
        self.textYmax.setValidator(QDoubleValidator(self.textYmax))

        self.defaultRes=float(10)
        self.sboxXres.setValue(self.defaultRes)
        self.sboxYres.setValue(self.defaultRes)

        # Init labels
        self.labelIter.hide()

        # Init variables
        self.OutFileName = 'grid.shp'
        self.encoding = 'System'


    #  ======= Update automatically when 1:1 ratio is checked
    def set_Yres(self, value):
        if self.checkRatio.isChecked():
            self.sboxYres.setValue(value)

    #  ======= Choose output shape file
    def out_file(self):
        self.textOutFilename.clear()
        ( self.OutFileName, self.encoding ) = ftools_utils.saveDialog( self )
        #if self.OutFileName is None or self.encoding is None:
        #    QMessageBox.information(parent, "Gridder",
        #            str( 'encoding' + str(self.encoding) + 'file: ' + str(self.OutFileName) ))
        #    return
        self.textOutFilename.setText( self.OutFileName  )
        self.raise_()
        self.activateWindow()

    #  ======= Choose output shape file
    def set_out_file(self):
        self.OutFileName = self.textOutFilename.text()

   #  ======= Update extents from layer
    def update_from_layer( self ):
        mLayerName = self.listSourceLayer.currentText()
        if not mLayerName == "" :
            mLayer = ftools_utils.getMapLayerByName( unicode( mLayerName ) )
            # get layer extents
            boundBox = mLayer.extent()
            self.update_extents( boundBox )

    #  ======= Update extents from current map canvas
    def update_from_canvas( self ):
        canvas = self.iface.mapCanvas()
        boundBox = canvas.extent()
        self.update_extents( boundBox )

    #  ======= Update extents in text boxes
    def update_extents( self, boundBox ):
        self.textXmin.setText( unicode( boundBox.xMinimum() ) )
        self.textYmin.setText( unicode( boundBox.yMinimum() ) )
        self.textXmax.setText( unicode( boundBox.xMaximum() ) )
        self.textYmax.setText( unicode( boundBox.yMaximum() ) )

    # ======= Estimate number of grid cells
    def estim_number_grid_cells(self,value = ' '):

        try :
            Xmin = float( self.textXmin.text() )
            Xmax = float( self.textXmax.text() )
            Ymin = float( self.textYmin.text() )
            Ymax = float( self.textYmax.text() )
            Xres = float( self.sboxXres.value() )
            Yres = float( self.sboxYres.value() )
            if Xres != 0 and Yres !=0:
                Nx = round((Xmax - Xmin) / Xres)
                Ny = round((Ymax - Ymin) / Yres)
                N = abs(int(Nx*Ny))
            else :
                N = ' '
        except :
            N = ' '

        self.labelNumberCells.setText( unicode(N) )

    # ======= Build grid ========================================
    def run_write_grid(self):
        self.buttonWriteGrid.setEnabled( False )

        # Check input data
        if (self.textXmin.text() == "" or self.textXmax.text() == "" or
                self.textYmin.text() == "" or self.textYmax.text() == ""):
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Please specify valid extent coordinates")
                    )
        elif self.textOutFilename.text() == "":
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Please specify valid output shapefile")
                    )
        elif self.sboxXres.value() == 0:
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Please specify valid resolution")
                    )
        elif float( self.textXmin.text() ) >= float( self.textXmax.text() ) or \
                float( self.textYmin.text() ) >= float( self.textYmax.text() ):
                    QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Check extent coordinates")
                    )
        else:
            try:
                boundBox = QgsRectangle(
                float( self.textXmin.text() ),
                float( self.textYmin.text() ),
                float( self.textXmax.text() ),
                float( self.textYmax.text() ) )
            except:
                QMessageBox.information(self, self.tr("Vector grid"),
                        self.tr("Invalid extent coordinates entered")
                        )
            Xres = self.sboxXres.value()
            Yres = self.sboxYres.value()

            # Compute number of elements
            n = int( round( (boundBox.yMaximum() - boundBox.yMinimum()) / Yres ) )
            m = int( round( (boundBox.xMaximum() - boundBox.xMinimum()) / Xres ) )

            # Adjust bounding box to respect Yres and Xres with linspace
            boundBox.setXMaximum( boundBox.xMinimum() + m*Xres )
            boundBox.setYMaximum( boundBox.yMinimum() + n*Yres )

            if n*m <= 0 :
                QMessageBox.information(self, self.tr("Gridder"),
                        self.tr("Invalid extent or resolution")
                        )
                return
            # TO DO : Here, you should check whether elements  is correct...
            # Or add it directly as information in the grid resolution frame
            QApplication.setOverrideCursor(Qt.WaitCursor)

            # ------------ Input data validated, build Grid


            # If a source layer is defined, retrieve CRS
            if ftools_utils.getMapLayerByName(unicode(self.listSourceLayer.currentText())) != None :
                crs = ftools_utils.getMapLayerByName(unicode(self.listSourceLayer.currentText())).crs()
                if not crs.isValid():
                    crs = None
            else :
                crs = None

            # Initialize field for base feature
            # TO DO : add useful attributes
            #fields = {0:QgsField("ID", QVariant.Int)}
            fields = QgsFields()
            fields.append(QgsField("ID", QVariant.Int))
            # Initialize base rectangle feature
            rectFeat = QgsFeature()
            rectGeom = QgsGeometry()
            rectFeat.setGeometry(rectGeom.fromRect(boundBox))
            rectFeat.initAttributes(1)
            idVar = 0
            rectFeat.setAttribute(0, idVar)

            # if the file exits, remove it
            check = QFile(self.OutFileName)
            if QFile(self.OutFileName).exists():
                if not QgsVectorFileWriter.deleteShapeFile(self.OutFileName):
                    QMessageBox.information(self, self.tr("Generate Vector Grid"),
                    "Cannot delete file:\n" + unicode(self.OutFileName) + "\n")
                    return

            # Load shape file writer
            writer = QgsVectorFileWriter(unicode(self.textOutFilename.text()), 
                    self.encoding, fields, QgsWkbTypes.Polygon, 
                    crs, driverName="ESRI Shapefile")

            # Call function to make grid
            qgridder_utils.make_rgrid(rectFeat, n, m, writer, self.progressBarBuildGrid)

            # Delete writer
            del writer
            
            # Load output layer if it is not already loaded
            if self.checkLoadLayer.isChecked():
                # list currently loaded layer. If the layer is loaded, unload it.
                for (name,layer) in QgsProject.instance().mapLayers().items():
                    # Note : reload() doesn't work.
                    if layer.source()==self.OutFileName:
                        QgsProject.instance().removeMapLayer( layer.id() )
                # load layer
                ftools_utils.addShapeToCanvas( self.OutFileName )
                # update layer list in plugin
                self.populate_layer_list(self.listSourceLayer)

        # Post-operation information
        QApplication.restoreOverrideCursor()

        # Enable Write Grid button
        self.buttonWriteGrid.setEnabled( True )

