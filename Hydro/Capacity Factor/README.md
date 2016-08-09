# Capacity Factors


This folder contains data that presents the .

All the data were extracted from National Water Commission in Mexico, known in Spanish as [CONAGUA][conagua]

The "Production-Drought-Precipitation" folder contains a .csv file per hydro station with the aforementioned values.
  - The files are classified by state.

The "correlation.py" script creates the "correlationResults.csv" file. It also produces scatter plots that may show whether there is a link between those variables or not.

In order to see the scatter plots you must type on command line:
```sh
$ python correlation.py [state] [hydro station name]
```
(You will be able to consult all available hydro stations on "[Data/Production-Drought-Precipitation][data]/[state]/[hydroStationName.csv]")


The "CorrelationResults" folder contains a '.csv' file with the correlation coefficients.
  - Each row contains the name of a hydro station, the state to which it belongs, and the correlation coefficients for both the "Production-Drought" and "Production-Precipitation".





[data]: <https://github.com/sergiocastellanos/switch_mexico_data/tree/master/Hydro/Data/Production-Drought-Precipitation>
[conagua]: <http://smn.cna.gob.mx/es/climatologia/temperaturas-y-lluvias/resumenes-mensuales-de-temperaturas-y-lluvias>
