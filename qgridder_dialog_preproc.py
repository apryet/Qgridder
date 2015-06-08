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
from ui_qgridder_preproc import Ui_QGridderPreproc

import ftools_utils
import qgridder_utils

class QGridderDialogPreproc(QGridderDialog, Ui_QGridderPreproc):
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
	self.proj = QgsProject.instance()

	# Connect buttons
	QObject.connect(self.buttonBrowseObsDir, SIGNAL("clicked()"), self.browse_obs_directory)
	QObject.connect(self.buttonBrowseSimulFile, SIGNAL("clicked()"), self.browse_simul_file)
	QObject.connect(self.buttonOK, SIGNAL("clicked()"), self.commit_changes)
	QObject.connect(self.buttonCancel, SIGNAL("clicked()"), self.exit)

	# Populate model type list
	model_types = ['Modflow','Newsam']
	for model_type in model_types :
	    self.listModelTypes.addItem(unicode(model_type))


	# if available, load settings from qgis project qgridder entries
	model_type = self.proj.readEntry('qgridder','model_type')
	obs_dir = self.proj.readEntry('qgridder','obs_dir')
	simul_file = self.proj.readEntry('qgridder','simul_file')

	if model_type[0] in model_types : 
	    self.listModelTypes.setCurrentIndex(listModelTypes.findText(model_type[0]))

	if obs_dir[1] : 
	    self.textObsDir.setText(str(obs_dir[0]))

	if simul_file[1] :
	    self.textSimulFile.setText(str(obs_file[0]))


    def browse_simul_file(self):
	"""
	Description
	----------
	Select simulation file. This file will be used to load simulation results.
	Note that this is model-dependent.

	"""
	    
        self.textSimulFile.clear()
        ( simul_file, encoding ) = ftools_utils.saveDialog( self )
        if simul_file is None or encoding is None:
            return
        self.textSimulFile.setText( self.OutFileName  )

    def browse_obs_directory(self):
	"""
	Description
	----------
	Select observation directory which contains CSV observations files
 
	"""
	    
        self.textObsDir.clear()
        ( simul_file, encoding ) = ftools_utils.dirDialog( self )
        if simul_file is None or encoding is None :
            return
        self.textObsDir.setText( self.simul_file  )


    def commit_changes(self):
	"""
	Description
	----------
	Save changes to project instance and close settings

	"""
	model_type = str(self.listModelTypes.currentText())
	obs_dir = str(self.textObsDir.text())
	simul_file = str(self.textSimulFile.text())

	success = True

	success = success*self.proj.writeEntry('qgridder','model_type', model_type)
	success = success*self.proj.writeEntry('qgridder','obs_dir', obs_dir)
	success = success*self.proj.writeEntry('qgridder','simul_file', simul_file)

	self.reject()


    def exit(self):
	"""
	Description
	----------
	Close settings without saving

	"""
	    
        self.reject()

		
