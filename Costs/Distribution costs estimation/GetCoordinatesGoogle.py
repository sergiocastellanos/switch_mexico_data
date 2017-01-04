
# coding: utf-8

# In[1]:

import sys
import pandas as pd
import numpy as np
import geocoder 
df1=pd.read_csv("tables/Counties.csv",skiprows=5,usecols=[2,3])
df1=df1.dropna()
#droping the "Otros municipios" county listed in INEGI's list.
df1=df1.drop(198)
#correct encoding problems in the table caused by special characters
for index in df1.index.tolist():
    df1.loc[index,'County']=df1.loc[index,'County'].replace("\xf1","n")
    df1.loc[index,'County']=df1.loc[index,'County'].replace("\xfc","u")


# In[2]:

for index,rows in df1.iterrows():
    loc="{0}, {1}".format(str(rows['County']),str(rows['State']))
    g=geocoder.google(loc)
    df1.loc[index,'lat']=g.lat
    df1.loc[index,'lon']=g.lng


# In[ ]:




# In[3]:

df2=df1[df1.isnull().any(axis=1)]


# In[4]:

for index in df2.index.tolist():
    loc="{0}, {1}".format(str(rows['County']),str(rows['State']))
    g=geocoder.google(loc)
    df1.loc[index,'lat']=g.lat
    df1.loc[index,'lon']=g.lng


# In[ ]:




# In[13]:

df1['County']=df1['County'].str.replace("\xfc","u")
df1['County']=df1['County'].str.replace("\xf1","n")
df1.to_csv('tables/CountiesCoordinatesGoogle.csv',index=False)


# In[ ]:




# In[ ]:



