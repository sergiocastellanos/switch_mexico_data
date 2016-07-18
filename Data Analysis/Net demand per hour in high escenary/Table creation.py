
# coding: utf-8

# In[1]:

import pandas as pd
import random
import matplotlib.pyplot as plt
import random
import numpy as np

def nearest_value(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx


# In[2]:

df = pd.read_csv("2016.csv",index_col=range(4),skiprows=range(4),header=0)
y=['CEL', 'ORI', 'OCC', 'NOR', 'NTE', 'NES', 'PEN', 'BCN', 'Unnamed: 12', 'BCS', 'MUG', 'SIN', 'SIN8', 'SIN9', 'SEN', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 27', 'Unnamed: 33', 'Unnamed: 43','Central', 'Unnamed: 54',   'Unnamed: 64', 'Unnamed: 70',  'Unnamed: 75']

for i in range(2017,2031):
    a=pd.read_csv("{0}.csv".format(i),index_col=range(4),skiprows=range(4),header=0,skipfooter=24)
    a=a.drop(y,axis=1)
    a.columns=df.columns.tolist()
    df=df.append(a)
df=df.astype('float64')


# In[7]:

columnas =[df.columns.tolist(),['DiaPico','ValorPico','PromedioMensual']]
col = pd.MultiIndex.from_product(columnas)
dfp=pd.DataFrame(index=pd.MultiIndex.from_tuples(df.xs([1,1],level=[2,3]).index.tolist()),columns=col)
dfp
for k in df.columns.tolist():
    for a in range(2016,2031):
        for m in range (1,13):
            promedio_dias =[] 
            for d in df.xs([a,m,1],level=[0,1,3])['Hermosillo'].index.tolist():
                promedio_dias.append(float(df.xs([a,m,d],level=range(3))[k].mean()))
            p=max(promedio_dias)
            dfp.xs([a,m])[k,'DiaPico']=promedio_dias.index(p)
            dfp.xs([a,m])[k,'ValorPico']=p
            dfp.xs([a,m])[k,'PromedioMensual']=(sum(promedio_dias)-p)/(len(promedio_dias)-1)


# In[8]:

df.to_csv("demand per node.csv")
dfp.to_csv("highlights per node.csv")

