#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 02:22:25 2026

@author: ejaicer
Para algunas partes de este código se utilizó IA, las cuales fueron modificadas
para las necesidades de este trabajo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


############3 cofiguración juego de la vida de conway
def gof(grid):
    
    ############# vecindad de moore, es decir, todos los vecinos son aquellos que
    ### rodean la celda actual, contando las diagonales
    vecinos = (
        np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )
    ###### reglas del juego de la vida de Conway
    siguiente_grid = np.zeros_like(grid)
    ########## si la celula esta viva y tiene 2 o 3 vecinos vivos: sobrevive
    siguiente_grid[(grid == 1) & ((vecinos == 2) | (vecinos == 3))] = 1
    ########## si una celula está muerta y tiene exactamente tres vecinos vivos: revive
    siguiente_grid[(grid == 0) & (vecinos == 3)] = 1

    return siguiente_grid

####################3 parámetros figura
N = 50
grid = np.random.choice([0, 1], size=(N, N), p=[0.8, 0.2]) #### condición inicial aleatoria

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(grid, cmap='Accent')
ax.axis('off')

##### función que actualiza cada frame utilizando las reglas del juego de la vida
def actualizar(frame):
    global grid
    grid = gof(grid)
    im.set_array(grid)
    ax.set_title(f"Paso {frame}", fontsize=12)
    return [im]

############  se crea y se guarda el gif
anim = FuncAnimation(fig, actualizar, frames=100, interval=100, blit=True)
anim.save("conway.gif", writer="pillow", fps=10)
plt.show()




