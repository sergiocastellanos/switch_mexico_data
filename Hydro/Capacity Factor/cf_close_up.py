import pandas as pd
import sys
import random
import csv
import os



percentile_25= [2013,2009,2007]
percentile_50= [2006,2012,2015]
percentile_75 = [2010,2011,2008,2014]


header = ["name_switch","name_prodesen","load_zone","load_area","timestamp","capacity_factor"]
class capacity_factor:
    def __init__(self):
        self.date = ["01-31","02-29","03-31","04-30","05-31","06-30","07-31","08-31","09-30","10-31","11-30","12-31"]
        self.a0 = 0
        self.a1 = 0
        self.a2 = 0

    def storeresults(self):
        with open(r"meaty_data.csv", "wb") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                 quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(header)

            with open("load_area.csv") as csvfile:
                for line in csv.reader(csvfile):
                    if line[0] == "name_switch":pass
                    else:
                        planta = line[0]
                        percentiles = self.close_up(planta)
                        dates = [str(self.a0),str(self.a1),str(self.a2)]
                        for i,e in enumerate(percentiles): # chacamovement
                            for il,el in enumerate(e):
                                row = line[0],line[1],line[2],line[3],dates[i]+"-"+str(self.date[il]),"%6f"%el                       #print "row"
                                spamwriter.writerow(row)



    def get_anio(self,data,anio):
        dates = data.index.values
        for i,e in enumerate(dates):
            if e[:4] == str(anio):
                return i



    def capacityFactor(self,data, mw):

        #print "MW:    ",mw
        lista = [0,0,0,0,0,0,0,0,0,0,0,0]
        for i,e in enumerate(data):
            lista[i] = (e/(720*mw))*100

        return lista


    def close_up(self,planta):
        estados  = os.listdir("../Data/Production")

        for estado in estados:
            try:
                datas = pd.read_csv("../Data/Production/%s/%s.csv" % (estado,planta), index_col=0)  # production info
            except IOError:pass
        effective_capacity = pd.read_csv("../Data/capacidad_efectiva.csv", index_col=0)  # production info
        cfrecords = pd.read_csv("capacityFactorAD.csv") # capacity factors info

        e_c = effective_capacity[[effective_capacity.columns.values[0]]]

        effective_capacity = e_c.loc[planta].tolist()[0]

        self.a0 = percentile_25[random.randint(0, len(percentile_25)-1)]
        self.a1 = percentile_50[random.randint(0, len(percentile_50)-1)]
        self.a2 = percentile_75[random.randint(0, len(percentile_75)-1)]
        anios = [self.a0,self.a1,self.a2]
        print "%15s%35s"%(planta,anios)
        meaty_data = []
        for an in anios:
            k = self.get_anio(datas,an)
            c_up = datas[k:k+12]
            c_up = c_up[[c_up.columns.values[0]]]
            lista = []
            for i in range(12):
                a = c_up.loc[ c_up.index.values[i]][0]
                lista.append(a)
            meaty_data.append(self.capacityFactor(lista,effective_capacity))

        return (meaty_data[0],meaty_data[1],meaty_data[2])





c = capacity_factor()

c.storeresults()







#close_up()
