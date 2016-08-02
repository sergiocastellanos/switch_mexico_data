import forecastio
import datetime
import json, pickle
from stats import Statistics as stats
from termcolor import colored
from production import Order

seasonlist = ["Winter","Spring","Summer","Autumn"]
mediaChico = 2024.4
import csv

class PrecipAccumulation:
    def retrieveCSV(self):
        '''Opens a .csv file and returns a dictionary'''
        data = {}
        for year in range(2006,2016):
             with open('precipAccCSV/%s.csv'%year, 'rb') as csvfile:
                 reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                 for row in reader:
                     if row[0] == "CHIAPAS":
                         precip = row[1:13]
             data[year] = precip
        return data

    def data(self,entidad,average):
        '''Opens a .csv file and returns a dictionary'''
        data = {}
        devst = []
        for year in range(2006,2016):
             with open('precipAccCSV/%s.csv'%year, 'rb') as csvfile:
                 reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                 for row in reader:
                     if row[0] == entidad.upper():
                         precip = row[13]
             data[year] = precip
             devst.append(float(precip))

        s = stats(devst).deviation()

        #average = 2024.4 #------------------------------------------------------help
        damp = max(devst)
        ave = min(devst, key=lambda x:abs(x-average))

        drought = min(devst)

        ivd = dict((v, k) for k, v in data.items())
        results = {}
        results["drought"] = ivd[str(drought).replace(".0","")]
        results["ave"] = ivd[str(ave).replace(".0","")]
        results["damp"] = ivd[str(damp).replace(".0","")]
        return data, results

def printer(data):
    '''this function prints all the results of the precipAccumulation levels classified by season'''
    for element in data:
        print colored(element,color="magenta")
        for e in data[element]:
            print colored(e, color="white"), colored("%.5s"%data[element][e],color="cyan")


if __name__ == '__main__':
    p = PrecipAccumulation()
    #for e in p.ux():
    #    s = stats(p.ux()[e]).media()
    #    print s


    printer(p.retrieveCSV())
    #p.data("chiapas",2400)

    #printer(p.retrieveCSV())
    p.data("colima")
