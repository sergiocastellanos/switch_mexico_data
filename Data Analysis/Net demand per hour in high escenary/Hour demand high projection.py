
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().magic(u'matplotlib inline')


# In[2]:

df = pd.read_csv("2016.csv",index_col=range(4),skiprows=range(4),header=0)
y=['CEL', 'ORI', 'OCC', 'NOR', 'NTE', 'NES', 'PEN', 'BCN', 'Unnamed: 12', 'BCS', 'MUG', 'SIN', 'SIN8', 'SIN9', 'SEN', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 27', 'Unnamed: 33', 'Unnamed: 43','Central', 'Unnamed: 54',   'Unnamed: 64', 'Unnamed: 70',  'Unnamed: 75']

for i in range(2017,2031):
    a=pd.read_csv("{0}.csv".format(i),index_col=range(4),skiprows=range(4),header=0,skipfooter=24)
    a=a.drop(y,axis=1)
    a.columns=df.columns.tolist()
    df=df.append(a)
df=df.astype('float64')


# In[4]:

for index, k in enumerate(df.columns.tolist()):
    
    plt.figure(index,figsize=(10,7),dpi = 200)
    
    data1=[]
    for a in range(2016,2031):
        try: f=df.xs(a,level=0)[k]
        except ValueError: print "{0},{1},{2}".format(a,m,d)
        yy=[]
        for m in range(1,13):
            for d in range(1,32):
                try: yy.append(f.xs([m,d],level=[0,1]).mean())
                except KeyError: yy.append(0)
                
        
        color =[np.random.rand(3)]*372
        plt.scatter(range(1,373), yy, s=20, c=color, alpha=0.5,label='{0}'.format(a))
    plt.xticks([15,105,195,285], ['Enero','Mayo','Julio','Octubre'], rotation='vertical')
    name='Variacion anual escenario alto en nodo {0}'.format(k)
    plt.ylabel('Demanda')
    plt.title(name)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


# In[5]:

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
print dfp


# In[30]:

get_ipython().magic(u'matplotlib inline')
plt.figure(1,figsize=(10,8),dpi = 200)
ano=2027
mes=12
for d in df.xs([ano,mes,1],level=[0,1,3])['Mexicali'].index.tolist():
    yy=[]
    for h in range(1,25):
        yy.append(df.xs([ano,mes,d,h])['Mexicali'])
    plt.scatter(range(1,25),yy,s=40,c=[np.random.rand(3)]*24,alpha=.6,label='{0}'.format(d))
name='Variacion diaria Mexicali en {0},{1}'.format(ano,mes)

plt.ylabel('Demanda')
plt.title(name)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# In[22]:

import bokeh.mpl as bk
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
show(bk.to_bokeh(plt.figure(1)))


# In[ ]:



