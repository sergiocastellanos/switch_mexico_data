'''
To generate SAM simulations over a set of .cvs files with solar energy info.:

    ~: python samsimul.py ../MeshMexico.csv /home/ludwig/switch/SAM/2014 2014 30 500 Optimal

     / python samsimul.py <Mesh file.csv> <NSRDB Files and Metafiles path> <Year> <Minutes> <KW> <Tilt ("Optimal"/"Normal")>
'''
import pandas as pd
import numpy as np
import sys, os
import simplejson
import urllib
import ctypes as ct
import site
site.addsitedir('SDK/languages/python/')
import sscapi
from tqdm import tqdm

def create_folders (path, year, interval, MW, tilt):
    if not os.path.exists (path + '/' + year + 'SAMgen_' + interval + 'mins_' + MW + 'MW_' + tilt):
        print ('Creating folder >> ' + path + '/' + year + 'SAMgen_' + interval + 'mins_' + MW + 'MW_' + tilt)
        os.makedirs (path + '/' + year + 'SAMgen_' + interval + 'mins_' + MW + 'MW_' + tilt)
        
def get_csvs_simulations (mesh, path, year, interval, kw, tiltc):
    mesh = pd.read_csv(mesh, header = -1, encoding = "ISO-8859-1")[1:]
    
    for i, val in tqdm (enumerate(mesh[1]), desc = "Counties in Mexico completed for this day/dataframe"):
        info = pd.read_csv(str(path + '/' + str(year) + 'meta/' + mesh[1].iloc[i] + '.csv'), nrows = 1)
        timezone = info['Local Time Zone']
        elevation = info['Elevation']
        df = pd.read_csv(str(path + '/' + str(year) + '/' + mesh[1].iloc[i] + '.csv'))
        latitude = float(mesh[2].iloc[i])
        longitude = float(mesh[3].iloc[i])

        kw = int(kw)
        year = df['Year'][i]
        month = df['Month'][i]
        day = df['Day'][i]
        hour = df['Hour'][i]
        minute = df['Minute'][i]

        df = df.set_index(pd.date_range('1/1/{yr} 00:00'.format(yr = year), freq = interval + 'Min', periods = 525600 / int(interval)))
        ssc = sscapi.PySSC()

        wfd = ssc.data_create()
        ssc.data_set_number(wfd, 'lat'.encode('utf-8'), latitude)
        ssc.data_set_number(wfd, 'lon'.encode('utf-8'), longitude)
        ssc.data_set_number(wfd, 'tz'.encode('utf-8'), timezone)
        ssc.data_set_number(wfd, 'elev'.encode('utf-8'), elevation)
        ssc.data_set_array(wfd, 'year'.encode('utf-8'), df.index.year)
        ssc.data_set_array(wfd, 'month'.encode('utf-8'), df.index.month)
        ssc.data_set_array(wfd, 'day'.encode('utf-8'), df.index.day)
        ssc.data_set_array(wfd, 'hour'.encode('utf-8'), df.index.hour)
        ssc.data_set_array(wfd, 'minute'.encode('utf-8'), df.index.minute)
        ssc.data_set_array(wfd, 'dn'.encode('utf-8'), df['DNI'])
        ssc.data_set_array(wfd, 'df'.encode('utf-8'), df['DHI'])
        ssc.data_set_array(wfd, 'wspd'.encode('utf-8'), df['Wind Speed'])
        ssc.data_set_array(wfd, 'tdry'.encode('utf-8'), df['Temperature'])

        dat = ssc.data_create()
        ssc.data_set_table(dat, 'solar_resource_data'.encode('utf-8'), wfd)
        ssc.data_free(wfd)

        # System Capacity in KW
        system_capacity = kw
        ssc.data_set_number(dat, 'system_capacity'.encode('utf-8'), system_capacity)

        # Set DC/AC ratio (or power ratio). See https://sam.nrel.gov/sites/default/files/content/virtual_conf_july_2013/07-sam-virtual-conference-2013-woodcock.pdf
        dc_ac_ratio = 1.1
        ssc.data_set_number(dat, 'dc_ac_ratio'.encode('utf-8'), dc_ac_ratio)

        # Set tilt of system in degrees (default: 25)
        # Optimum: (latitude * .76) + 3.1
        tilt = (float(mesh[2].iloc[i])) if tiltc == "Normal" else ((float(mesh[2].iloc[1])*.76) + 3.1)
        ssc.data_set_number(dat, 'tilt'.encode('utf-8'), tilt)

        # Set azimuth angle (in degrees) from north (0 degrees)
        azimuth = 180
        ssc.data_set_number(dat, 'azimuth'.encode('utf-8'), azimuth)

        # Set the inverter efficiency
        inv_eff = 96
        ssc.data_set_number(dat, 'inv_eff'.encode('utf-8'), inv_eff)

        # Set the system losses, in percent
        losses = 14.0757
        ssc.data_set_number(dat, 'losses'.encode('utf-8'), losses)

        # Specify fixed tilt system (1=true, 0=false)
        array_type = 1
        ssc.data_set_number(dat, 'array_type'.encode('utf-8'), array_type)

        # Set ground coverage ratio
        gcr = 0.4
        ssc.data_set_number(dat, 'gcr'.encode('utf-8'), gcr)

        # Set constant loss adjustment
        loss_adjustment = 0
        ssc.data_set_number(dat, 'adjust:constant'.encode('utf-8'), loss_adjustment)
        
        # Execute and put generation results back into dataframe
        mod = ssc.module_create('pvwattsv5'.encode('utf-8'))
        ssc.module_exec(mod, dat)
        df['generation'] = np.array(ssc.data_get_array(dat, 'gen'.encode('utf-8')))
        
        # Free the memory
        ssc.data_free(dat)
        ssc.module_free(mod)
        
        # Divide sum of generation by the number of periods times the system size
        df['generation'].sum() / (525600/int(interval) * system_capacity)
        
        # Total Energy:
        df['generation'].sum()
        
        df['latitude'] = latitude
        df['longitude'] = longitude
        df['timezone'] = np.array(timezone)[0]
        df['elevation'] = np.array(elevation)[0]
        systemconfig_id = 'sc' + str(system_capacity) + 'dcac' + str(dc_ac_ratio) +\
                          'tilt' + str(tilt) + 'az' + str(azimuth) + 'eff' + str(inv_eff) +\
                          'loss' + str(losses) + 'gc' + str(gcr) +\
                          ('adj' + str(loss_adjustment) if loss_adjustment != 0 else '') +\
                          ('fixed' if array_type == 1 else '')
        df['ID_scenario'] = systemconfig_id

        df.to_csv (str(path + '/' + str(year) + 'SAMgen_' + str(interval) + 'mins_' + str(float(kw)/1000.0) + 'MW_' + tiltc + '/' + mesh[1].iloc[i] + '.csv'), index = False)


if (len(sys.argv) != 7):
    print ("There was an error with the parameters. Expected arguments: \n\n\t <Path to CSV with coordinates> <SAM Files and Metafiles path> <Year> <Minutes> <KW> <Tilt (\"Optimal\"/\"Normal\")>")
else:
    if (sys.argv[2].endswith('/')):
        sys.argv[2] = (sys.argv[2])[:-1]

    if sys.argv[6] != "Optimal" and sys.argv[6] != "Normal":
        print ("Error in tilt value.")
        exit

    create_folders (sys.argv[2], sys.argv[3], sys.argv[4], str(float(sys.argv[5])/1000.0), sys.argv[6])
    get_csvs_simulations (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
