
# coding: utf-8

# In[13]:

#another fuel cost table created, based on data from the piirce. Check documentation for further reference
import pandas as pd
import numpy as np
df1=pd.read_csv("tables/PiircePowerPlantsUsingFuel.csv",header=0,index_col=[6,3])
df2=pd.read_csv("tables/PiirceFuels.csv",header=0,usecols=range(3),index_col=range(2),skip_blank_lines=True)
first=df1.index.levels[0].tolist()[0]
c=pd.DataFrame(index=pd.MultiIndex.from_product([[first],set(list(df1.xs([first]).index.tolist())),range(2016,2031)]),columns=['fuel_cost'])
for f in c.index.levels[1].tolist():
    fclist=list(set(df1.xs([first,f])['fuel_code'].tolist()))
    for a in range(2016,2031):
        c.xs([first,f,a])['fuel_cost']=df2.ix[[(x,a) for x in fclist]].mean().astype('float64')['cost']
for k in df1.index.levels[0].tolist()[1:]:
    print list(set(df1.xs([k]).index.tolist()))
    b=pd.DataFrame(index=pd.MultiIndex.from_product([[k],list(set(df1.xs([k]).index.tolist())),range(2016,2031)]),columns=['fuel_cost'])
    for f in b.index.levels[1].tolist():
        fclist=list(set(df1.xs([k,f])['fuel_code'].tolist()))
        print fclist
        for a in range(2016,2031):
            print df2.ix[[(x,a) for x in fclist]]
            b.xs([k,f,a])['fuel_cost']=df2.ix[[(x,a) for x in fclist]].mean().astype('float64')['cost']
    c=c.append(b)


# In[15]:

c.index.names=['load_area','fuel','year']
c.to_csv('tables/fuel_costs_load_area_details.csv')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



