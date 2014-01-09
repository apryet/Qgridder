# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GridderDialog
                                 A QGIS plugin
 BUILDS 2D grids for finite difference
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

from ui_qgridder import Ui_QGridder

import ftools_utils
import qgridder_utils

import numpy as np

# create the dialog for zoom to point
class QGridderDialog(QDialog, Ui_QGridder):
    def __init__(self,iface):

	# Set up the user interface from Designer.
     	QDialog.__init__(self)
	self.iface = iface
	self.setupUi(self)

	# Set up widgets
	self.checkRatio.setCheckState(Qt.Checked)
	self.checkLoadLayer.setCheckState(Qt.Checked)
	self.checkDivideRatio.setCheckState(Qt.Checked)
	self.checkTopo.setCheckState(Qt.Checked)
	
	# Connect buttons
	QObject.connect(self.buttonUpdateFromLayer, SIGNAL("clicked()"), self.update_from_layer)
	QObject.connect(self.buttonUpdateFromCanvas, SIGNAL("clicked()"), self.update_from_canvas)
	QObject.connect(self.buttonBrowse, SIGNAL("clicked()"), self.out_file)
	QObject.connect(self.buttonWriteGrid, SIGNAL("clicked()"), self.run_write_grid)
	QObject.connect(self.buttonRegularRefile, SIGNAL("clicked()"), self.run_regular_refine)
	QObject.connect(self.buttonExport, SIGNAL("clicked()"), self.run_export)
	QObject.connect(self.buttonProceedNumbering, SIGNAL("clicked()"), self.run_preprocessing)

	# Connect actions
	QObject.connect(self.sboxXres, SIGNAL("valueChanged(double)"), self.set_Yres)
	QObject.connect(self.sboxDivideHoriz, SIGNAL("valueChanged(int)"), self.set_divide_vert)
	
	QObject.connect(self.textXmin, SIGNAL("textChanged(const QString &)"), self.estim_number_grid_cells)
	QObject.connect(self.textXmax, SIGNAL("textChanged(const QString &)"), self.estim_number_grid_cells)
	QObject.connect(self.textYmin, SIGNAL("textChanged(const QString &)"), self.estim_number_grid_cells)
	QObject.connect(self.textYmax, SIGNAL("textChanged(const QString &)"), self.estim_number_grid_cells)
	QObject.connect(self.sboxXres, SIGNAL("valueChanged(double)"), self.estim_number_grid_cells)
	QObject.connect(self.sboxYres, SIGNAL("valueChanged(double)"), self.estim_number_grid_cells)

	# Populate layer list
	for modelName in ['Modflow','Newsam']:
	    self.listModelName.addItem(unicode(modelName))

	# Populate model name list
	self.populate_layers(self.listSourceLayer)
	self.populate_layers(self.listGridLayer)

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
	self.labelIterations.hide()
	self.labelIter.hide()

	# Init variables 
	self.OutFileName = 'grid.shp'
	self.encoding = 'System'


    #  ======= Update automatically when 1:1 ratio is checked
    def set_Yres(self, value):
        if self.checkRatio.isChecked():
            self.sboxYres.setValue(value)

    def set_divide_vert(self, value):
	if self.checkDivideRatio.isChecked():
            self.sboxDivideVert.setValue(value)

    #  ======= Choose output shape file
    def out_file(self):
        self.textOutFilename.clear()
        ( self.OutFileName, self.encoding ) = ftools_utils.saveDialog( self )
        if self.OutFileName is None or self.encoding is None:
            return
        self.textOutFilename.setText( self.OutFileName  )

    #  ======= Populate input layer list
    def populate_layers( self,listOfLayers):
        listOfLayers.clear()
        layermap = QgsMapLayerRegistry.instance().mapLayers()

	if type(layermap)==dict :
	    if len(layermap) > 0:
		listOfLayers.setEnabled(True)
		for name, layer in layermap.iteritems():
		    listOfLayers.addItem( unicode( layer.name() ) )
		    if layer == self.iface.activeLayer():
			listOfLayers.setCurrentIndex( self.listSourceLayer.count() -1 )
	    else :
		listOfLayers.setEnabled(False)
	else :
	    listOfLayers.setEnabled(False)
	    

    #  ======= Update extents from layer
    def update_from_layer( self ):
        mLayerName = self.listSourceLayer.currentText()
        if not mLayerName == "":
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
			self.tr("Invalid extent or resolution entered")
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
	    #rectFeat.setAttributeMap(fields)
	    rectFeat.initAttributes(1)
	    idVar = 0
	    #rectFeat.addAttribute(0, QVariant(idVar))
	    rectFeat.setAttribute(0, idVar)

	    # if the file exits, remove it
	    check = QFile(self.OutFileName)
	    if QFile(self.OutFileName).exists():
		if not QgsVectorFileWriter.deleteShapeFile(self.OutFileName):
		    return

	    # Load shape file writer
	    #writer = QgsVectorFileWriter(str(self.OutFileName), self.encoding, fields, QGis.WKBPolygon, crs)
	    writer = QgsVectorFileWriter(unicode(self.OutFileName), self.encoding, fields, QGis.WKBPolygon, crs)
	    
	    # Call function to make grid
	    qgridder_utils.make_rgrid(rectFeat, n, m, writer, self.progressBarBuildGrid)

	    # Delete writer
	    del writer

	    # Post-operation information
	    QApplication.restoreOverrideCursor()
	    QMessageBox.information(self, self.tr("Generate Vector Grid"), 
		    "Created output shapefile:\n" + unicode(self.OutFileName) + "\n"
		    )

	    # Load output layer if it is not already loaded
	    if self.checkLoadLayer.isChecked():
		# list currently loaded layer. If the layer is loaded, unload it.	
		for (name,layer) in	QgsMapLayerRegistry.instance().mapLayers().iteritems():
		    # Note : reload() doesn't work.
		    if layer.source()==self.OutFileName:
			QgsMapLayerRegistry.instance().removeMapLayers( layer.id() )
			
		# load layer
		ftools_utils.addShapeToCanvas( self.OutFileName )
		# update layer list in plugin
		self.populate_layers(self.listSourceLayer)
		self.populate_layers(self.listGridLayer)
	# Enable Write Grid button
	self.buttonWriteGrid.setEnabled( True )


    # ======= Refine grid ========================================
    def run_regular_refine(self):

	# selected grid layer name 
	grid_layer_name = self.listGridLayer.currentText()
	# number of elements, horizontally
	n =  self.sboxDivideHoriz.value()
	# number of elements, vertically
	m = self.sboxDivideVert.value() 

	# Check input data
        if (type(n) != int or type(m) != int or m<1 or n<1):
            QMessageBox.information(self, self.tr("Gridder"), 
		    self.tr("Can't divide features, please verify the number of elements")
		    )
	    return
        elif (grid_layer_name == "") :
            QMessageBox.information(self, self.tr("Gridder"),
		    self.tr("Please specify a valid vector layer shapefile")
		    )
	    return


	if self.listModelName.currentText() == 'Newsam':
	    if n != m :
		QMessageBox.information(self, self.tr("Qgridder"),
			self.tr("Only 1:1 ratio for Newsam")
		    )
		return

	    if n not in (2, 4) :
		QMessageBox.information(self, self.tr("Qgridder"),
			self.tr("For Newsam, you can only divide cells by 2 or 4")
		    )
		return

	# Set up topo Rules
	if self.checkTopo.isChecked() :
	    if self.listModelName.currentText() == 'Modflow':
		topoRules = {'model':'modflow','nmax':1}
	    elif self.listModelName.currentText() == 'Newsam': 
		 topoRules = {'model':'newsam', 'nmax':2}
	    else :
		QMessageBox.information(self, self.tr("Gridder"),
		    self.tr("Unknown model name for topology check")
		    )
		return
	else :
	    topoRules = {'model': None, 'nmax': None}


	# Load input grid layer
	grid_layer = ftools_utils.getMapLayerByName( unicode( grid_layer_name ) )
		
	if (grid_layer.selectedFeatureCount() == 0):
	    QMessageBox.information(self, self.tr("Gridder"),
		    self.tr("No selected features in the chosen grid layer.")
		    )
	    return

	# Set "wait" cursor and disable button
        QApplication.setOverrideCursor(Qt.WaitCursor)
	self.buttonRegularRefile.setEnabled( False )

	# Fetch selected features from input grid_layer
	selected_fIds = grid_layer.selectedFeaturesIds()
	
	# Clean user selection
	grid_layer.setSelectedFeatures([])

	# Init labels
	self.labelIterations.show()
	self.labelIter.show()
	self.labelIter.setText(unicode(1))

	# Refine grid 
	qgridder_utils.refine_by_split(selected_fIds, n, m, topoRules, grid_layer, self.progressBarRegularRefine, self.labelIter)

	# Post-operation information
	QMessageBox.information(self, self.tr("Gridder"), 
		self.tr("Vector Grid Refined")
		)	

	# Refresh refined grid layer
	#grid_layer.reload()
	self.iface.mapCanvas().refresh()

	# Enable Write Grid button and reset cursor
	self.buttonRegularRefile.setEnabled( True )
	QApplication.restoreOverrideCursor()

    # ======= Refine grid ========================================
    def run_export(self):

	# selected grid layer name 
	gridLayerName = self.listGridLayer.currentText()
	# selected export format
	# exportFormat = self.listExportFormat.currentText()

	# Grid numbering 
	# call grid numbering
	# 	1. compute element centroids with existing function from ftools
	#       2. classify centroids from top left to bottom right
	#       3. Numbering from this classification (with numpy sorting)

	# If export format = gis2wacs

	# call export_gis2wacs
	#ID AUTO
	# 	X1, Y1
	# 	X2, Y2
	# 	X3, Y3
	# 	X4, Y4
	# 	X1, Y1
	# END
	# ...
	#END

	# If export format = text 
	# call export_txt:
	# ID PT1 PT2 PT3 PT4 PARAM1 PARAM2 ... PARAMN

    def run_preprocessing(self):

	gridLayerName = self.listGridLayer.currentText()

	gridLayer = ftools_utils.getMapLayerByName( unicode( gridLayerName ) )

	modelName = self.listModelName.currentText()

	if modelName == 'Modflow':
	    # add fields NROW, NCOL to gridLayer
	    qgridder_utils.rgrid_numbering(gridLayer)
	    # get nrow and ncol
	    gridLayer.nrow, gridLayer.ncol = qgridder_utils.get_rgrid_nrow_ncol(gridLayer)
	    # get delr and delc
	    gridLayer.delr, gridLayer.delc = qgridder_utils.get_rgrid_delr_delc(gridLayer)

	# Output message
	QMessageBox.information(self, self.tr("Qgridder"),
			self.tr("Variables nrow, ncol, delr, delc have been added to the vector layer \n \
				To get the data : \n \
				>> vLayer = qgis.utils.iface.activeLayer() \n \
				>> ncol, nrow = vLayer.ncol, vLayer.nrow \n \
				\n \
			         Attributes NROW, NCOL have been added to the vector layer")
			)

