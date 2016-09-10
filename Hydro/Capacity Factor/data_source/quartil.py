
import csv
import os
import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib as mpl
import pickle
import numpy as np
import datetime as dt
import sys


archivo = open("dataset.pkl")   #open a pickle file that contains data reated to each hydro station and its production from 2006 to 20015
arch = pickle.load(archivo)     #store the data into a arch variable
archivo.close()                 #closes the aforementioned file
years =['2006', '2007', '2008', '2009','2010', '2011', '2012', '2013','2014', '2015'] #initialize a list containing the years that may be iterated


def ave_of_ave():
    '''This function iterates over a dictionary that contain every hydro stations and their production from 2006 to 2015 and returns a list of averages per year'''
    aves = [[],[],[],[],[],[],[],[],[],[]] #initialize a list of lists it will contain every production data ordered by year there are 10 lists due there are 10 years to operete over
    #the next loop place all the data of the power station ordered by year, i,e. all 2006 of each hydro-station data will be together in a list
    for element in arch: #iterates over the aforementioned dictionary (the one extracted from the pickle)
        for i,e in enumerate(arch[element]): # extracts the list that contains the production of the power station
            aves[i].append(arch[element][i]) #fullfill a list (aves) in order to place all the production of the year together
    averages = [] #Initialize a list
    for i,e in enumerate(aves): #iterates over 'aves' ( the list of lists that contains all production of every hydro station ordered by year)
        aves[i] = [x for x in aves[i] if x != 'nan' and x > 0] # take out zeros and nan values
        averages.append(sum(aves[i])/len(aves[i])) # get the average per year it will return 10 averages, one for 2006, another for 2007 and so and so
    return averages #return the data


def allx():
    '''This function oparates over a list of averages and return the percentiles of the set, it will show which year was the mendian as well as which one was the 25 percentile and the 75 percentile'''
    data = pd.DataFrame({'year':years, 'aves_of_aves':ave_of_ave()}) #creates a data frame that will contain two columns one for years and another for the realted average (production)
    d = data['aves_of_aves'] #get the averages
    qs, bins = pd.qcut(d,[.25, .5, .75], retbins=True) #oparates over the averages and get the percentiles
    dfList = data['aves_of_aves'].tolist() #creates a list that contain the average
    d0 = min(dfList, key=lambda x:abs(x-bins[0])) #calculate which of the values of this list is closer to the percentile 25
    d1 = min(dfList, key=lambda x:abs(x-bins[1])) #calculate which of the values of this list is closer to the percentile 50
    d2 = min(dfList, key=lambda x:abs(x-bins[2])) #calculate which of the values of this list is closer to the percentile 75
    dato0 = data[data['aves_of_aves'] == d0].index.tolist() # get the index of the closer value
    year0 = data.loc[dato0] # get the year of the closest value
    year0 = year0.year.values[0] #get the raw value i,e. 2006
    dato1 = data[data['aves_of_aves'] == d1].index.tolist() #idem
    year1 = data.loc[dato1] #idem
    year1 = year1.year.values[0]#idem
    dato2 = data[data['aves_of_aves'] == d2].index.tolist()#idem
    year2 = data.loc[dato2]#idem
    year2 = year2.year.values[0]
    #print str(en[:len(en)-4])+","+str(bins[0])+","+str(bins[1])+","+str(bins[2])+","+str(year0)+","+str(year1)+","+str(year2)
    years = [year0,year1,year2] #creates a list of the 25, 50 and 50 percentiles
    gen = [d0,d1,d2] # creates a list withe production values
    fact = ["dry","medium","wet"] #creates a list of the representative values
    results = pd.DataFrame({'Type':fact,'Year':years, 'Generation':gen}) #creates a data frame with the aforementioned values
    results.to_csv("results.csv") #store the dataframe to a csv
    print  #print the dataframe


#allx()


def plotAves():
    '''This function plots the results'''
    data = pd.DataFrame({'year':years, 'aves_of_aves':ave_of_ave()})
    d = data['aves_of_aves']
    qs, bins = pd.qcut(d,[.25, .5, .75], retbins=True)
    print data.columns.values[0]
    fig, ax = plt.subplots()
    fig.canvas.draw()
    ax.set_xticklabels(years)
    plt.plot(years, data[data.columns.values[0]], marker='o', linestyle='-')
    plt.axhline(y=bins[0],linestyle='--', color='g', label="percentil_25")
    plt.axhline(y=bins[1],linestyle='--', color='c', label="percentil_50")
    plt.axhline(y=bins[2],linestyle='--', color='m', label="percentil_75")
    plt.xlabel('Time')
    plt.ylabel('Net Generation [MW/h]')
    plt.title('Net Generation')
    plt.legend()
    plt.show()


#plotAves()

#content = os.listdir("../Data/Production-Drought-Precipitation") # returns list
#printG = "Planta,percentil_25,percentil_50,percentil_75,year_percentil_25,year_percentil_50,year_percentil_75"

def historical():
    with open(r"capacityFactor.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(printG)
        for element in content:

            ent = os.listdir("../Data/Production/%s"%element)
            for en in ent:
                print en
                try:
                    data = pd.read_csv("../Data/Production/%s/%s"%(element,en),index_col=0)
                    dato = str(data.columns.values[0])
                    data[data == 0] = None
                    qs, bins = pd.qcut(data,[.25, .5, .75], retbins=True)
                    print bins[0], bins[1],bins[2]
                    dfList = data[dato].tolist()
                    dato0 = min(dfList, key=lambda x:abs(x-bins[0]))
                    dato1 = min(dfList, key=lambda x:abs(x-bins[1]))
                    dato2 = min(dfList, key=lambda x:abs(x-bins[2]))
                    dato0 = data[data[dato] == dato0].index.tolist()
                    dato1 = data[data[dato] == dato1].index.tolist()
                    dato2 = data[data[dato] == dato2].index.tolist()
                    print dato0, dato1, dato2
                    #print pd.Series(bins, index=['Production_25', 'Production_50', 'Production_75'])
                    row = str(en[:len(en)-4])+","+str(bins[0])+","+str(bins[1])+","+str(bins[2])+","+str(dato0[0][:4])+","+str(dato1[0][:4])+","+str(dato2[0][:4])
                    spamwriter.writerow([row])
                except (ValueError, IndexError):
                    pass

def annual():
    with open(r"capacityFactorAD.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(printG)
        for element in content:
            ent = os.listdir("../Data/Production/%s"%element)
            for en in ent:
                #print en
                try:
                    lista= []
                    for i in range(0,120,12):
                        data = pd.read_csv("../Data/Production/%s/%s"%(element,en),index_col=0)
                        data =  data[i:i+12]
                        column = data.columns.values[0]
                        lista.append(data[column].mean())
                    data = pd.DataFrame({'year':years, 'Production-Ave':lista})
                    d= data['Production-Ave']
                    qs, bins = pd.qcut(d,[.25, .5, .75], retbins=True)
                    dfList = data['Production-Ave'].tolist()
                    dato0 = min(dfList, key=lambda x:abs(x-bins[0]))
                    dato1 = min(dfList, key=lambda x:abs(x-bins[1]))
                    dato2 = min(dfList, key=lambda x:abs(x-bins[2]))
                    dato0 = data[data['Production-Ave'] == dato0].index.tolist()
                    year0 = data.loc[dato0]
                    year0 = year0.year.values[0]
                    dato1 = data[data['Production-Ave'] == dato1].index.tolist()
                    year1 = data.loc[dato1]
                    year1 = year1.year.values[0]
                    dato2 = data[data['Production-Ave'] == dato2].index.tolist()
                    year2 = data.loc[dato2]
                    year2 = year2.year.values[0]
                    #print str(en[:len(en)-4])+","+str(bins[0])+","+str(bins[1])+","+str(bins[2])+","+str(year0)+","+str(year1)+","+str(year2)
                    row = str(en[:len(en)-4])+","+str(bins[0])+","+str(bins[1])+","+str(bins[2])+","+str(year0)+","+str(year1)+","+str(year2)
                    spamwriter.writerow([row])
                except (ValueError, IndexError):
                    pass


def plotC(element,en):
    lista = []
    for i in range(0,120,12):
        data = pd.read_csv("../Data/Production/%s/%s.csv"%(element,en),index_col=0)
        data =  data[i:i+12]
        column = data.columns.values[0]
        lista.append(data[column].mean())
    years =['2006', '2007', '2008', '2009','2010', '2011', '2012', '2013','2014', '2015']
    data = pd.DataFrame({'year':years, 'Production-Ave':lista})

    d= data['Production-Ave']
    #print d
    qs, bins = pd.qcut(d,[.25, .5, .75], retbins=True)

    print data.columns.values[0]
    fig, ax = plt.subplots()
    fig.canvas.draw()
    years =['2006', '2007', '2008', '2009','2010', '2011', '2012', '2013','2014', '2015']
    ax.set_xticklabels(years)
    plt.plot(years, data[data.columns.values[0]], marker='o', linestyle='-')
    plt.axhline(y=bins[0],linestyle='--', color='g', label="percentil_25")
    plt.axhline(y=bins[1],linestyle='--', color='c', label="percentil_50")
    plt.axhline(y=bins[2],linestyle='--', color='m', label="percentil_75")
    plt.xlabel('Time')
    plt.ylabel('Net Generation [MW/h]')
    plt.title('Net Generation')
    plt.legend()
    plt.show()

# plotC(sys.argv[1],sys.argv[2])
# annual()
