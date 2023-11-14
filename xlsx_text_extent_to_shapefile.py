#!/usr/bin/env python
# Filename: xlsx_text_extent_shapefile.py 
"""
introduction: read extents or points (lat/lon) in shapefile,then 

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 14 November, 2023
"""

import os
import extent_text_shapefile
import pandas as pd

import tools

def xlsx_latlon_text_to_shapefile(xlsx_path,save_path):

    df_tables = pd.read_excel(xlsx_path, sheet_name=None)  # sheet_name=None: read all sheets
    # print(df_tables)
    data_frame_list = []
    # print(df_tables.keys())
    for key in df_tables.keys():
        data_frame_list.append(df_tables[key])
    pd_all = pd.concat(data_frame_list).reset_index()
    # print(pd_all)
    print('count of all records:', len(pd_all))

    # remove invalid records
    df_valid = pd_all.loc[ pd_all['extent-lat-lon'] != 'TBA' ]
    print('count of valid records:', len(df_valid))

    # # drop duplicated records
    # df_valid = df_valid.drop_duplicates(subset=["extent-lat-lon"])
    # print('count of all records after dropping duplicates:', len(df_valid))

    df_valid = df_valid.reset_index()
    extent_list = []
    extext_row_idx = []

    point_list = []
    point_row_idx = []


    for idx, row in df_valid.iterrows():
        # print(idx, row)
        # print(idx,row['ID'], row['extent-lat-lon'])

        polygons, points = extent_text_shapefile.latlon_text_to_geometry(row['extent-lat-lon'],delimiter=';')

        # print(polygons)
        # print(points)
        if len(polygons) > 0:
            extent_list.extend(polygons)
            extext_row_idx.extend([idx]*len(polygons))

        if len(points) > 0:
            point_list.extend(points)
            point_row_idx.extend([idx]*len(points))


    # print(extent_list)
    # print(point_list)

    # save to geopackage

    # save to file
    wkt = 'EPSG:4326'
    if len(extent_list) > 0:
        save_pd = df_valid.iloc[extext_row_idx]
        save_pd = save_pd[['ID','Article Title','Authors','extent-lat-lon','DOI']]
        save_pd['Polygons'] = extent_list
        tools.save_geometry_to_files(save_pd, 'Polygons', wkt, save_path)
        print('saved to %s'%save_path)

    if len(point_list) > 0:
        save_pd = df_valid.iloc[point_row_idx]
        save_pd = save_pd[['ID','Article Title','Authors','extent-lat-lon','DOI']]
        save_pd['Points'] = point_list
        save_path = os.path.splitext(save_path)[0] + '_point'+ os.path.splitext(save_path)[1]
        tools.save_geometry_to_files(save_pd, 'Points', wkt, save_path)
        print('saved to %s'%save_path)




def main():

    input_xlsx = "rts_paper_list_v0_Nov14.xlsx"
    save_path = "rts_research_sites.shp"
    xlsx_latlon_text_to_shapefile(input_xlsx, save_path)

    pass

if __name__ == '__main__':
    main()