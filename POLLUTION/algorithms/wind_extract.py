'''
This code is used to place related wind data into a summary dataframe. The uwnd and vwnd obtained comes from NOAA: 
ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/surface/ . The nc file is converted to csv files for 
Apache Spark through matlab. The matlab file is saved as convert.m . 
'''

import requests, StringIO, pandas as pd, json, re
import numpy as np

content_string_u = get_file_content(credentials_u)
uwnd = pd.read_csv(content_string_u, names = ['lon','lat','time','uwnd'])

content_string_v = get_file_content(credentials_v)
vwnd = pd.read_csv(content_string_v,names = ['lon','lat','time','vwnd'])

#Altering data on the uwnd and vwnd such that it matches the US coordinate system
#US has latitude between N 25 and N 50, and longitude between E 170 and E 310
new_uwnd = uwnd[uwnd.uwnd != 0]
new_uwnd = new_uwnd[uwnd.lon >= 170.0]
new_uwnd = new_uwnd[uwnd.lon <= 310.0]
new_uwnd = new_uwnd[uwnd.lat >= 17.5]
new_uwnd = new_uwnd[uwnd.lat <= 50.0]

new_vwnd = vwnd[vwnd.vwnd != 0]
new_vwnd = new_vwnd[vwnd.lon >= 170.0]
new_vwnd = new_vwnd[vwnd.lon <= 310.0]
new_vwnd = new_vwnd[vwnd.lat >= 17.5]
new_vwnd = new_vwnd[vwnd.lat <= 50.0]


#Combine the dataframes together and take away the redundant columns
new_df = pd.concat([new_uwnd, new_vwnd], axis = 1,keys = ['time','lon','lat'],ignore_index =True)
del new_df[4]
del new_df[5]
del new_df[6]
new_df.columns = ['lon','lat','time','uwnd','vwnd']


#Change the units of time from "hours after 1800-01-01" to "year-month-day"
import time
z=0
month = 1
new_df['datetype'] = ""
for index,rows in new_df.iterrows():
    #Check to see which month it is and add the appropriate date.
    #makes it easier to merge the dates together
    if ((month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12)):
        date = 30
    elif ((month == 4) or (month == 6) or (month == 9) or (month == 11)):
        date = 29
    else: 
        if (z%4):
            date = 28
        else:
            date = 27
    if month < 10:
        date_string = str(int(2000)+z)+'-0'+str(month)+'-' + str(date)
    else:
        date_string = str(int(2000)+z)+'-'+str(month)+'-' + str(date)
    date = time.strptime(date_string, "%Y-%m-%d")
    new_df.set_value(index,'datetype',date)
    month += 1
    if(month == 13): 
        month=1
        z += 1
    if (rows['time'] == 1892664):
        month = 1
        z = 0

del new_df['time']
new_df.reset_index()


def get_file_content(credentials):
    '''For given credentials, this functions returns a StringIO object containg the file content.'''
    
    url1 = ''.join([credentials['auth_url'], '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': credentials['username'],'domain': {'id': credentials['domain_id']},
            'password': credentials['password']}}}}}
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    resp1_body = resp1.json()    
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                if(e2['interface']=='public'and e2['region']==credentials['region']):
                    url2 = ''.join([e2['url'],'/', credentials['container'], '/', credentials['filename']])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    resp2 = requests.get(url=url2, headers=headers2)
    return StringIO.StringIO(resp2.content)

credentials_u = {
    'auth_url': 'https://identity.open.softlayer.com',
    'domain_id': '24ea5bc355c340fb89109ee990246e8c',
    'username': 'admin_490197b2-3772-4817-9fb0-414179ab8ac2_0889ddcf4d99',
    'region' : 'dallas',
    'password': 'I?tu,#ngLV=FT98I',
    'filename': 'uwnd_mon_mean.csv',
    'container': 'test_store'
}

credentials_v = {
    'auth_url': 'https://identity.open.softlayer.com',
    'domain_id': '24ea5bc355c340fb89109ee990246e8c',
    'username': 'admin_490197b2-3772-4817-9fb0-414179ab8ac2_0889ddcf4d99',
    'region' : 'dallas',
    'password': 'I?tu,#ngLV=FT98I',
    'filename': 'vwnd_mon_mean.csv',
    'container': 'test_store'
}