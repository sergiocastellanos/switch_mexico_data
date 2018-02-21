
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
area=pd.read_csv("tables/BalancingAreas.csv",index_col=0)
names=pd.read_csv('tables/Fuels.csv',usecols=[3],header=0)
names=names.dropna()
fuel_types=[]
for i in names['Name2'].tolist():
    fuel_types.append(i[0:i.index(';')].lower())
fuel_types=list(set(fuel_types))
fdict={}
for i in fuel_types:
    fdict[i]=pd.read_excel("tables/FuelsAnalysis.xlsx",sheetname=i,header=range(2),index_col=0)


# In[3]:

names=names.dropna()
fuel_types=[]
for i in names['Name2'].tolist():
    fuel_types.append(i[0:i.index(';')].lower())
fuel_types=list(set(fuel_types))
dfi=pd.DataFrame(index=pd.MultiIndex.from_product([area.index.tolist(),fuel_types,range(2016,2031)]),columns=['fuel_price'])
dfi.index.names=['load_area',"fuel",'year']
for k in area.index.tolist():
    for f in fuel_types:
        for a in range(2016,2031):
            try: dfi.xs([k,f,a])['fuel_price']=fdict[f].loc[a,area.loc[k,'balancing_area']].mean()
            except KeyError: dfi.xs([k,f,a])['fuel_price']=fdict[f].loc[a,:].mean()
            
        


# In[4]:

dfi.to_csv("tables/fuels_cost_balancing_areas_average.csv")



# In[ ]:




# In[ ]:




# In[ ]:



