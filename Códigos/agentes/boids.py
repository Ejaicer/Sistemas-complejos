#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:45:47 2026

@author: ejaicer
Para algunas partes de este código se utilizó IA, las cuales fueron modificadas
para las necesidades de este trabajo
"""

import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

###################### funcion distancia
def d(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)   

##################### parametros
n = 100.0 #### tamaño de la malla
nboid = 100 ###### numero de agentes
r = 6.0   ###### Radio de percepcion
v_max = 2.5          ###### rapidez maxima
f_max = 0.10      ###### fuerza maxima 

w_s = 1.8 ######### peso separacion
w_a = 0.5 ######### peso alineacion
w_c = 2.2 ######### peso cohesion

################ Condiciones iniciales
pos_x = []
pos_y = []
vel_x = []
vel_y = []

         #### velocidades y posiciones aleatorias de los agentes
for i in range(nboid):
    pos_x.append(random.uniform(0, n))
    pos_y.append(random.uniform(0, n))
    vel_x.append(random.uniform(-2.0, 2.0))
    vel_y.append(random.uniform(-2.0, 2.0))

################ grafica
fig, ax = plt.subplots(figsize=(6, 6))
((puntos,)) = ax.plot([], [], 'ro', ms=4)  
ax.set_xlim(0, n)
ax.set_ylim(0, n)
ax.set_title("Modelo de Boids")



################# Modelo de boids  #########################
def actualizar(frame):
    global pos_x, pos_y, vel_x, vel_y

############## Paso 1: Copias

    pos_x_copia = list(pos_x)
    pos_y_copia = list(pos_y)
    vel_x_copia = list(vel_x)
    vel_y_copia = list(vel_y)

    nuevas_vel_x = []
    nuevas_vel_y = []

    for i in range(nboid):
        xi = pos_x_copia[i]
        yi = pos_y_copia[i]
        vxi = vel_x_copia[i]
        vyi = vel_y_copia[i]

        ###### vectores de las reglas locales
        s_x = 0.0 ##### separacion
        s_y = 0.0
        a_x = 0.0 ##### alineacion
        a_y = 0.0
        c_x = 0.0 ##### cohecion
        c_y = 0.0

        n_veci = 0
        suma_vel_x = 0.0
        suma_vel_y = 0.0
        suma_pos_x = 0.0
        suma_pos_y = 0.0

############################ Paso 2:  Calculo de reglas
        for j in range(nboid):
            if i != j:  #### auto exclusion
                dist = d(xi, yi, pos_x_copia[j], pos_y_copia[j]) ### calculo de distancia

                if 0 < dist < r:
                    n_veci += 1

        ####### Regla 1: separacion
                    s_x += (xi - pos_x_copia[j]) / (dist**2)
                    s_y += (yi - pos_y_copia[j]) / (dist**2)


                    suma_vel_x += vel_x_copia[j]
                    suma_vel_y += vel_y_copia[j]
                    suma_pos_x += pos_x_copia[j]
                    suma_pos_y += pos_y_copia[j]

        if n_veci > 0:
            
        ####### Regla 2: alineacion

            a_x = (suma_vel_x / n_veci) - vxi
            a_y = (suma_vel_y / n_veci) - vyi

        ####### Regla 3: cohecion
            c_x = (suma_pos_x / n_veci) - xi
            c_y = (suma_pos_y / n_veci) - yi


        ########### combinacion de las regla
        delta_vx = (w_s * s_x) + (w_a * a_x) + (w_c * c_x)
        delta_vy = (w_s * s_y) + (w_a * a_y) + (w_c * c_y)

################# Paso 3: calcular nuevas velocidades con limitaciones 

######## actualizar vi
        f = math.sqrt(delta_vx**2 + delta_vy**2)
        if f > f_max:
            delta_vx = (delta_vx / f) * f_max
            delta_vy = (delta_vy / f) * f_max

        n_vxi = vxi + delta_vx
        n_vyi = vyi + delta_vy

######## actualizar xi
        rapidez = math.sqrt(n_vxi**2 + n_vyi**2)
        if rapidez > v_max:
            n_vxi = (n_vxi / rapidez) * v_max
            n_vyi = (n_vyi / rapidez) * v_max

        nuevas_vel_x.append(n_vxi)
        nuevas_vel_y.append(n_vyi)

        ####### actualizacion de velocidad y posicion
    for i in range(nboid):
        vel_x[i] = nuevas_vel_x[i]
        vel_y[i] = nuevas_vel_y[i]

        pos_x[i] += vel_x[i]
        pos_y[i] += vel_y[i]

#################### Paso 4:  Bordes periodicos
        if pos_x[i] > n:
            pos_x[i] = pos_x[i] - n
        elif pos_x[i] < 0:
            pos_x[i] = pos_x[i] + n

        if pos_y[i] > n:
            pos_y[i] = pos_y[i] - n
        elif pos_y[i] < 0:
            pos_y[i] = pos_y[i] + n

    puntos.set_data(pos_x, pos_y)
    return ((puntos,))

############  se crea y se guarda el gif

anim = animation.FuncAnimation(fig, actualizar, frames=1000, interval=40, blit=True)
anim.save('boids.gif', writer='pillow', fps=25)
