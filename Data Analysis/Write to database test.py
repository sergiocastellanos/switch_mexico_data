
# coding: utf-8

# In[19]:

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine=create_engine('postgresql://sayeg:edema7-Warbled@switch-db2.erg.berkeley.edu:5433/switch_mexico')


# In[20]:

df=pd.DataFrame(np.random.randn(6,4))
print df
df.to_sql('aldo',engine,schema='mexico',if_exists='replace',chunksize=10)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



