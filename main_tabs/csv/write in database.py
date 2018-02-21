import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import glob
#asking for swicht database username and password
user=str(raw_input("SWITCH username: "))
password=str(raw_input("password: "))
sch=str(raw_input("schema: "))
#creating sql engine based on the last input
engine=create_engine('postgresql://{0}:{1}@127.0.0.1:5433/switch_mexico'.format(user,password))
#exclude files that are too large for efficient uploading
for file in [x for x in glob.glob("*.csv") if x not in ["loads_high.csv","loads_low.csv","loads_mid.csv","la_hourly_demand_low.csv","la_hourly_demand_mid.csv","la_hourly_demand_high.csv"]]:
	print file.split(".")[0]
	ex=pd.read_csv(file)
	ex.to_sql(file.split(".")[0] ,engine, schema=sch, if_exists ="replace", chunksize=None)