import pandas as pd
import os
import csv

def storeresults():
    with open(r"pruebita.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        with open("../../Main Tabs/region_transmision.tab") as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"):
                line = line[0],",",line[1],",",line[2],",",line[3]
                spamwriter.writerow(line)
    pruebita1 = pd.read_csv("pruebita.csv", index_col = 0)
    with open(r"pruebita2.csv", "wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        with open("../../Main Tabs/capacity_factors.tab") as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"):
                line = line[0],",",line[1],",",line[2],",",line[3],",",line[4],",",line[5],",",line[6]
                spamwriter.writerow(line)
    pruebita2 = pd.read_csv("pruebita2.csv", index_col=0)
    result = pd.concat([pruebita1, pruebita2], axis=1, join='inner')
    print result
    result = pd.concat([pruebita1, pruebita2], axis=1, join_axes=[pruebita1.index])
    print result
    result.to_csv("pruebitafinal.csv", sep=',', encoding='utf-8')


storeresults()
