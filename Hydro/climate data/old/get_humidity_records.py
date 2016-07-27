import forecastio
import datetime
import json, pickle
from stats import Statistics as stats

api_key = "2f32cd6123f1b5af9f83951f4fb6b92b"


lat = 16.74
lng = -93.14

def precipAccumulation():
    '''It make API calls in order to obtain the precipAccumulation level of the given coordinates and dates'''
    precipAccumulation_record = {}
    for year in range(2009,2016):
        for month in range(01,13):
            for day in range(1,31):
                try :
                    date = datetime.datetime(year,month,day)
                    forecast = forecastio.load_forecast(api_key, lat, lng, time=date)
                    try:
                        lista = []
                        c_precipAccumulation = forecast.hourly().data
                        for e in c_precipAccumulation:
                             lista.append(e.precipIntensity)
                        c_precipAccumulation  = stats(lista).media()
                    except forecastio.utils.PropertyUnavailable: c_precipAccumulation = 0
                    print date , c_precipAccumulation
                    precipAccumulation_record[str(date.date())] = c_precipAccumulation
                except ValueError:
                    pass
    return precipAccumulation_record


def storePickle(data):
    '''It stores data(precipAccumulation levels) in a .pkl file for further use'''
    output = open('chicoasen.pkl', 'wb')
    pickle.dump(data, output)
    output.close()


storePickle(precipAccumulation())


# cont =0
# date = datetime.datetime(2006,1,1)
# print date
# forecast = forecastio.load_forecast(api_key, lat, lng, time = date)
# lista = []
# c_precipAccumulation = forecast.hourly().data
# for e in c_precipAccumulation:
#      lista.append(e.precipIntensity)
# s = stats(lista).media()
# print  s
