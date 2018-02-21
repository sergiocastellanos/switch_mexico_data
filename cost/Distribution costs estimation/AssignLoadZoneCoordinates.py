
# coding: utf-8

# In[72]:

import pandas as pd
import numpy as np
import geocoder
df1=pd.read_csv('tables/BalancingAreas.csv',index_col=0,header=0)
df1=df1.drop('00-autoabasto_local',axis=0)
df2=pd.read_csv('tables/CountiesCoordinates.csv',header=0)
#setting the name format as we need it
df2['County']=df2['County'].str.replace(" ","_")
df2['County']=df2['County'].str.lower()
df2['County']=df2['County'].str.replace("\xfc","u")
df2['County']=df2['County'].str.replace("\xf1","n")
#selecting the load area names with names that do not match any county and assigning them one
xname={'03-obregon':"cajeme","04-los_mochis":"ahome","11-laguna": 'torreon',"12-rio_escondido":'piedras_negras',"28-carapan":"charapan",'31-central':'coyoacan','32-poza_rica':'poza_rica_de_hidalgo',"35-acapulco":'acapulco_de_juarez',"36-temascal":'oaxaca_de_juarez','39-grijalva':"tuxtla_gutierrez",'44-chetumal':'othon_p._blanco','50-villa_constitucion':"comondu"}
#selecting th load area names with multiple matches and assigning them the right one
yname={"07-juarez":234,"08-moctezuma":1925,"15-matamoros":1998,"18-valles":1824,"19-huasteca":2005,"29-lazaro_cardenas":832,"43-cancun":1807,"51-la_paz":18}


# In[77]:

for index in df1.index.tolist():
    if index in xname.keys():
        df1.loc[index,'lat']=float(df2[df2['County']==xname[index]]['lat'])
        df1.loc[index,'lon']=float(df2[df2['County']==xname[index]]['lon'])
    elif index in yname.keys():
        df1.loc[index,'lat']=float(df2.iloc[yname[index],2])
        df1.loc[index,'lon']=float(df2.iloc[yname[index],3])
    else: 
        df1.loc[index,'lat']=float(df2[df2['County']==index[3:]]['lat'])
        df1.loc[index,'lon']=float(df2[df2['County']==index[3:]]['lon'])


# In[78]:

df1.to_csv('tables/LoadZoneCoordinates.csv')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



