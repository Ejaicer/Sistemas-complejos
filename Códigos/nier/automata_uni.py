
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 20:03:10 2026

@author: ejaic
"""

import numpy as np
import matplotlib.pyplot as plt

############### Parámetros

regla = int(input("Da un valor de regla entre 0 y 255: "))

while regla < 0 or regla > 255:
  print("Debe ser un número entre 0 y 255.")
  regla = int(input("Da un valor con las condiciones que se piden: "))

n_cell = int(input("Número de celdas por renglón: "))
n_step = int(input("Número de pasos: "))

#######vecindad radio r=2
vecindarios = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]

############ Conversión a binario y convertimos cada carácter en entero

r_bin = format(regla,"08b") ###convertimos la regla a usar a código binario


######## generamos el vector que contiene como entradas los dígitos de la regla en binario
bits_R =[]
for i in range(0,8):
  bit = int(r_bin[i])
  bits_R.append(bit)
  #print(bit)
  

########### matriz

matriz = np.zeros((n_step,n_cell), dtype=int)

matriz[0, n_cell // 2] = 1 ####condición incial:  1 en el centro de la malla


###########llenar matriz
for f in range(1, n_step):
    #for c in range(1,n_cell-1): ####### primera y última columna en estado cero
    for c in range(n_cell): ########## para frontera perdiódica
        #izq = matriz[f-1,c-1]
        izq = matriz[f-1, (c-1) % n_cell] ########## para frontera perdiódica
        cen = matriz[f-1, c]
        #der = matriz[f-1,c+1]
        der = matriz[f-1, (c+1) % n_cell] ########## para frontera perdiódica
        
        ############### asignación del nuevo estado
        for i in range(0,8):
            mi = izq == vecindarios[i][0]
            mc = cen == vecindarios[i][1]
            md = der == vecindarios[i][2]
            
            if mi and mc and md:
                ne = bits_R[i]
                matriz[f][c] = ne
                
print(matriz)

############ Gráfica

plt.figure(figsize=(10, 6))
plt.imshow(matriz, cmap='copper', interpolation='nearest')
plt.title(f"Autómata Celular 1D - Regla {regla} (Binario: {r_bin})")
plt.xlabel("Celda")
plt.ylabel("Generaciones")
plt.tight_layout()
plt.savefig(fr"AC_1D_r{regla}.png")
plt.show()