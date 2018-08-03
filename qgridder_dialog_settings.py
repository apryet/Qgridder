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
from ui_qgridder_settings import Ui_QGridderSettings

import ftools_utils


class QGridderDialogSettings(QGridderDialog, Ui_QGridderSettings):
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
        QObject.connect(self.buttonBrowseModelSrcDir, SIGNAL("clicked()"), self.browse_model_src_dir)
        QObject.connect(self.buttonBrowseObsDir, SIGNAL("clicked()"), self.browse_obs_dir)
        QObject.connect(self.buttonBrowseSimulDir, SIGNAL("clicked()"), self.browse_simul_dir)
        QObject.connect(self.buttonBrowseSimulFile, SIGNAL("clicked()"), self.browse_simul_file)
        QObject.connect(self.buttonOK, SIGNAL("clicked()"), self.commit_changes)
        QObject.connect(self.buttonCancel, SIGNAL("clicked()"), self.exit)
        QObject.connect(self.listSimulSources, SIGNAL("currentIndexChanged(const QString&)"), self.update_simul_sources)
        QObject.connect(self.checkPlotSimul, SIGNAL("clicked()"), self.update_simul_sources)

        # Populate model type list
        model_types = self.settings.model_types
        for model_type in self.settings.model_types :
            self.listModelTypes.addItem(unicode(model_type))

        # Populate source of simulation data list
        simul_data_sources = ['CSV Files', 'Flopy project']
        for simul_data_source in simul_data_sources :
            self.listSimulSources.addItem(unicode(simul_data_source))

        # update dialog from settings
        self.load_settings_to_dialog()

        # manage widget enabling
        self.update_simul_sources()

    def load_settings_to_dialog(self):

        # Populate model name list
        self.populate_layer_list(self.listGridLayer)

        # (re)load settings
        # self.settings.load_settings(self.proj)

        # load settings
        model_type = self.settings.dic_settings['model_type']
        obs_dir = self.settings.dic_settings['obs_dir']
        simul_src = self.settings.dic_settings['simul_src']
        simul_dir = self.settings.dic_settings['simul_dir']
        simul_file = self.settings.dic_settings['simul_file']
        model_src_dir = self.settings.dic_settings['model_src_dir']
        simul_start_date = self.settings.dic_settings['simul_start_date']
        support_grid_layer_name = self.settings.dic_settings['support_grid_layer_name']
        plot_obs =  self.settings.dic_settings['plot_obs']
        plot_simul =  self.settings.dic_settings['plot_simul']
        grid_backup =  self.settings.dic_settings['grid_backup']

        self.listModelTypes.setCurrentIndex(self.listModelTypes.findText(model_type))
        self.listGridLayer.setCurrentIndex(self.listGridLayer.findText(support_grid_layer_name))
        self.textObsDir.setText(str(obs_dir))
        self.textSimulDir.setText(str(simul_dir))
        self.textModelDir.setText(str(model_src_dir))
        self.textSimulStartDate.setText(str(simul_start_date))
        self.textSimulFile.setText(str(simul_file))

        if plot_obs == 'True' :
            self.checkPlotObs.setChecked( True )
        else :
            self.checkPlotObs.setChecked( False )

        if plot_simul == 'True' :
            self.checkPlotSimul.setChecked( True )
        else :
            self.checkPlotSimul.setChecked( False )

        if grid_backup == 'True' :
            self.checkGridBackup.setChecked( True )
        else :
            self.checkGridBackup.setChecked( False )


    def browse_simul_file(self):
        """
        Description
        ----------
        Select simulation file. This file will be used to load simulation results.
        Note that this is model-dependent.

        """

        self.textSimulFile.clear()
        ( simul_file, encoding ) = ftools_utils.openDialog( self, filtering="All files (*.*)" )
        if simul_file is None or encoding is None:
            return
        self.textSimulFile.setText( simul_file  )

    def browse_obs_dir(self):
        """
        Description
        ----------
        Select directory which contains CSV observations files

        """

        self.textObsDir.clear()
        ( obs_dir, encoding ) = ftools_utils.dirDialog( self )
        if obs_dir is None or encoding is None :
            return
        self.textObsDir.setText( obs_dir  )

    def browse_simul_dir(self):
        """
        Description
        ----------
        Select directory which contains CSV simulation files

        """

        self.textSimulDir.clear()
        ( simul_dir, encoding ) = ftools_utils.dirDialog( self )
        if simul_dir is None or encoding is None :
            return
        self.textSimulDir.setText( simul_dir  )



    def browse_model_src_dir(self):
        """
        Description
        ----------
        Select path to model python modules (e.g. Flopy)

        """

        self.textModelDir.clear()
        ( model_src_dir, encoding ) = ftools_utils.dirDialog( self )
        if model_src_dir is None or encoding is None :
            return
        self.textModelDir.setText( model_src_dir  )



    def commit_changes(self):
        """
        Description
        ----------
        Save changes to project instance and close settings

        """
        dic_settings = self.settings.dic_settings.copy()

        dic_settings['model_type'] = str(self.listModelTypes.currentText())
        dic_settings['obs_dir'] = str(self.textObsDir.text())
        dic_settings['simul_src'] = str(self.listSimulSources.currentText())
        dic_settings['simul_dir'] = str(self.textSimulDir.text())
        dic_settings['simul_file'] = str(self.textSimulFile.text())
        dic_settings['simul_start_date'] = str(self.textSimulStartDate.text())
        dic_settings['model_src_dir'] = str(self.textModelDir.text())
        dic_settings['support_grid_layer_name'] = str(self.listGridLayer.currentText())
        dic_settings['plot_obs'] = str(self.checkPlotObs.isChecked())
        dic_settings['plot_simul'] = str(self.checkPlotSimul.isChecked())
        dic_settings['grid_backup'] = str(self.checkGridBackup.isChecked())

        # update self.settings.dic_settings
        self.settings.update_settings(dic_settings)

        # save settings to project
        self.settings.save_settings(self.proj)

        self.reject()


    def update_simul_sources(self):

        if self.checkPlotSimul.isChecked() :

            self.listSimulSources.setEnabled(True)
            self.labelSimulSources.setEnabled(True)

            if self.listSimulSources.currentText() == 'CSV Files':
                self.groupBoxSimulText.setEnabled(True)
                self.groupBoxSimulFlopy.setEnabled(False)

            if self.listSimulSources.currentText() == 'Flopy project':
                self.groupBoxSimulText.setEnabled(False)
                self.groupBoxSimulFlopy.setEnabled(True)

        else :
            self.listSimulSources.setEnabled(False)
            self.labelSimulSources.setEnabled(False)
            self.groupBoxSimulText.setEnabled(False)
            self.groupBoxSimulFlopy.setEnabled(False)


    def exit(self):
        """
        Description
        ----------
        Close settings without saving

        """

        self.reject()


