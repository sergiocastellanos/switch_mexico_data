
# coding: utf-8

# In[1]:

#script regarding the creation of the "loads.tab" and "lz_peak_loads"
import pandas as pd
import numpy as np
df=pd.read_csv("OrganizedTables/HourlyLoadPerNode.csv",index_col=range(4),header=0)


# In[2]:

#creation of an axuliary dataframe for the "loads.tab" file with needed columns
a=pd.DataFrame(index=df.index,columns=['load_area','timepoint','lz_demand_tz'])


# In[3]:

#creation of timestamps for the new table
for y in range(2016,2031):
        for m in range(1,13):
            for d in a.xs([y,m,1],level=[0,1,3]).index.tolist():
                for h in range(1,25):
                    a.xs([y,m,d,h])['timepoint']=str(y)+str(m).zfill(2)+str(d).zfill(2)+str(h-1).zfill(2)
time=a['timepoint'].tolist()  
del a


# In[4]:

'''creation of an empty data frame that will receive, by concatenation, 
 a dataframe created for each load zone'''
final=pd.DataFrame()
for k in df.columns.tolist():
    b=pd.DataFrame(index=df.index,columns=['load_area','timepoint','lz_demand_mw'])
    #filling load area column with the load area name
    b['load_area']=k
    #pasting the complete load from that load area to the lz_demand_mw column
    b['lz_demand_mw']=df[k]
    b.set_index('load_area',append=False,inplace=True)
    #paste timestamps in the "timepoint" column
    b['timepoint']=time
    final=final.append(b)


# In[5]:

#Import of the tables to another place
final.to_csv("OrganizedTables/loads_mid.csv")
final.to_csv("../../../Main Tabs/csv/loads_mid.csv")
final.to_csv("../../../Main Tabs/loads_mid.tab",sep='\t')


# In[6]:

#creation of data frame for the "lz_peak_loads file"
c=pd.DataFrame()
for k in df.columns.tolist():
    #creation of temporary dataframe for every load zone
    d=pd.DataFrame(index=range(3),columns=['load_zone','period','peak_demand_mw'])
    #filling the load zone column with load zone name
    d['load_zone']=k
    #iterating over the periods
    for i in range(3):
        #selecting the period day
        d.loc[i,'period']=2016+(i*5)
        #assigning the maximum demand for that period of 5 years to the "peak demand mw"column
        d.loc[i,'peak_demand_mw']=df.loc[[2016+(i*5),2020+i*5],:][k].max()
    #reset the index to the load_zone
    d.set_index('load_zone',append=False,inplace=True)
    c=c.append(d)  


# In[7]:

#import
c.to_csv("OrganizedTables/lz_peak_loads_mid.csv")
c.to_csv("../../../Main Tabs/lz_peak_loads_mid.csv")
c.to_csv("../../../Main Tabs/lz_peak_loads_mid.tab",sep='\t')


# In[ ]:



