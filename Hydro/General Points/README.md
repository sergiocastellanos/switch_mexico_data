# General Points

This folder contains a script that produces line plots.
In order to see the line plots you must type on command line:

```sh
  $ python generalities.py [data] [state]
  ```

  - [data] argument corresponds to the variable of interest it could be the drought, precipitation or production
  - [state] argument corresponds to the state of interest, all states available are stored in this [folder][folder]


By running the script you will get a result like this:

![alt tag](https://github.com/sergiocastellanos/switch_mexico_data/blob/master/Hydro/plots/chiapasNG.png)

In this case the vertical axis represents Net Generation per hydro station, it is given as [MWh][MWh] units.
The abscissa shows the time value in years (from 2006 to 2016).
  - Each point on axis x represents the average per year of the given hydro station.

[folder]: <https://github.com/sergiocastellanos/switch_mexico_data/tree/master/Hydro/Data/Production-Drought-Precipitation>
[MWh]:<https://es.wikipedia.org/wiki/Vatio#Megavatio>
