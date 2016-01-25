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

#Things that we still need to do before passing into the algorithm#

1. merge the uwnd and vwnd data into the final_summary dataframe
2. delete the last row of dates (2015-12-30) because the information there is not sufficient. A lot of datapoints are missing
3. For the rest of the pollutant data that has NaN as a value, need to use interpolate function to interpolate the elements back.
4. Test the algorithm
5. Check how to incorporate state symbols to latitudes and longitudes
6. After calculating A and X, we need to add the sources that are of the same state to see how a state affects a certain longitude and latitude. Again, this is done because we only consider places in terms of specific longitude and latitude, the effects of each location would appear puny. 

#Algorithm#

algorithm.py stores the current algorithm we have.

Currently, the algorithm is written such that the matrix function takes in a dataframe with lat, lon, alt, uwnd, vwnd and concentration of pollutants of ONE SINGLE MONTH and outputs 

1. X: which is the rate of emission from sources; and
2. A: the coefficeints that is supposed to be multiplied to the sources. It can be seen as the weight of each source with respect to a single location.

Some inference from the two matrices:

1. Row N indicates at place (xN,yN), what is the weight of each city. By taking row N and multiplying it element wise with column A, it should yield the rate of emission of pollutants from one single city and the weight of the source of pollution. Take the weighted average of the product would yield you the weighted average. 
2. The whole matrix, A and X, only gives you one single month of data. 

