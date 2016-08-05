import pandas
import os
import csv
content = os.listdir("Production-Drought-Precipitation") # returns list


printG = "Planta,Entidad,Production-Drought,Production-Precipitation"

def storeresults():
    with open(r"CorrelationResults/CorrelationResults.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(printG)
        for element in content:
            print element
            ent = os.listdir("Production-Drought-Precipitation/%s"%element)
            for en in ent:
                try:
                    print en
                    metadata = pandas.read_csv("Production-Drought-Precipitation/%s/%s"%(element,en))
                    metadata = metadata.corr(method='pearson', min_periods=1)
                    print metadata
                    production =  metadata.columns.values[0]
                    print production
                    metadata = metadata.loc[:production]
                    columns = metadata.columns.values
                    data = metadata[[columns[1],columns[2]]]
                    print data
                    drought = data[[columns[1]]]
                    precipitation = data[[columns[2]]]

                    dindex =  drought.index.values[0]
                    dcol = drought.columns.values[0]
                    drought = drought.get_value(dindex, dcol, takeable=False)

                    pindex =  precipitation.index.values[0]
                    pcol = precipitation.columns.values[0]
                    precipitation = precipitation.get_value(pindex, pcol, takeable=False)

                    print drought, precipitation

                    row = str(en[:len(en)-4])+","+element+","+str(drought)+","+str(precipitation)
                    spamwriter.writerow([row])
                except IndexError:
                    row = str(en[:len(en)-4])+","+element+","+str(0)+","+str(0)
                    spamwriter.writerow([row])



data = pandas.read_csv("CorrelationResults/correlationResults.csv",index_col =0)
print data
