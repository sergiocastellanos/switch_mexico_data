import sys
from termcolor import colored
usage = "You must type : python %s [state] [hydroStationName]"
info = "Check the 'Data/Production-Drought-Precipitation' folder for more info."
if len(sys.argv) != 3:
    print >> sys.stderr, \
    colored(usage % sys.argv[0], "yellow")
    print >> sys.stderr, \
    colored(info, "white")
    sys.exit(1)


import pandas
import os
import csv

#content = os.listdir("Production-Drought-Precipitation") # returns list

import matplotlib.pyplot as plt

import matplotlib
matplotlib.style.use('ggplot')

printG = "Station,State,Production-Drought,Production-Precipitation"

def storeresults():
    with open(r"CorrelationResults/CorrelationResults.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(printG)
        for element in content:
            print element
            ent = os.listdir("Production-Drought-Precipitation/%s"%element)
            for en in ent:
                try:
                    print en
                    metadata = pandas.read_csv("Production-Drought-Precipitation/%s/%s"%(element,en))
                    metadata = metadata.corr(method='pearson', min_periods=1)
                    print metadata
                    production =  metadata.columns.values[0]
                    print production
                    metadata = metadata.loc[:production]
                    columns = metadata.columns.values
                    data = metadata[[columns[1],columns[2]]]
                    print data
                    drought = data[[columns[1]]]
                    precipitation = data[[columns[2]]]

                    dindex =  drought.index.values[0]
                    dcol = drought.columns.values[0]
                    drought = drought.get_value(dindex, dcol, takeable=False)

                    pindex =  precipitation.index.values[0]
                    pcol = precipitation.columns.values[0]
                    precipitation = precipitation.get_value(pindex, pcol, takeable=False)

                    print drought, precipitation

                    row = str(en[:len(en)-4])+","+element+","+str(drought)+","+str(precipitation)
                    spamwriter.writerow([row])
                except IndexError:
                    row = str(en[:len(en)-4])+","+element+","+str(0)+","+str(0)
                    spamwriter.writerow([row])


def plotCorrelation(entidad,planta):
    '''Receives a Hydro-station name and returns scatter plots showing both the drought and precipitation levels in order to correlate them with the production of the given hydro station'''
    ma = "0000000000"
    if sys.argv[1] == "global":
        data = pandas.read_csv("CorrelationResults/globals.csv")
    else : data = pandas.read_csv("../Data/Production-Drought-Precipitation/%s/%s.csv"%(entidad,planta))
    production,drought,precip = (data.columns.values[1],data.columns.values[2],data.columns.values[3])
    columns = data.columns.values
    pro = data[[columns[1]]]
    dro = data[[columns[2]]]
    dfList = data[columns[1]].tolist()
    minimum = min(dfList)
    print minimum
    o =  minimum*.18
    m,l = str(minimum).split(".")
    print m
    m = ma[:len(m)]
    print m
    if len(m) > 4:
        o = .0002
        print "mayor que cuatro"
    else: o = .03
    pre = data[[columns[3]]]
    frames = [pro,pre,dro]
    prodro = pandas.concat([pro,dro], axis=1)
    propre = pandas.concat([pro,pre], axis=1)
    precipitacion = pre.columns.values[0]
    production = pro.columns.values[0]
    drought = dro.columns.values[0]

    propre.plot.scatter(subplots=True,x=precipitacion, y=production, label='%s   [MW/h]'%planta, s=propre[production]*o*.01,title="h")
    prodro.plot.scatter(x=drought, y=production, color='DarkGreen', label='%s  [MW/h]'%planta, s=propre[production]*o*.01)


    plt.show()




if __name__ == '__main__':
    plotCorrelation(sys.argv[1],sys.argv[2])


#storeresults()
#
# # data = pandas.read_csv("CorrelationResults/correlationResults.csv",index_col =0)
# print data
