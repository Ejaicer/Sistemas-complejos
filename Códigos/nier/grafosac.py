# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:27:40 2026

@author: ejaic

Para algunas partes de este código se utilizó IA, las cuales fueron modificadas
para las necesidades de este trabajo
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

################ Parámetros
regla = int(input("Da un valor de regla entre 0 y 255: "))

while regla < 0 or regla > 255:
  print("Debe ser un número entre 0 y 255.")
  regla = int(input("Da un valor con las condiciones que se piden: "))

n_cell = int(input("Número de celdas por renglón: "))

#######vecindad radio r=2
vecindarios = [(1,1,1), (1,1,0), (1,0,1), (1,0,0), (0,1,1), (0,1,0), (0,0,1), (0,0,0)]

############ Conversión a binario y convertimos cada carácter en entero

r_bin = format(regla,"08b") ###convertimos la regla a usar a código binario


######## generamos el vector que contiene como entradas los dígitos de la regla en binario
bits_R =[]
for i in range(0,8):
  bit = int(r_bin[i])
  bits_R.append(bit)


################# evolución de la matriz
def aplicar_regla(estado_actual):
    ####### condicones de frontera periodicas
    nuevo_estado = np.zeros(n_cell, dtype=int)
    for c in range(n_cell):
        izq = estado_actual[(c - 1) % n_cell]
        cen = estado_actual[c]
        der = estado_actual[(c + 1) % n_cell]
        
        for i in range(8):
            if (izq, cen, der) == vecindarios[i]:
                nuevo_estado[c] = bits_R[i]
                break
    return nuevo_estado

#############3 parámetros matriz de adyacencia para el grafo
ne = 2**n_cell   #### 2^{n} estados posibles
M_a = np.zeros((ne, ne), dtype=int) #### matriz de adyacencia

############################ generación de la matriz de adyacencia
for i in range(ne):
    bin_str = format(i, f'0{n_cell}b')
    estado_vector = np.array([int(b) for b in bin_str])
    
    # Calcular el estado siguiente
    siguiente_vector = aplicar_regla(estado_vector)
    
    # Convertir el vector siguiente de nuevo a entero (índice j)
    j = int("".join(map(str, siguiente_vector)), 2)
    
    # Transición de i -> j
    M_a[i, j] = 1

print(f"Matriz de Adyacencia ({ne}x{ne}):")
print(M_a)

############### grafo a partir de la matriz de adyacencia
G = nx.DiGraph(M_a) # Grafo Dirigido

################################## Calculos

for i in range(ne):
    bin_str = format(i, f'0{n_cell}b')
    estado_vector = np.array([int(b) for b in bin_str])
    siguiente_vector = aplicar_regla(estado_vector)
    j = int("".join(map(str, siguiente_vector)), 2)
    G.add_edge(i, j)

############# Se utilizó la libreria networkx para estudiar los grafos, pues es una 
### libreria dedicada para trabajar con redes.

atractores = list(nx.simple_cycles(G)) ######### encuentra ciclos

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
    print(f"  - Tamaño de la cuenca de atracción: {tamano_cuenca} estados ({tamano_cuenca / ne * 100:.1f}% del espacio de estados)")
    print("-" * 50)


######################## grafo


labels = {i: str(i) for i in range(ne)} ####las etiquetas se muestran en valor
#### decimal para optimizar el espacio

#################### parámetros grafo
plt.figure(figsize=(16, 16))
pos = nx.spring_layout(G, k = 0.3, iterations = 100, seed= 100)
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='thistle')
nx.draw_networkx_edges(G, pos,width = 0.3, arrowstyle='->', arrowsize=5, edge_color='gray')
nx.draw_networkx_labels(G, pos, labels=labels, font_size=3, font_weight='bold')


##### parámetros imagen
plt.title(f"Grafo de Transición de Estados - Regla {regla} ({n_cell} celdas)")
plt.axis('off')
plt.tight_layout()
plt.savefig(fr'grafo_r{regla}_n{n_cell}.png', dpi = 300)
plt.show()