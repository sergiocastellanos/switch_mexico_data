import forecastio
import datetime
import json, pickle
from termcolor import colored
from precipAccumulation import PrecipAccumulation
from generation import Order
import pandas
import collections

data = pandas.read_excel("data/plantas.xlsx",index_col=0)
plantas = data.index.values

a = Order()
for planta in plantas:
    production = a.annual_data(planta)
    production =  a.normalize_annual_data(production)

precipAccumulation = PrecipAccumulation().ux()


listax= ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

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
    lista = []
    for season in seasonlist:
        j = 0
        for h,p in zip(precipAccumulation,production):
            for a,b in zip(precipAccumulation[h],production[p]):
                if a == season:
                    j+=1
                    lista.append("var %s = {x: %20s, y: %20s, r: %20s, };"%(a.lower()+str(j),precipAccumulation[h][a],production[p][b],production[p][b]+5))
    return lista


def insertInJS(lista1,lista2):
    i=0
    with open('Charts/bubble.js', 'r') as input_file, open('bubble.js', 'w') as output_file:
        for line in input_file:
            try :
                if line[:15] == lista1[i][:15]:
                    print line[:15] , lista1[i][:15]
                    output_file.write(lista1[i])
                    i+=1
                else:
                    output_file.write(line)
            except IndexError: output_file.write(line)

    with open('bubble.js', 'r') as input_file, open('chart.js', 'w') as output_file:
        i =0
        for line in input_file:
            try :
                if line[:18] == lista2[i][:18]:
                    print line[:18] , lista2[i][:18]
                    print lista2[i]
                    output_file.write(lista2[i])
                    i+=1
                else:

                    output_file.write(line)
            except IndexError: output_file.write(line)



def insertAnnualInJS(precipAccumulation,production):
    print precipAccumulation
    annual_list = []
    production = collections.OrderedDict(sorted(production.items()))
    j= 0
    for h,p in zip(precipAccumulation,production):
        i = 0
        for a,b in zip(precipAccumulation[h],production[p]):
            print a,b
            annual_list.append("var %s%s = {x: %s, y: %s, r: 10};"%(listax[i],j,precipAccumulation[h],production[p]))
            print listax[i]
            i+=1
        j+=1
    return annual_list

def external():
    return precipAccumulation,production




insertAnnualInJS(jsprinter(precipAccumulation,norm_production))
