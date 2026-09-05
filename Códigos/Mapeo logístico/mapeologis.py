#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


########Diagrama de bifurcaciones: Mapeo Logístico


import numpy as np
import matplotlib.pyplot as plt



############ mapeo logístico
def ml(x,a):
    return a*x*(1-x)


#### Parameters
a_min = 0
a_max = 4
n_a = 100
n_plot = 100

a = np.linspace(a_min, a_max,n_a) ###tamaño parabola

#####Condición inicial
x=np.full(n_a,0.2)

### eliminación de transitorios
for i in range(500):
    x = ml(x,a)

##dibujar las últimas iteraciones 
plt.figure(figsize= (12,7))


for i in range(n_plot):

    x = a*x*(1-x)
    plt.plot(a,x, 'k', alpha = 0.1)


####grafica
plt.xlabel(r"$a$", fontsize=14)
plt.ylabel(r"$x$", fontsize=14)
plt.title("Diagrama de bifuraciones del mapeo logístico", fontsize=16)
    
plt.xlim(a_min,a_max)
plt.ylim(0,1)

plt.show()
####




