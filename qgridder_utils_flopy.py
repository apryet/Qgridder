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

# Compute budget for one or several cells
# If several cells are considered, the budgets are aggregated
# ml : Modflow class from flopy
# cells : the cells of interest 
#         format : [ [lay1,row1,col1], [lay2, row2, col2], ... ]
# cbc : Budget array of dimensions (ntstep, nlay, nrow, ncol, n)
#       where n=3 for 2d mesh (nlay=1) and n=3 for 3D mesh (nlay >1)  
def cells_budget(ml, cbc, cells = [], tstep = 1 ):
    """
    Description

    Parameters
    ----------
    p1 : parameter 1

    Returns
    -------

    out1 : output1

    Examples
    --------
    >>> 
    """

    # Get model dimensions from Flopy class
    nrow, ncol, nlay, nper = ml.nrow_ncol_nlay_nper

    # init output variable
    cellsBudget3D = 0

    # iterate over considered cells
    for cell in cells : 
	lay, row, col = cell

	left = right = front = back = above = below = 0

	# for any cell flow through right and front face are available
	# note : front face between cell i,j,k and i+1,j,l
	# note : right face between cell i, j, k and i, j+1, k
	right = cbc[tstep - 1, lay-1,row-1,col-1,1]
	front = cbc[tstep-1,lay-1,row-1,col-1,2]

	# if the model has multiple layers, consider the neighbor below
	if nlay > 1 :
	    below = cbc[tstep-1,lay-1,row-1,col-1,3]
	# if the cell considered is not at the grid left border, consider the left neighbor
	if col - 2 >= 0 :
	    left  = cbc[tstep-1,lay-1,row-1,col-2,1]
	# if the cell considered is not at the grid right border, consider the right neighbor
	if row -2 >= 0 :
	    back  = cbc[tstep-1,lay-1,row-2,col-1,2]
	# if the cell considered is not in the first layer, consider the layer above
	if lay -2 >= 0 : 
	    above = cbc[tstep-1,lay-2,row-1,col-1,3]

	# compute budget
	cellsBudget3D += left + back + above - right - front - below 	

    return(cellsBudget3D)


