#!/usr/bin/env python
# Filename: extent_text_shapefile.py 
"""
introduction: parse the extent information (latitude and longitude ) from the text,
then create polygons and saved to shapefile

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 01 November, 2023
"""
import os.path
import re
import pandas as pd

import tools

def get_lat_lon_one_line(text):
    # Define the regex pattern to extract latitude and longitude
    # pattern = r'(\d+\.\d+)°([NS]) to (\d+\.\d+)°([EW])'
    # ([NS]): Matches either "N" or "S" to represent the latitude direction.
    # °?: Matches the degree symbol if there.
    # ([EW]): Matches either "E" or "W" to represent the longitude direction.
    pattern_lat = r'(\d+\.\d+)°?([NSns])'
    pattern_lon = r'(\d+\.\d+)°?([EWew])'
    lat_res = re.findall(pattern_lat, text)
    lon_res = re.findall(pattern_lon, text)

    # print(lat_res)
    # print(lon_res)
    # [('67.5', 'N'), ('68.5', 'N')]
    lat_list = sorted([float(item[0]) for item in lat_res if len(item[0]) > 1] )
    lat_list = [ -lat if ns[1] in ['S','s'] else lat for lat, ns in zip(lat_list, lat_res) ] # add sign

    lon_list = sorted([float(item[0]) for item in lon_res if len(item[0]) > 1 ])
    lon_list = [ -lon if ew[1] in ['W','w'] else lon for lon, ew in zip(lon_list,lon_res)]
    # print(lat_list)
    # print(lon_list)

    return lat_list, lon_list


def test_get_lat_lon_one_line():
    sentense = '1. Peel Plateau and Richardson Mountains ("Peel") - 67.5°N to 68.5°N, 133.5°W to 138.5°W'
    sentense_nodeg = '1. Peel Plateau and Richardson Mountains ("Peel") - 67.5N to 68.5N, 133.5W to 138.5W'
    sentense_nodeg2 = '1. Peel Plateau and Richardson Mountains ("Peel") 8.5w'

    get_lat_lon_one_line(sentense)
    # get_lat_lon_one_line(sentense_nodeg)
    # get_lat_lon_one_line(sentense_nodeg2)

def test_extract_latlon_from_text():
    with open('chatpdf-out-example.txt') as f_obj:
        lines = f_obj.readlines()
        for line in lines:
            lats, lons = get_lat_lon_one_line(line)
            if len(lats) > 0 and len(lons) > 0:
                print(lats, lons)

def latlon_text_to_shapefile(input,save_path):

    if os.path.isfile(input):
        with open(input) as f_obj:
            text_lines = f_obj.readlines()
    else:
        text_lines = input

    extent_list = []
    extext_texts = []
    point_list = []
    point_texts = []
    for line in text_lines:
        lats, lons = get_lat_lon_one_line(line)
        if len(lats) == 2 and len(lons) == 2:   # polygon
            extent_list.append([lats,lons])
            extext_texts.append(line)
        elif len(lats) == 1 and len(lons) == 1: # points
            point_list.append([lats,lons])
            point_texts.append(line)
        elif len(lats) < 1 or len(lons) < 1:    # no data
            continue
        else:
            print('cannot parse a correct point or polygons from:', line)

    # # bounding box: (left, bottom, right, top)
    bounds = [[ item[1][0], item[0][0], item[1][1], item[0][1]] for item in extent_list]
    polygons_shp = [tools.convert_bounds_to_polygon(bound) for bound in bounds]

    points = [ [item[1][0], item[0][0]] for item in point_list]     # x,y: lon, lat
    points_shp = [tools.to_points(p)  for p in points ]

    # save to file
    wkt = 'EPSG:4326'
    if len(polygons_shp) > 0:
        save_pd = pd.DataFrame({'Polygons': polygons_shp, 'poly_text':extext_texts})
        tools.save_geometry_to_files(save_pd, 'Polygons', wkt, save_path)
        print('saved to %s'%save_path)

    if len(points_shp) > 0:
        save_pd = pd.DataFrame({'Points': points_shp, 'poly_text':point_texts})
        save_path = os.path.splitext(save_path)[0] + '_point'+ os.path.splitext(save_path)[1]
        tools.save_geometry_to_files(save_pd, 'Points', wkt, save_path)
        print('saved to %s'%save_path)


def main():
    # test_get_lat_lon_one_line()
    # test_extract_latlon_from_text()

    save_path = 'bernhard-assessing-2022.shp'
    latlon_text_to_shapefile('chatpdf-out-example.txt', save_path)

    pass

if __name__ == '__main__':
    main()