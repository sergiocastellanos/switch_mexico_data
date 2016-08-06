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

import stats

data = pandas.read_excel("data/plantas.xlsx",index_col=0)
plantas = data.index.values


seasonlist = ["Winter","Spring","Summer","Autumn"]


class Analisis:

    def __init__(self):
        self.plantas = []
        self.anios = {}
        self.word = []

    def bounds(self,mesInicio,mesFin):
        ''''''
        data = pandas.read_excel("generacionNeta.xlsx",index_col='planta')
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


    def datos_anuales(self,planta,mesInicio,mesFin):
        cont = 0
        data = pandas.read_excel("generacionNeta.xlsx",index_col='planta')
        self.plantas = data.index.values
        anios = []
        for element in data.iloc[:0]:
            anios.append(element)
        meses = anios[:13]
        i,f = self.bounds(mesInicio,mesFin)
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
        print self.anios
        return self.anios

    def monthly(self,planta):
        cont = 0
        data = pandas.read_excel("generacionNeta.xlsx",index_col='planta')
        self.plantas = data.index.values
        anios = []
        for element in data.iloc[:0]:
            anios.append(element)
        meses = anios[:13]

        i,f = self.bounds()
        meses = meses[i:f]

        anio = 2000
        for i in range(6,16):
            an = anio+i
            l = []
            for i,e in enumerate(meses):
                meses[i] = meses[i][:7]
                print meses[i]
                lele = data.loc[planta,meses[i]+str(an)]
                if lele  != 0.0:
                    l.append(lele)
                else:cont += 1
            self.anios[str(an)] = l
        #print "Datos perdidos: %i"%cont
        return self.anios

    def clean(self,name):
        #name = "Mazatlan_II_(Jose_Aceves_Pozos)_U1"
        if name.find("("):
            replace = name[name.find("("):name.find(")")+1]
        name = name.replace(replace,"")
        name = name.replace("S.A. DE C.V.","")
        name = name.replace("S. DE R.L. DE C.V.","")
        name = name.replace("S. DE R. L. DE C.V.","")
        name = name.replace("S. A. DE C. V.","")
        name = name.replace("S. DE R. L. DE C. V.","")
        name = name.replace("__","_")
        name = name.replace("-","_")
        name = name.replace("S.A.","")
        name = name.replace("S. A. P. I. DE C. V.","")
        if name.endswith("_"):
            name = name[:len(name)-1]

        return name




    def hydroelectric_fuel(self):
        data = pandas.read_excel("BAL_data_Mexico_bi_08_06.xlsx",index_col="Balmorel name")
        runOf  = data.loc[:,["Fuel"]]
        reservoir = data.loc[:,["Fuel"]]
        runOf  = data.loc[data['Fuel'] == "Water - Run-of-river"]
        reservoir = data.loc[data['Fuel'] == "Water - Reservoir"]
        fuel = [reservoir,runOf]
        result = pandas.concat(fuel)
        result =  result.loc[:,["Fuel"]]
        result.to_excel(excel_writer="fuelresults.xlsx")




#,sheetname="Planned units"
    def res(self):
        tabla = {}
        for ind,e in enumerate(plantas):
            try:
                elementos = self.monthly(plantas[ind])
                results = {}
                anio = 2000
                for i in range(6,16):
                    an = anio+i
                    e = elementos[str(an)]
                    try:
                        p = stats.Estadisticas(e)
                        results[str(an)] = round(p.media(),4)
                    except ValueError:
                        pass
                try :
                    tabla[plantas[ind]] = results
                except IndexError:
                    print ""
                s = stats.Estadisticas(results)
            except ZeroDivisionError:
                pass
        return tabla


    def test_plantas_season(self):
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
                        elementos = self.datos_anuales(plantas[ind],mesInicio,mesFin)
                        e = elementos[str(year)]
                        p = stats.Estadisticas(e)
                        results[seasonlist[i]] = round(p.media(),4)
                    data[year]= results
                try :
                    tabla[plantas[ind]] = data
                except IndexError:
                    print "error en " + str(i) + plantas[ind]
            except ZeroDivisionError:
                print "zero division"
                pass
        return (tabla,data)



if __name__ == '__main__':
    archivo = sys.argv[1]
    a = Analisis(archivo)
    c,b = a.test_plantas_season()
    print c,b
    #a.hydroelectric_fuel()
    #a.compare()
    #tabla = {}

        #print s.media()
    #print tabla
