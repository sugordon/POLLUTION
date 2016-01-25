#Algorithm#

This readme file is used to allow people tko understand the data extraction, data organization and algorithmic processes involved in Polldentify. 

#Data Extraction#
The historical data used comes from two major sources, namely

1. EPA for air quality information; and
2. NOAA for wind data.

Monthly data is used. When comparing daily, monthly and yearly information, we discovered that daily data was too heavy for the web app to process fastly for the user, while yearly provides very coarse information. Hence, monthly data is a good compromise for data points and computational speed.

The programs used to extract data is:

1. openFiles.m: extracting wind data from NOAA. The wind data was stored as an nc file, and due to inability to convert nc files in ibm bluemix, we downloaded nc files, extracted the date, latitude, longitude, uwnd (wind in north south direction) and vwnd (wind in east west direction), place them in a csv file. 

2. wind_extract.py : The csv file is uploaded to object storage in IBM bluemix. After reading the csv file with function get_file_content, the data is reorganized and the time is converted to the format as year-month-day (e.g. 2000-01-31)
