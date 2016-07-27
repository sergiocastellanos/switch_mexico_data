import pandas
from generation import Order
from stats import Statistics as s
from precipAccumulation import PrecipAccumulation
import csv


metadata = pandas.read_excel("data/plantas.xlsx",index_col="Plantas")
plantas = metadata.index.values
o = Order()

cont =0
printG = "Nombre,Clasificacion,Combustible,CapacidadEfectiva,ENE,FEB,MAR,ABR,MAY,JUN,JUL,AGO,SEP,OCT,NOV,DIC,ANNUAL"
print printG




with open('results.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(printG)
    for planta in plantas:
        drought = []
        ave = []
        damp = []

        p = PrecipAccumulation()
        data, interest_years = p.data(metadata.loc[planta,"Entidad"],metadata.loc[planta,"PrecipitacionNormalAnual"])
        lista = []
        drought.append(interest_years["drought"])
        ave.append(interest_years["ave"])
        damp.append(interest_years["damp"])



        ce = metadata.loc[planta,"CapacidadEfectiva"]
        d  = o.capacityFactor(o.datos_anuales(planta,"ENE","DIC"),drought,ce)
        m  = o.capacityFactor(o.datos_anuales(planta,"ENE","DIC"),ave,ce)
        h  = o.capacityFactor(o.datos_anuales(planta,"ENE","DIC"),damp,ce)
        printd = str(metadata.loc[planta,"Nombre"])+",s"+","+str(metadata.loc[planta,"Combustible"])+","+str(metadata.loc[planta,"CapacidadEfectiva"])+","+str(d[0])+","+str(d[1])+","+str(d[2])+","+str(d[3])+","+str(d[4])+","+str(d[5])+","+str(d[6])+","+str(d[7])+","+str(d[8])+","+str(d[9])+","+str(d[10])+","+str(d[11])+","+str(s(d).media())
        printm = str(metadata.loc[planta,"Nombre"])+",m"+","+str(metadata.loc[planta,"Combustible"])+","+str(metadata.loc[planta,"CapacidadEfectiva"])+","+str(m[0])+","+str(m[1])+","+str(m[2])+","+str(m[3])+","+str(m[4])+","+str(m[5])+","+str(m[6])+","+str(m[7])+","+str(m[8])+","+str(m[9])+","+str(m[10])+","+str(m[11])+","+str(s(m).media())
        printh = str(metadata.loc[planta,"Nombre"])+",h"+","+str(metadata.loc[planta,"Combustible"])+","+str(metadata.loc[planta,"CapacidadEfectiva"])+","+str(h[0])+","+str(h[1])+","+str(h[2])+","+str(h[3])+","+str(h[4])+","+str(h[5])+","+str(h[6])+","+str(h[7])+","+str(h[8])+","+str(h[9])+","+str(h[10])+","+str(h[11])+","+str(s(h).media())

        spamwriter.writerow([printd])
        spamwriter.writerow([printm])
        spamwriter.writerow([printh])
