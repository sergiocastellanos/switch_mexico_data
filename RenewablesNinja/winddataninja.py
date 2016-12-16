'''
This files gets the info. about simulations of the hourly power output from wind plants located in a specific area.
It uses the Renewable.ninja API. To make use of this file, you can run the following in your console:

   ~: python winddataninja.py <Path to CSV with Coordinates (lon/lat)> <Path to save the retrieved data> <Year> <Token for the API> <Height of the turbine> <Model of the turbine> <KW>

   Example:

   ~: python winddataninja.py ../Mesh.csv /home/benito/BECI/RenewablesNinjaData/2014/ 2014 "*Benito's Token*" 80 "Vestas V90 2000" 1000


To get your token and info. regarding the height and model of the turbines, refer to: https://www.renewables.ninja/

'''
import requests
import pandas as pd
import json
import time
import sys, os
import io
from tqdm import tqdm

def create_folders (path, year):
    if not os.path.exists (path + '/' + year):
        os.makedirs (path + '/' + year)

def get_data (mesh, path, year, token, height, model, kw):
    api_base = 'https://www.renewables.ninja/api/v1/data/wind'

    s = requests.session()
    s.headers = {'Authorization' : 'Token ' + token}

    counties = pd.read_csv(r'../MeshMexico.csv', header = -1, encoding = "ISO-8859-1")
    counties = counties[1:]

    for i, val in tqdm(enumerate(counties[1]), desc = "Iteration"):
        args = {
            'lat' : counties[2].iloc[i],
            'lon' : counties[3].iloc[i],
            'date_from' : str(year + '-01-01'),
            'date_to' : str(year + '-12-31'),
            'capacity' : kw, #KW
            'height' : height,
            'turbine' : model,
            'format' : 'csv'
        }

        csv_string = s.get(api_base, params = args)
        cvs_handle = io.StringIO(csv_string.text)
        values = pd.read_csv(cvs_handle, index_col = 0, parse_dates = True)
        filenameoutput = '{}'.format(i+1)
        df = values.to_csv(path + '/' + year + '/' + filenameoutput + '.csv')

if len(sys.argv) != 8:
    print("There was an error with the parameters. Expected arguments:\n\n\t <Path to CSV with coordinates> <Save to... path> <Year> <Token> <Height> <Model of the turbine> <Capacity (KW)> \n")
else:
    create_folders (sys.argv[2], sys.argv[3])
    get_data (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
