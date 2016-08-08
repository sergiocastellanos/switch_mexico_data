import pandas
import os
import csv
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas
from termcolor import colored
from pandas import DataFrame, Series
import statsmodels.formula.api as sm
import statsmodels.api as s
from sklearn.linear_model import LinearRegression
import scipy, scipy.stats
matplotlib.style.use('ggplot')



metadata = pandas.read_csv("../Data/Production-Drought-Precipitation/chiapas/chicoasen.csv")
columns = metadata.columns.values
X = metadata[columns[3]]
Y = metadata[columns[1]]
print colored(columns[3],"white")
result = sm.OLS( Y, X ).fit()
result.summary()



fig = s.graphics.plot_partregress_grid(result)

X = metadata[columns[2]]
Y = metadata[columns[1]]
print colored(columns[2],"white")
result = sm.OLS( Y, X ).fit()
result.summary()

fig, ax = plt.subplots(figsize=(12,8))
fig = s.graphics.influence_plot(result, ax=ax, criterion="cooks")
plt.show()
