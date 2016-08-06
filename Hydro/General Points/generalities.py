import sys
from termcolor import colored
usage = "You must type : python %s [state]"
info = "Check the 'Data/Production-Drought-Precipitation' folder for more info."
if len(sys.argv) != 2:
    print >> sys.stderr, \
    colored(usage % sys.argv[0], "yellow")
    print >> sys.stderr, \
    colored(info, "white")
    sys.exit(1)

import pandas as pd
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt







content = os.listdir("../Data/Production-Drought-Precipitation") # returns list
printG = "Planta,25%,50%,75%,Year25%,Year50%,Year75%"
def annual(element):
    ent = os.listdir("../Data/Precipitation/%s"%element)
    d = {}
    e = ent[0]
    for e in ent:
        lista= []
        for i in range(0,120,12):
            data = pd.read_csv("../Data/Precipitation/%s/%s"%(element,e),index_col=0)
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
    showPlot(sys.argv[1])
