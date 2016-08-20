
# coding: utf-8

# In[1]:

import pandas as pd
import random
import numpy as np
def nearest_value(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx


# In[14]:

df = pd.read_csv("OrganizedTables/2016.csv",index_col=range(3),header=0)
df['year']=2016
df.set_index('year',append=True,inplace=True)
df=df.reorder_levels(['year', 'month', 'day','hour'])
for i in range(2017,2031):
    a=pd.read_csv("OrganizedTables/{0}.csv".format(i),index_col=range(3),header=0)
    a.columns=df.columns.tolist()
    a['year']=i
    a.set_index('year',append=True,inplace=True)
    a=a.reorder_levels(['year', 'month', 'day','hour'])
    df=df.append(a)
df=df.astype('float64')


# In[16]:

columnas =[df.columns.tolist(),['PeakDay','PeakDayValue','MonthlyAverage']]
col = pd.MultiIndex.from_product(columnas)
dfp=pd.DataFrame(index=pd.MultiIndex.from_tuples(df.xs([1,1],level=[2,3]).index.tolist()),columns=col)
dfp
for k in df.columns.tolist():
    for a in range(2016,2031):
        for m in range (1,13):
            promedio_dias =[] 
            for d in df.xs([a,m,1],level=[0,1,3])['01-hermosillo'].index.tolist():
                promedio_dias.append(float(df.xs([a,m,d],level=range(3))[k].mean()))
            p=max(promedio_dias)
            dfp.xs([a,m])[k,'PeakDay']=promedio_dias.index(p)+1
            dfp.xs([a,m])[k,'PeakDayValue']=p
            dfp.xs([a,m])[k,'MonthlyAverage']=(sum(promedio_dias)-p)/(len(promedio_dias)-1)


# In[17]:

df.to_csv("OrganizedTables/HourlyLoadPerNode.csv")
dfp.to_csv("OrganizedTables/LoadHighlightsPerNode.csv")


# In[ ]:



