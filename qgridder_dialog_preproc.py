# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_dialog_settings.py
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
from ui_qgridder_preproc import Ui_QGridderPreProc

import ftools_utils
import qgridder_utils

class QGridderDialogPreProc(QGridderDialog, Ui_QGridderPreProc):
    """
    Qgridder settings dialog class
    """
    def __init__(self,iface, settings):
        """
        Description
        -----------
        Initialize settings window

        """
        # Set up the user interface
        QDialog.__init__(self)
        self.iface = iface
        self.settings = settings
        self.setupUi(self)

        # Populate model name list
        self.populate_layer_list(self.listGridLayer)

        # Connect buttons
        QObject.connect(self.buttonProceedNumbering, SIGNAL("clicked()"), self.run_numbering)


    def run_numbering(self):
        """
        Description
        ----------

        """
        # selected grid layer name
        grid_layer_name = self.listGridLayer.currentText()
        # Load input grid layer
        grid_layer = ftools_utils.getMapLayerByName( unicode( grid_layer_name ) )

        res = qgridder_utils.rgrid_numbering(grid_layer)

        if res == True :
            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Numbering successful, refer to layer attribute table.")
                    )

        else :

            QMessageBox.information(self, self.tr("Gridder"),
                    self.tr("Fail to number, your grid is probably not regular.")
                    )

        self.reject()



