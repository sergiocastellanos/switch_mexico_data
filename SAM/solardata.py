'''
This file gets info. regarding solar energy generation in an area through the NREL API. To use it:

    ~: python solardata.py "mesh.csv" "path to save" "year" "interval in minutes" "name" "email" "reason of use" "institution" "NREL API Key" "use UTC (True/False)"

    Example:

    ~: python solardata.py ../mesh.csv /home/benito/BECI/2014/ 2014 30 "Benito Juárez" "benitojuarezgarcia@presidencia.gob.mx" "Research" "Estados Unidos Mexicanos" "*Benito's API Key*"

 You can get your own personal API Key in the following website: https://developer.nrel.gov/signup/

Dec 13, 2016.

'''
import requests
import pandas as pd
import numpy as np
import time
import sys, os
import io
from tqdm import tqdm

def create_folders (path, year):
    if not os.path.exists (path + '/' + year):
        os.makedirs (path + '/' + year)

    if not os.path.exists (path + '/'+ year + 'meta/'):
        os.makedirs (path + '/'+ year + 'meta/')

def is_leap_year (year):
    year = int(year)
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    return False

def get_name (name):
    return name.replace (" ", "+")

def get_data (mesh, path, year, interval, name, email, reason, institution, api_key, utc):
    mesh = (pd.read_csv(mesh, header = -1, encoding = "ISO-8859-1"))[1:]
    name = get_name(name)
    
    for i, val in tqdm (enumerate(mesh[1]), desc = "Counties in Mexico completed for this day/dataframe"):
        time.sleep(10)
        latitude = mesh[2].iloc[i]
        longitude = mesh[3].iloc[i]
        attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp,solar_zenith_angle'
        leap_year = 'true' if is_leap_year(year) else 'false'
        tinterval = str(interval)
        user_name = name
        reason_for_use = reason
        affiliation = institution
        user_email = email

        url = 'http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year = year, lat = latitude, lon = longitude, leap = leap_year, interval = tinterval, utc = utc, name = user_name, email = user_email, mailing_list = 'false', affiliation = institution, reason = reason_for_use, api = api_key, attr = attributes)

        data = requests.get(url).content
        
        meta = pd.read_csv (io.StringIO(data.decode('utf-8')), nrows = 1)
        info = pd.read_csv (io.StringIO(data.decode('utf-8')), skiprows = 2)
        
        filenameoutput = '{}'.format (i + 1)

        info = info.to_csv (path + '/' + year + '/' + filenameoutput + '.csv')
        meta = meta.to_csv (path + '/' + year + 'meta/' + filenameoutput + '.csv')

create_folders (sys.argv[2], sys.argv[3])
get_data (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], 'true' if (sys.argv[10] == 'True') else 'false')
