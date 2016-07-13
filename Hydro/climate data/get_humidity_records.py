import forecastio
import datetime
import json, pickle

api_key = "2f32cd6123f1b5af9f83951f4fb6b92b"


lat = 16.9416721
lng = -93.1027447

def precipAccumulation():
    '''It make API calls in order to obtain the precipAccumulation level of the given coordinates and dates'''
    precipAccumulation_record = {}
    for year in range(2006,2016):
        for month in range(01,12):
            for day in range(1,31):
                try :
                    date = datetime.datetime(year,month,day)
                    forecast = forecastio.load_forecast(api_key, lat, lng, time=date)
                    try:
                        c_precipAccumulation = forecast.currently().precipAccumulation
                    except forecastio.utils.PropertyUnavailable: c_precipAccumulation = 0
                    print str(date.date()) , c_precipAccumulation
                    precipAccumulation_record[str(date.date())] = c_precipAccumulation
                except ValueError:
                    pass
    return precipAccumulation_record


def storePickle(data):
    '''It stores data(precipAccumulation levels) in a .pkl file for further use'''
    output = open('precipAccumulation.pkl', 'wb')
    pickle.dump(data, output)
    output.close()


storePickle(precipAccumulation())
