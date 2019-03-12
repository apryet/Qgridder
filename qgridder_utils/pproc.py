# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_utils_pproc.py
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

from .base import *
from . import ftools_utils

# ---------------------------------

def get_param(grid_layer, output_type = 'array', layer = '', field_name = ''):
    """
    Description
    ----------
    Returns modflow-like parameter list or array
    This function first checks all parameters. If successful, then
    calls get_param_list or get_param_array

    Parameters
    ----------
    grid_layer : QgsVectorLayer, grid from which to fetch attributes
    output_type : string, either 'array' or 'list'
    layer (optional) : integer, the (modflow) grid layer number
    field_name : string, name of the attribute to get in grid_layer


    Returns
    -------
    parameter list or array

    Examples
    --------
    >>> get_param(grid_layer, output_type = 'array', field_name = 'IBOUND')

    """
    all_features = {feat.id():feat for feat in grid_layer.getFeatures()}

    # init error flags for field indexes
    row_field_idx = col_field_idx = attr_field_idx = -1

    # Fetch selected features from input grid_layer
    selected_feature_ids = grid_layer.selectedFeatureIds()

    # Selection should not be empty if output_type 'list' is selected
    if len(selected_feature_ids) == 0 and output_type == 'list':
        print("Empty selection. To export all features, export as array.")
        return(False)

    # Selection will not be considered if output_type 'array' is selected
    if len(selected_feature_ids) != 0 and output_type == 'array':
        print("Export type is array. Feature selection is not considered. All features will be exported")

    # If a field name is provided, get corresponding field index
    if field_name !='' :
        attr_field_idx = grid_layer.dataProvider().fieldNameIndex(field_name)

        # If the field is not found in attribute table
        if attr_field_idx == -1 :
            print("Field " + field_name + "  not found in grid attribute table.")
            # If output_type is array, return
            if output_type == 'array':
                return(np.array([]))
    else :
        # Field name should not be '' if output type is 'array'
        if output_type == 'array':
                print("A valid field name must be provided for output_type \'array\' ")
                return(np.array([]))

    # Get row and col field indexes
    row_field_idx = grid_layer.dataProvider().fieldNameIndex('ROW')
    col_field_idx = grid_layer.dataProvider().fieldNameIndex('COL')

    # If row and col fields are not found, call rgrid_numbering
    if row_field_idx == -1 | col_field_idx == -1 :
        rgrid_numbering(grid_layer)
        row_field_idx = grid_layer.dataProvider().fieldNameIndex('ROW')
        col_field_idx = grid_layer.dataProvider().fieldNameIndex('COL')

    if output_type == 'list':
        output = get_param_list(grid_layer, all_features, layer = layer, field_name = field_name)
    elif output_type =='array' :
        output = get_param_array(grid_layer, field_name = field_name)
    else :
        print("Output type must be either \'list\' or \'array\'")
        return([])

    return(output)


# -----------------------------------------------------
# return modflow-like list from selected features and field_name
def get_param_list(grid_layer, all_features,  layer = '', field_name = ''):
    """
    Description

    Parameters
    ----------
    grid_layer :  QgsVectorLayer, containing the (regular) grid
    layer (optional) : Integer corresponding to the (modflow) grid layer number
    field_name : String, name of the attribute to get in grid_layer

    Returns
    -------

    List of selected features with selected attribute (field_name)

    Examples
    --------
    >>> output = get_param_list(grid_layer, all_features, layer = layer, field_name = field_name)
    """

    # Get selected features from input grid_layer
    selected_feature_ids = grid_layer.selectedFeaturesIds()

    # Get field_name attribute index
    attr_field_idx = grid_layer.dataProvider().fieldNameIndex(field_name)

    # Get ROW and COL fields attribute indexes
    row_field_idx = grid_layer.dataProvider().fieldNameIndex('ROW')
    col_field_idx = grid_layer.dataProvider().fieldNameIndex('COL')

    # init output list
    grid_list = []

    # iterate over selected feature ids
    for fId in selected_feature_ids:
        feat = all_features[fId]
        row = feat[row_field_idx]
        col = feat[col_field_idx]

        this_feat_list = []

        # add layer number
        if layer != '':
            this_feat_list.append(layer)

        # add row and col number
        this_feat_list.append(row)
        this_feat_list.append(col)

        # add attribute value
        if field_name != '' :
            field_value = feat[attr_field_idx]
            if field_value.toFloat()[1] == True:
                this_feat_list.append(field_value)
            else :
                this_feat_list.append(str(field_value.toString()))

        grid_list.append(this_feat_list)

    return grid_list

# -----------------------------------------------------
# return modflow-like list from selected features and field_name
def get_param_array(grid_layer, field_name = 'ID'):
    """
    Description

    Parameters
    ----------
    grid_layer :  QgsVectorLayer, the (regular) grid
    String field_name : name of the attribute to get from grid_layer

    Returns
    -------
    Array with field_name attribute

    Examples
    --------
    >>> get_param_array(grid_layer, field_name = field_name)
    """

    # Get nrow, ncol
    nrow, ncol =  get_rgrid_nrow_ncol(grid_layer)

    # Get field_name attribute index
    attr_field_idx = grid_layer.dataProvider().fieldNameIndex(field_name)

    # init lists
    rows = [feat['ROW'] for feat in grid_layer.getFeatures()]
    cols = [feat['COL'] for feat in grid_layer.getFeatures()]
    field_values = [feat[field_name] for feat in grid_layer.getFeatures()]

    rowColVal = np.array ([ [feat['ROW'], feat['COL'], feat[field_name] ] for feat in grid_layer.getFeatures()] )

    idx = np.lexsort( [rowColVal[:,1], rowColVal[:,0]] )

    val = rowColVal[idx,2]
    val.shape = (nrow, ncol)

    #field_values = field_values[idx]

    #field_values.shape = (nrow, ncol)

    #return(field_values)
    return(val)


# -----------------------------------------------------
def get_ptset_xy(v_layer, id_field_name = 'ID'):
    """
    Description
    ----------
    Usefull for pilot points.
    From a selection of points in v_layer, returns
    a dict of tuple containing points coordinates (x,y)
    returns

    Parameters
    ----------
    v_layer : Vector layer containing the observation points.
             Only selected points are considered
    grid_layer : Qgridder grid layer
    id_field_name : Column in v_layer containing points ID
                  which will be used in the output dictionary
    nNeighbors : number of neighboring grid cells to fetch

    Returns
    -------

    {'ID1':(x, y), 'ID2':(x, y), ... }

    Examples
    --------
    >>>
    """
    dic_ptset = {}

    # iterate over v_layer features
    for feat in v_layer.getFeatures() :
        feat_id = feat[id_field_name]
        feat_point = feat.geometry().asPoint()
        dic_ptset[feat_id] = ( feat_point.x(), feat_point.y() )

    return(dic_ptset)


# -----------------------------------------------------
def get_ptset_centroids(v_layer, grid_layer, id_field_name = 'ID',nNeighbors = 3):
    """
    Description
    ----------
    From a selection of points in v_layer, returns
    a dict of tuple (nrow, ncol) in grid_layer
    returns

    Parameters
    ----------
    v_layer : Vector layer containing the observation points.
             Only selected points are considered
    grid_layer : Qgridder grid layer
    id_field_name : Column in v_layer containing points ID
                  which will be used in the output dictionary
    nNeighbors : number of neighboring grid cells to fetch

    Returns
    -------

    {'ID1':(nrow1, ncol1), 'ID2':(nrow2, ncol2), ... }

    Examples
    --------
    >>>
    """

    # v_layer : vector layer of points with a selection of point
    # grid_layer : the grid vector Layer
    # field_name : the attribute field of v_layer containing feature identificator
    # nNeighbors : number of neighboring cells to fetch for each point

    # check that grid_layer is a grid
    try :
        res = rgrid_numbering(grid_layer)
        if res == False:
            print("The grid layer does not seem to be valid")
            return(False)
    except :
        return(False)

    # -- create temporary layer of cell centroids
    # init layer type (point) and crs
    cLayerCrs = grid_layer.crs().authid()
    # create layer
    cLayer = QgsVectorLayer("Point?crs=" + cLayerCrs, "temp_centroids", "memory")
    cProvider = cLayer.dataProvider()
    cProvider.addAttributes( grid_layer.dataProvider().fields().toList() )

    # fill layer with centroids
    feat_centroids = []
    for cell in grid_layer.getFeatures():
        feat = QgsFeature()
        geom = cell.geometry().centroid()
        feat.setAttributes( cell.attributes() )
        feat.setGeometry( QgsGeometry(geom) )
        feat_centroids.append(feat)

    cProvider.addFeatures( feat_centroids )

    # -- Create and fill spatial Index
    cLayerIndex = QgsSpatialIndex(cLayer.getFeatures())

    # init distance tool
    d = QgsDistanceArea()

    # PtsetCentroids : { pointIDValue:[ (nrow, ncol, dist), ... ] }
    PtsetCentroids = {}

   # check that the selection in v_layer is not empty
    selected_feature_ids = v_layer.selectedFeaturesIds()
    if len(selected_feature_ids) == 0:
        print("Empty selection, all features considered")
        features = v_layer.getFeatures()
    else :
        print("Only selected features will be considered")
        features = v_layer.selectedFeatures()

    # iterate over selected points, find neighbors, fill pointCentroids dictionary
    for selectedPoint in features:
        neighborsIds = cLayerIndex.nearestNeighbor(selectedPoint.geometry().asPoint(), nNeighbors)
        neighborsData = []
        # iterate over neighbors
        for neighborId in neighborsIds:
            neighborFeat = QgsFeature()
            cProvider.getFeatures( QgsFeatureRequest().setFilterFid( neighborId ) ).nextFeature( neighborFeat )
            row = neighborFeat['ROW']
            col = neighborFeat['COL']
            dist = d.measureLine( neighborFeat.geometry().asPoint(), selectedPoint.geometry().asPoint() )
            neighborsData.append( (row, col, dist) )
        PtsetCentroids[selectedPoint[id_field_name]] = neighborsData

    return(PtsetCentroids)


#
## -----------------------------------------------------


def get_pline_data(pline, pline_layer) :
    """
    Description
    -----------
    Fetch necessary data to compute the curvilinear abscissa of the
    projection of a grid cell centroid over a polyline.

    Parameters
    ----------
    pline : the polyline
    pline_layer : the vector layer

    Returns
    -------
    A tuple :
    pline_feat_dic, pline_point_layer_index, pline_cumdist_dic

    Examples
    --------
    >>> pline_feat_dic, pline_point_layer_index, pline_cumdist_dic = get_pline_data(pline, pline_layer)
    """

    # get points from polyline
    pline_point_list = pline.geometry().asPolyline()

    # build list of features constituting the polyline
    pline_feat_list = []

    for point in pline_point_list :
        feat = QgsFeature()
        geom = QgsGeometry.fromPoint(point)
        feat.setGeometry(geom)
        pline_feat_list.append(feat)

    # init and populate memory layer with polyline features
    pline_point_layer = QgsVectorLayer("Point?crs=" + pline_layer.crs().authid(), 'pline_point_layer', providerLib =  'memory')
    pline_point_layer.dataProvider().addFeatures(pline_feat_list)

    # build spatial index from pline features
    pline_point_layer_index = get_spatial_indexes([pline_point_layer])[0]

    # build dic of keys
    pline_feat_dic = {feat.id():feat for feat in pline_point_layer.getFeatures()}

    # build list of distances of polyline segments
    pline_dist_list = []

    for i in range(len(pline_point_list) - 1) :
        dist = pline_feat_list[i].geometry().distance( pline_feat_list[i+1].geometry() )
        pline_dist_list.append(dist)

    # build list of cumulated distances along polyline
    pline_cumdist_list = list(np.cumsum(pline_dist_list))
    pline_cumdist_list = [0] + pline_cumdist_list

    # build dictionary of cumulated distances for each layer id

    pline_cumdist_dic = {}

    for i, key in zip( range(len(pline_cumdist_list)), sorted(pline_feat_dic.keys()) ):
        pline_cumdist_dic[key] = pline_cumdist_list[i]


    # return variables of interest for get_dist_pline_centroid
    return(pline_feat_dic, pline_point_layer_index, pline_cumdist_dic)


def get_dist_pline_centroid(centroid, pline, pline_feat_dic, pline_point_layer_index, pline_cumdist_dic) :
    """
    Description
    -----------
    Returns the distance between the origin of a polyline (pline) and the projection
    of a point (centroid) onto the polyline.

    Parameters
    ----------
    pline : the polyline
    pline_feat_dic : dictionary of polyline point features from QgsGeometry().asPolyline()
    pline_point_layer_index : QgsSpatialIndex of polyline memory vector layer

    Returns
    -------
    dist_centroid_origin (float)

    Examples
    --------
    >>> dist_centroid_origin = get_dist_pline_centroid(centroid, pline, pline_feat_dic, pline_point_layer_index, pline_cumdist_dic)
    """

    # for a given centroid, find the two nearest neighbors in the polyline
    neighbor_ids = pline_point_layer_index.nearestNeighbor(centroid.asPoint(),2)

    # first neighbor along the polyline, this is not necessarily the closest to the centroid.
    first_neighbor_id = sorted(neighbor_ids)[0]
    first_neighbor_feat = pline_feat_dic[first_neighbor_id]

    # get shortest distance to the polyline
    dist_centroid_pline = centroid.distance( pline.geometry() )

    # get distance of centroid to the first neighbor (along polyline)
    dist_centroid_point = centroid.distance( first_neighbor_feat.geometry() )

    # get projection of the centroid over the polyline segment (Pythagore theorem)
    dist_centroid_projected = sqrt( dist_centroid_point**2 - dist_centroid_pline**2)

    # compute cumulated distance from polyline origin
    dist_centroid_origin = pline_cumdist_dic[first_neighbor_id] + dist_centroid_projected

    # compute normalized distance ( curvilinear distance from pline origin / total pline length )
    norm_dist_centroid_origin = dist_centroid_origin / np.max(pline_cumdist_dic.values())

    return(norm_dist_centroid_origin)


def get_pline_centroids(pline_layer, grid_layer, id_field_name = 'ID', get_ndist = False) :
    """
    Description
    -----------
    Returns, for each (selected) polyline in pline_layer the row and column
    of intersected grid cells from grid_layer.
    If get_ndsit is True, the normalized distance between each centroid
    of selected cells is added (see Returns).
    The normalized distance, ndist, is the distance from the polyline origin to
    the curvilinear abscissa of the cell centroid projected onto the polyline.
    When edited with Qgis, the polyline origin is the first point of the polyline
    at the time of polyline creation.

    Parameters
    ----------
    pline_layer : polyline layer (vector)
    grid_layer : grid layer (vector)
    id_field_name : field name in polyline layer with unique feature id
    get_ndist : whether to add or not the normalized distance

    Returns
    -------
    if get_ndist is False :
        { pline_feat_id : [ (row, col), ... ] , ... }
    if get_ndist is True :
        { pline_feat_id : [ (row, col, ndist), ... ] , ... }

    Examples
    --------
    >>> rivRowCol = get_pline_centroids(rivers, grid, id_field_name = 'ID', get_ndist = True)
    """
    # -- iterate over polylines

    # Init output dictionary
    pline_cells_dic = {}

    # check that the selection in pline_layer is not empty
    selected_feat_ids = pline_layer.selectedFeaturesIds()
    if len(selected_feat_ids) == 0:
        print("Empty selection, all features considered")
        plines = pline_layer.getFeatures()
    else :
        print("Only selected features will be considered")
        plines = pline_layer.selectedFeatures()


    print('QGRIDDER _UTILS.... Get spatial index')
    # create and fill spatial Index
    grid_layer_index = get_spatial_indexes([grid_layer])[0]
    print('QGRIDDER _UTILS.... END Get spatial index')

    # build grid feature dictionary
    grid_feat_dic = { feat.id():feat for feat in grid_layer.getFeatures()}

    # Iterate over plines in pline_layer
    for pline in plines:

        # list of grid cells intersected by pline
        intersected_cells_list = []

        # get additional pline data
        if get_ndist == True :
            pline_feat_dic, pline_point_layer_index, pline_cumdist_dic = get_pline_data(pline, pline_layer)

        # get grid cells in the bbox of the pline
        pline_geom = QgsGeometry(pline.geometry())
        grid_feat_intersect_ids = grid_layer_index.intersects(pline_geom.boundingBox())

        # shorten selection to grid cells intersected by the pline
        for id in grid_feat_intersect_ids:
            grid_cell = grid_feat_dic[id]
            grid_cell_geom = QgsGeometry(grid_cell.geometry())
            # Within grid cells in the bbox of feat, select those intersecting feat
            if pline_geom.intersects(grid_cell_geom):
                if get_ndist == True :
                    grid_cell_centroid = grid_cell_geom.centroid()
                    ndist = get_dist_pline_centroid(grid_cell_centroid, pline, pline_feat_dic, pline_point_layer_index, pline_cumdist_dic)
                    # add grid_cell ROW and COL and ndist attributes
                    intersected_cells_list.append( [ grid_cell['ROW'], grid_cell['COL'], ndist ] )
                else :
                    # add grid_cell ROW and COL attributes
                    intersected_cells_list.append( [ grid_cell['ROW'], grid_cell['COL'] ] )

        # add pline entry into output dictionary
        pline_cells_dic[ pline[id_field_name] ] =  intersected_cells_list

    return(pline_cells_dic)


# -----------------------------------------------------
def get_polygon_centroids(polygon_layer, grid_layer, pline_layer = None, id_field_name = 'ID') :
    """
    Description
    -----------
    Returns, for each (selected) polygons in polygon_layer the row and column
    of intersected grid cells from grid_layer.
    If pline_layer is not None, the normalized distance (ndist) between each centroid and the corresponding
    polyline of pline_layer is added to the output (see Returns).
    The normalized distance, ndist, is the distance from the polyline origin to
    the curvilinear abscissa of the cell centroid projected onto the polyline.
    The polyline corresponding to each polygon is identified with the ID field.
    When edited with Qgis, the polyline origin is the first point of the polyline
    at the time of polyline creation.

    Parameters
    ----------
    polygon_layer : polygon layer (vector)
    grid_layer : grid layer (vector)
    pline_layer (optional) : polyline layer (vector)
    id_field_name (optional) : field name in polyline layer with unique feature id

    Returns
    -------
    if pline_layer is None :
        { polygon_feat_id : [ (row, col), ... ] , ... }
    if pline_layer not None :
        { polygon_feat_id : [ (row, col, ndist), ... ] , ... }

    Examples
    --------
    >>> rivRowCol = get_polygon_centroids(polygon_rivers, grid, \
            pline_layer = pline_rivers, id_field_name = 'ID')

    """

    # Init output dictionary
    polygon_cells_dic = {}

    # check that the selection in polygon_layer is not empty
    selected_feat_ids = polygon_layer.selectedFeaturesIds()
    if len(selected_feat_ids) == 0:
        print("Empty selection, all features considered")
        polygons = polygon_layer.getFeatures()
    else :
        print("Only selected features will be considered")
        polygons = polygon_layer.selectedFeatures()

    # create and fill spatial Index
    grid_layer_index = get_spatial_indexes([grid_layer])[0]

    # build grid feature dictionary
    grid_feat_dic = { feat.id():feat for feat in grid_layer.getFeatures()}

    # init pline dictionary
    if pline_layer is not None :
        pline_dic = { feat[id_field_name]:feat for feat in pline_layer.getFeatures() }

    # Iterate over polygons in polygon_layer
    for polygon in polygons :

        # list of grid cells intersected by polygon
        intersected_cells_list = []

        # get grid cells in the bbox of the polygon
        polygon_geom = QgsGeometry(polygon.geometry())
        grid_feat_intersect_ids = grid_layer_index.intersects(polygon_geom.boundingBox())

        # fetch corresponding pline based on ID atribute
        if pline_layer is not None :
            pline = pline_dic[ polygon[id_field_name] ]
            pline_feat_dic, pline_point_layer_index, pline_cumdist_dic = get_pline_data(pline, pline_layer)

        # shorten selection to grid cells intersected by the polygon
        for id in grid_feat_intersect_ids:
            grid_cell = grid_feat_dic[id]
            grid_cell_geom = QgsGeometry(grid_cell.geometry())
            # Within grid cells in the bbox of feat, select those intersecting feat
            if polygon_geom.intersects(grid_cell_geom):
                if pline_layer is not None :
                    grid_cell_centroid = grid_cell_geom.centroid()
                    ndist = get_dist_pline_centroid(grid_cell_centroid, pline, pline_feat_dic, pline_point_layer_index, pline_cumdist_dic)
                    intersected_cells_list.append( [ grid_cell['ROW'], grid_cell['COL'], ndist ] )
                else :
                    intersected_cells_list.append( [ grid_cell['ROW'], grid_cell['COL'] ] )

        # add polygon entry into output dictionary
        polygon_cells_dic[ polygon[id_field_name] ] =  intersected_cells_list

    return(polygon_cells_dic)


# -----------------------------------------------------
# From a selection of features in a vector layer
# returns ptset_field_values, a dictionary { 'ID1':fieldValue, 'ID2':FieldValue, ...}
def get_feat_param(v_layer, id_field_name = 'ID', field_name = 'PARAM',):
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
    # v_layer : vector layer of points with a selection of point
    # field_name : the attribute field of v_layer containing feature identificator

   # check that the selection in v_layer is not empty
    selected_feature_ids = v_layer.selectedFeaturesIds()
    if len(selected_feature_ids) == 0:
        print("Empty selection, all features considered")
        features = v_layer.getFeatures()
    else :
        print("Only selected features will be considered")
        features = v_layer.selectedFeatures()

    # init output dictionary
    ptset_field_values = {}

    for feat in features:
        this_feat_id = feat[ id_field_name ]
        this_feat_field_value = feat[ field_name ]
        ptset_field_values[ this_feat_id  ] = this_feat_field_value

    return(ptset_field_values)

# -----------------------------------------------------
# From 2D array, fills shape file attribute table
def data_to_grid(data, grid_layer, field_name = 'PARAM', fieldType = QVariant.Double ):
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
    # Note : to date, only fieldType Double is applicable
    # TODO check that data has same number of elements of grid_layer
    # Select all features along with their attributes
    #allAttrs = grid_layer.pendingAllAttributesList()
    #grid_layer.select(allAttrs)
    print('STARTING')
    # load dic of current layer attributes
    field_name_map = grid_layer.dataProvider().fieldNameMap()

    # if field "field_name" does not exist in attribute map, add it
    if field_name not in field_name_map.keys():
        grid_layer.dataProvider().addAttributes(  [QgsField( field_name, fieldType)] )
        grid_layer.updateFields()

    # reshape array to a 1D vector
    # elements are sorted from top left to bottom right
    data = np.reshape(data, -1)

    print('building all_features')
    # Init variables
    all_features = {feat.id():feat for feat in grid_layer.getFeatures()}
    print('building all_centroids')
    all_centroids = [feat.geometry().centroid().asPoint() \
                        for feat in all_features.values()]
    print('sorting centroids')
    centroids_ids = all_features.keys()
    centroids_x = np.around(np.array([centroid.x() for centroid in all_centroids]), MAX_DECIMALS)
    centroids_y = np.around(np.array([centroid.y() for centroid in all_centroids]), MAX_DECIMALS)
    centroids = np.array( [centroids_ids , centroids_x, centroids_y] )
    centroids = centroids.T

    # sort by decreasing y and increasing x (from top left to bottom right)
    # for regular grids, this corresponds to row-wise and column wise
    idx = np.lexsort( [centroids_x,-1*centroids_y] )
    centroids = centroids[idx,:]

    print('building attribute map')
    # populate change attribute map
    field_idx = grid_layer.fieldNameIndex(field_name)
    attr_map = { centroids[i,0] : { field_idx : float(data[i]) } for i in range( centroids.shape[0] ) }

    print('updating attributes')
    # write attributes
    grid_layer.startEditing()
    res = grid_layer.dataProvider().changeAttributeValues(attr_map)
    grid_layer.commitChanges()

    return res


