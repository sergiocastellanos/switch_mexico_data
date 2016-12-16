'''

 This script takes a list of longitudes and a list of latitudes (lat, lon)
 and returns the address of the location of each point given.

'''
import requests
import pandas as pd
import time

def reverseGeodata():
    datapoints = pd.read_csv('MeshMexico.csv')

    latitudes = []
    longitudes = []
    
    for index, row in datapoints.iterrows():
        latitudes.append(row['LAT'])
        longitudes.append(row['LON'])
        
    address = []

    print (len(latitudes))
    print (len(longitudes))
    
    for i in range (len(latitudes)):
        base = "http://maps.googleapis.com/maps/api/geocode/json?"
        params = "latlng={lat},{lon}&sensor={sen}".format(
            lat=latitudes[i],
            lon=longitudes[i],
            sen='false'
        )
        url = "{base}{params}".format(base=base, params=params)
        response = requests.get(url)

        print (str(response.json()['results'][0]['formatted_address']))
        
        address.append(str(response.json()['results'][0]['formatted_address']))
        time.sleep(1)
        
    datapoints['address'] = address
    datapoints.to_csv('reversedgeodata.csv')

reverseGeodata()
