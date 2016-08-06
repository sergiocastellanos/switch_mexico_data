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
from sklearn.linear_model import LinearRegression
import scipy, scipy.stats
matplotlib.style.use('ggplot')



metadata = pandas.read_csv("../Data/Production-Drought-Precipitation/chiapas/chicoasen.csv")
columns = metadata.columns.values
X = metadata[columns[3]]
Y = metadata[columns[1]]
print colored(columns[3],"white")
result = sm.OLS( Y, X ).fit()
print result.summary()

X = metadata[columns[2]]
Y = metadata[columns[1]]
print colored(columns[2],"white")
result = sm.OLS( Y, X ).fit()
print result.summary()
