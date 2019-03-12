# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_utils_flopy.py
                                 Qgridder - A QGIS plugin

 This file gathers functions which facilitates interactions with Qgridder
 and Flopy : https://github.com/modflowpy/flopy

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

def cells_budget(ml, cbc, cells = [], tsteps = [], aggr = False ):
    """
    Description
    ----------
    Compute budget for one or several cells
    If several cells are considered, the budgets are aggregated

    Parameters
    ----------
    ml : Modflow class from flopy
    cbc : cell budget file, instance of CellBudgetFile
    cells :  list of tuple (lay, row, col)
    tsteps : list of time steps
    aggr : Boolean, whether to aggregate over tsteps.


    Returns :
    -------

    out1 : output1

    Examples
    --------
    >>> cbc = bf.CellBudgetFile(name + '.cbc')
    >>> cells_budget(ml,cbc, cells=[(0, 0, 0)],[0,1],aggr=False)

    """

    # Get model dimensions from Flopy class
    nrow, ncol, nlay, nper = ml.nrow_ncol_nlay_nper

    # Load data
    frf_array = cbc.get_data(text='FLOW RIGHT FACE')
    fff_array = cbc.get_data(text='FLOW FRONT FACE')

    # for 3D models only
    if nlay > 1 :
        flf_array = cbc.get_data(text='FLOW LOWER FACE')

    # for transient models only
    if nper > 1 :
        str_array = cbc.get_data(text='STORAGE')

    # init output variable
    budget = []

    # iterate over time steps

    for tstep in tsteps :

        cells_3d_budget = 0

        # iterate over considered cells
        for cell in cells :
            lay, row, col = cell

            left = right = front = back = above = below = 0

            # for any cell flow through right and front face are available
            # note : front face between cell i,j,k and i+1,j,l
            # note : right face between cell i, j, k and i, j+1, k
            right = frf_array[tstep][lay,row,col]
            front = fff_array[tstep][lay,row,col]

            # if the model has multiple layers, consider the neighbor below
            if nlay > 1 :
                below = flf_array[tstep][lay,row,col]
            # if the cell considered is not at the grid left border, consider the left neighbor
            if col - 1 >= 0 :
                left = frf_array[tstep][lay,row,col-1]
            # if the cell considered is not at the grid back border, consider the back neighbor
            if row -1 >= 0 :
                back  = fff_array[tstep][lay,row-1,col]
            # if the cell considered is not in the first layer, consider the layer above
            if lay -1 >= 0 :
                above = flf_array[tstep][lay-1,row,col]

            # compute budget
            cells_3d_budget += left + back + above - right - front - below

        budget.append(cells_3d_budget)

        if aggr == True:
            return( np.sum(budget) )
        else :
            return(budget)


def cells_budget_mp(ml, cbc, cells = [], tsteps = [], aggr = False ):
    """
    Description
    ----------
    Compute budget for one or several cells
    If several cells are considered, the budgets are aggregated

    Parameters
    ----------
    ml : Modflow class from flopy
    cbc : cell budget file, instance of CellBudgetFile
    cells :  list of tuple (lay, row, col)
    tsteps : list of time steps
    aggr : Boolean, whether to aggregate over tsteps.

    
    Returns : 
    -------

    out1 : output1

    Examples
    --------
    >>> cbc = bf.CellBudgetFile(name + '.cbc')
    >>> cells_budget(ml,cbc, cells=[(0, 0, 0)],[0,1],aggr=False)

    """
    # Get model dimensions from Flopy class
    nrow, ncol, nlay, nper = ml.nrow_ncol_nlay_nper

    # Load data
    frf_array = cbc.get_data(text='FLOW RIGHT FACE')
    fff_array = cbc.get_data(text='FLOW FRONT FACE')

    # for 3D models only
    if nlay > 1 : 
	flf_array = cbc.get_data(text='FLOW LOWER FACE')

    # for transient models only
    if nper > 1 :
	str_array = cbc.get_data(text='STORAGE')

    # init output variable
    budget = []

    # iterate over time steps

    for tstep in tsteps :

	cells_3d_budget = 0

	# iterate over considered cells
	for cell in cells : 
	    lay, row, col = cell

	    left = right = front = back = above = below = 0

	    # for any cell flow through right and front face are available
	    # note : front face between cell i,j,k and i+1,j,k
	    # note : right face between cell i, j, k and i, j+1, k
	    right = -frf_array[tstep][lay,row,col]
	    front = -fff_array[tstep][lay,row,col] 

	    # if the model has multiple layers, consider the neighbor below
	    if nlay > 1 :
		below = flf_array[tstep][lay,row,col]
	    # if the cell considered is not at the grid left border, consider the left neighbor
	    if col - 1 >= 0 :
		left = frf_array[tstep][lay,row,col-1]
	    # if the cell considered is not at the grid back border, consider the back neighbor
	    if row -1 >= 0 :
		back  = fff_array[tstep][lay,row-1,col]
	    # if the cell considered is not in the first layer, consider the layer above
	    if lay -1 >= 0 : 
		above = flf_array[tstep][lay-1,row,col]

	    # compute budget
	    budget_face = np.array([left,back,above,right,front,below])
	    condlist = [budget_face>0]
	    choicelist = [budget_face]
	    mp_budget = np.select(condlist, choicelist)
	    mp_budget = np.sum(mp_budget)
	    cells_3d_budget += mp_budget 

	budget.append(cells_3d_budget)

	if aggr == True:
	    return( np.sum(budget) )
	else :
	    return(budget)


