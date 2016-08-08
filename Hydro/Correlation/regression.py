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



metadata = pandas.read_csv("CorrelationResults/globals.csv")

columns = metadata.columns.values
X = metadata[[columns[3],columns[2]]]
X = s.add_constant(X)
Y = metadata[columns[1]]
print colored("%s %s"%(columns[3],columns[2]),"white")
result = sm.OLS( Y, X ).fit()
print result.summary()
