"""
Simple demo of a scatter plot.
"""
import numpy as np
import matplotlib.pyplot as plt
import printer as p

x,y = p.external()

area = np.array([115,115,115,115,115,115,115,115,115,115,115,115])# 0 to 15 point radiuses




colors = np.random.rand(4)
j =  np.array(y["2006"])
k =  np.array(x[2006])
plt.scatter(j, k, s=area, c=colors, alpha=0.5)

o =  np.array(y["2007"])
z =  np.array(x[2007])
colors = np.random.rand(4)
plt.scatter(o, z, s=area, c=colors, alpha=0.5)



l =  np.array(y["2008"])
m =  np.array(x[2008])
colors = np.random.rand(4)
plt.scatter(l, m, s=area, c=colors, alpha=0.5)

n =  np.array(y["2009"])
p =  np.array(x[2009])
colors = np.random.rand(4)
plt.scatter(n, p, s=area, c=colors, alpha=0.5)



q =  np.array(y["2010"])
r =  np.array(x[2010])
colors = np.random.rand(4)
plt.scatter(q, r, s=area, c=colors, alpha=0.5)

s =  np.array(y["2011"])
t =  np.array(x[2011])
colors = np.random.rand(4)
plt.scatter(s, t, s=area, c=colors, alpha=0.5)

plt.show()
