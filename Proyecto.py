import networkx as nx
import matplotlib.pyplot as plt

# Definición de las actividades y sus duraciones
actividades = {
    'A': {'duración': 7, 'predecesoras': []},
    'B': {'duración': 3, 'predecesoras': ['A']},
    'C': {'duración': 6, 'predecesoras': []},
    'D': {'duración': 3, 'predecesoras': ['C']},
    'E': {'duración': 2, 'predecesoras': ['B', 'D']}
}

# Crear el gráfico dirigido
G = nx.DiGraph()

# Añadir nodos y aristas al gráfico
for actividad, info in actividades.items():
    G.add_node(actividad, duración=info['duración'])
    for predecesora in info['predecesoras']:
        G.add_edge(predecesora, actividad)

# Función para calcular las fechas de inicio y finalización
def calcular_fechas(G):
    # Calcular las fechas de inicio y finalización más tempranas
    for nodo in nx.topological_sort(G):
        predecesores = list(G.predecessors(nodo))
        if predecesores:
            G.nodes[nodo]['ES'] = max([G.nodes[p]['EF'] for p in predecesores])
        else:
            G.nodes[nodo]['ES'] = 0
        G.nodes[nodo]['EF'] = G.nodes[nodo]['ES'] + G.nodes[nodo]['duración']

    # Calcular las fechas de inicio y finalización más tardías
    for nodo in reversed(list(nx.topological_sort(G))):
        sucesores = list(G.successors(nodo))
        if sucesores:
            G.nodes[nodo]['LF'] = min([G.nodes[s]['LS'] for s in sucesores])
        else:
            G.nodes[nodo]['LF'] = G.nodes[nodo]['EF']
        G.nodes[nodo]['LS'] = G.nodes[nodo]['LF'] - G.nodes[nodo]['duración']

    # Calcular holgura y determinar la ruta crítica
    ruta_crítica = []
    for nodo in G.nodes:
        G.nodes[nodo]['holgura'] = G.nodes[nodo]['LS'] - G.nodes[nodo]['ES']
        if G.nodes[nodo]['holgura'] == 0:
            ruta_crítica.append(nodo)

    return ruta_crítica

ruta_crítica = calcular_fechas(G)

# Visualización de la red del proyecto
pos = nx.spring_layout(G)
etiquetas = {nodo: f"{nodo}\n{G.nodes[nodo]['ES']}/{G.nodes[nodo]['EF']}\n{G.nodes[nodo]['LS']}/{G.nodes[nodo]['LF']}" for nodo in G.nodes}

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, labels=etiquetas, node_size=3000, node_color='lightblue', font_size=8, font_weight='bold')
nx.draw_networkx_nodes(G, pos, nodelist=ruta_crítica, node_color='orange')
plt.title("Red del Proyecto de Mantenimiento de Dos Máquinas\n(Valores: ES/EF, LS/LF)")
plt.show()

# Mostrar los resultados en una tabla
import pandas as pd

resultados = []
for nodo in G.nodes:
    resultados.append({
        'Actividad': nodo,
        'Inicio más temprano (ES)': G.nodes[nodo]['ES'],
        'Inicio más tardío (LS)': G.nodes[nodo]['LS'],
        'Terminación más temprana (EF)': G.nodes[nodo]['EF'],
        'Terminación más tardía (LF)': G.nodes[nodo]['LF'],
        'Holgura (LS - ES)': G.nodes[nodo]['holgura'],
        '¿Ruta crítica?': 'Sí' if G.nodes[nodo]['holgura'] == 0 else 'No'
    })

df_resultados = pd.DataFrame(resultados)
print(df_resultados)
