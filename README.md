#Algorithm#

This readme file is used to allow people tko understand the data extraction, data organization and algorithmic processes involved in Polldentify. 

#Data Extraction#
The historical data used comes from two major sources, namely

1. EPA for air quality information; and
2. NOAA for wind data.

Monthly data is used. When comparing daily, monthly and yearly information, we discovered that daily data was too heavy for the web app to process fastly for the user, while yearly provides very coarse information. Hence, monthly data is a good compromise for data points and computational speed.

The programs used to extract data is:

1. openFiles.m: extracting wind data from NOAA. The wind data was stored as an nc file, and due to inability to convert nc files in ibm bluemix, we downloaded nc files, extracted the date, latitude, longitude, uwnd (wind in north south direction) and vwnd (wind in east west direction), place them in a csv file. 

2. airdata.py: Does web crawling and extract information from the EPA AQS website. Loops from 2000 to 2015 and collects pollutant information for ozone, carbon monoxide, sulphur dioxide, nitrogen dioxide and PM10. The output of this step should be a dataframe with all the pollutants and an empty column reserved for altitude, uwnd and vwnd.

3. groupbylocation.py: This file is used to connect with the google API and extract related altitude information. The return format is a JSON file and the data is extracted in the form of a dictionary. The code then proceeds to place the respective altitudes into the final_summary dataframe. If there is no data on the latitude and longitude given, the element would be filled in a zero. 

4. wind_extract.py : The csv file is uploaded to object storage in IBM bluemix. After reading the csv file with function get_file_content, the data is reorganized and the time is converted to the format as year-month-day (e.g. 2000-01-31)

The instructions to obtain all the data is as follow:

1. use openFiles.m to convert the nc files to csv files
2. Use airdata.py to complete the web crawling process. 
3. use groupbylocation.py to add altitude
4. use wind extract.py to add uwnd and vwnd.

(To yash: I am still working on adding uwnd and vwnd, but it should be easy)


