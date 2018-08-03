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
from ui_qgridder_export import Ui_QGridderExport

import ftools_utils
import qgridder_utils

class QGridderDialogExport(QGridderDialog, Ui_QGridderExport):
    """
    Qgridder settings dialog class
    """
    def __init__(self,iface, settings):
        """
        Description
        -----------
        Initialize export window

        """
        # Set up the user interface
        QDialog.__init__(self)
        self.iface = iface
        self.settings = settings
        self.setupUi(self)
        self.proj = QgsProject.instance()

        # Connect buttons
        QObject.connect(self.buttonExportTextFile, SIGNAL("clicked()"), self.export_geometry)
        QObject.connect(self.buttonBrowseOutputFile, SIGNAL("clicked()"), self.out_text_file)

        # Populate layer list
        self.populate_layer_list(self.listGridLayer)


    def out_text_file(self):
        """
        Description
        -----------
        Choose output shape file

        """

        self.textOutTextFileName.clear()
        fileName, self.encoding  = ftools_utils.saveDialog( self )
        if fileName is None or self.encoding is None:
            return
        self.textOutTextFileName.setText( fileName  )


    def export_geometry(self) :
        """
        Description
        -----------
        Export grid to text file

        """

        gridLayerName = self.listGridLayer.currentText()

        outTextFileName = self.textOutTextFileName.text()

        # settings
        delimiter = ','
        lineterminator = '\r'
        max_decimals = 2

        # Error checks
        if len(outTextFileName) <= 0:
                return "No output file given"

        gridLayer = ftools_utils.getMapLayerByName( unicode( gridLayerName ) )

        if gridLayer == None:
                return "Layer " + gridLayerName + " not found"

        # Create the CSV file
        try:
                txtfile = open(outTextFileName, 'w')
        except ValueError:
            print "Writing Error.  Try again..."

        # Iterate through each feature in the source layer
        feature_count = gridLayer.dataProvider().featureCount()

        # Initialize progress bar
        progress=QProgressDialog("Exporting attributes...", "Abort Export", 0, feature_count);
        progress.setWindowModality(Qt.WindowModal)

        # Select all features along with their attributes
        allAttrs = gridLayer.pendingAllAttributesList()
        gridLayer.select(allAttrs)

        # Iterate over grid cells
        for feat in gridLayer.getFeatures():
            p0, p1, p2, p3 = ftools_utils.extractPoints(feat.geometry())[:4]
            txtfile.write(str(feat.id()) + ' AUTO' + lineterminator)
            for point in [p0,p1,p2,p3,p0]:
                xcoor = round(point.x(), max_decimals)
                ycoor = round(point.y(), max_decimals)
                txtfile.write('\t' + str(xcoor) + delimiter + str(ycoor) + lineterminator)
            txtfile.write('END' + lineterminator)
            progress.setValue(feat.id())
            if (progress.wasCanceled()):
                   return "Export canceled "

        txtfile.write('END' + lineterminator)

        progress.close()
        txtfile.close()

