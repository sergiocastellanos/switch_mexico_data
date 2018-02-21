
# coding: utf-8

# In[2]:

#distribution cost estimation. For further detail, check the report on this directory
import pandas as pd
import numpy as np
dfs=pd.read_csv("tables/CategorizedCounties.csv")
'''The calculations of each of the distribution cost estimates 
is made using a simplified version of the formulas contained in the report
for improving performance and for asuring none of our variables becomes cero (as some of them are really small)'''
annual_cost=1872.5
for c in dfs.index.tolist():
    dfs.set_value(c,"DistributionCost2 (millions of MXN)", dfs.loc[c,"real state with electricity"].astype("int64")*annual_cost/(3*dfs["real state with electricity"].astype('int64').sum())+dfs.loc[c,"land area (km^2)"].astype("int64")*annual_cost/(dfs["land area (km^2)"].astype('int64').sum()*3))

    if str(dfs.loc[c,'county type'])=="urban":
        dfs.set_value(c,'DistributionCost1 (millions of MXN)',dfs.loc[c,'land area (km^2)'].astype("float64")*.5*.003+dfs.loc[c,"real state with electricity"].astype("int64")*.005*.003 + dfs.loc[c,"real state with electricity"].astype("int64")/80 * .035)
    else:
        dfs.set_value(c,'DistributionCost1 (millions of MXN)',dfs.loc[c,'land area (km^2)'].astype("float64")*1*.005+dfs.loc[c,"real state with electricity"].astype("int64")*.05*.005 + dfs.loc[c,"real state with electricity"].astype("int64")/40 *.025)
    dfs.set_value(c,"diference of estimation (millions of MXN)",abs(dfs.loc[c,'DistributionCost1 (millions of MXN)']-dfs.loc[c,"DistributionCost2 (millions of MXN)"]))
dfs.to_csv("tables/CategorizedCounties.csv",index=False)


# In[ ]:


# In[ ]:




# In[ ]:




# In[ ]:



