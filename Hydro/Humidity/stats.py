from __future__ import division
from math import sqrt

import numpy as np


class Estadisticas:
    def __init__(self, elementos):
        self.n = 0
        self.elementos = elementos
        self.horapico = []
        self.demandaPicoHora = []
        self.cont = 1
        #try:
        #    self.elementos = map(int, elementos)
        #except ValueError:
        #    self.elementos.pop()
        #    self.elementos = map(int, elementos)
        #print self.elementos

    def media(self):
        med = 0
        for i in self.elementos:
            med += i
        med/=len(self.elementos)
        return med

    def varianza(self):
        var = 0
        for i in self.elementos:
            var += (i- self.media())** 2
        var/=len(self.elementos)
        return var

    def desviacion(self):
        return sqrt(self.varianza())

if __name__ == '__main__':
    prueba = [0.86, 0.79, 0.73, 0.83, 0.82, 0.72, 0.79, 0.86, 0.81, 0.83, 0.8, 0.79, 0.86, 0.86, 0.87, 0.77, 0.73, 0.79, 1, 0.93, 0.93, 0.95, 0.86, 0.9, 0.84, 0.91, 0.87, 0.88, 0.96, 0.93]

    #[10, 18, 15, 12, 3, 6, 5, 7]
    e = Estadisticas(prueba)
    print e.media()
    #assert e.varianza() == 23.75
    #assert e.desviacion() >= 4.8 and e.desviacion() <= 4.9
