import forecastio
import datetime
import json, pickle

api_key = "2f32cd6123f1b5af9f83951f4fb6b92b"


lat = 16.9416721
lng = -93.1027447

def humidity():hu
    '''It make API calls in order to obtain the humidity level of the given coordinates and dates'''
    humidity_record = {}
    for year in range(2006,2016):
        for month in range(01,12):
            for day in range(1,31):
                try :
                    date = datetime.datetime(year,month,day)
                    forecast = forecastio.load_forecast(api_key, lat, lng, time=date)
                    c_humidity = forecast.currently().humidity
                    print str(date.date()) , c_humidity
                    humidity_record[str(date.date())] = c_humidity
                except ValueError:
                    pass
    return humidity_record


def storePickle(data):
    '''It stores data(humidity levels) in a .pkl file for further use'''
    output = open('humidity.pkl', 'wb')
    pickle.dump(data, output)
    output.close()


storePickle(humidity())
