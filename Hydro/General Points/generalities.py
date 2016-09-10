import pandas as pd

import os

import matplotlib

import pickle
#import matplotlib.pyplot as plt


content = os.listdir("../Data/Production-Drought-Precipitation") # returns list
printG = "Planta,25%,50%,75%,Year25%,Year50%,Year75%"

def historical(): #n^3
    d = {}                                                                                                  #initialize a dictionary
    content = os.listdir("../Data/Production-Drought-Precipitation")                                        #returns a list containing all folder names inside  'http://switch_mexico_data/Hydro/Data/Production-Drought-Precipitation/'
    for element in content:                                                                                 #iterates over the list of folder names each name will be assigned to 'element'
        ent = os.listdir("../Data/Production/%s"%element)                                                   #returns a list containing all folder names inside  'http://switch_mexico_data/Hydro/Data/Production/[element]'
        e = ent[0]
        for e in ent:                                                                                       #iterates over the list of file names each name will be assigned to 'e'
            lista= []
            for i in range(0,120,12):
                data = pd.read_csv("../Data/Production/%s/%s"%(element,e),index_col=0)                      #reads the content of each file and returns a panda data frame
                data =  data[i:i+12]                                                                        #separates the entire table in blocks (one per year)
                column = data.columns.values[0]                                                             #get the entire column
                anio = data.index.values[0][:4]                                                             #get the current yerar
                lista.append(data[column].mean())                                                           #creates a list with the mean of each column
            d[e] = lista                                                                                    #appends the listo to a dictionary (the one at the top of the function)
    output = open('dataset.pkl', 'wb')                                                                      #creates a pkl file to store the dictionary
    pickle.dump(d, output)                                                                                  #stores the data
    output.close()
    return d

def annual(element):#n^2
    ent = os.listdir("../Data/Production/%s"%element)
    d = {}
    e = ent[0]
    for e in ent:
        lista= []
        for i in range(0,120,12):
            data = pd.read_csv("../Data/Production/%s/%s"%(element,e),index_col=0)                          # the same but the state name must be given
            data =  data[i:i+12]
            column = data.columns.values[0]
            anio = data.index.values[0][:4]
            lista.append(data[column].mean())
        d[e] = lista
    return d



def showPlot(state):                                                                                       #creates a plot of a given state (net generation over the years for each dam)
    fig, ax = plt.subplots()
    fig.canvas.draw()
    years =['2006', '2007', '2008', '2009','2010', '2011', '2012', '2013','2014', '2015']
    labels = [item.get_text() for item in ax.get_xticklabels()]
    ax.set_xticklabels(years)
    colors = ["b","g","r","c","m","y","k","w"]
    data  = annual(state)
    for i,e in enumerate(data):
        plt.plot(years, data[e], marker='o', linestyle='-', color=colors[i], label='%s'%e[:len(e)-4])
    plt.xlabel('Time')
    plt.ylabel('Net Generation [MW/h]')
    plt.title('%s Net Generation'%state.capitalize())

    plt.legend()
    plt.show()



if __name__ == '__main__':
    print historical()                                                                                      #executes only the historical function
    #showPlot(sys.argv[1])
