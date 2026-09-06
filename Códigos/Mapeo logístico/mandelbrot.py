#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 01:56:23 2026

@author: ejaicer
"""
##########33 Modulos
import numpy as np
import matplotlib.pyplot as plt


################## Iteraciones
def itman(c, max_iter):
    z = 0.0j
    for i in range(max_iter):
        z = z**2 + c
        if np.abs(z) > 2.0:
            return i
    return max_iter


#############  Mapa complejo para generar el grafo de mandelbrot
def mandelbrot(xmin, xmax, ymin, ymax, w, h, max_iter):
    
    r1 = np.linspace(xmin, xmax, w)
    r2 = np.linspace(ymin, ymax, h)
    image = np.empty((h, w))
    
    for i in range(h):
        for j in range(w):
            c = r1[j] + 1j*r2[i]
            image[i, j] = itman(c, max_iter)
    return image


########### Parámetros 
xmin, xmax = -2.1, 0.6 #### eje Real
ymin, ymax = -1.25, 1.25 ### eje complejo
w, h = 800, 800 ####resolución mapa
max_iter = 100  

####################
data = mandelbrot(xmin, xmax, ymin, ymax, w, h, max_iter)

################grafica

plt.figure(figsize=(10, 8))
plt.imshow(data, extent=[xmin, xmax, ymin, ymax], cmap='jet')
plt.axhline(0, color='white', linestyle='--', linewidth=0.8, alpha=0.7)
plt.colorbar(label = 'Iteraciones antes del escape')
plt.title("Conjunto de Mandelbrot ($z_{n+1} = z_n^2 + c$)")
plt.xlabel("Re(c)")
plt.ylabel("Im(c)")
plt.show()
