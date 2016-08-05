# Correlation

This folder contains data that aims to expose the correlation between the climate events and the production of each hydro station.

All the data was extracted from National Water Comission in Mexico, known in spanish as [CONAGUA][conagua]

The "Production-Drought-Precipitation" folder contains a .csv file per hydro-station whith the aforementioned values.
  - The files are classified by state.

The "CorrelationResults" folder contains a .csv file with the correlation coefficients.
  - Each row contains the name of a hydro-station, the state to which it belongs, and the correlation coefficients for both the "Production-Drought" and "Production-Precipitation".

The "correlation.py" script creates the "correlationResults.csv" file.

[conagua]: <http://smn.cna.gob.mx/es/climatologia/temperaturas-y-lluvias/resumenes-mensuales-de-temperaturas-y-lluvias>
