import pickle

import pandas
from production import Order
from stats import Statistics as s
from precipAccumulation import PrecipAccumulation
import csv
import collections
import datetime
import os
import pickle



content = os.listdir("plantas/Drought-Production")

metadata = pandas.read_excel("data/production/plantas.xlsx",index_col="Plantas")
plantas = metadata.index.values
o = Order()
with open(r"data/drought/monitorSequia/msequia.pkl", "rb") as input_file:
    drought = pickle.load(input_file)
#print drought
printG = "Date,Production,DroughtLevel,Precipitation"
import os
content = os.listdir("plantas/Production") # returns list


with open(r"CorrelationResults/globals.csv", "wb") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                         quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(printG)
    for element in content:
        ent = os.listdir("plantas/Production/%s"%element)
        for en in ent:
            print element, en
            with open(r"plantas/Production/%s/%s"%(element,en), "rb") as input_file:
                production = pickle.load(input_file)

            with open(r"plantas/Precipitation/%s.pkl"%element[2:], "rb") as input_file:
                precipitation = pickle.load(input_file)

            production = collections.OrderedDict(sorted(production.items()))
            precipitation = collections.OrderedDict(sorted(precipitation.items()))

            for year in range(2006,2016):
                cont = 0

                for month in range(01,13):
                    try:
                        lele = datetime.date(year,month,31)
                    except ValueError:
                        try:
                            lele = datetime.date(year,month,30)
                        except ValueError:
                            try:
                                lele = datetime.date(year,month,29)
                            except ValueError:
                                lele = datetime.date(year,month,28)

                    try:

                        row = str(lele)+","+str(production[str(year)][cont])+","+str(drought[int(element[:2])][year][month-1])+","+str(precipitation[year][cont])
                        print row
                    except IndexError:

                        row = str(lele)+","+str(0)+","+str(drought[int(element[:2])][year][month-1])+","+str(precipitation[year][cont])
                    spamwriter.writerow([row])
                    cont+=1


#metadata = pandas.read_csv("sequia.csv")

#print metadata




# print content
# from precipAccumulation import PrecipAccumulation as pacc
# for element in content:
#     print element
#     precipitation = pacc().retrieveCSV(element)                                            #precipitacion
#     output = open('plantas/Precipitation/%s.pkl'%(element), 'wb')
#     pickle.dump(precipitation, output)
#     output.close()
#
#
#
