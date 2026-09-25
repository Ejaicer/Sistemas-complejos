# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:24:36 2026

@author: ejaic
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Configuración de parámetros
N = 50          
INTERVALO = 100 
grid = np.random.choice([0, 1], size=(N, N), p=[0.8, 0.2])

# 2. Función de actualización
def update(frame, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((
                grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, j] + grid[(i - 1) % N, (j + 1) % N] +
                grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, j] + grid[(i + 1) % N, (j + 1) % N]
            ))
            if grid[i, j] == 1:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
                    
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

# 3. Configuración de la figura
fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(grid, cmap='binary', interpolation='nearest')
ax.set_title("Juego de la Vida de Conway")
ax.axis('off')

# 4. Crear la animación
ani = animation.FuncAnimation(
    fig, 
    update, 
    fargs=(img, grid, N), 
    frames=100,          # Número total de fotogramas a guardar en el GIF
    interval=INTERVALO, 
    blit=True
)

# 5. Guardar como archivo GIF
print("Guardando animación GIF...")
ani.save('juego_de_la_vida.gif', writer='pillow', fps=10)
print("¡GIF guardado con éxito como 'juego_de_la_vida.gif'!")

plt.close() # Cierra la figura en lugar de mostrarla en pantalla