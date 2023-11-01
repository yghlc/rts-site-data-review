#!/usr/bin/env python
# Filename: tools.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 01 November, 2023
"""

import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point

import geopandas as gpd

def convert_bounds_to_polygon(bounds):
    # bounding box: (left, bottom, right, top)
    letftop1 = (bounds[0],bounds[3])
    righttop1 = (bounds[2],bounds[3])
    rightbottom1 = (bounds[2],bounds[1])
    leftbottom1 = (bounds[0],bounds[1])
    polygon = Polygon([letftop1, righttop1,rightbottom1,leftbottom1])
    return polygon

def to_points(a_point):
    # point (x,y)
    point = Point(a_point[0], a_point[1])
    return point


def save_geometry_to_files(data_frame, geometry_name, wkt_string, save_path,format='ESRI Shapefile'):
    '''
    :param data_frame: include polygon list and the corresponding attributes
    :param geometry_name: dict key for the polgyon in the DataFrame
    :param wkt_string: wkt string (projection)
    :param save_path: save path
    :param format: use ESRI Shapefile or "GPKG" (GeoPackage)
    :return:
    '''
    # data_frame[geometry_name] = data_frame[geometry_name].apply(wkt.loads)
    poly_df = gpd.GeoDataFrame(data_frame, geometry=geometry_name)
    poly_df.crs = wkt_string # or poly_df.crs = {'init' :'epsg:4326'}
    poly_df.to_file(save_path, driver=format)

    return True