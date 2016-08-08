# OLS Regression Results


In order to find a relationship between climate data and the net production of all Reservoir Hydro Power Stations, we applied a linear regression using the ordinary least squares method.

Our finds, as shown below, reveal that in certain way both the precipitation and drought levels are correlated with the hydro power production however it is not as significant as we would expect.





|                   |                |                           |                                         |
| ----------------- | -------------- | ------------------------- | --------------------------------------- |
|Dep. Variable:     | **Production**          |   R-squared:             |            **0.053**            |
|Model:             |                  **OLS**|   Adj. R-squared:        |            **0.053**            |
|Method:            |        **Least Squares**|   F-statistic:           |            **182.7**            |
|Date:              |     **Sat, 06 Aug 2016**|   Prob (F-statistic):    |         **6.55e-78**            |
|Time:              |             **21:14:36**|   Log-Likelihood:        |          **-84806.**            |
|Df Residuals:      |                 **6527**|   BIC:                   |            **1.696e+05**        |
|No. Observations:  |                 **6530**|   AIC:                   |            **1.696e+05**        |
|Df Model:          |                    **2**|                                                     |
|Covariance Type:   |            **nonrobust**|                                                    |



  - R-squared is very low, meaning that drought and precipitation levels aren't connected to the production. It is a sign that using both drought or precipitation to predict the production simply will not return a significant regression (and thus prediction).



|                          |      coef  |  std err   |     t     |   P>[t]   |    [95.0% Conf. Int.]  |
| -----------------------  | ---------- | ---------- | --------- | --------- | ---------------------- |
|const                     | 3.109e+04  |  1968.363  |  15.796   |   0.000   |**2.72e+04**  -  **3.5e+04**|
|P r e c i p i t a t i o n | 207.6100   |  11.773    |  17.635   |   0.000   |**184.532**  -  **230.688**|
|D r o u g h t L e v e l   |-7061.0093  |  1507.152  |  -4.685   |   0.000   |**-1e+04**  -  **4106.498**  |





|                          |               |                              |                           |
|------------------------- | ------------- | ---------------------------- | ------------------------- |
|Omnibus:                  |   **5662.650**|  Durbin-Watson:              |     **0.207**             |
|Prob(Omnibus):            |      **0.000**|  Jarque-Bera (JB):           |     **191695.245**        |
|Skew:                     |      **4.097**|  Prob(JB):                   |     **0.00**              |
|Kurtosis:                 |     **28.247**|  Cond. No.                   |      **245.**             |
