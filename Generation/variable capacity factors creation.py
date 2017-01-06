
# coding: utf-8

# In[37]:

import pandas as pd
import numpy as np
df1=pd.read_csv("data/PowerPlantsWithCosts.csv")
df2=df1[df1['gen_tech'].isin(['wind'])]
df2=df2[df2['balancing_area'] != "00-autoabasto"]
df3=df1[df1['gen_tech'].isin(['solar'])]
renewable=df2['project_name'].tolist()+df3['project_name'].tolist()
time=pd.read_csv('../Main Tabs/timepoints.tab',sep="\t")
df=pd.DataFrame(index=range(time.shape[0]*len(renewable)),columns=['PROJECT','timepoint','proj_max_capacity_factor'])


# In[ ]:

renewable=df2['project_name'].tolist()+df3['project_name'].tolist()
i=0
for name in renewable:
    print renewable.index(name)
    df4=pd.read_csv('data/renewable simulations/{0}.csv'.format(name),index_col=range(3))
    df.loc[range(renewable.index(name)*time.shape[0],((renewable.index(name)+1)*time.shape[0])),'PROJECT']=name
    for index, row in time.iterrows():
        date=str(row['timestamp'])
        i=index + renewable.index(name)*time.shape[0]
        df.loc[i,'timepoint']=index
        df.loc[i,'proj_max_capacity_factor']=df4.loc[(int(date[4:6]),int(date[6:8]),int(date[8:10])),'capacity_factor']


# In[43]:
df.to_csv('../Main Tabs/variable_capacity_factors.tab',sep="\t",index=False)


# In[ ]:




# In[ ]:



