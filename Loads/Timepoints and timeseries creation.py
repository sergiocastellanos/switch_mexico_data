
# coding: utf-8

# In[67]:

import pandas as pd
import numpy as np
def median(lis):
    lis=np.sort(lis)
    if len(lis)%2==0:
        return lis[((len(lis))/2)-1]
    else: return lis[(len(lis)-1)/2]
def investment_period(y):
    if y in range(2016,2021): return 2016
    elif y in range(2021,2026): return 2021
    else: return 2026
df1=pd.read_csv("Medium scenario/OrganizedTables/HourlyLoadPerNode.csv",index_col=range(4),dtype=np.float64)


# In[68]:

df5=pd.DataFrame()
for y in range(2016,2031):
    for m in range(1,13):
        #peak days timestamp creation
        df2=df1.xs([y,m])
        a=df2.max()
        place=a.idxmax()
        date=df2[place].idxmax()
        df3=pd.DataFrame()
        if date[1]%2==0:
            for h in range(1,24,2):
                df3.loc[(h-1)/2,'timestamp']="{0}{1}{2}{3}".format(y,str(m).zfill(2),str(int(date[0])).zfill(2),str(h).zfill(2))
        else: 
            for h in range(0,24,2):
                df3.loc[h/2,'timestamp']="{0}{1}{2}{3}".format(y,str(m).zfill(2),str(int(date[0])).zfill(2),str(h).zfill(2))
        df3['timeseries']="{0}{1}P".format(y,str(m).zfill(2))
        #median days timestamp creation
        df4=pd.DataFrame()
        b=[]
        for i in range(len(df2.values)):
            b=b+[x for x in df2.values[i]]
        d=df2[df2.isin([median(b)])].dropna(how='all').index.tolist()[0][0]
        for h in range(12):
            df4.loc[h+12,'timestamp']="{0}{1}{2}{3}".format(y,str(m).zfill(2),str(int(d)).zfill(2),str(h*2).zfill(2))
        df4['timeseries']="{0}{1}M".format(y,str(m).zfill(2))
        df5=df5.append(df3)
        df5=df5.append(df4)
df5=df5.reset_index(drop=True)
df5.index.name="timepoint_id"


# In[69]:

df5.to_csv("../Main Tabs/timepoints.tab",sep="\t")


# In[70]:

df6=pd.DataFrame(index=df5['timeseries'].unique())
df6.index.name='TIMESERIES'
for index,row in df6.iterrows():
    df6.loc[index,'ts_period']=investment_period(int(index[:4]))
    if index[-1]=='M': 
        #calculating scaling factor according to "timescales.py"
        df6.loc[index,'ts_scale_to_period']= 1*24*(df1.xs([int(index[:4]),int(index[4:6]),1],level=[0,1,3]).shape[0]-1)
    else: df6.loc[index,'ts_scale_to_period']= 1*24
df6['ts_duration_of_tp']=2
df6['ts_num_tps']=24
df6['ts_period']=df6['ts_period'].astype('int64')


# In[71]:

#rearreging columns and exporting table
df6=df6[[0,2,3,1]]
df6.to_csv("../Main Tabs/timeseries.tab",sep="\t")


# In[ ]:




# In[ ]:



