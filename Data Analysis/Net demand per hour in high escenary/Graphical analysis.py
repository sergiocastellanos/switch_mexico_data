
# coding: utf-8

# In[8]:

import pandas as pd
import random
import matplotlib.pyplot as plt
import random
import numpy as np

def nearest_value(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx
df=pd.read_csv("demand per node.csv",index_col=range(4))
dfp=pd.read_csv("highlights per node.csv",index_col=range(2),header=range(2))


# In[10]:


for index, k in enumerate(df.columns.tolist()):
    
    plt.figure(index,figsize=(10,7),dpi = 200)
    
    data1=[]
    for a in range(2016,2031):
        try: f=df.xs(a,level=0)[k]
        except ValueError: print "{0},{1},{2}".format(a,m,d)
        yy=[]
        for m in range(1,13):
            for d in range(1,32):
                try: yy.append(f.xs([m,d],level=[0,1]).mean())
                except KeyError: yy.append(0)
                
        
        color =[np.random.rand(3)]*372
        plt.scatter(range(1,373), yy, s=20, c=color, alpha=0.5,label='{0}'.format(a))
    plt.xticks([15,105,195,285], ['Enero','Mayo','Julio','Octubre'], rotation='vertical')
    name='Variacion anual escenario alto en nodo {0}'.format(k)
    plt.ylabel('Demanda')
    plt.title(name)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


# In[9]:

print "Analisis horario de un un nodo determinado. Dado un nodo, ano y mes, mostrara la demanda horaria diaria todos los dias en un grafico, mientras que en otro mostrara la demanda del dia pico, un dia promedio, el dia medio y un dia aleatorio"


k=raw_input("Planta: ")
a=int(raw_input("Ano: "))
m=int(raw_input("Mes: "))
res=int(raw_input("¿Cada cuantas horas quieres que grafique?  "))


get_ipython().magic(u'matplotlib inline')
plt.figure(1,figsize=(10,8),dpi = 200)

for d in df.xs([a,m,1],level=[0,1,3])[k].index.tolist():
    yy=[]
    for h in range(1,25):
        yy.append(df.xs([a,m,d,h])[k])
    plt.scatter(range(1,25,res),[yy[i] for i in range(0,24,res)],s=40,c=[np.random.rand(3)]*24,alpha=.6,label='{0}'.format(d))
name='Variacion diaria {0} en {1},{2}'.format(k,a,m)
print dfp.xs([a, m])[k]
plt.ylabel('Demanda')
plt.xlabel('Hora')
plt.title(name)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()



zz=[]
for d in df.xs([a,m,1],level=[0,1,3])[k].index.tolist():
    zz.append(df.xs([a,m,d],level=range(3))[k].mean())
aleatorio=random.choice(zz)
indx_ale=zz.index(aleatorio)
indx_mean= nearest_value(np.array(zz),dfp.xs([a,m])[k,'PromedioMensual'])
mean = zz[indx_mean]
if len(zz)%2 ==1:
    median = np.median(np.array(zz))
    indx_median = zz.index(median)
else:
    n=np.random.randint(len(zz))
    median = np.median(zz[-n])
    indx_median = zz.index(median)
    if indx_median>= n:
        indx_median= indx_median+1
        

plt.figure(2,figsize=(10,8),dpi = 200)
plt.scatter(range(1,25,res),[df.xs([a,m,indx_ale],level=range(3))[k].tolist()[i] for i in range(0,24,res)],s=80,c=[np.random.rand(3)]*24,alpha=.6,label="Dia Aleatorio ({0})".format(indx_ale))
plt.scatter(range(1,25,res),[df.xs([a,m,indx_mean],level=range(3))[k].tolist()[i] for i in range(0,24,res)],s=80,c=[np.random.rand(3)]*24,alpha=.6,label="Dia Promedio ({0})".format(indx_mean))
plt.scatter(range(1,25,res),[df.xs([a,m,indx_median],level=range(3))[k].tolist()[i] for i in range(0,24,res)],s=80,c=[np.random.rand(3)]*24,alpha=.6,label="Dia Mediano ({0})".format(indx_median))
plt.scatter(range(1,25,res),[df.xs([a,m,dfp.xs([a,m])[k,'DiaPico']],level=range(3))[k].tolist()[i] for i in range(0,24,res)],s=80,c=[np.random.rand(3)]*24,alpha=.6,label="Dia Pico")
plt.xlabel('Hora')
plt.ylabel('Demanda')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Dias significativos en nodo {0}, {1}/{2}'.format(k,m,a))
plt.show()


# In[ ]:



