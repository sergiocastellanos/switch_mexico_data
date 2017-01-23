
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
df1=pd.read_csv('tables/CategorizedCounties.csv',header=0)
df2=pd.read_csv('tables/BalancingAreas.csv',index_col=0,header=0)
df2=df2.drop('00-autoabasto_local')
df3=pd.read_csv('../../Loads/High scenario/OrganizedTables/HourlyLoadPerNode.csv',header=0,index_col=range(4))
df4=pd.read_csv('tables/CountiesLoadZones.csv')


# In[9]:

#df1[df1['load_zone']=='47-ensenada']
df1[df1['county']=='ensenada']


# In[2]:

df=pd.DataFrame(index=df2.index,columns=['lz_cost_multipliers','existing_local_td',"local_td_annual_cost_per_mw"])
df['lz_cost_multipliers']=1
"""we calculate the existing local td as the peak demand 
of that load area multiplied by a factor that compensates 
ditribution loses. 
This factor contemplates that 15% of the energy generated is lost 
during the transmission and distribution."""
for k in df.index.tolist():
    df.loc[k,'existing_local_td']=df3[k].max()*100/85
"""Now we must assign a distribution cost to each load zone
as a first aproach, we will asign the distribution cost of each load area
to the distribution cost of the county where the load area is located 
(for example, the distribution cost of '20-tamazunchale' 
is the distribution cost of the tamazunchale county).
This is not representative as a load area distributes electricity to 
much more counties that the county that gives name to it."""


# In[3]:

for index in df1.index:
    df1.loc[index,'load_zone']=df4.loc[index,'lz']


# In[10]:

for k in df.index:
    if k!='53-mulege': df.loc[k,"local_td_annual_cost_per_mw"]=df1[df1['load_zone']==int(k[0:2])]['DistributionCost2 (millions of MXN)'].sum()
    df.loc['53-mulege','local_td_annual_cost_per_mw']=2
    df.loc['47-ensenada','local_td_annual_cost_per_mw']=float(df1[df1['county']=='ensenada']['DistributionCost2 (millions of MXN)'])
    df.loc[k,'local_td_annual_cost_per_mw']=df.loc[k,'local_td_annual_cost_per_mw']*(10000000/15.8675574)/df.loc[k,'existing_local_td']


# In[12]:

df.to_csv('../../Main Tabs/csv/load_zones.csv')
df.to_csv('../../Main Tabs/load_zones.tab',sep="\t")


# In[ ]:




# In[ ]:



