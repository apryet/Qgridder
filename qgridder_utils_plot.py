# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_utils_plot.py
                                 Qgridder - A QGIS plugin

 This file gathers functions which facilitate pre- and post-processing of
 spatially distributed numerical models based on Qgridder grids.

 Qgridder builds 2D regular and unstructured grids and comes together with
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
 ****
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
import numpy as np
from math import *

from qgridder_utils_base import *
import ftools_utils

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

# ======= Plot
def plot_chart(obs = {'t':[], 'val':[]}, simul = {'t':[], 'val':[]}, xlim = [], ylim = [], title=''):
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
    axes = plt.axes()
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
    plt.show()


