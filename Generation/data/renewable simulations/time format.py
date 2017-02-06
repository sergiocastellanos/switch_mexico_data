import os
import pandas as pd
files=os.listdir(os.getcwd())
files.remove('README.md')
files.remove('time format.py')
for file in files:
    print file
    df=pd.read_csv(file)
    try: 
        df['hour']=df['hour'].astype('int64')
        df['timepoint']='2014'+df['month'].astype('string').str.zfill(2)+df['day'].astype('string').str.zfill(2)+df['hour'].astype('string').str.zfill(2)+'00'
        df=df.set_index('timepoint')
        df=df.drop(['month','day','hour'],axis=1)
        df.to_csv(file)
    except KeyError: pass
    