# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder.py
                                 Qgridder - A QGIS plugin

 Plugin main file. 
 
 Qgridder Builds 2D regular and unstructured grids and comes together with 
 pre- and post-processing capabilities for spatially distributed modeling.

			      -------------------
        begin                : 2013-04-08
        copyright            : (C) 2013 by Pryet
        email                : alexandre.pryet@ensegid.fr
 ***************************************************************************/
 This plugin uses functions from fTools
     Copyright (C) 2008-2011  Carson Farmer
     EMAIL: carson.farmer (at) gmail.com
     WEB  : http://www.ftools.ca/fTools.html

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Import PyQt and QGIS modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialogs
from qgridder_dialog_new import QGridderDialogNew
from qgridder_dialog_refinement import QGridderDialogRefinement
from qgridder_dialog_check3D import QGridderDialogCheck3D
from qgridder_dialog_preproc import QGridderDialogPreproc
from qgridder_dialog_plot import QGridderDialogPlot
from qgridder_dialog_export import QGridderDialogExport
from qgridder_dialog_settings import QGridderDialogSettings

#  ---------------------------------------------
class QGridder:
    """
    Description
    -----------
    Qgridder plugin class 
    """


    def __init__(self, iface):
	"""
	Description
	-----------
	Initialize Qgridder plugin
	"""
        # Save reference to the QGIS interface
        self.iface = iface

	# load settings
	self.settings = QgridderSettings()

        # Create the dialogs and keep reference
        self.dlg_new = QGridderDialogNew(self.iface, self.settings)
        self.dlg_refinement = QGridderDialogRefinement(self.iface,  self.settings)
        self.dlg_check3D = QGridderDialogCheck3D(self.iface,  self.settings)
        self.dlg_plot = QGridderDialogPlot(self.iface,  self.settings)
        self.dlg_export = QGridderDialogExport(self.iface,  self.settings)
        self.dlg_settings = QGridderDialogSettings(self.iface,  self.settings)
	# Initialize menu
	self.qgridder_menu = None
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/Qgridder"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale")[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/Qgridder_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
   
    def initGui(self):
	"""
	Description
	-----------
	Initialize plugin Gui :  dialogs, icons and menu
	"""
	#Create actions that will set up plugin
        self.action_new = QAction(QIcon(":/plugins/Qgridder/icon_new.png"), \
            "New grid", self.iface.mainWindow())
	self.action_refinement = QAction(QIcon(":/plugins/Qgridder/icon_refinement.png"), \
            "Refine grid", self.iface.mainWindow())
	self.action_check3D = QAction(QIcon(":/plugins/Qgridder/icon_check3D.png"), \
            "3D grid", self.iface.mainWindow())
	self.action_plot = QAction(QIcon(":/plugins/Qgridder/icon_plot.png"), \
            "Plot chart", self.iface.mainWindow())
	self.action_export = QAction(QIcon(":/plugins/Qgridder/icon_export.png"), \
            "Export", self.iface.mainWindow())
	self.action_settings = QAction(QIcon(":/plugins/Qgridder/icon_settings.png"), \
            "Settings", self.iface.mainWindow())

        # connect the action to the run method
        QObject.connect(self.action_new, SIGNAL("activated()"), self.run_new)
        QObject.connect(self.action_refinement, SIGNAL("activated()"), self.run_refinement)
        QObject.connect(self.action_check3D, SIGNAL("activated()"), self.run_check3D)
        QObject.connect(self.action_plot, SIGNAL("activated()"), self.run_plot)
        QObject.connect(self.action_export, SIGNAL("activated()"), self.run_export)
        QObject.connect(self.action_settings, SIGNAL("activated()"), self.run_settings)

        # Add toolbar buttons 
        self.iface.addToolBarIcon(self.action_new)
        self.iface.addToolBarIcon(self.action_refinement)
        self.iface.addToolBarIcon(self.action_check3D)
        self.iface.addToolBarIcon(self.action_plot)
        self.iface.addToolBarIcon(self.action_export)
        self.iface.addToolBarIcon(self.action_settings)

	# Add menu items
        self.iface.addPluginToMenu("Qgridder", self.action_new)
        self.iface.addPluginToMenu("Qgridder", self.action_refinement)
        self.iface.addPluginToMenu("Qgridder", self.action_check3D)
        self.iface.addPluginToMenu("Qgridder", self.action_plot)
        self.iface.addPluginToMenu("Qgridder", self.action_export)
        self.iface.addPluginToMenu("Qgridder", self.action_settings)

    def unload(self):
	"""
	Description
	-----------
	Remove the plugin menu item and icon
	"""
	self.iface.removeToolBarIcon(self.action_new)
        self.iface.removeToolBarIcon(self.action_refinement)
        self.iface.removeToolBarIcon(self.action_check3D)
        self.iface.removeToolBarIcon(self.action_plot)
        self.iface.removeToolBarIcon(self.action_export)
        self.iface.removeToolBarIcon(self.action_settings)

	self.iface.removePluginMenu("Qgridder", self.action_new)
        self.iface.removePluginMenu("Qgridder", self.action_refinement)
        self.iface.removePluginMenu("Qgridder", self.action_check3D)
        self.iface.removePluginMenu("Qgridder", self.action_plot)
        self.iface.removePluginMenu("Qgridder", self.action_export)
        self.iface.removePluginMenu("Qgridder", self.action_settings)



    def run_new(self):
	"""
	Description
	-----------
	Launch grid creation dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# Populate layer list
	self.dlg_new.populate_layer_list(self.dlg_new.listSourceLayer)
	# Get update extents from map canvas
	self.dlg_new.update_from_canvas()
	# show the dialog
	self.dlg_new.show()
	# Run the dialog event loop
	result = self.dlg_new.exec_()

    def run_refinement(self):
	"""
	Description
	-----------
	Launch grid refinement dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# Populate layer list
	self.dlg_refinement.populate_layer_list(self.dlg_refinement.listGridLayer)

	# show the dialog
	self.dlg_refinement.show()
	# Run the dialog event loop
	result = self.dlg_refinement.exec_()

    def run_check3D(self):
	"""
	Description
	-----------
	Launch pseudo 3D grid topology check dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# Populate layer list
	self.dlg_check3D.populate_layer_list(self.dlg_check3D.listReferenceGrid)
	self.dlg_check3D.populate_layer_list(self.dlg_check3D.listExistingLayer)

	# show the dialog
	self.dlg_check3D.show()
	# Run the dialog event loop
	result = self.dlg_check3D.exec_()

    def run_plot(self):
	"""
	Description
	-----------
	Launch plot chart dialog 
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# show the dialog
	self.dlg_plot.show()
	# plot data
	self.dlg_plot.run_plot()
	# Run the dialog event loop
	result = self.dlg_plot.exec_()

    def run_preproc(self):
	"""
	Description
	-----------
	Launch pre-processing dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# show the dialog
	self.dlg_preproc.show()
	# Run the dialog event loop
	result = self.dlg_preproc.exec_()

    def run_export(self):
	"""
	Description
	-----------
	Launch grid creation dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )
	# Populate layer list
	self.dlg_export.populate_layer_list(self.dlg_export.listGridLayer)

	# show the dialog
	self.dlg_export.show()
	# Run the dialog event loop
	result = self.dlg_export.exec_()

    def run_settings(self):
	"""
	Description
	-----------
	Launch grid creation dialog
	"""
	# update settings
	self.settings.load_settings( QgsProject.instance() )

	# refresh dialog with current settings
	self.dlg_settings.load_settings_to_dialog()

	# show the dialog
	self.dlg_settings.show()
	# Run the dialog event loop
	result = self.dlg_settings.exec_()


class QgridderSettings : 
    """
    Description
    -----------
    Qgridder settings
    """
    def __init__(self) :
	self.proj = QgsProject.instance()
	# default settings
	self.dic_settings = { 'model_type':'Modflow',
		'obs_dir':'./', 
		'simul_file':'simul.file',
		'model_src_dir':'./',
		'simul_start_date':'2015-01-01 00:00',
		'support_grid_layer_name' : 'gridLayer',
		'plot_obs':'True',
		'plot_simul':'False'
		}
	# support model types (grid topology)
	self.model_types = ['Modflow','Newsam']
	# load settings from Qgis project
	self.load_settings(self.proj)
    
    def load_settings(self, proj) : 
	"""
	Description
	-----------
	Load settings from Qgis project
	"""
	# make a copy of current settings
	dic_settings = self.dic_settings.copy()

	# load settings from Qgis project
	success = True
	for key in dic_settings.keys() :
	    dic_settings[key], valid_entry = self.proj.readEntry('qgridder', str(key))
	    success = success * valid_entry

	# if successful, update dic_settings
	if success : 
	    self.dic_settings = dic_settings
		    
	return(success)

	
    def save_settings(self, proj) : 
	"""
	Description
	-----------
	Save settings to Qgis project
	"""

	success = True
	for key,val in zip(self.dic_settings.keys(),self.dic_settings.values()) :
	    success = success*self.proj.writeEntry('qgridder', str(key), str(val))

	return(success)


    def update_settings(self, dic_settings) : 
	"""
	Description
	-----------
	Update settings from Qgis project
	"""

	self.dic_settings = dic_settings




