



#Loops through each row
for index,rows in final_summary.iterrows():
    a = rows['lat']
    b = rows['lon']
    #Checks whether there is a value in df_latitude that matches the longitude and latitude final_summary
    ss = df_altitude[(df_altitude.lat == a) & (df_altitude.lon == b)].values
    if (len(ss) != 0):
    	#If it is a number, return the value to the cell
        ss1 = ss[0][2]
        final_summary.set_value(index, 'alt',ss1 )
    else:
    	#if there is no number, then return Not a NUmber for the element
        final_summary.set_value(index,'alt','NaN')

upper_lat = 50.0
lower_lat = 17.5
upper_lon = 310.0
lower_lon = 170.0
n_lat = 14
n_lon = 57

#declare empty dataframe
index = range(0,627)
df_altitude = pd.DataFrame(index = index, columns = ['lon','lat','alt'])
index=0

for lon in np.linspace(lower_lon,upper_lon,n_lon):
    for lat in np.linspace(lower_lat,upper_lat,n_lat): 
        df_altitude.iloc[index,0] = lon
        df_altitude.iloc[index,1] = lat
        if lon > 180:
            lon = 360 - lon
        url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=' + str(lat)+','+str(lon)+'&key=AIzaSyCFcP2vrQ4rk9I9Q6mgwRTv48XeQmnIDLI'
        request = Request(url)
        response = urlopen(request)
        elevations = response.read()
        data = json.loads(elevations)
        el = []
        for result in data['results']:
            el.append(result[u'elevation'])
        df_altitude.iloc[index,2] = el[0]
        index+=1
        time.sleep(1)
