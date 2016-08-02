#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import pickle
from termcolor import colored
import pandas
import re
import unicodedata
import math


data = pandas.read_excel("../data/plantas.xlsx",index_col=0)

class Order:

    def __init__(self):
        self.plantas = []
        self.anios = {}
        self.word = []




    def datos_anuales(self):
        '''Returns a dictionary of dictionaries that contains the years and months as keys and the generation related to a hydroelectric dam as values (between 2006 - 2015), it returns data in an interval which contains month_ini and month_end, as well as all months between them'''
        cont = 0
<<<<<<< HEAD
        ecglobal = {}
        aglobal = 1
        data = pandas.read_excel("drought.xlsx",sheetname="MUNICIPIOS",index_col="CVE_CONCATENADA")
        g = {2006:[0,0,0,0,0,0,0,0,0,0,0,0,0],2007:[0,0,0,0,0,0,0,0,0,0,0,0,0],2008:[0,0,0,0,0,0,0,0,0,0,0,0,0],2009:[0,0,0,0,0,0,0,0,0,0,0,0,0],2010:[0,0,0,0,0,0,0,0,0,0,0,0,0],2011:[0,0,0,0,0,0,0,0,0,0,0,0,0],2012:[0,0,0,0,0,0,0,0,0,0,0,0,0],2013:[0,0,0,0,0,0,0,0,0,0,0,0,0],2014:[0,0,0,0,0,0,0,0,0,0,0,0,0],2015:[0,0,0,0,0,0,0,0,0,0,0,0,0]}
        boo = True
        entidad  = data.index.values[0]-1
        cont = -1
        listaEntidad = [0,0,0,0,0,0,0,0,0,0,0,0]

        while boo:
            try:
                cont+=1
                entidad +=1
                for year in range(2006,2016):
                    lista= []
                    for month in range(01,13):
                        try:
                            lele = data.loc[entidad,datetime.datetime(year,month,31)]
                        except ValueError:
                            try:
                                lele = data.loc[entidad,datetime.datetime(year,month,30)]
                            except ValueError:
                                try:
                                    lele = data.loc[entidad,datetime.datetime(year,month,29)]
                                except ValueError:
                                    lele = data.loc[entidad,datetime.datetime(year,month,28)]
                        if lele == "D0":
                            lista.append(1)
                        elif lele == "D1":
                            lista.append(2)
                        elif lele == "D2":
                            lista.append(3)
                        elif lele == "D3":
                            lista.append(4)
                        elif lele == "D4":
                            lista.append(5)
                        elif math.isnan(lele):
                            lista.append(0)
                    for i in range(12): g[year][i] += lista[i]
                    g[year][12] = cont+1

            except KeyError:
                for year in range(2006,2016):
                    for i in range(12):
                        try:
                            g[year][i] = g[year][i]/g[year][12]
                        except ZeroDivisionError:
                            g[year][i] = 0
                    del(g[year][12])
                ecglobal[aglobal] = g
                aglobal += 1
                g = {2006:[0,0,0,0,0,0,0,0,0,0,0,0,0],2007:[0,0,0,0,0,0,0,0,0,0,0,0,0],2008:[0,0,0,0,0,0,0,0,0,0,0,0,0],2009:[0,0,0,0,0,0,0,0,0,0,0,0,0],2010:[0,0,0,0,0,0,0,0,0,0,0,0,0],2011:[0,0,0,0,0,0,0,0,0,0,0,0,0],2012:[0,0,0,0,0,0,0,0,0,0,0,0,0],2013:[0,0,0,0,0,0,0,0,0,0,0,0,0],2014:[0,0,0,0,0,0,0,0,0,0,0,0,0],2015:[0,0,0,0,0,0,0,0,0,0,0,0,0]}
                entidad += (1000-cont)-1
                cont = -1
                if entidad > 32058:
                    print entidad
                    boo = False
        return ecglobal
=======

        data = pandas.read_excel("m.xlsx",sheetname="MUNICIPIOS",index_col="NOMBRE_MUN")
        for year in range(2003,2016):
            lista= []
            print year
            for month in range(01,13):
                try:
                    lele = data.loc["Chicoasen",datetime.datetime(year,month,31)]
                except ValueError:
                    try:
                        lele = data.loc["Chicoasen",datetime.datetime(year,month,30)]
                    except ValueError:
                        try:
                            lele = data.loc["Chicoasen",datetime.datetime(year,month,29)]
                        except ValueError:
                            lele = data.loc["Chicoasen",datetime.datetime(year,month,28)]
                if lele == "D0":
                    lista.append(1)
                elif lele == "D1":
                    lista.append(2)
                elif lele == "D2":
                    lista.append(3)
                elif lele == "D3":
                    lista.append(4)
                elif lele == "D4":
                    lista.append(5)
                elif math.isnan(lele):
                    lista.append(0)



            print lista
>>>>>>> aa6929b19a167f4b58a0d02aaa0adbab25c5d32e




    def annual_data(self,planta):
        annual = ["ENE","DIC"]
        data  = self.datos_anuales(planta,annual[0],annual[1])
        return data



<<<<<<< HEAD
    def storePickle(self,data):
        '''It stores data (drought levels) in a .pkl file for further use'''
        output = open('msequia.pkl', 'wb')
        pickle.dump(data, output)
        output.close()
=======
>>>>>>> aa6929b19a167f4b58a0d02aaa0adbab25c5d32e



if __name__ == '__main__':
    a = Order()
<<<<<<< HEAD
    a.storePickle(a.datos_anuales())
=======
    a.datos_anuales()
>>>>>>> aa6929b19a167f4b58a0d02aaa0adbab25c5d32e
    anos = [2007,2008,2010,2011]
    #b = a.test_plantas_season()
    #for planta in plantas:
    #    a.capacityFactor(a.datos_anuales(planta,"ENE","DIC"),anos,2400)
    #print a.normalized_data(b)
