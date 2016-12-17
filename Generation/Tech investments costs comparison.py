
# coding: utf-8

# In[209]:

import pandas as pd
import numpy as np
df1=pd.read_csv('data/TechCosts.csv')
df2=pd.read_csv('data/gen_new_build_costs_v2-Draft.tab',sep='\t')


# In[210]:

df1=df1.rename(columns = {df1.columns.tolist()[0]:'gen_tech'})
df1=df1.sort_values('gen_tech',axis=0)
df1=df1.reset_index(drop=True)
df1=df1.fillna(0)
df2=df2[df2['investment_period']==2020]
df2=df2.replace('wind','eolic')
df2=df2.replace('thermosolar ','termosolar')
df2=df2.sort_values('generation_technology',axis=0)
df2=df2.reset_index(drop=True)
df2=df2.fillna(0)


# In[ ]:




# In[211]:

df3=pd.DataFrame()
for i in list(set(df1['gen_tech'].tolist())):
    a= df1[df1['gen_tech']==i].mean()
    a['gen_tech']=i
    df3=df3.append(a,ignore_index=True)
b=df3.columns.tolist()
b=[b[2]]+[x for x in b if x not in ["gen_tech"]]
df3=df3[b]
df3=df3.sort_values('gen_tech')
df3=df3.reset_index(drop=True)
df4=pd.concat([df2,df3],axis=1)
df4[df4.columns.tolist()[2:4]]=df4[df4.columns.tolist()[2:4]]/1000


# In[163]:




# In[187]:

import matplotlib.pyplot as plt


# In[212]:

df5=df4[['gen_tech','g_overnight_cost','overnight_cost']]
df5['average']=(df5.iloc[:,1]+df5.iloc[:,2])/2
df5['difference']=abs(df5.iloc[:,1]-df5.iloc[:,2])
plt.figure(1,figsize=[14,7],dpi=200)
plt.plot(df5.iloc[:,1],marker='o',label='Sergio')
plt.plot(df5.iloc[:,2],marker='o',label='Aldo (COPAR)')
plt.grid()
plt.title('Overnight costs',fontsize=24)
plt.ylabel('USD/KW', fontsize=18)
plt.xticks(df5.index.tolist(),df5['gen_tech'].tolist(),rotation='vertical')
plt.errorbar(range(len(df5.index.tolist())),df5['average'],label='average',fmt='o')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# In[213]:

df6=df4[['gen_tech','g_fixed_o_m','fixed_o_m']]
df6['average']=(df6.iloc[:,1]+df6.iloc[:,2])/2
df6['difference']=abs(df6.iloc[:,1]-df6.iloc[:,2])
plt.figure(2,figsize=[14,7],dpi=200)
plt.plot(df6.iloc[:,1],marker='o',label='Sergio')
plt.plot(df6.iloc[:,2],marker='o',label='Aldo (COPAR)')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=18)
plt.grid()
plt.title('Fixed O & M  costs',fontsize=25,y=1.08)
plt.ylabel('USD/MWh',fontsize=18)
plt.xticks(df5.index.tolist(),df5['gen_tech'].tolist(),rotation='vertical')
plt.errorbar(range(len(df6.index.tolist())),df6['average'],label='average',fmt='o')
plt.show()


# In[ ]:




# In[ ]:



