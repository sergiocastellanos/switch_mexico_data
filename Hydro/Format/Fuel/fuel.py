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
mesInicio = sys.argv[2]
mesFin = sys.argv[3]


class Fuel:
    def __init__(self,archivo,mesInicio,mesFin):
        self.archivo = archivo
        self.mesInicio = mesInicio
        self.mesFin = mesFin
        self.plantas = []
        self.anios = {}
        self.word = []


    def strip_accents(self, text):
        try:
            text.encode('utf-8').strip()
        except NameError: # unicode is a default on python 3
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def text_to_id(self,text):
        text = self.strip_accents(text.lower())
        text = re.sub('[ ]+', '_', text)
        text = re.sub('[^0-9a-zA-Z_-]', '', text)
        return text

    def names(self,names):
        for i in range(len(names)):
            word = self.clean(names[i])
            word = self.text_to_id(word)
            self.word.append(self.clean(word))
        return self.word

    def match(self):
        fuel = pandas.read_excel("Permisos generación CRE 2012.xlsx")
        fuel = fuel["PERMISIONARIO"]
        fuel = fuel.tolist()
        runOf = self.names(fuel)
        data = pandas.read_excel("Nombres_Nomenclatura_GENERACION.xlsx")
        data = data.loc[:,["Central/Proyecto_Clean","Combustible"]]
        for i in range(len(data.index)):
            central = data.iloc[i]
            for j in runOf:
                if j in str(central["Central/Proyecto_Clean"]).lower():
                    central["Combustible"] = "Run Of The River"
                    data.loc[i,"Combustible"] = "Run Of The River"
        data.to_excel('fuel.xlsx', sheet_name='Fuel')


if __name__ == '__main__':
    archivo = sys.argv[1]
    a = Fuel(archivo,mesInicio,mesFin)
    #a.hydroelectric_fuel()
    a.match()
    #tabla = {}

        #print s.media()
    #print tabla
