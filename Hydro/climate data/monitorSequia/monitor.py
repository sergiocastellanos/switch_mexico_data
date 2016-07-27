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




    def annual_data(self,planta):
        annual = ["ENE","DIC"]
        data  = self.datos_anuales(planta,annual[0],annual[1])
        return data






if __name__ == '__main__':
    a = Order()
    a.datos_anuales()
    anos = [2007,2008,2010,2011]
    #b = a.test_plantas_season()
    #for planta in plantas:
    #    a.capacityFactor(a.datos_anuales(planta,"ENE","DIC"),anos,2400)
    #print a.normalized_data(b)
