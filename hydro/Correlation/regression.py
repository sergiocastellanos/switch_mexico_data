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



metadata = pandas.read_csv("CorrelationResults/globals.csv")#returns data of the drought, precipitation and production of the dams

columns = metadata.columns.values#returns the columns of the set
X = metadata[[columns[3],columns[2]]]#asigns to x  the drough level and the precipitation (as ndependient values)
X = s.add_constant(X)#add the data to the model
Y = metadata[columns[1]]#set the production as dependient value
print colored("%s %s"%(columns[3],columns[2]),"white") #print drought and precipitation values
result = sm.OLS( Y, X ).fit()       #returns the linear regresion
print result.params #prints the results parameters
print result.summary()#prints the summary
