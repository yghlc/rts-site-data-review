#!/usr/bin/env python
# Filename: extract-paper-info.py 
"""
introduction: extract paper information: geographical locations,  investigating period into a new excel file

# install packages:
pip install spacy geonamescache
python -m spacy download en_core_web_sm

python -m spacy download en_core_web_lg  # download the largest english model

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 30 October, 2023
"""

import spacy
import geonamescache

import pandas as pd
import os
import glob

# 'Source Title', published journal or conference.
# 'Document Type', Article or review, or proceeding
# 'WoS Categories', research field: Geography, Physical; Geosciences, Multidisciplinary
#
attribute_list = ['Article Title','Authors', 'Source Title', 'Language', 'Document Type',
                  'Author Keywords', 'Times Cited, All Databases','Publication Year',
                  'DOI','DOI Link', 'Abstract']

attribute_add = ['investigate regions', 'investigate period']


def extract_date_locations(nlp,in_text):

    if type(in_text) is float:
        return [], []

    doc = nlp(in_text)
    locations = []
    dates = []
    for entity in doc.ents:
        if entity.label_ == "GPE":  # GPE represents geopolitical entity, like Canada or London
            locations.append(entity.text)
        if entity.label_ == "LOC":  # represent locations
            locations.append(entity.text)
        if entity.label_ == "DATE":
            dates.append(entity.text)

    # get unique values
    dates = list(set(dates))
    locations = list(set(locations))

    return dates, locations

def extract_countries(geoname, locations):
    # it only checks a location is a country or not.
    # cannot check if a city belong to which country
    countries = []
    for location in locations:
        country = geoname.get_countries_by_names().get(location)
        if country:
            countries.append(country["name"])
    return countries

def test_extract_locations():
    # 'en_core_web_sm' is an English language multi-task Convolutional Neural Network(CNN) trained on OntoNotes. Assigns
    # context-specific token vectors, POS tags, dependency parse, and named entities.

    # The model (en_core_web_lg) is the largest English model of spaCy with size 788 MB.
    # There are smaller models in English and some other models for other languages
    # (English, German, French, Spanish, Portuguese, Italian, Dutch, Greek). Step-3: Import Library and Load the Model

    # npl = spacy.load('en_core_web_sm')
    npl = spacy.load('en_core_web_lg')

    gc = geonamescache.GeonamesCache()

    # nlp.get_pipe('ner').labels
    #  no location info
    # abstract = "Thaw slumps are clear indicators of rapid permafrost degradation. They form preferentially in near-surface ice -rich permafrost of northern high latitudes after initial thermal disturbance by the subsequent interplay of thermal (thawing of frozen deposits and melting of ice) and mechanical (slumping and erosion) processes. The largest known thaw slump on Earth - the Batagay megaslump - has been identified in sloping terrain on the Yana Upland in northern Yakutia. Its initiation began in the 1980s, with a current area of >0.8 km2. It continues to grow and has headwall retreat rates of up to 15 m per year. While various satellite remote sensing studies of the Batagay thaw slump have been undertaken, on-site studies characterizing internal landforms, terrain changes, and geomorphic processes have not yet been conducted. To fill this knowledge gap and to enhance our under-standing of the dynamics of very large thaw slumps, our study employs on-site observations and detailed permafrost sampling combined with unoccupied aerial vehicle data from 2019. The latter were used to generate an orthomosaic, a digital surface model, hypsometric slope profiles and a map of relief types in the thaw slump. Within the Batagay thaw slump, the dynamic relationship between headwall morphology and slump floor is largely determined by the cryolithological structure of the permafrost horizons exposed across the headwall rising up to 55 m above the slump floor. Factors include the thickness and overall high volumetric ground-ice content (up to 87 %) of the cryostratigraphic horizons. Furthermore, the diurnal and seasonal insolation expo-sure of the headwall perimeter superimposes both thermal denudation activity and meltwater transport of eroded material. Thus, recent degradation patterns are linked to permafrost properties. Therefore, the Batagay thaw slump is not only a window into Earth's past as it reveals ancient permafrost, but its modern dynamics highlight that ongoing rapid permafrost thaw under present Arctic warming is directly influenced by its Quaternary geological and permafrost history."

    # cannot extract Tibetan Plateau
    # abstract = "Retrogressive thaw slumps (RTSs) are among the most dynamic landforms in permafrost areas, and their formation can be attributed to the thawing of ice-rich permafrost. The spatial distribution and impacts of RTSs on the Tibetan Plateau are poorly understood due to their remote location and the technical challenges of automatic mapping. In this study, we innovatively applied DeepLabv3+, a cutting-edge deep learning algorithm for semantic segmentation, to Planet CubeSat images, which are satellite images with high spatial and temporal resolution. Our method allows us to automatically delineate 220 RTSs within an area of 5200 km2 with an average precision of 0.541. The corresponding precision, recall, and F1 score are 0.863, 0.833, and 0.848 respectively, when the threshold of intersection over union is 0.5. Moreover, approximately 100 experiments on k-fold cross-validation (k = 3, 5, and 10) and data augmentation show that our method is robust. And a test in a different geographic area shows that the generalization of the trained model is very good. We find that (1) most of the RTSs are small (areas < eight ha and perimeters < 2000 m) and (2) RTSs preferentially develop at locations with gentle slopes (four to eight degrees), and in areas lower than the surroundings (the mean topographic position index is − 0.17 ) and receiving less solar radiation (i.e., north-facing slopes). The results show that the method can map RTSs automatically from Planet CubeSat images and can potentially be applied to larger areas."

    # only output Canada, cannot find Arctic, Siberia
    # abstract = "Retrogressive thaw slumps (RTS) are thermokarst features in ice-rich hillslope permafrost terrain, and their occurrence in the warming Arctic is increasingly frequent and has caused dynamic changes to the landscape. RTS can significantly impact permafrost stability and generate substantial carbon emissions. Understanding the spatial and temporal distribution of RTS is a critical step to understanding and modelling greenhouse gas emissions from permafrost thaw. Mapping RTS using conventional Earth observation approaches is challenging due to the highly dynamic nature and often small scale of RTS in the Arctic. In this study, we trained deep neural network models to map RTS across several landscapes in Siberia and Canada. Convolutional neural networks were trained with 965 RTS features, where 509 were from the Yamal and Gydan peninsulas in Siberia, and 456 from six other pan-Arctic regions including Canada and Northeastern Siberia. We further tested the impact of negative data on the model performance. We used 4-m Maxar commercial imagery as the base map, 10-m NDVI derived from Sentinel-2 and 2-m elevation data from the ArcticDEM as model inputs and applied image augmentation techniques to enhance training. The best-performing model reached a validation Intersection over Union (IoU) score of 0.74 and a test IoU score of 0.71. Compared to past efforts to map RTS features, this represents one of the best-performing models and generalises well for mapping RTS in different permafrost regions, representing a critical step towards pan-Arctic deployment. The predicted RTS matched very well with the ground truth labels visually. We also tested how model performance varied across different regional contexts. The result shows an overall positive impact on the model performance when data from different regions were incorporated into the training. We propose this method as an effective, accurate and computationally undemanding approach for RTS mapping."

    abstract ="Deep learning has been used for mapping retrogressive thaw slumps and other periglacial landforms but its application is still limited to local study areas. To understand the accuracy, efficiency, and transferability of a deep learning model (i.e., DeepLabv3+) when applied to large areas or multiple regions, we conducted several experiments using training data from three different regions across the Canadian Arctic. To overcome the main challenge of transferability, we used a generative adversarial network (GAN) called CycleGAN to produce new training data in an attempt to improve transferability. The results show that (1) data augmentation can improve the accuracy of the deep learning model but does not guarantee transferability, (2) it is necessary to choose a good combination of hyper-parameters (e.g., backbones and learning rate) to achieve an optimal trade-off between accuracy and efficiency, and (3) a GAN can significantly improve the transferability if the variation between source and target is dominated by color or general texture. Our results suggest that future mapping of retrogressive thaw slumps should prioritize the collection of training data from regions where a GAN cannot improve the transferability."


    dates, locations = extract_date_locations(npl, abstract)
    print('dates:',dates)
    print("locations:", locations)

    countries = extract_countries(gc, locations)
    print('countries:',countries)


def read_excel_files_into_one_df(excel_files):
    data_frame_list = []
    for e_file in excel_files:
        df = pd.read_excel(e_file)
        data_frame_list.append(df)

    res = pd.concat(data_frame_list)
    return res.reset_index()

def extract_paper_info(dataframe):



    # remove duplicate records
    df = dataframe.drop_duplicates() # subset="Article Title"
    print('record count after removing duplicates:', len(df))

    #
    df_col_sel = df[attribute_list]
    sheet_dict = {'all-webofscience': df_col_sel}

    # extract dates and locations from abstract
    npl = spacy.load('en_core_web_lg')
    # gc = geonamescache.GeonamesCache()

    # add columns
    date_list = []
    location_list = []
    for abstract in df['Abstract']:
        date, location = extract_date_locations(npl,abstract)
        if len(date) < 1:
            date.append('NA')
        if len(location) < 1:
            location.append('NA')
        date_list.append(','.join(date))
        location_list.append(','.join(location))
    df_col_sel.insert(loc=2,column='inv-regions', value=location_list)
    df_col_sel.insert(loc=3,column='inv-period', value=date_list)

    df_slump = df_col_sel.loc[ df['Article Title'].str.contains('slump',case=False) &
                               df['Author Keywords'].str.contains('slump',case=False)]

    # print('df_slump:',len(df_slump))
    sheet_dict['slump-in-Title-Keyword'] = df_slump


    return sheet_dict #df_col_sel



def main():
    # test_extract_locations()

    excel_files = glob.glob('paper-lists/*.xls')
    df_all = read_excel_files_into_one_df(excel_files)
    # print(df_all['DOI Link'])
    print('record count:',len(df_all))
    sheet_dict = extract_paper_info(df_all)

    save_file = 'paper_list.xlsx'
    # Create an Excel writer object
    writer = pd.ExcelWriter(save_file)
    for key in sheet_dict.keys():
        # Write the DataFrame to different sheets of the Excel file
        sheet_dict[key].to_excel(writer, sheet_name=key)  # index=False
    writer.save()
    print('saved to %s'%save_file)



    pass

if __name__ == '__main__':
    main()