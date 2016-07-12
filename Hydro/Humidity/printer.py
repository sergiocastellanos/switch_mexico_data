import forecastio
import datetime
import json, pickle
import stats
from termcolor import colored
from humidity import Humidity
from generacion import Analisis

humidity = Humidity().get_data()

a = Analisis()
production = a.test_plantas_season()
norm_production =  a.normalized_data(production)


def printer(humidity,production):
    '''Prints on shell of a given humidity and production dictionaries'''
    for h,p in zip(humidity,production):
        print colored(h,color="magenta")
        for a,b in zip(humidity[h],production[p]):
            print colored(a, color="white"),\
                  colored("%.10s"%humidity[h][a],color="cyan"),\
                  colored("%.10s"%production[p][b],color="cyan")

# humidity = x

def jsprinter(humidity,production):
    '''Prints data required to build charts'''
    for h,p in zip(humidity,production):
        for a,b in zip(humidity[h],production[p]):
            if a == "Winter":
                print "var %s = {x: %s, y: %s, r: %s, };"%(a.lower(),humidity[h][a],production[p][b],production[p][b]+5)


printer(humidity,norm_production)
