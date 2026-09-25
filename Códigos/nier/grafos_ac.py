# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:27:40 2026

@author: ejaic
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# 1. Parámetros
regla = 90       # Ejemplo: Regla 30
n_cell = 5       # Número de celdas (usamos un valor pequeño como 4 para visualizar $2^4 = 16$ estados)

# 2. Convertir la regla a binario (8 bits)
r_bin = format(regla, "08b")
bits_R = [int(bit) for bit in r_bin]
vecindarios = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]

def aplicar_regla(estado_actual):
    """Aplica la regla del autómata celular a un estado global con condiciones de frontera periódicas (toroide)."""
    nuevo_estado = np.zeros(n_cell, dtype=int)
    for c in range(n_cell):
        # Manejo de bordes periódicos (el último vecino se conecta con el primero)
        izq = estado_actual[(c - 1) % n_cell]
        cen = estado_actual[c]
        der = estado_actual[(c + 1) % n_cell]
        
        for i in range(8):
            if (izq, cen, der) == vecindarios[i]:
                nuevo_estado[c] = bits_R[i]
                break
    return nuevo_estado

# 3. Construcción del Espacio de Estados y Matriz de Adyacencia
num_estados = 2**n_cell
matriz_adyacencia = np.zeros((num_estados, num_estados), dtype=int)

# Generar todos los estados posibles de 0 a 2^N - 1
for i in range(num_estados):
    # Convertir el número entero i a un vector binario de n_cell celdas
    bin_str = format(i, f'0{n_cell}b')
    estado_vector = np.array([int(b) for b in bin_str])
    
    # Calcular el estado siguiente
    siguiente_vector = aplicar_regla(estado_vector)
    
    # Convertir el vector siguiente de nuevo a entero (índice j)
    j = int("".join(map(str, siguiente_vector)), 2)
    
    # Transición de i -> j
    matriz_adyacencia[i, j] = 1

print(f"Matriz de Adyacencia ({num_estados}x{num_estados}):")
print(matriz_adyacencia)

# 4. Graficar el Grafo de Transiciones con NetworkX
G = nx.DiGraph(matriz_adyacencia) # Grafo Dirigido

################################## Calculos
num_estados = 2**n_cell

for i in range(num_estados):
    bin_str = format(i, f'0{n_cell}b')
    estado_vector = np.array([int(b) for b in bin_str])
    siguiente_vector = aplicar_regla(estado_vector)
    j = int("".join(map(str, siguiente_vector)), 2)
    G.add_edge(i, j)

# --- 3. Extracción de Atractores, Períodos y Cuencas ---

# A. Encontrar todos los ciclos simples (Atractores)
atractores = list(nx.simple_cycles(G))

print(f"=== RESULTADOS PARA REGLA {regla} ({n_cell} CELDAS) ===")
print(f"• Número de atractores (ciclos): {len(atractores)}\n")

# B. Analizar cada atractor y su cuenca de atracción
G_inv = G.reverse()  # Invertimos las aristas para rastrear qué nodos llegan a cada atractor

for idx, atractor in enumerate(atractores, start=1):
    # 1. Período del atractor (longitud del ciclo)
    periodo = len(atractor)
    
    # 2. Tamaño de la cuenca de atracción:
    # Se obtienen todos los nodos alcanzables desde los nodos del atractor en el grafo invertido
    nodos_cuenca = set()
    for nodo in atractor:
        # nx.descendants en G_inv equivale a los ancestros en G
        ancestros = nx.descendants(G_inv, nodo)
        nodos_cuenca.update(ancestros)
    nodos_cuenca.update(atractor)  # Incluir los propios nodos del atractor
    
    tamano_cuenca = len(nodos_cuenca)
    
    # Representación en binario de los nodos del atractor
    atractor_bin = [format(nodo, f'0{n_cell}b') for nodo in atractor]
    
    print(f"Atractor #{idx}:")
    print(f"  - Estados del atractor (binario): {atractor_bin}")
    print(f"  - Estados del atractor (decimal): {atractor}")
    print(f"  - Período: {periodo}")
    print(f"  - Tamaño de la cuenca de atracción: {tamano_cuenca} estados ({tamano_cuenca / num_estados * 100:.1f}% del espacio de estados)")
    print("-" * 50)


######################## grafo

# Etiquetas en formato binario para los nodos (ej. '0101')
#labels = {i: format(i, f'0{n_cell}b') for i in range(num_estados)}
labels = {i: str(i) for i in range(num_estados)}

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=1024)
nx.draw_networkx_nodes(G, pos, node_size=150, node_color='thistle')
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color='gray')
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_weight='bold')

plt.title(f"Grafo de Transición de Estados - Regla {regla} ({n_cell} celdas)")
plt.axis('off')
plt.tight_layout()
plt.show()