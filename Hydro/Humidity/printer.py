import forecastio
import datetime
import json, pickle
from termcolor import colored
from precipAccumulation import PrecipAccumulation
from generation import Order



a = Order()
production = a.test_plantas_season()
norm_production =  a.normalized_data(production)

precipAccumulation = PrecipAccumulation().get_data()
precipAccumulation = a.normalized_data(precipAccumulation)


seasonlist = ["Winter","Spring","Summer","Autumn"]

def printer(precipAccumulation,production):
    '''Prints on shell of a given precipAccumulation and production dictionaries'''
    for h,p in zip(precipAccumulation,production):
        print colored(h,color="magenta")
        for a,b in zip(precipAccumulation[h],production[p]):
            print colored(a, color="white"),\
                  colored("%.10s"%precipAccumulation[h][a],color="cyan"),\
                  colored("%.10s"%production[p][b],color="cyan")

# precipAccumulation = x

def jsprinter(precipAccumulation,production):
    '''Prints data required to build charts'''
    for season in seasonlist:
        j = 0
        for h,p in zip(precipAccumulation,production):
            for a,b in zip(precipAccumulation[h],production[p]):
                if a == season:
                    j+=1
                    print "var %s = {x: %20s, y: %20s, r: %20s, };"%(a.lower()+str(j),precipAccumulation[h][a],production[p][b],production[p][b]+5)


jsprinter(precipAccumulation,norm_production)
