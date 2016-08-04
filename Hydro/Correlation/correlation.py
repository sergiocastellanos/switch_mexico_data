import pandas
import os
import csv
content = os.listdir("plantas/Production-Drought-Precipitation") # returns list


printG = "Planta,Entidad,Production-Drought,Production-Precipitation"
with open(r"plantas/CorrelationResults/CorrelationResults.csv", "wb") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                         quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(printG)
    for element in content:
        print element
        ent = os.listdir("plantas/Production-Drought-Precipitation/%s"%element)
        for en in ent:
            print en
            metadata = pandas.read_csv("plantas/Production-Drought-Precipitation/%s/%s"%(element,en),index_col =0)
            metadata = metadata.corr(method='pearson', min_periods=1)
            production =  metadata.columns.values[0]
            metadata = metadata.loc[:production]
            columns = metadata.columns.values
            data = metadata[[columns[1],columns[2]]]
            #sprint data
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
