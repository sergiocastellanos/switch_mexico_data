
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import random 
from sqlalchemy import create_engine
engine=create_engine('postgresql://sayeg:edema7-Warbled@127.0.0.1:5433/switch_mexico')
#importing data from our tables
df=pd.read_csv("tables/HourlyLoadPerNode.csv",index_col=range(4))
dfp=pd.read_csv("tables/LoadHighlightsPerNode.csv",index_col=range(2),header=range(2))


# In[2]:

#Creating a new dataframe for Median and Peak day dates and values
col=[df.columns.tolist(),['MedianDay','MedianDayValues','PeakDay','PeakDayValues']]
indx=[range(2016,2031),range(1,13)]
dfs=pd.DataFrame(index=pd.MultiIndex.from_product(indx),columns=pd.MultiIndex.from_product(col))


# In[48]:

#searching for the median and peak days of every node at each year and month
for k in df.columns.tolist():
    for a in range(2016,2031):
        for m in range(1,13):
            zz=[]
            for d in df.xs([a,m,1],level=[0,1,3])[k].index.tolist():
                zz.append(df.xs([a,m,d],level=range(3))[k].mean())

    
            if len(zz)%2 ==1:
                median = np.median(np.array(zz))
                indx_median = zz.index(median)
            else:
                n=np.random.randint(len(zz))
                median = np.median(zz[-n])
                indx_median = zz.index(median)
                if indx_median>= n:
                    indx_median= indx_median+1
            dfs.xs([a,m])[k,'MedianDay']=str(indx_median).zfill(2)
            dfs.xs([a,m])[k,'MedianDayValues']=df.xs([a,m,indx_median],level=range(3))[k].tolist()
            dfs.xs([a,m])[k,'PeakDay']=str(dfp.xs([a,m])[k,'PeakDay']).zfill(2)
            dfs.xs([a,m])[k,'PeakDayValues']=df.xs([a,m,dfp.xs([a,m])[k,'PeakDay']],level=range(3))[k].tolist()


# In[62]:

#Create a new dataframe to exoport into the tab file used in SWITCH
col=["load_area",'hour','load_mw']
indx=[df.columns.tolist(),range(2016,2031),range(1,13),range(2),range(12)]
#the "range(2)" part of the multindex is for selecting peak day (0) and median day (1)"
export=pd.DataFrame(index=pd.MultiIndex.from_product(indx),columns =col)
for k in df.columns.tolist():
    for a in range(2016,2031):
        for m in range(1,13):
             for h in range(1,13):
                export.xs([k,a,m,0,h%12])["load_area"]=k
                export.xs([k,a,m,1,h%12])["load_area"]=k
                export.xs([k,a,m,0,h%12])["hour"]="{0}{1}{2}{3}".format(a,str(m).zfill(2),dfs.xs([a,m])[k,'PeakDay'][0:dfs.xs([a,m])[k,'PeakDay'].index(".")].zfill(2),str((h*2)%24).zfill(2))
                export.xs([k,a,m,1,h%12])["hour"]="{0}{1}{2}{3}".format(a,str(m).zfill(2),str(dfs.xs([a,m])[k,'MedianDay']).zfill(2),str(((h*2)%24)+1).zfill(2))
                export.xs([k,a,m,0,h%12])["load_mw"]=dfs.xs([a,m])[k,'PeakDayValues'][((h*2) -1)]
                export.xs([k,a,m,1,h%12])["load_mw"]=dfs.xs([a,m])[k,'MedianDayValues'][(h*2)%24]
            
export.index=export["load_area"].tolist()
export.index.name="load_area"
export=export.drop('load_area',axis=1)
    


# In[ ]:

export.to_csv('tables/la_hourly_demand_high.csv')
export.to_sql('la_hourly_demand_high',engine,schema='mexico',if_exists='replace',chunksize=10000)


# In[ ]:




# In[ ]:



