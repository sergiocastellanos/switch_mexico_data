

import G
import sys
import collections
import Printer
import pandas


p =  G.Analisis(sys.argv[1],sys.argv[2],sys.argv[3])
table = p.res()
tup1 = []
dos = 2006
data = {}
for e in table:
     data[e] = collections.OrderedDict(sorted(table[e].items()))

d = Printer.Printer(data)
d.printing()

panda = pandas.read_excel("results.xlsx",index_col=0)
print panda
