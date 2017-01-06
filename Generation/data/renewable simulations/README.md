# Renewable simulations
All of these files have the name of an existing or planned wind or solar power plant. Manually, we searched for each of the plants location and, if we could not find it, we supposed that it was located in the center of the load zone to which the plant belongs. Each plant location can be found in the "renewable_plants.csv" file in the upper directory. After georeferencing the plants, we simulated their generation supposing they had a generation capacity of 100 MW.

For the solar plants, we used solar irradiance data from NREL of the year 2014 and the SAM simulator

For the wind plants, we used RenewablesNinja to simulate the plant and suposed that the turbine used in the plants was a Vestas V90 2000.

The simulations do not show the generation of the plant, but instead show its hourly capacity factor in 2014. All of the dates are in Mexico's capital local time, UTC-6