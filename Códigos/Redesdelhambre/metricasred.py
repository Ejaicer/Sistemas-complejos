#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ejaicer
"""



import pandas as pd
import networkx as nx

####### Cargar matriz de interacciones y asignar tamaño del nodo dependiendo las menciones
df_matriz = pd.read_csv('matriz_interacciones_sinsajo.csv', index_col=0)
G = nx.from_pandas_adjacency(df_matriz)

df_apariciones = pd.read_csv('apariciones_personajes_sinsajo.csv')
dict_apariciones = dict(zip(df_apariciones['Personaje'], df_apariciones['Apariciones']))
nx.set_node_attributes(G, dict_apariciones, name='apariciones')

####### Calculo de Medidas
grado = dict(G.degree())
grado_ponderado = dict(G.degree(weight='weight'))
betweenness = nx.betweenness_centrality(G, weight='weight')
closeness = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)

###### Generacion de la tabla de datos
df_metricas = pd.DataFrame({
    'Personaje': df_matriz.index,
    'Apariciones': [dict_apariciones.get(node, 0) for node in df_matriz.index],
    'Grado': [grado.get(node, 0) for node in df_matriz.index],
    'Grado Ponderado': [grado_ponderado.get(node, 0) for node in df_matriz.index],
    'Intermediación': [round(betweenness.get(node, 0), 4) for node in df_matriz.index],
    'Cercanía': [round(closeness.get(node, 0), 4) for node in df_matriz.index],
})

df_metricas = df_metricas.sort_values(by='Apariciones', ascending=False)

###########Exportar en una tabla para html

# Tabla HTML limpia con clases para CSS
tabla_html = df_metricas.to_html(
    index=False, 
    classes='tabla-metricas-red', 
    border=0
)

with open('metricas_sinsajo.html', 'w', encoding='utf-8') as f:
    f.write(tabla_html)

#############exportar en csv
#df_metricas.to_csv('metricas_red.csv', index=False, encoding='utf-8')
