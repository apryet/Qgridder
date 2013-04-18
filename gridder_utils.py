from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import numpy as np
import time

import ftools_utils

# --------------------------------------------------------------------------------------------------------------
# Makes regular grid of n lines and m columns,
# from QgsRectangle bbox. Resulting features are 
# appended to  vprovider
def make_rgrid(inputFeat, n, m, vprovider, progressBar = QProgressDialog("Building grid...", "Abort",0,100) ):
         
	# Retrieve bbox and attributes from input feature
    	bbox = inputFeat.geometry().boundingBox()
	attr = inputFeat.attributeMap()

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
		outFeat.setAttributeMap(attr)
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
    return { 'x' :  p2.x()-p1.x(), 'y': p2.y()-p1.y() }

# --------------------------------------------------------------------------------------------------------------
# Check if two vectors are colinear
def is_colinear(v1, v2):
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

TOLERANCE = 1e-6

# isEqual (from Ftools, voronoi.py)
# Check if two values are identical, given a tolerance interval
def is_equal(a,b,relativeError=TOLERANCE):
    # is nearly equal to within the allowed relative error
    norm = max(abs(a),abs(b))
    return (norm < relativeError) or (abs(a - b) < (relativeError * norm))

# --------------------------------------------------------------------------------------------------------------
# Check if two QgsPoints are identical 
def is_over(geomA,geomB,relativeError=TOLERANCE):
    return ( is_equal( geomA.x(), geomB.x() ) and
	    is_equal( geomA.y(), geomB.y() )
	    )

# --------------------------------------------------------------------------------------------------------------
# Split inputFeatures in vLayer and check their topology
def refine_by_split(featIds, n, m, topoRules, vLayer, progressBar = QProgressDialog("Building grid...", "Abort",0,100), labelIter = QLabel() ) :

    # init dictionary
    fixDict = { 'id':featIds , 'n':[n]*len(featIds), 'm':[m]*len(featIds) }
    
    # init iteration counter
    itCount = 0
    
    # Continue until inputFeatures is empty
    while len(fixDict['id']) > 0:

	#print('len(fixDict[\'id\']):')
	#print(len(fixDict['id']))

	# Split inputFeatures
	newFeatIds = split_cells(fixDict, n, m, vLayer)

	# --  Initialize spatial index for faster lookup	
	# Get all the features from vLayer
	# Select all features along with their attributes
	allAttrs = vLayer.pendingAllAttributesList()
	vLayer.select(allAttrs)
	# Get all the features to start
	allFeatures = {feature.id(): feature for (feature) in vLayer}
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
    
    print('Number of iterations :' )
    print(itCount)

# --------------------------------------------------------------------------------------------------------------
def split_cells(fixDict, n, m, vLayer):

    # Select all features along with their attributes
    allAttrs = vLayer.pendingAllAttributesList()
    vLayer.select(allAttrs)

    # Get all the features from vLayer
    allFeatures = {feature.id(): feature for (feature) in vLayer}

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

def is_valid_boundary( feat1, feat2, direction, topoRules ):

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
    # If the boundary doesn't satisfiy topoRules, or
    # if the direction is not valid
    return(False)


# --------------------------------------------------------------------------------------------------------------
# Check topology of feat's neighbors and
# return the neighbors that don't satisfy topoRules
def check_topo(featId, n, m, topoRules, allFeatures, vLayer, vLayerIndex):

    # Get the feature
    feat = allFeatures[featId]

    # Initialize list of features to be fixed
    fixDict = { 'id':[] , 'n':[], 'm':[] }

    # Find neighbors
    neighbors = find_neighbors(feat, allFeatures, vLayerIndex)

    print('len(neighbors[\'feature\'])')
    print(len(neighbors['feature']))

    # Check the compatibility of inputFeature and neighbors with topoRules
    for direction, neighbor in zip(neighbors['direction'], neighbors['feature']):
	if direction in [1, 2, 3, 4]:
	    #print('direction:')
	    #print(direction)
	    #print('is_valid_boundary:')
	    #print(is_valid_boundary( feat, neighbor, direction, topoRules ))
	    if not is_valid_boundary( feat, neighbor, direction, topoRules ) :
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
		# Update fixDict
		#print('n:')
		#print(n)
		#print('m:')
		#print(m)
		fixDict = update_fixDict( fixDict, { 'id':[neighbor.id()] , 'n':[N], 'm':[M] } )

    # return features that do not satisfy topoRules
    return fixDict

# --------------------------------------------------------------------------------------------------------------
# Finf the neighbors of inputFeature neighbor and identify the direction
def find_neighbors(inputFeature, allFeatures, vLayerIndex):

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

