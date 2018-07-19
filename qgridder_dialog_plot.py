# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_time_utils
                        Part of Qgridder - A QGIS plugin
 Builds 2D grids for finite difference
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
from ui_qgridder_plot import Ui_QGridderPlot

import qgridder_utils
import ftools_utils

import os
import sys
import numpy as np
import datetime as dt

try : 
    import matplotlib.dates as mdates
except : 
    print('Could not load matplotlib.dates module')



# ================================================================================================
# ================================================================================================
class QGridderDialogPlot(QGridderDialog,Ui_QGridderPlot):

    # ======= Initialization
    def __init__(self, iface, settings) :
        """
        Draws a plot of observed and simulated records. Designed to accept dates from mdates on the x-axis.  

        Parameters
        ----------
        obs : dictionary  {'t':[], 'val':[] } with observed values
        simul : dictionary  {'t':[], 'val':[] } with observed values


        Returns
        -------


        Examples
        --------

        """

        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.settings = settings
        self.obs_dir = self.settings.dic_settings['obs_dir']
        self.simul_file = self.settings.dic_settings['simul_file']

        


    # ======= Plot
    def plot_chart(self, obs = {'t':[], 'val':[]}, simul = {'t':[], 'val':[]}, xlim = [], ylim = [], title=''):
        """
        Draws a plot of observed and simulated records. Designed to accept dates from mdates on the x-axis.  

        Parameters
        ----------
        obs : dictionary  {'t':[], 'val':[] } with observed values
        simul : dictionary  {'t':[], 'val':[] } with observed values


        Returns
        -------


        Examples
        --------

        """

         # initialize plot
        axes = self.widget.canvas.ax
        axes.clear()

        t_obs = obs['t']
        val_obs = obs['val']
        t_simul = simul['t']
        val_simul = simul['val']

        if len(xlim) == 2 :
            axes.set_xlim(xlim[0],xlim[1])

        if len(ylim) == 2 :
            axes.set_ylim(ylim[0],ylim[1])

        # plot records
        axes.plot(t_obs,val_obs,'g+',label='Obs.')
        axes.plot(t_simul,val_simul,'r-',label='Simul.')

        # print plot decoration
        axes.grid()

        # plot title
        axes.set_title(title)        

        # print plot decoration
        l = axes.legend()
        l.legendPatch.set_alpha(0.5)

        # show plot
        self.widget.canvas.draw()



    # Plot data
    def run_plot(self):
        """
        Draws a plot of observed and simulated records. Designed to accept dates from mdates on the x-axis.  

        Parameters
        ----------
        obs : dictionary  {'t':[], 'val':[] } with observed values
        simul : dictionary  {'t':[], 'val':[] } with observed values


        Returns
        -------


        Examples
        --------

        """
        # identify selected layer
        vLayer = self.iface.mapCanvas().currentLayer()

        # check whether a layer is selected
        if not vLayer:
            QMessageBox.warning(self.iface.mainWindow(),\
                "Qgridder Plugin Warning", 'Please choose a valid layer and select a feature before plotting.')
            return

        # check whether the selected layer is a valid vector layer
        if  vLayer.type()!=0:
            QMessageBox.warning(self.iface.mainWindow(),\
                "Qgridder Plugin Warning", 'Please choose a valid layer and select a feature before plotting.')
            return

        if vLayer.selectedFeatureCount()==0:
            QMessageBox.warning(self.iface.mainWindow(),\
                "Qgridder Plugin Warning", 'Please select one feature.')
            return
            
        elif vLayer.selectedFeatureCount()>1:
            QMessageBox.warning(self.iface.mainWindow(),\
                "Qgridder Plugin Warning", 'Please select only one feature.')
            return


        # load settings
        plot_obs = self.settings.dic_settings['plot_obs']
        plot_simul = self.settings.dic_settings['plot_simul']
        obs_dir = self.settings.dic_settings['obs_dir']
        simul_src = self.settings.dic_settings['simul_src']
        simul_dir = self.settings.dic_settings['simul_dir']
        simul_file = self.settings.dic_settings['simul_file']
        simul_start_date = self.settings.dic_settings['simul_start_date']
        model_src_dir = self.settings.dic_settings['model_src_dir']
        support_grid_layer_name = self.settings.dic_settings['support_grid_layer_name']

        # -- init variables
        dates_obs = []
        vals_obs = []
        dates_simul = []
        vals_simul = []

        obs_key_col = 'ID'
        obs_lay_col = 'lay'
        #date_string_format = '%Y-%m-%d %H:%M'
        date_string_format = '%Y-%m-%d'

        obs_lay = 0

        # get data from observation location
        obs_feature = vLayer.selectedFeatures()[0]
        obs_feature_id = obs_feature[obs_key_col]
        obs_lay = obs_feature[obs_lay_col]

        # -- Process observed records
        if plot_obs == 'True' :
            
            obs_key = obs_feature[obs_key_col]

            # get observation file
            csv_delimiter = ','
            skip_header = True

            obs_file_path = str(obs_dir) + '/' + str(obs_key) + '.csv'
            try :
                dates_obs, vals_obs = np.genfromtxt(obs_file_path,delimiter=csv_delimiter, 
                        unpack=True,skip_header=skip_header,
                        converters={ 0: mdates.strpdate2num(date_string_format)}
                        )
                dates_obs = mdates.num2date(dates_obs)

            except :
                QMessageBox.warning(self.iface.mainWindow(),\
                "Qgridder Plugin Warning", 'Error while reading file ' + obs_file_path + '\n'+
                    'Check file path and format (should be a 2 column CSV file).')



        # -- Process simulated records
        if self.settings.dic_settings['plot_simul'] == 'True' :

            # Plot from text files
            if self.settings.dic_settings['simul_src'] == 'CSV Files':
            

                obs_key = obs_feature[obs_key_col]

                # get observation file
                csv_delimiter = ','
                skip_header = True

                simul_file_path = str(simul_dir) + '/' + str(obs_key) + '.csv'
                try :
                    dates_simul, vals_simul = np.genfromtxt(simul_file_path, delimiter=csv_delimiter, 
                            unpack=True, skip_header=skip_header,
                            converters={ 0: mdates.strpdate2num(date_string_format)}
                            )
                    dates_simul = mdates.num2date(dates_simul)

                except :
                    QMessageBox.warning(self.iface.mainWindow(),\
                    "Qgridder Plugin Warning", 'Error while reading file ' + simul_file_path + '\n'+
                        'Check file path and format (should be a 2 column CSV file).')

            # Plot from Flopy project
            if self.settings.dic_settings['simul_src'] == 'Flopy project': 

                # load flopy module 
                sys.path.append(str( model_src_dir ))

                try : 
                    import flopy 

                except : 
                    QMessageBox.warning(self, self.tr("QGridder"), 
                       'Could not load flopy' 
                       )

                # fetch model reference grid
                grid_layer = ftools_utils.getVectorLayerByName(support_grid_layer_name)

                # find nearest grid cell centroid from selected point in vLayer
                dic_centroids = qgridder_utils.get_ptset_centroids(vLayer, grid_layer, idFieldName = 'ID', nNeighbors = 1)

                obs_row, obs_col, obs_dist = dic_centroids[obs_feature_id][0]

                # load simulation file
                model_dir = os.path.dirname( self.simul_file)
                os.chdir(model_dir)
                mf_model = flopy.modflow.Modflow.load(self.simul_file)
                model_name = mf_model.get_name()

                # time unit converter to seconds
                dic_itmuni_mult = {0: None, 1: 1, 2: 60,
                                    3: 3600, 4: 86400, 5: 31536000}

                # get time unit from flopy model
                itmuni = mf_model.dis.itmuni
                itmuni_mult = dic_itmuni_mult[itmuni]            

                # load results
                headobj = flopy.utils.binaryfile.HeadFile(model_dir + '/' + model_name + '.hds')

                # read binary file
                ts = headobj.get_ts( (obs_lay, obs_row, obs_col) )
                times = ts[:,0]
                vals_simul = ts[:,1]

                # generate simulation date sequence
                simul_start_date = dt.datetime.strptime(simul_start_date, '%Y-%m-%d %H:%M')
                dates_simul = [ simul_start_date + dt.timedelta(seconds = time*1.) for time in times]


        # show plot
        obs = {'t':dates_obs, 'val':vals_obs}
        simul = {'t':dates_simul, 'val':vals_simul}
        self.plot_chart(obs,simul)


