#!/usr/bin/python
# -*- coding: utf8 -*-
import forecastio
import datetime
import json, pickle
from termcolor import colored
from precipAccumulation import PrecipAccumulation as pacc
from production import Order
import pandas
import collections
from stats import Statistics as s
import sys



data = pandas.read_excel("data/plantas.xlsx",index_col=0)
plantas = data.index.values
dat = pandas.read_excel("generacionNeta.xlsx",index_col='planta')
a = Order()
#8 infernillo,
index =  int(sys.argv[2])
planta = dat.index.values[index]
print planta
production = a.annual_data(planta)                                #generacion
varprod =  production

with open(r"msequia.pkl", "rb") as input_file:
    drought = pickle.load(input_file)                                           #Sequia

precipitation = pacc().retrieveCSV()                                            #precipitacion


def norms(param):
    norm_normalized = a.bigList(param)
    media_norm = {}
    for element in norm_normalized:
        media_norm[element] = s(norm_normalized[element]).media()
    media_norm = collections.OrderedDict(sorted(media_norm.items()))
    lista = []
    for element in media_norm:
        lista.append(media_norm[element])
    lista  = a.normalize(lista)
    return lista

normalized = ["production","drought","precipitation"]

#19 oaxaca, 7 chiapas, 16 michoacan, 18 nayarit
entidad = drought[int(sys.argv[1])]
#print entidad
#print entidad

all_normalized_data = []

print all_normalized_data.append(norms(production))

d = str(norms(entidad)).replace(", ",", -")
d = d.replace("[","[-")
all_normalized_data.append(d)
all_normalized_data.append(norms(precipitation))

#print all_normalized_data


listas= ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
variables = ["SEIS","SIETE","OCHO","NUEVE","DIEZ","ONCE","DOCE","TRECE","CATORCE","QUINCE"]



def printer(precipitation,production):
    '''Prints on shell of a given precipitation and production dictionaries'''
    for h,p in zip(precipitation,production):
        print colored(h,color="magenta")
        for a,b in zip(precipitation[h],production[p]):
            print colored(a, color="white"),\
                  colored("%.10s"%precipitation[h][a],color="cyan"),\
                  colored("%.10s"%production[p][b],color="cyan")

def jsprinter(precipitation,production):
    '''Prints data required to build charts'''
    lista = []
    for season in seasonlist:
        j = 0
        for h,p in zip(precipitation,production):
            for a,b in zip(precipitation[h],production[p]):
                if a == season:
                    j+=1
                    lista.append("var %s = {x: %20s, y: %20s, r: %20s, };"%(a.lower()+str(j),precipitation[h][a],production[p][b],production[p][b]+5))
    return lista

def insertInJS(lista2,row):
    i=0
    with open('Charts/js/bubble.js', 'r') as input_file, open('%s.js'%planta.lower(), 'wb') as output_file:
        i =0
        for line in input_file:
            try :
                #print line[:row] , lista2[i][:row]
                if line[:row] == lista2[i][:row]:
                    #print line[:row] , lista2[i][:row]
                    output_file.write(lista2[i])
                    i+=1
                else:
                    output_file.write(line)
            except IndexError: output_file.write(line)

def insertVariablesJS(seqa,listx,x):
    annual_list = []
    for i,e in enumerate(seqa):
        annual_list.append("var %s%s = %s;"%(x,listx[i],seqa[e]))
    return annual_list

def insertAnnualInJS(precipitation,production,listax):
    annual_list = []
    j= 0
    for h,p in zip(precipitation,production):
        i = 0
        for a,b in zip(precipitation[h],production[p]):
            #print "var %s%s = {x: %s, y: %s, r: 10};"%(listax[i],j,a,b)
            annual_list.append("var %s%s = {x: %s, y: %s, r: 10};"%(listax[i],j,a,b))
            i+=1
        j+=1
    return annual_list


def NormalAnnualInJS(listax):
    annual_list = []
    for i,e in enumerate(listax):
        annual_list.append("var %s = %s;"%(normalized[i],e))
    return annual_list



def external():
    return precipitation,production
insertInJS(insertAnnualInJS(entidad,production,listas),15)
#print insertVariablesJS(entidad,variables,"S")

print insertVariablesJS(varprod,variables,"G")
#print insertVariablesJS(precipitation,variables,"")
#insertInJS(NormalAnnualInJS(all_normalized_data),8)             #grafica con valoresnormalizados
