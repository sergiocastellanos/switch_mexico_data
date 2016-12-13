import pandas as pd
from sqlalchemy import create_engine
import glob
#asking for swicht database username and password
user=str(raw_input("SWITCH username: "))
password=str(raw_input("password: "))
sch=str(raw_input("schema: "))
#creating sql engine based on the last input
engine=create_engine('postgresql://{0}:{1}@127.0.0.1:5433/switch_mexico'.format(user,password))
for file in glob.glob("*.csv"):
	print file.split(".")[0]
	ex=pd.read_csv(file)
	ex.to_sql(file.split(".")[0] ,engine, schema="sandbox", if_exists ="replace", chunksize=None)
