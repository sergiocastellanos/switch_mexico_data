import xlsxwriter
workbook = xlsxwriter.Workbook('results.xlsx')
worksheet = workbook.add_worksheet()

row = 1
col = 0
anio = 2006
for i in range(1,11):
    worksheet.write(0, 0,     "Planta")
    worksheet.write(0, i,     str(anio))
    anio+=1



class Printer:
    def __init__(self,data):
        self.data = data



    def printing(self):
        row = 1
        col = 0
        anio = 2006
        for i,average in enumerate(self.data):
            #print self.data[average][str(2006)]
            worksheet.write(row, col,     average)
            worksheet.write(row, col + 1,self.data[average][str(2006)])
            worksheet.write(row, col + 2,self.data[average][str(2007)])
            worksheet.write(row, col + 3,self.data[average][str(2008)])
            worksheet.write(row, col + 4,self.data[average][str(2009)])
            worksheet.write(row, col + 5,self.data[average][str(2010)])
            worksheet.write(row, col + 6,self.data[average][str(2011)])
            worksheet.write(row, col + 7,self.data[average][str(2012)])
            worksheet.write(row, col + 8,self.data[average][str(2013)])
            worksheet.write(row, col + 9,self.data[average][str(2014)])
            worksheet.write(row, col + 10,self.data[average][str(2015)])
            row += 1
        workbook.close()




    def printi(self):
        #print data
        for i,e in enumerate(data):
            print "var " + e.upper()[:5] + "="
            print "["
            for element in data[e]:
                print  str(data[e][element]) + ","
            print "];"
