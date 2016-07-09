#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import datetime
import pickle
from termcolor import colored
import pandas
from selenium import webdriver
import pyexcel as excel
import pyexcel.ext.xls
import stats

data = pandas.read_excel("data/plantas.xlsx",index_col=0)
plantas = data.index.values
mesInicio = sys.argv[2]
mesFin = sys.argv[3]


class Analisis:

    def __init__(self,archivo,mesInicio,mesFin):
        self.archivo = archivo
        self.mesInicio = mesInicio
        self.mesFin = mesFin
        self.plantas = []
        self.anios = {}

    def bounds(self):
        data = pandas.read_excel("generacionNeta.xlsx",index_col='planta')
        self.plantas = data.index.values
        anios = []
        for element in data.iloc[:0]:
            anios.append(element)
        meses = anios[:12]
        for i,mes in enumerate(meses):
            mes = str(mes)
            if self.mesInicio in mes:
                inicio = i
            if self.mesFin in mes:
                fin = i+1
        return inicio,fin



    def datos_anuales(self,planta):
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
                lele = data.loc[planta,meses[i]+str(an)]
                if lele  != 0.0:
                    l.append(lele)
                else:cont += 1
            self.anios[str(an)] = l
        #print "Datos perdidos: %i"%cont
        return self.anios

    def res(self):
        tabla = {}
        for ind,e in enumerate(plantas):
            try:
                elementos = self.datos_anuales(plantas[ind])
                results = {}
                anio = 2000
                for i in range(6,16):
                    an = anio+i
                    e = elementos[str(an)]
                    p = stats.Estadisticas(e)
                    results[str(an)] = round(p.media(),4)
                try :
                    tabla[plantas[ind]] = results
                except IndexError:
                    print ""
                s = stats.Estadisticas(results)
            except ZeroDivisionError:
                pass
        return tabla



if __name__ == '__main__':
    archivo = sys.argv[1]
    a = Analisis(archivo,mesInicio,mesFin)
    tabla = {}
    mesInicio = "MAR"
    mesFin = "JUN"
    for ind,e in enumerate(plantas):
        try:
            elementos = a.datos_anuales(plantas[ind])
            results = {}
            anio = 2000
            for i in range(6,16):
                an = anio+i
                e = elementos[str(an)]
                p = stats.Estadisticas(e)
                results[str(an)] = round(p.media(),4)
            try :
                tabla[plantas[ind]] = results
            except IndexError:
                print "error en " + str(i) + plantas[ind]
            s = stats.Estadisticas(results)
        except ZeroDivisionError:
            pass

        #print s.media()
    #print tabla
