#!/usr/bin/env python
# Filename: sync_record_in_tables.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 29 November, 2023
"""

import os
import pandas as pd

def sync_record_values_in_diff_tables(in_xlsx, out_xlsx):
    sheet_all_rec = 'all-webofscience'

    # copy values in the following table to "all-webofscience"
    sheet_slumpTitle =  'slump-in-Title-or-Keyword'
    sheet_landslide = 'landslide-in-Tit-or-KW-no-slump'
    sheet_added = 'manually-add'
    other_sheet = [sheet_slumpTitle, sheet_landslide, sheet_added]
    other_sheet_df = []

    column_to_update = ['period-from-paper', 'extent-lat-lon', 'link-to-data']

    df_all_rec = pd.read_excel(in_xlsx, sheet_name=sheet_all_rec)
    for sheet_nm in other_sheet:
        # read
        df_rec = pd.read_excel(in_xlsx, sheet_name=sheet_nm)
        other_sheet_df.append(df_rec)

        # find the same records, then copy values
        for index, row in df_rec.iterrows():
            sel_df = df_all_rec.loc[ (df_all_rec['ID'] == row['ID']) & (df_all_rec['Article Title'] == row['Article Title'])]
            if len(sel_df) < 1:
                continue
            if len(sel_df) > 1:
                raise ValueError('multi recodes in %s, with title: %s'%(sheet_all_rec, row['Article Title']))

            for column in column_to_update:
                if row[column] == 'TBA':
                    continue
                if sel_df.iloc[0][column] == 'TBA':

                    # sel_df.iloc[0][column] = row[column]  # only write to the copy of data frame
                    # print('paper id: %d, copy value'%row['ID'])
                    df_all_rec.loc[(df_all_rec['ID'] == row['ID']), column] = row[column]   # write to the orignal dataframe
                else:
                    print('warning: paper id: %d, there is already value in column %s, skip copying'%(row['ID'],column))


    # save
    # Create an Excel writer object
    writer = pd.ExcelWriter(out_xlsx)

    df_all_rec.to_excel(writer, sheet_name=sheet_all_rec, index=False)
    for sheet_nm, sheet_df in zip(other_sheet,other_sheet_df):
        # Write the DataFrame to different sheets of the Excel file
        sheet_df.to_excel(writer, sheet_name=sheet_nm, index=False)  # index=False
    writer.save()
    print('saved to %s' % out_xlsx)


def main():

    # test_read_all_sites_from_folder()

    input_xlsx = "rts_paper_list_v0_Nov21.xlsx"
    out_xlsx = "rts_paper_list_v1.xlsx"
    sync_record_values_in_diff_tables(input_xlsx, out_xlsx)

    pass

if __name__ == '__main__':
    main()