import pandas as pd
import sys


estado = "chiapas"
planta = "chicoasen"

data = pd.read_csv("../Data/Production/%s/%s.csv"%(estado,planta),index_col=0)#production info

def get_anio(anio):
    dates = data.index.values
    for i,e in enumerate(dates):
        if e[:4] == str(anio):
            return i


def close_up():
    data = pd.read_csv("../Data/Production/%s/%s.csv" % (estado, planta), index_col=0)  # production info
    cfrecords = pd.read_csv("capacityFactorAD.csv")

    column  = cfrecords.columns.values[0]
    di = cfrecords.columns.values[3]
    t = cfrecords.columns.values[4]
    h = cfrecords.columns.values[5]
    index_planta =  cfrecords[cfrecords[column] == planta].index.tolist()
    anios = cfrecords.loc[index_planta]
    anios =  [anios.year25_percent.values[0],anios.year50_percent.values[0],anios.year75_percent.values[0]]
    for an in anios:
        k = get_anio(an)
        c_up = data[k:k+12]
        print c_up

close_up()

