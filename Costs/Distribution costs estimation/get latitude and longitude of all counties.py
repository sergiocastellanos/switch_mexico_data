
# coding: utf-8

# In[16]:

import pandas as pd
import numpy as np
import geocoder
df1=pd.read_csv("tables/Counties.csv",skiprows=5,usecols=[2,3])
df1=df1.dropna()
#droping the "Otros municipios" county listed in INEGI's list.
df1=df1.drop(198)


# In[ ]:

for index,rows in df1.iterrows():
    print index
    loc="{0}, {1}".format(str(rows['County']),str(rows['State']))
    g=geocoder.google(loc)
    df1.loc[index,'lat']=g.lat
    df1.loc[index,'lon']=g.lng


# In[18]:

df1.to_csv("tables/CountiesCoordinates.csv",index=False)


# In[20]:




# In[ ]:

df2

