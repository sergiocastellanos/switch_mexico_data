from __future__ import division
from math import sqrt

import numpy as np


class Statistics:
    def __init__(self, elements):
        self.n = 0
        self.elements = elements
        self.cont = 1
        #try:
        #    self.elements = map(int, elements)
        #except ValueError:
        #    self.elements.pop()
        #    self.elements = map(int, elements)
        #print self.elements

    def media(self):
        med = 0
        for i in self.elements:
            med += i
        med/=len(self.elements)
        return med

    def variance(self):
        var = 0
        for i in self.elements:
            var += (i- self.media())** 2
        var/=len(self.elements)
        return var

    def deviation(self):
        return sqrt(self.variance())

if __name__ == '__main__':
    prueba = [0.86, 0.79, 0.73, 0.83, 0.82, 0.72, 0.79, 0.86, 0.81, 0.83, 0.8, 0.79, 0.86, 0.86, 0.87, 0.77, 0.73, 0.79, 1, 0.93, 0.93, 0.95, 0.86, 0.9, 0.84, 0.91, 0.87, 0.88, 0.96, 0.93]

    #[10, 18, 15, 12, 3, 6, 5, 7]
    e = Statistics(prueba)
    print e.media()
    #assert e.variance() == 23.75
    #assert e.deviation() >= 4.8 and e.deviation() <= 4.9
