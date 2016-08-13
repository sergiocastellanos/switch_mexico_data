import pandas as pd

import os

import matplotlib

import pickle
#import matplotlib.pyplot as plt


content = os.listdir("../Data/Production-Drought-Precipitation") # returns list
printG = "Planta,25%,50%,75%,Year25%,Year50%,Year75%"

def historical():
    d = {}
    content = os.listdir("../Data/Production-Drought-Precipitation")
    print content
    for element in content:
        ent = os.listdir("../Data/Production/%s"%element)

        e = ent[0]
        for e in ent:
            lista= []
            for i in range(0,120,12):
                data = pd.read_csv("../Data/Production/%s/%s"%(element,e),index_col=0)
                data =  data[i:i+12]
                column = data.columns.values[0]
                anio = data.index.values[0][:4]
                lista.append(data[column].mean())
            d[e] = lista
    output = open('dataset.pkl', 'wb')
    pickle.dump(d, output)
    output.close()
    return d





def annual(element):

    ent = os.listdir("../Data/Production/%s"%element)
    d = {}
    e = ent[0]
    for e in ent:
        lista= []
        for i in range(0,120,12):
            data = pd.read_csv("../Data/Production/%s/%s"%(element,e),index_col=0)
            data =  data[i:i+12]
            column = data.columns.values[0]
            anio = data.index.values[0][:4]
            lista.append(data[column].mean())
        d[e] = lista
    return d



def showPlot(state):
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
    print historical()
    #showPlot(sys.argv[1])
