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
import re

wkt = 'EPSG:4326'

def read_all_sites_from_folder(folder):
    folders = [item for item in os.listdir(folder) if os.path.isdir(os.path.join(folder,item) ) ]
    # print(folders)

    # get paper-id and file list
    paper_regions = {}
    for ff in folders:
        match = re.match(r'^(\d+)', ff)
        ff_path = os.path.join(folder,ff)
        if match:
            paper_id = int(match.group())
            file_list = tools.get_file_list_by_ext(['.shp','.geojson'],ff_path,bsub_folder=False)
            paper_regions[paper_id] = file_list

    return paper_regions

def read_sites_from_file(path):
    # read the polygons
    polygons = tools.read_shape_gpd_to_NewPrj(path,wkt)
    return polygons


def test_read_all_sites_from_folder():
    folder_path = 'study_area_polygons'
    paper_regions = read_all_sites_from_folder(folder_path)
    print(paper_regions)

    for key in paper_regions.keys():
        polygons = read_sites_from_file(paper_regions[key][0])
        print(polygons)

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

    paper_regions = read_all_sites_from_folder('study_area_polygons')
    print(paper_regions)
    # df_site_in_files = pd_all[pd_all['ID'].isin(paper_regions.keys())]
    # print(df_site_in_files)

    # remove invalid records
    df_valid = pd_all.loc[ (pd_all['extent-lat-lon'] != 'TBA') | (pd_all['ID'].isin(paper_regions.keys()) )]
    print('count of valid records:', len(df_valid))

    # drop duplicated records
    df_valid = df_valid.drop_duplicates(subset=["ID"])
    print('count of all records after dropping duplicates:', len(df_valid))

    df_valid = df_valid.reset_index()
    extent_list = []
    extext_row_idx = []

    point_list = []
    point_row_idx = []


    for idx, row in df_valid.iterrows():
        # print(idx, row)
        # print(idx,row['ID'], row['extent-lat-lon'])

        if row['ID'] in paper_regions.keys():
            polygons = []
            for file_path in paper_regions[row['ID']]:
                polys = read_sites_from_file(file_path)
                polygons.extend(polys)

            extent_list.extend(polygons)
            extext_row_idx.extend([idx] * len(polygons))

        else:
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

    # test_read_all_sites_from_folder()

    input_xlsx = "rts_paper_list_v0_Nov16.xlsx"
    save_path = "rts_research_sites.shp"
    xlsx_latlon_text_to_shapefile(input_xlsx, save_path)

    pass

if __name__ == '__main__':
    main()