import pandas as pd
import sys
import random
import csv



percentile_25= [2013,2009,2007]
percentile_50= [2006,2012,2015]
percentile_75 = [2010,2011,2008,2014]

estado = "chiapas"
planta = "malpaso"

data = pd.read_csv("../Data/Production/%s/%s.csv"%(estado,planta),index_col=0)#production info



header = "name_switch,name_prodesen,load_zone,load_area,percentile_25,percentile_50,percentile_75"
print header
def storeresults():
    with open(r"meaty_data.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(header)
        with open("load_area.csv") as csvfile:
            for line in csv.reader(csvfile):
                percentile_25,percentile_50,percentile_75 = close_up()
                for i,e in enumerate(percentile_25): # chacamovement
                        row = str(line[0]),",",str(line[1]),",",str(line[2]),",",str(line[3]),",",str(percentile_25[i]),",",str(percentile_50[i]),","+str(percentile_75[i])
                        print row
                        spamwriter.writerow([row])








def get_anio(anio):
    dates = data.index.values
    for i,e in enumerate(dates):
        if e[:4] == str(anio):
            return i



def capacityFactor(data, mw):
    lista = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i,e in enumerate(data):
        lista[i] = e/(720*mw)*100
    return lista


def close_up():
    data = pd.read_csv("../Data/Production/%s/%s.csv" % (estado, planta), index_col=0)  # production info
    effective_capacity = pd.read_csv("../Data/capacidad_efectiva.csv", index_col=0)  # production info
    cfrecords = pd.read_csv("capacityFactorAD.csv") # capacity factors info
    e_c = effective_capacity[[effective_capacity.columns.values[0]]]
    effective_capacity = e_c.loc[e_c.index.values[0]].tolist()[0]
    a0 = percentile_25[random.randint(0, len(percentile_25)-1)]
    a1 = percentile_50[random.randint(0, len(percentile_50)-1)]
    a2 = percentile_75[random.randint(0, len(percentile_75)-1)]
    anios = [a0,a1,a2]
    meaty_data = []
    for an in anios:
        k = get_anio(an)
        c_up = data[k:k+12]
        c_up = c_up[[c_up.columns.values[0]]]
        lista = []
        for i in range(12):
            a = c_up.loc[ c_up.index.values[i]][0]
            lista.append(a)
        meaty_data.append(capacityFactor(lista,effective_capacity))
    return (meaty_data[0],meaty_data[1],meaty_data[2])


storeresults()







#close_up()
