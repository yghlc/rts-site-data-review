# rts-site-data-review
Compiling and reviewing the study sites for retrogressive thaw slumps (RTS), 
a part of works of International Permafrost Association (IPA) action group
[RTS InTrain: Retrogressive thaw slump inventory and machine learning training-data development](https://www.permafrost.org/group/rts-intrain-retrogressive-thaw-slump-inventory-and-machine-learning-training-data-development/). 


### RTS papers, reports, or data sets of : 

I used the keywords: permafrost and (thaw slump or landslide or (thermokarst, not lake, not pond)) and exported paper records from the database of Web of Science. 
Then I used panda (a python package) to organize the table and manually uploaded it 
to Google Drive: https://docs.google.com/spreadsheets/d/1hIF7aP7iuFzR5b-piq09TpagGzs1VpfF/edit#gid=921013092

This spreadsheet includes four sheets (tables):

```
"all-weofscience": all the records from Web-of-Science
"slump-in-Title-or-keyword": only the records that contain "slump" in the "Article Title" or "Keyword"
"landslide-in-Tit-or-KW-no-slump": the records that contain "landslide" in the Title or Keyword and "slump" is not in the Title or Keywords 
"manually-added": to add some papers or reports that are not in the database of Web-of-Science or missed by the keywords I used
```

### How to contribute:

**Let's work on the later three tables and add information.**
In each table, we need to fill in the information in the column **"extent-lat-lon"**, 
which is default set as TBA (to be added). 
If information of investigation period or links to data are available, 
please also fill in the columns: "period-from-paper" and "link to data". 
Here I show you how to contribute:

```
1. choose a record that "extent-lat-lon" is "TBA", then find the full text of this paper.
2. find the information on the study area(s) in the paper. If the study area is very small, or  the work just investigated one or a few RTSs close to each other, please input a point (latitude, longitude): such as  68.9 N, 133.8 W. If you think you need to input multiple points (for the case with multiple RTS or sites), then please use semicolons (";") as delimiters to separate each points. 
3. if the paper has the extent(s) of the study area, please input the extent (south to north, west to east), such as  72.93 N to 73.16N, 117.88 W to 118.72W. Again, if there are multiple extents in the paper, please also use ";" as delimiters to separate each extent. 
4. If the paper doesn't present specific thaw slumps (such as a review paper), please replace the "TBA" as "no thaw slumps". If the paper didn't provide latitude and longitude but only mentioned the location name, please fill in the name. 
```
Notes: for the format of the latitude and longitude, 
please use decimal degrees (e.g. 68.923 N), 
not "Degrees Minutes Seconds" (68°55 '22 S"). If the paper didn't provide lat/lon in decimal degrees, please convert them to decimal degrees.  A consistent format is necessary for scripts to convert them (lat/lon) into a map.



### Remarks: 

We hope to have a map to present during ICOP 2024 (June 16-20, 2024) and will try my best to get this map ready as soon as possible.  
The most time-consuming and tedious parts are downloading each paper or report and finding the information we need. 
I also tried to use AI to extract the latitude and longitude from the full text of papers, but from my experience, 
the AI may make up some information that looks reasonable, but actually, inaccurate or incorrect. 
For example, I uploaded a paper to ChatPDF, and asked for the  extent of study areas. 
The AI output 10 extents (lat/lon) of 10 research sites across the Arctic in that paper. 
It looks reasonable but when I looked closely and compared with the map in the original paper, none of the extents was correct. 
If the paper explicitly mentioned the study area and lat/lon in text, the AI may do a good job. 
So, I don't think we can totally use AI to do this work. 


Thank you for reading this and looking forward to your contribution.  
Please let me know if you have any questions, comments or suggestions by 
creating an issue in this repo. 

