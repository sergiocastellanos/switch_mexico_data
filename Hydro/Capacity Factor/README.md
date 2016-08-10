# Capacity Factors


This folder contains data that presents that describes the production of hydro station on given scenarios.


The "capacityFactorHistoric.csv" contains a historical analysis of the production of a hydro station.
  - Each row represents a hydro station.

  - Column 50% contains the median of the historical data.
  - The "25%" column is defined as the middle number between the smallest number and the median of the data set.
  - The "75%" column is the middle value between the median and the highest value of the data set.


The "Year#%" columns represent the year to which each value belongs.

The next plot illustrates the result

![alt tag](https://github.com/sergiocastellanos/switch_mexico_data/blob/master/Hydro/Plots/cf.png)


You will be able to generate a plot for a given hydro station by typing on command line:

```sh
  $ python capacityFactorHistoric.py [state] [station name]
  ```

  - [state] argument corresponds to the state of interest, all states available are stored in this [folder][folder]
  - [data] argument corresponds to the variable of interest it could be the drought, precipitation or production

**You will be able to consult all available hydro stations on "[Data/Production-Drought-Precipitation][data]/[state]/[hydroStationName.csv]"**


[data]: <https://github.com/sergiocastellanos/switch_mexico_data/tree/master/Hydro/Data/Production-Drought-Precipitation>
