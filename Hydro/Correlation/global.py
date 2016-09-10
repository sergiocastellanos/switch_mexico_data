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


'''This script merge the drought, precipitation and production data into global.csv'''


content = os.listdir("plantas/Drought-Production")#list all the content of the given folder

metadata = pandas.read_excel("data/production/plantas.xlsx",index_col="Plantas")#open the dams (names) data
plantas = metadata.index.values
o = Order()
with open(r"data/drought/monitorSequia/msequia.pkl", "rb") as input_file:#open the drought data
    drought = pickle.load(input_file)

printG = "Date,Production,DroughtLevel,Precipitation"
import os
content = os.listdir("plantas/Production") # returns list


with open(r"CorrelationResults/globals.csv", "wb") as csvfile:#open a file to store data
    spamwriter = csv.writer(csvfile, delimiter=' ',
                         quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(printG)
    for element in content:#iterates over eech element listed on the plantas/Production folder
        ent = os.listdir("plantas/Production/%s"%element)#list the content of the folder
        for en in ent:
            print element, en
            with open(r"plantas/Production/%s/%s"%(element,en), "rb") as input_file:
                production = pickle.load(input_file)#returns the produc data per dam

            with open(r"plantas/Precipitation/%s.pkl"%element[2:], "rb") as input_file:
                precipitation = pickle.load(input_file)# returns the precipitation data of the dams

            production = collections.OrderedDict(sorted(production.items()))#store the data into a coletion
            precipitation = collections.OrderedDict(sorted(precipitation.items()))#store the data into a coletion

            for year in range(2006,2016):#iterates over years
                cont = 0

                for month in range(01,13):#iterates over months
                    try:
                        lele = datetime.date(year,month,31)#convert the the values to valid dates case the month has 31 days
                    except ValueError:
                        try:
                            lele = datetime.date(year,month,30)#convert the the values to valid dates case the month has 30 days
                        except ValueError:
                            try:
                                lele = datetime.date(year,month,29)#convert the the values to valid dates case the month has 29 days
                            except ValueError:
                                lele = datetime.date(year,month,28) #convert the the values to valid dates case the month has 28 days

                    try:

                        row = str(lele)+","+str(production[str(year)][cont])+","+str(drought[int(element[:2])][year][month-1])+","+str(precipitation[year][cont])
                        spamwriter.writerow([row])
                        cont+=1#write the results on the file

                        #print row
                    except IndexError:#catch the error in case that a year is not listed

                        #row = str(lele)+","+str(0)+","+str(drought[int(element[:2])][year][month-1])+","+str(precipitation[year][cont])
                        print "0"
                        pass
                    # spamwriter.writerow([row])
                    # cont+=1


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
