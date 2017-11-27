#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import pickle
from termcolor import colored
import pandas
from selenium import webdriver
import re
import unicodedata
from stats import Statistics as stats

data = pandas.read_excel("data/production/plantas.xlsx",index_col=0)
plantas = data.index.values

nombres =  pandas.read_excel("data/production/plantas.xlsx",index_col=1)

nombres = nombres.index.values
entidades =  pandas.read_excel("data/production/plantas.xlsx",index_col=4)
entidades = entidades.index.values

seasonlist = ["Winter","Spring","Summer","Autumn"]

archivoGeneracion = "data/production/generacionNeta.xlsx"

class Order:

    def __init__(self):
        self.plantas = []
        self.anios = {}
        self.word = []

    def bounds(self,mesInicio,mesFin):
        '''Returns the index_col of the given months, it works with the generacionNeta.xlsx file '''
        data = pandas.read_excel(archivoGeneracion,index_col='planta')
        self.plantas = data.index.values
        anios = []
        for element in data.iloc[:0]:
            anios.append(element)
        meses = anios[:12]
        for i,mes in enumerate(meses):
            mes = str(mes)
            if mesInicio in mes:
                inicio = i
            if mesFin in mes:
                fin = i+1
        return inicio,fin


    def datos_anuales(self,planta,month_ini,month_end):
        '''Returns a dictionary of dictionaries that contains the years and months as keys and the generation related to a hydroelectric dam as values (between 2006 - 2015), it returns data in an interval which contains month_ini and month_end, as well as all months between them'''
        cont = 0
        data = pandas.read_excel(archivoGeneracion,index_col='planta')
        self.plantas = data.index.values

        anios = []
        for element in data.iloc[:0]:
            anios.append(element)
        meses = anios[:13]
        i,f = self.bounds(month_ini,month_end)
        meses = meses[i:f]
        for year in range(2006,2016):
            l = []
            for i,e in enumerate(meses):
                meses[i] = meses[i][:7]
                lele = data.loc[planta,meses[i]+str(year)]
                if lele  != 0.0:
                    l.append(lele)
                else:cont += 1
            self.anios[str(year)] = l
        #print "Datos perdidos: %i"%cont
        return self.anios

    def annual_data(self,planta):
        annual = ["ENE","DIC"]
        data  = self.datos_anuales(planta,annual[0],annual[1])
        return data





    def test_plantas_season(self):
        '''It takes a dictionary of dictionaries that contains the years and months as keys and the generation related to a hydroelectric dam as values (between 2006 - 2015) and returns the same data separated by season, i.e, Autumn Summer... '''
        seasons = [["ENE","MAR"],["ABR","JUN"],["JUL","SEP"],["OCT","DIC"]]
        data = {}
        tabla = {}
        for ind,e in enumerate(plantas):
            try:
                for year in range(2006,2016):
                    results = {}
                    for i,season in enumerate(seasons):
                        mesInicio = season[0]
                        mesFin = season[1]
                        elementos = self.datos_anuales(plantas[ind],mesInicio,mesFin) #dictionary of dictionaries that contains the years and months as keys and the generation ral....
                        e = elementos[str(year)]
                        p = stats(e)
                        results[seasonlist[i]] = round(p.media(),4)
                    data[year]= results
                try :
                    tabla[plantas[ind]] = data
                except IndexError:
                    print "error en " + str(i) + plantas[ind]
            except ZeroDivisionError:
                print "zero division"
                pass
        return data



    def normalize(self,lista):
        print lista
        '''Returns a list containing normalized (0-1) data from a given list'''

        rang = float(max(lista)) - float(min(lista))
        average = stats(lista).media()
        for i,e in enumerate(lista):
            try:
                lista[i] = (float(e) -average)/rang
            except ZeroDivisionError:
                lista[i] = 0
        minimum = min(lista)
        for i,e in enumerate(lista):
            lista[i] = e - minimum
        return lista


    def bigList(self,data):

        lista = []
        for d in data:

            lista = lista + data[d]
        #print lista
        lista  = self.normalize(lista)
        for d in data:
            data[d] = lista[:12]
            del(lista[:12])
        return data


    def normalized_data(self, data):
        '''It takes a dictionary of dictionaries that contains the years and months as keys and the generation related to a hydroelectric dam as values (between 2006 - 2015) and returns the same but normalized values'''
        aux = []
        for season in seasonlist:
            aux= []
            for d in data:
                for value in data[d]:
                    if value == season:
                        aux.append(data[d][value])
            aux = self.normalize(aux)
            i=0
            for year in range(2006,2016):
                data[year][season]=aux[i]
                i+=1
        return data

    def normalize_annual_data(self, data):
        '''It takes a dictionary of dictionaries that contains the years as keys and the generation related to a hydroelectric dam as values (between 2006 - 2015) and returns the same but normalized values'''
        aux = []
        for year in range(2006,2016):
            try:
                data[str(year)] = self.normalize(data[str(year)])
            except KeyError:
                data[year] = self.normalize(data[year])
        return data


    def capacityFactor(self, data, anios, mw):
        lista = [0,0,0,0,0,0,0,0,0,0,0,0]
        for year in anios:
            for i,e in enumerate(data[str(year)]):
                lista[i] += e
        for i,e in enumerate(lista):
            lista[i] = e/len(anios)
        for i,e in enumerate(lista):
            lista[i] = lista[i]/(720*mw)*100
        return lista



if __name__ == '__main__':
    a = Order()
    anos = [2007]
    for i,planta in enumerate(plantas):
        data = a.datos_anuales(planta,"ENE","DIC")
        print planta, nombres[i],entidades[i]
        output = open('plantas/%s/%s.pkl'%(entidades[i],nombres[i]), 'wb')
        pickle.dump(data, output)
        output.close()


    #b = a.test_plantas_season()
    # for planta in plantas:
    #     a.capacityFactor(a.datos_anuales(planta,"ENE","DIC"),anos,2400)
    #print a.normalized_data(b)
