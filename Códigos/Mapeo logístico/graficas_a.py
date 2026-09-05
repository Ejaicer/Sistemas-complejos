#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:45:48 2026

@author: ejaicer
"""

########### modulos
import numpy as np
import matplotlib.pyplot as plt


############ mapeo logístico
def ml(x,a):
    return a*x*(1-x)

#################### Parámetros

a= 3.75
xo = 0.2
n_t = 100

################# arreglo para el grafico
x = np.zeros(n_t)
x[0]=xo

###################### iteraciones
for i in range(n_t-1):
    x[i+1] =  ml(x[i],a)
    
######### gráficas
plt.figure(figsize=(8, 8))
plt.ylim(0,1)
plt.xlim(0,n_t)
plt.plot(range(n_t),x, 'o-')    
plt.show()

