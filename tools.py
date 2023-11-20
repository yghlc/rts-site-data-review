#!/usr/bin/env python
# Filename: tools.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 01 November, 2023
"""

import os
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point

import geopandas as gpd
from packaging import version

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


def read_shape_gpd_to_NewPrj(shp_path, prj_str):
    '''
    read polyogns using geopandas, and reproejct to a projection.
    :param polygon_shp:
    :param prj_str:  project string, like EPSG:4326
    :return:
    '''
    shapefile = gpd.read_file(shp_path)
    # print(shapefile.crs)

    # shapefile  = shapefile.to_crs(prj_str)
    if version.parse(gpd.__version__)  >= version.parse('0.7.0'):
        shapefile = shapefile.to_crs(prj_str)
    else:
        shapefile  = shapefile.to_crs({'init':prj_str})
    # print(shapefile.crs)
    polygons = shapefile.geometry.values
    # fix invalid polygons
    # polygons = fix_invalid_polygons(polygons)

    return polygons


def get_file_list_by_ext(ext,folder,bsub_folder):
    """

    Args:
        ext: extension name of files want to find, can be string for a single extension or list for multi extension
        eg. '.tif'  or ['.tif','.TIF']
        folder:  This is the directory, which needs to be explored.
        bsub_folder: True for searching sub folder, False for searching current folder only

    Returns: a list with the files abspath ,eg. ['/user/data/1.tif','/user/data/2.tif']
    Notes: if input error, it will exit the program
    """

    extension = []
    if isinstance(ext, str):
        extension.append(ext)
    elif isinstance(ext, list):
        extension = ext
    else:
        raise ValueError('input extension type is not correct')
    if os.path.isdir(folder) is False:
        raise IOError('input error, directory %s is invalid'%folder)
    if isinstance(bsub_folder,bool) is False:
        raise ValueError('input error, bsub_folder must be a bool value')

    files = []
    sub_folders = []
    sub_folders.append(folder)

    while len(sub_folders) > 0:
        current_sear_dir = sub_folders[0]
        file_names = os.listdir(current_sear_dir)
        file_names = [os.path.join(current_sear_dir,item) for item in file_names]
        for str_file in file_names:
            if os.path.isdir(str_file):
                sub_folders.append(str_file)
                continue
            ext_name = os.path.splitext(str_file)[1]
            for temp in extension:
                if ext_name == temp:
                    # files.append(os.path.abspath(os.path.join(current_sear_dir,str_file)))
                    files.append(str_file)
                    break
        if bsub_folder is False:
            break
        sub_folders.pop(0)

    return files


def read_list_from_txt(file_name):
    with open(file_name,'r') as f_obj:
        lines = f_obj.readlines()
        lines = [item.strip() for item in lines]
        return lines