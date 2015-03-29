# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_utils_base.py
                                 Qgridder - A QGIS plugin

 This file gathers main plugin functions.
 
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import numpy as np

import ftools_utils

# --------------------------------------------------------------------------------------------------------------

# Note : floating point values is an issue that deserves more attention in this script.
TOLERANCE = 1e-6  # expressed relative to a value
max_decimals = 2  # used to limit the effects of numerical noise

# --------------------------------------------------------------------------------------------------------------
# Makes regular grid of n lines and m columns,
# from QgsRectangle bbox. Resulting features are 
# appended to  vprovider
def make_rgrid(inputFeat, n, m, vprovider, progressBar = QProgressDialog("Building grid...", "Abort",0,100) ):
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
     
    # Retrieve bbox and attributes from input feature
    bbox = inputFeat.geometry().boundingBox()
    #attr = inputFeat.attributeMap()
    attr = inputFeat.attributes()

    # Compute grid coordinates
    x = np.linspace(bbox.xMinimum(), bbox.xMaximum(), m+1)
    y = np.linspace(bbox.yMinimum(), bbox.yMaximum(), n+1)
    xx, yy = np.meshgrid(x, y)

    # Initialize progress bar
    progressBar.setRange(0,100)	
    progressBar.setValue(0)
    count = 0
    countMax = n*m
    countUpdate = countMax * 0.05 # update each 5%

    # Initialize feature output list
    outFeatList = []

    # iterate over grid lines
    for i in range(len(y)-1):
	# iterate over grid columns
	for j in range(len(x)-1):
	    # compute feature coordinate
	    # clock-wise point numbering (top-left, top-right, bottom-right, bottom-left)
	    # i for lines (top to bottom), j for columns (left to right)
	    x1, x2, x3, x4 = xx[i+1,j],  xx[i+1,j+1],  xx[i,j+1],  xx[i,j]
	    y1, y2, y3, y4 = yy[i+1,j],  yy[i+1,j+1],  yy[i,j+1],  yy[i,j]
	    # define feature points
	    pt1, pt2, pt3, pt4 =  QgsPoint(x1, y1), QgsPoint(x2, y2), QgsPoint(x3, y3), QgsPoint(x4, y4) 
	    pt5 = pt1
	    # define polygon from points
	    polygon = [[pt1, pt2, pt3, pt4, pt5]]
	    # initialize new feature 
	    outFeat = QgsFeature()
	    #outFeat.setAttributeMap(attr)
	    outFeat.setAttributes(attr)
	    outGeom = QgsGeometry()
	    outFeat.setGeometry(outGeom.fromPolygon(polygon))
	    # save features 
	    outFeatList.append(outFeat)
	    # update counter
	    count += 1
	    # update ID (TO DO : check numbering)
	    #idvar = count
	    # each 5%, update progress bar
	    if int( np.fmod( count, countUpdate ) ) == 0:
		    prog = int( count / countMax * 100 )
		    progressBar.setValue(prog)
		    QCoreApplication.processEvents()

    progressBar.setValue(100)
    # Check type of vector provider 
    # If vprovider is a layer provider
    if repr(QgsVectorDataProvider) == str(type(vprovider)):
	isFeatureAddSuccessful, newFeatures = vprovider.addFeatures(outFeatList)
	return([feat.id() for feat in newFeatures])

    # Else, if provider is a writer
    else :
	for outFeat in outFeatList:
	    vprovider.addFeature(outFeat)
	return([]) 


# --------------------------------------------------------------------------------------------------------------
# Format of topoRules dictionary
# -- for Modflow
#topoRules = {'model':'modflow','nmax':1}
# -- for Newsam
# topoRules = {'model':'newsam', 'nmax':2}
# -- no check
# topoRules = {'none':'newsam', 'nmax':None}

# --------------------------------------------------------------------------------------------------------------
def rect_size(inputFeature):
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

    # Extract the four corners of inputFeature
    # Note : rectangle points are numbered from top-left to bottom-left, clockwise
    p0, p1, p2, p3 = ftools_utils.extractPoints(inputFeature.geometry())[:4]
    # Compute size
    dx = abs(p1.x() - p0.x())
    dy = abs(p3.y() - p0.y())
    return( {'dx':dx,'dy':dy} )

# --------------------------------------------------------------------------------------------------------------
# Return vector coordinates as { 'x' : x, 'y': y } from two QgisPoint()
def build_vect(p1, p2):
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
    return { 'x' :  p2.x()-p1.x(), 'y': p2.y()-p1.y() }

# --------------------------------------------------------------------------------------------------------------
# Check if two vectors are colinear
def is_colinear(v1, v2):
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

    if( is_equal( v1['y']*v2['x'] - v1['x']*v2['y'] , 0 ) ):
	return True
    else : 
	return False

# --------------------------------------------------------------------------------------------------------------

# Append records of thisFixDict to fixDict
# thisFixDict and fixDict have the same structure : fixDict = { 'id':[] , 'n':[], 'm':[] }
# If a record of thisFixDict is already in fixDict, update the corresponding record
# If not, simply append the record to fixDict
def update_fixDict(fixDict, thisFixDict):
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

    for fId, n, m in zip( thisFixDict['id'], thisFixDict['n'], thisFixDict['m'] ):
	# if the feature is already in fixDict, update this record
	if fId in fixDict['id']:
	    i = fixDict['id'].index(fId)
	    fixDict['n'][i] = max( n, fixDict['n'][i] )
	    fixDict['m'][i] = max( m, fixDict['m'][i] )
	 # if the feature is not in fixDict, append it
	else :
	    fixDict['id'].append(fId)
	    fixDict['n'].append(n)
	    fixDict['m'].append(m)

    return fixDict



# --------------------------------------------------------------------------------------------------------------

# isEqual (from Ftools, voronoi.py)
# Check if two values are identical, given a tolerance interval
def is_equal(a,b,relativeError=TOLERANCE):
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

    # is nearly equal to within the allowed relative error
    norm = max(abs(a),abs(b))
    return (norm < relativeError) or (abs(a - b) < (relativeError * norm))

# --------------------------------------------------------------------------------------------------------------
# Check if two QgsPoints are identical 
def is_over(geomA,geomB,relativeError=TOLERANCE):
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

    return ( is_equal( geomA.x(), geomB.x() ) and
	    is_equal( geomA.y(), geomB.y() )
	    )

# --------------------------------------------------------------------------------------------------------------
# Split inputFeatures in vLayer and check their topology
def refine_by_split(featIds, n, m, topoRules, vLayer, progressBar = QProgressDialog("Building grid...", "Abort",0,100), labelIter = QLabel() ) :
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

    # init dictionary
    fixDict = { 'id':featIds , 'n':[n]*len(featIds), 'm':[m]*len(featIds) }
    
    # init iteration counter
    itCount = 0
    
    # Continue until inputFeatures is empty
    while len(fixDict['id']) > 0:

	# Split inputFeatures
	newFeatIds = split_cells(fixDict, n, m, vLayer)

	# Get all the features 	
	allFeatures = {feature.id(): feature for feature in vLayer.getFeatures()}

	# Initialize spatial index 
	vLayerIndex = QgsSpatialIndex()
	# Fill spatial Index
	for feat in allFeatures.values():
	    vLayerIndex.insertFeature(feat)

	# re-initialize the list of features to be fixed
	fixDict = { 'id':[] , 'n':[], 'm':[] }

	# Initialize progress bar
	progressBar.setRange(0,100)	
	progressBar.setValue(0)
	count = 0
	countMax = len(newFeatIds)
	countUpdate = countMax * 0.05 # update each 5%

	# Iterate over newFeatures to check topology
	for newFeatId in newFeatIds:
	    # Get the neighbors of newFeatId that must be fixed
	    thisFixDict = check_topo( newFeatId, n, m, topoRules, allFeatures, vLayer, vLayerIndex)
	    # Update fixDict with thisFixDict
	    fixtDict = update_fixDict(fixDict,thisFixDict)
	    # update counter
	    count += 1
	   # update progressBar
	    if int( np.fmod( count, countUpdate ) ) == 0:
		prog = int( count / countMax * 100 )
		progressBar.setValue(prog)
		QCoreApplication.processEvents()

	progressBar.setValue(100)

	# Update iteration counter
	itCount+=1
	labelIter.setText(unicode(itCount))
    

# --------------------------------------------------------------------------------------------------------------
def split_cells(fixDict, n=2, m=2, vLayer = QgsVectorLayer()):
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

    # note that n and m parameters are obsolete.

    # Get all the features from vLayer
    allFeatures = {feature.id(): feature for (feature) in vLayer.getFeatures()}

    # remove features that must be split from vLayer
    # this operation must be done before any feature add
    # since ids() are updated
    vLayer.dataProvider().deleteFeatures(fixDict['id'])

    # Initialize the list of new features 
    newFeatIds = []

    # Split each element of fixDict
    for featId, n, m in zip( fixDict['id'], fixDict['n'], fixDict['m'] ):
	feat = allFeatures[featId]
	newFeatIds.extend( make_rgrid(feat, n, m, vLayer.dataProvider() ) )

    # Return new features 
    return(newFeatIds)

# --------------------------------------------------------------------------------------------------------------
# Check the coherence of a boundary between 2 grid elements
def is_valid_boundary( feat1, feat2, direction, topoRules ):
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

    # feat1, feat2 (QgsFeature) : the features considered
    # direction (Int)
    	# Numbering rule for neighbors of feature 0 :
	# | 8 | 1 | 5 |
	# | 4 | 0 | 2 |
	# | 7 | 3 | 6 |
    # topo Rules (Dict) : 
	# -- for Modflow
	#topoRules = {'model':'modflow','nmax':1}
	# -- for Newsam
	# topoRules = {'model':'newsam', 'nmax':2}

    # get feat1 geometry
    dx1, dy1 = rect_size(feat1)['dx'], rect_size(feat1)['dy'] 

    # get feat2 geometry
    dx2, dy2 = rect_size(feat2)['dx'], rect_size(feat2)['dy'] 

    # Check if the boundary satisfies topoRules
    # Note: in the logic of this program, we only consider the case
    # when the neighbor is bigger than the given cell (dy2/dy1 >=1)
    # Indeed, we
    # start with a regular grid. The topology is checked at each
    # feature split.

    if direction == 2 or direction == 4  : # horizontal directions
	if  dy2 / dy1 <  1 or is_equal(dy2 / dy1, 1 )  or \
		dy2 / dy1 < topoRules['nmax'] or is_equal(dy2 / dy1, topoRules['nmax'])  :
	    return(True)
    if direction == 1 or direction == 3 :  # vertical directions
	if ( dx2 / dx1 <  1 or is_equal(dx2 / dx1, 1 ) ) or \
		(dx2 / dx1 < topoRules['nmax'] or is_equal(dx2 / dx1, topoRules['nmax']) ) :
	    return(True)
    # If the boundary doesn't satisfy topoRules, or
    # if the direction is not valid
    return(False)


# --------------------------------------------------------------------------------------------------------------
# Check topology of feat's neighbors and
# return the neighbors that don't satisfy topoRules
def check_topo(featId, n, m, topoRules, allFeatures, vLayer, vLayerIndex):
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

    # Get the feature
    feat = allFeatures[featId]

    # Initialize list of features to be fixed
    fixDict = { 'id':[] , 'n':[], 'm':[] }

    # Find neighbors
    neighbors = find_neighbors(feat, allFeatures, vLayerIndex)

    # Check the compatibility of inputFeature and neighbors with topoRules
    for direction, neighbor in zip(neighbors['direction'], neighbors['feature']):
	if direction in [1, 2, 3, 4]:
	    # Special case for newsam grid
	    if topoRules['model']=='newsam':
		N = M = 2
	    else :
		N = n
		M = m
		# Set refinement to 1 for orthogonal directions
		if direction in [2,4] : # horizontally
		    M = 1
		elif direction in [1,3] : # vertically
		    N = 1
	    # check feat, neighbor boundary
	    if not is_valid_boundary( feat, neighbor, direction, topoRules ) :
		# update fixDict : add neighbor
		fixDict = update_fixDict( fixDict, { 'id':[neighbor.id()] , 'n':[N], 'm':[M] } )
	    # check neighbor, feat boundary
	    if not is_valid_boundary( neighbor, feat, direction, topoRules ) :
		# update fixDict : add feat
		fixDict = update_fixDict( fixDict, { 'id':[feat.id()] , 'n':[N], 'm':[M] } )

    # return features that do not satisfy topoRules
    return fixDict

# --------------------------------------------------------------------------------------------------------------
# Find the neighbors of inputFeature neighbor and identify the direction
def find_neighbors(inputFeature, allFeatures, vLayerIndex):
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

    # Get neighbors Ids.
    neighborsId = vLayerIndex.intersects( inputFeature.geometry().boundingBox() )

    # Get neighbors
    featNeighbors = [ allFeatures[featId] for featId in neighborsId ]

    # Initialize dictionary
    neighbors = { 'direction':[], 'feature':[] }
   
    # Extract the four corners of inputFeature
    # Note : rectangle points are numbered from top-left to bottom-left, clockwise
    p0, p1, p2, p3 = ftools_utils.extractPoints(inputFeature.geometry())[:4]

    # Iterate over neighbors
    for featNeighbor in featNeighbors:

	# Extract the four corners of neighbor
	# Note : rectangle points are numbered from top-left to bottom-left, clockwise
	q0, q1, q2, q3 = ftools_utils.extractPoints(featNeighbor.geometry())[:4]

	# Numbering rule for neighbors of feature 0 :
	# | 8 | 1 | 5 |
	# | 4 | 0 | 2 |
	# | 7 | 3 | 6 |

	# Identify type of neighborhood 
	if is_over(p0, q0) and is_over(p1, q1) and is_over(p2, q2) and is_over(p3, q3):
	    cell_dir = 0 # features overlap
	elif is_over(p0, q3) and is_over(p1, q2):
	    cell_dir = 1 # feature B is above A
	elif is_over(p1, q0) and is_over(p2, q3):
	    cell_dir = 2 # feature B is to the right of A
	elif is_over(p2, q1) and is_over(p3, q0):
	    cell_dir = 3 # feature B is below A
	elif is_over(p3, q2) and is_over(p0, q1):
	    cell_dir = 4 # feature B is to the left of A
	elif is_over(p1, q3):
	    cell_dir = 5 # feature B is to the top-right corner of A
	elif is_over(p2, q0):
	    cell_dir = 6 # feature B is to the bottom-right corner of A
	elif is_over(p3, q1):
	    cell_dir = 7 # feature B is to the bottom-left corner of A
	elif is_over(p0, q2):
	    cell_dir = 8 # feature B is to the top-left corner of A
	elif is_colinear( build_vect(q3, p0), build_vect(p1, q2) ) and \
		is_colinear(build_vect(q3, p0), {'x':1, 'y':0} ) and \
		is_colinear(build_vect(p1, q2), {'x':1, 'y':0} ) :
	    cell_dir = 1 # feature B is above A
	elif is_colinear( build_vect(q3, p2), build_vect(p1, q0) ) and \
		is_colinear(build_vect(q3, p2), {'x':0, 'y':1} ) and \
		is_colinear(build_vect(p1, q0), {'x':0, 'y':1} ) :
	    cell_dir = 2 # feature B is to the right of A
	elif is_colinear( build_vect(q0, p3), build_vect(p2, q1) ) and \
		is_colinear(build_vect(q0, p3), {'x':1, 'y':0} ) and \
		is_colinear(build_vect(p2, q1), {'x':1, 'y':0} ) :
	    cell_dir = 3 # feature B is below A
	elif is_colinear( build_vect(q2, p3), build_vect(p0, q1) ) and \
		is_colinear(build_vect(q2, p3), {'x':0, 'y':1} ) and \
		is_colinear(build_vect(p0, q1), {'x':0, 'y':1} ) :
		    cell_dir = 4 # feature B is to the left of A
	else : 
	    cell_dir = -1 # feature B is not a neighbor in a valid grid
	    
	# If the feature is an "actual" neighbor, save it to the dictionary
	# "actual" = neither the feature itself, neither neighbors from corners
	#if cell_dir > 0 : 
	neighbors['direction'].append(cell_dir)
	neighbors['feature'].append(featNeighbor)

    # Return dictionary with neighbors
    return neighbors


# -----------------------------------------------------
# get nrow and ncol or a regular (modflow) grid layer
def get_rgrid_nrow_ncol(gridLayer):
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

    # TODO : check if the grid is actually regular 
    
    # Load layer
    #allAttrs = gridLayer.pendingAllAttributesList()
    #gridLayer.select(allAttrs)

    # Init variables 
    allFeatures = {feat.id():feat for feat in gridLayer.getFeatures()}
    allCentroids = [feat.geometry().centroid().asPoint() \
			for feat in allFeatures.values()]
    centroids_ids = allFeatures.keys()
    centroids_x = [centroid.x() for centroid in allCentroids]
    centroids_y = [centroid.y() for centroid in allCentroids]
    centroids = np.array( [centroids_ids , centroids_x, centroids_y] )
    centroids = centroids.T

    # get ncol :
    # sort by decreasing y and increasing x
    idx_row = np.lexsort([centroids[:,1],-centroids[:,2]])
    yy = centroids[idx_row,2]
    # iterate along first row and count number of items with same y
    i=0
    #return yy
    while is_equal(yy[i],yy[i+1]):
	i+=1
	if i >= (yy.size - 1): 
	    break # for one-row grids
    ncol = i+1

    # get nrow :
    # sort by increasing x and decreasing y
    idx_col = np.lexsort([-centroids[:,2],centroids[:,1]])
    xx=centroids[idx_col,1]
    # iterate over first col and count number of items with same x
    i=0
    while is_equal(xx[i],xx[i+1]) :
	i+=1
	if i >= (xx.size-1):
	    break # for one-column grids
    nrow = i+1

    # return nrow, ncol
    return(nrow, ncol)

# -----------------------------------------------------
# get delr delc of a regular (modflow) grid layer
def get_rgrid_delr_delc(gridLayer):
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


    # TODO : check if the grid is actually regular 
    
    # Load layer
    #allAttrs = gridLayer.pendingAllAttributesList()
    #gridLayer.select(allAttrs)
    #gridLayer.dataProvider().select(allAttrs)

    # Init variables 
    allFeatures = {feat.id():feat for feat in gridLayer.getFeatures()}
    allCentroids = [feat.geometry().centroid().asPoint() \
			for feat in allFeatures.values()]
    centroids_ids = allFeatures.keys()
    centroids_x = [centroid.x() for centroid in allCentroids]
    centroids_y = [centroid.y() for centroid in allCentroids]
    centroids = np.array( [centroids_ids , centroids_x, centroids_y] )
    centroids = centroids.T

    # get nrow, ncol
    nrow, ncol =  get_rgrid_nrow_ncol(gridLayer)

    # init list
    delr = []
    delc = []

    # sort by decreasing y and increasing x
    idx_row = np.lexsort([centroids[:,1],-centroids[:,2]])
    # iterate along first row 
    for featId in centroids[idx_row,0][:ncol]:
	# Extract the four corners of feat
	# Note : rectangle points are numbered from top-left to bottom-left, clockwise
	p0, p1, p2, p3 = ftools_utils.extractPoints(allFeatures[featId].geometry())[:4]
	delr.append( p1.x() - p0.x() )

    # sort by increasing x and decreasing y    
    idx_col = np.lexsort([-centroids[:,2],centroids[:,1]])
    # iterate along first col
    for featId in centroids[idx_col,0][:nrow]:
	# Extract the four corners of feat
	# Note : rectangle points are numbered from top-left to bottom-left, clockwise
	p0, p1, p2, p3 = ftools_utils.extractPoints(allFeatures[featId].geometry())[:4]
	delc.append( p0.y() - p3.y() )

    # round 
    delr = [round(val, max_decimals) for val in delr]
    delc = [round(val, max_decimals) for val in delc]

    # If all values are identical, return scalar
    if delr.count(delr[0]) == len(delr):
	delr = delr[0]

    if delc.count(delc[0]) == len(delc):
	delc = delc[0]

    return(delr, delc)

# -----------------------------------------------------
# Add attributes NROW, NCOL to a regular (modflow) grid layer
def rgrid_numbering(gridLayer):
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

    # TODO : check if the grid is actually regular 

    caps = gridLayer.dataProvider().capabilities()

    # Init variables
    res = 1
    allFeatures = {feat.id():feat for feat in gridLayer.getFeatures()}
    allCentroids = [feat.geometry().centroid().asPoint() \
			for feat in allFeatures.values()]
    centroids_ids = allFeatures.keys()
    centroids_x = np.around(np.array([centroid.x() for centroid in allCentroids]), max_decimals)
    centroids_y = np.around(np.array([centroid.y() for centroid in allCentroids]), max_decimals)
    centroids = np.array( [centroids_ids , centroids_x, centroids_y] )
    centroids = centroids.T
    
    # Fetch field name index of ROW and COL
    # If columns don't exist, add them
    row_field_idx = gridLayer.dataProvider().fieldNameIndex('ROW')
    col_field_idx = gridLayer.dataProvider().fieldNameIndex('COL')
    cx_field_idx = gridLayer.dataProvider().fieldNameIndex('CX')
    cy_field_idx = gridLayer.dataProvider().fieldNameIndex('CY')

    if row_field_idx == -1:
	if caps & QgsVectorDataProvider.AddAttributes:
	  res = gridLayer.dataProvider().addAttributes(  [QgsField("ROW", QVariant.Int)] ) 
	  row_field_idx = gridLayer.dataProvider().fieldNameIndex('ROW')
      
    if col_field_idx == -1:
	if caps & QgsVectorDataProvider.AddAttributes:
	  res = res*gridLayer.dataProvider().addAttributes( [QgsField("COL", QVariant.Int)] )
	  col_field_idx = gridLayer.dataProvider().fieldNameIndex('COL')

    if cx_field_idx == -1:
	if caps & QgsVectorDataProvider.AddAttributes:
	  res = gridLayer.dataProvider().addAttributes(  [QgsField("CX", QVariant.Double)] ) 
	  row_field_idx = gridLayer.dataProvider().fieldNameIndex('CX')
      
    if cy_field_idx == -1:
	if caps & QgsVectorDataProvider.AddAttributes:
	  res = res*gridLayer.dataProvider().addAttributes( [QgsField("CY", QVariant.Double)] )
	  col_field_idx = gridLayer.dataProvider().fieldNameIndex('CY')

    # update fields
    gridLayer.updateFields()

    # get nrow, ncol
    nrow, ncol =  get_rgrid_nrow_ncol(gridLayer)

    # Iterate over grid row-wise and column wise 
    # sort by decreasing y and increasing x
    idx = np.lexsort( [centroids_x,-1*centroids_y] )
    centroids = centroids[idx,:]
    row = 1
    col = 1

    # start editing
    gridLayer.startEditing()

    attrValues = {}

    for i in range(centroids.shape[0]):
	if col > ncol:
	    col = 1
	    row = row + 1
	featId = centroids[i, 0]
	cx = float(centroids[i, 1])
	cy = float(centroids[i, 2])
	attr = { row_field_idx:row, col_field_idx:col,\
		cx_field_idx:cx, cy_field_idx:cy}
	attrValues[featId] = attr 
	col+=1
    # write attributes to shapefile 
    res = gridLayer.dataProvider().changeAttributeValues(attrValues)
    print(col)
    print(row)
    print(row_field_idx)
    print(col_field_idx)
    # commit
    gridLayer.commitChanges()

    # res should be True if the operation is successful 
    return(res) 

    
# ======================================================================
def count_overlapping_cells(feat, spatialIndex) : 
    # feat : QgsFeature (cell of a Qgridder mesh)
    # spatialIndex : QgsSpatialIndex of an (overlying / underlying) grid vector layer
    # get bbox of feat
    featBbox = feat.geometry().boundingBox()
    # shrink bbox of TOLERANCE
    # doing so, we do not select neighbor cells
    shrinkedBbox = QgsRectangle(featBbox.xMinimum()+TOLERANCE,
	    featBbox.yMinimum()+TOLERANCE,
	    featBbox.xMaximum()-TOLERANCE,
	    featBbox.yMaximum()-TOLERANCE
	    )
    # fetch overlapping cells (list of features)
    overlappingCells = spatialIndex.intersects( shrinkedBbox )
    # return number of overlapping features
    return(len(overlappingCells))



# update spatial indexes
def get_spatial_indexes(allLayers) : 
    spatialIndexes = []
    for vLayer in allLayers : 
	vLayerIndex = QgsSpatialIndex()
	for feat in vLayer.getFeatures() :
	    vLayerIndex.insertFeature(feat)
	spatialIndexes.append(vLayerIndex)
    return(spatialIndexes)


# ======================================================================
def correct_pseudo3D_grid(allLayers, topoRules) :
    nLayers = len(allLayers)
    # init fixDict for while condition below
    fixDict = { 'id':[NULL] , 'n':[NULL], 'm':[NULL] }
    nfix = 1
    while nfix > 0 :  
	nfix = 0
	# iterate over each layers of the pseudo-3D mesh
	for layerNum in range(nLayers) : 
	    # update spatial indexes
	    spatialIndexes = get_spatial_indexes(allLayers)
	    # update fix dictionary
	    fixDict = { 'id':[] , 'n':[], 'm':[] }
	    # iterate over each cells of layer layerNum
	    for feat in allLayers[layerNum].getFeatures() :
		# count overlapping cells in the overlying layer \
		# note that layer layerNum is not necessarily overlain by layerNum + 1 \
		# and underlain by layerNum - 1.
		# go to layer JUST BELOW layer numLayer...
		l = layerNum + 1
		# ... and check DOWNWARD for overlapping cells
		while l < nLayers :
		    # count number of features in spatialIndexes[l] overlapping feature "feat"
		    p = count_overlapping_cells(feat,spatialIndexes[l])
		    if p > 0 :
			if p > topoRules['pmax'] :
			    fixDict = update_fixDict( fixDict, { 'id':[feat.id()] , 'n':[2], 'm':[2] } )	    
			break # exit this while loop as features have been found below
		    # go to layer below
		    l = l + 1
		# go to layer JUST OVER layer numLayer...
		l = layerNum - 1
		# ... and check upward for overlapping cells
		while l >= 0 :
		    # check upward for overlapping cells
		    p = count_overlapping_cells(feat,spatialIndexes[l])
		    if p > 0 :
			if p > topoRules['pmax'] :
			    fixDict = update_fixDict( fixDict, { 'id':[feat.id()] , 'n':[2], 'm':[2] } )	    
			break # exit this while loop as features have been found above
		    # go to layer above
		    l = l - 1
	    # split cells
	    if len(fixDict['id']) > 0 : 
		refine_by_split(fixDict['id'], 2, 2, 
			topoRules, allLayers[layerNum], 
			)
	    nfix += len(fixDict['id'])



