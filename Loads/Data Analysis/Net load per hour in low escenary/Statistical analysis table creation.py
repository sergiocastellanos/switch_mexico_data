
# coding: utf-8

# In[1]:

import pandas as pd
import random
import numpy as np
def nearest_value(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx


# In[2]:

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


# In[17]:

columns =[df.columns.tolist(),['PeakDay','PeakValue','MonthlyAverage']]
col = pd.MultiIndex.from_product(columns)
dfp=pd.DataFrame(index=pd.MultiIndex.from_tuples(df.xs([1,1],level=[2,3]).index.tolist()),columns=col)
dfp
for k in df.columns.tolist():
    for a in range(2016,2031):
        for m in range (1,13):
            dfp.xs([a,m])[k,'PeakDay']=df.xs([a,m])[k].idxmax()[0]
            dfp.xs([a,m])[k,'PeakValue']=df.xs([a,m])[k].max()
            dfp.xs([a,m])[k,'MonthlyAverage']=(df.xs([a,m])[k].sum()-dfp.xs([a,m])[k,'PeakValue'])/(len(df.xs([a,m])[k])-1)


# In[20]:

df.to_csv("OrganizedTables/HourlyLoadPerNode.csv")
dfp.to_csv("OrganizedTables/LoadHighlightsPerNode.csv")


# In[ ]:




# In[15]:




# In[ ]:




# In[16]:




# In[15]:




# In[ ]:



