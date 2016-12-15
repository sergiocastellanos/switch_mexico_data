
import pandas as pd
import numpy as np
df=pd.read_csv("tables/Counties.csv", index_col=0, header=0)
dfs=pd.read_csv("tables/CountyData.csv",skiprows=range(5),index_col=3,header=0)
print dfs
#categorize every county depending on if they apear in the urban counties list.
for a in dfs.index.tolist():
	if a in df['urban towns'].tolist():
		dfs.loc[a,"County type"]="urban"
	else:
		dfs.loc[a,"County type"] = "rural"




dfs.to_csv("tables/CategorizedCounties.csv")