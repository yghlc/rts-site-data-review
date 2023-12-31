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


def read_continentalScale_works(ids_txt):
    ids = [ int(item.strip()) for item in tools.read_list_from_txt(ids_txt) ]
    return ids

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

    df_valid['ID'] = df_valid['ID'].astype('int')

    # save to geopackage
    extent_id_list = []
    point_id_list = []

    # save to file
    if len(extent_list) > 0:
        save_pd = df_valid.iloc[extext_row_idx]
        save_pd = save_pd[['ID','Article Title','Authors','extent-lat-lon','DOI']]
        save_pd.rename(columns={'Article Title':'Title', 'extent-lat-lon':'ext-lat-lon'}, inplace=True)
        save_pd['Polygons'] = extent_list
        extent_id_list = save_pd['ID'].to_list()

        # add indicator showing if the polygons belong to continental scale
        save_pd['contiScale'] = [0] * len(extent_list)
        contiscale_ids = read_continentalScale_works('continentalScale.txt')
        save_pd.loc[save_pd['ID'].isin(contiscale_ids), 'contiScale'] = 1

        tools.save_geometry_to_files(save_pd, 'Polygons', wkt, save_path)
        print('saved to %s'%save_path)

    if len(point_list) > 0:
        save_pd = df_valid.iloc[point_row_idx]
        save_pd = save_pd[['ID','Article Title','Authors','extent-lat-lon','DOI']]
        save_pd.rename(columns={'Article Title': 'Title', 'extent-lat-lon': 'ext-lat-lon'}, inplace=True)
        save_pd['Points'] = point_list
        point_id_list = save_pd['ID'].to_list()

        save_path = os.path.splitext(save_path)[0] + '_point'+ os.path.splitext(save_path)[1]
        tools.save_geometry_to_files(save_pd, 'Points', wkt, save_path)
        print('saved to %s'%save_path)


    print('Extent count:', len(extent_id_list))
    print('Unique Extent ID count:', len(set(extent_id_list)))

    print('Point count:', len(point_id_list))
    print('Unique Point ID count:', len(set(point_id_list)))

    all_ids = extent_id_list + point_id_list
    print('Unique ID count:', len(set(all_ids)))




def main():

    # test_read_all_sites_from_folder()

    input_xlsx = "rts_paper_list_v0_Nov21.xlsx"
    save_path = "rts_research_sites.shp"
    xlsx_latlon_text_to_shapefile(input_xlsx, save_path)

    pass

if __name__ == '__main__':
    main()