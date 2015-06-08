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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from qgridder_dialog_base import QGridderDialog
from ui_qgridder_refinement import Ui_QGridderRefinement

import ftools_utils
import qgridder_utils

import numpy as np

class QGridderDialogRefinement(QGridderDialog, Ui_QGridderRefinement):
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
	QObject.connect(self.buttonRefine, SIGNAL("clicked()"), self.run_regular_refine)

	# Populate model name list
	self.populate_layer_list(self.listGridLayer)

	# Init labels
	self.labelIterations.hide()
	self.labelIter.hide()

    #  ======= Update automatically when 1:1 ratio is checked
    def set_divide_vert(self, value):
	if self.checkDivideRatio.isChecked():
            self.sboxDivideVert.setValue(value)


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


	if self.settings.dic_settings['model_type'] == 'Newsam':
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
	    if self.settings.dic_settings['model_type'] == 'Modflow':
		topoRules = {'model':'modflow','nmax':1}
	    elif self.settings.dic_settings['model_type'] == 'Newsam': 
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
	self.buttonRefine.setEnabled( False )

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
	self.iface.mapCanvas().refresh()

	# Enable Write Grid button and reset cursor
	self.buttonRefine.setEnabled( True )
	QApplication.restoreOverrideCursor()


  
