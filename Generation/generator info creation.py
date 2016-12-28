
# coding: utf-8

# In[5]:

import pandas  as pd
import numpy as np
df1=pd.read_csv('data/chile_generator_info.tab',sep='\t')
df2=pd.read_csv('../Main Tabs/generator_energy_sources.tab',sep='\t',index_col=0)
df3=pd.read_csv('data/PowerPlants.csv')
df4=pd.read_csv('data/gen_new_build_costs_v2-Draft.tab',sep="\t",index_col=0)
df5=pd.read_csv('data/generator_max_age.tab',sep="\t",index_col=0)
df5=df5.fillna(value=0)
df3=df3.fillna(value=0)


# In[6]:

#using PIIRCE's information to estimate the full load heat rate for every generation technology 
#using a weighted average. For more information, check the report.
for i in df3['gen_tech'].unique():
    dfa=df3[df3['gen_tech']==i]
    t=dfa['capacity_mw'].sum()
    dfa['weight']=dfa['capacity_mw']/t
    df2.loc[i,'g_full_load_heat_rate']=((dfa['weight']*dfa['full_load_heat_rate_mbtu/mwh']).sum())


# In[ ]:




# In[ ]:




# In[ ]:




# In[7]:

for i in df2.index.tolist():
    print i
    df2.loc[i,'g_variable_o_m']=df4[df4['investment_period']==2020]['g_variable_o_m'].to_dict()[i]
    


# In[8]:

df2['g_min_build_capacity']=0
for i in df2.index.tolist():
    dfa=df3[df3['gen_tech']==i]
    t=dfa['capacity_mw'].sum()
    dfa['weight']=dfa['capacity_mw']/t
    df2.loc[i,'g_full_load_heat_rate']=((dfa['weight']*dfa['full_load_heat_rate_mbtu/mwh']).sum())
    df2.loc[i,'g_variable_o_m']=df4[df4['investment_period']==2020]['g_variable_o_m'].to_dict()[i]
    df2.loc[i,'g_scheduled_outage_rate']=df3[df3['gen_tech']==i]['scheduled_outage_rate'].tolist()[0]
    df2.loc[i,'g_forced_outage_rate']=df3[df3['gen_tech']==i]['scheduled_outage_rate'].tolist()[0]
    if i=='nuclear_uranium':
        df2.loc[i,'g_min_build_capacity']=sorted(df3[df3['gen_tech']=='nuclear_uranium']['capacity_mw'].tolist())[1]
    df2.loc[i,'g_max_age']=df5.loc[i,'g_max_age']
df2


# In[ ]:




# In[9]:

#optional parameters that will be ignored
ignored=["g_unit_size","g_ccs_capture_efficiency","g_ccs_energy_load","g_storage_efficiency","g_store_to_release_ratio"]
for i in ignored:
    df2[i]="."
#boolean parameters that will be estimated
boole=["g_is_variable","g_is_baseload","g_is_flexible_baseload","g_is_cogen","g_competes_for_space"]


# In[ ]:




# In[10]:

df2.to_csv('data/generator_info_trial.tab',sep="\t")

