
# coding: utf-8

# In[6]:

import pandas as pd
import numpy as np
df1=pd.read_csv('OrganizedTables/HourlyLoadPerNode.csv',index_col=range(4))
df2=pd.read_csv("../../Main Tabs/timepoints.tab",sep="\t",index_col=0)


# In[39]:

df3=pd.DataFrame()
for lz in df1.columns.tolist():
    print lz
    df4=pd.DataFrame()
    df4['timepoint']=range(df2.shape[0])
    df4['load_zone']=lz
    for i in range(df2.shape[0]):
        t=str(df2.loc[i,'timestamp'])
        df4.loc[i,'lz_demand_mw']=df1.xs([int(t[:4]),int(t[4:6]),int(t[6:8]),int(t[8:])+1])[lz]
    df3=df3.append(df4,ignore_index=True)
df3


# In[40]:

df3.to_csv("../../Main Tabs/loads.tab",sep="\t",index=False)
df3.to_csv("../../Main Tabs/csv/loads.csv",index=False)


# In[ ]:



