import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Configuración de parámetros ---
N = 50          # Tamaños de la cuadrícula (N x N)
INTERVALO = 100 # Tiempo entre fotogramas en milisegundos

# Inicializar cuadrícula con un tablero aleatorio (0 = muerta, 1 = viva)
# Densidad aproximada del 20% de celdas vivas
grid = np.random.choice([0, 1], size=(N, N), p=[0.8, 0.2])

# --- 2. Función para actualizar el estado del juego ---
def update(frame, img, grid, N):
    new_grid = grid.copy()
    
    for i in range(N):
        for j in range(N):
            # Calcular la suma de los 8 vecinos usando bordes periódicos (toroide)
            total = int((
                grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, j] + grid[(i - 1) % N, (j + 1) % N] +
                grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, j] + grid[(i + 1) % N, (j + 1) % N]
            ))
            
            # Reglas de Conway:
            # 1. Celda viva con < 2 o > 3 vecinos muere (soledad o sobrepoblación)
            # 2. Celda muerta con exactamente 3 vecinos nace (reproducción)
            if grid[i, j] == 1:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
                    
    # Actualizar los datos del gráfico y la matriz
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

# --- 3. Configuración de la animación con Matplotlib ---
fig, ax = plt.subplots(figsize=(7, 7))
img = ax.imshow(grid, cmap='binary', interpolation='nearest')
ax.set_title("Juego de la Vida de Conway")
ax.axis('off')

# Crear la animación paso a paso
ani = animation.FuncAnimation(
    fig, 
    update, 
    fargs=(img, grid, N), 
    frames=200, 
    interval=INTERVALO, 
    save_count=50
)

plt.tight_layout()
plt.show()