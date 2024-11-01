import random

# Definir el grafo como una lista de nodos y una lista de aristas con feromonas
edges = [
    {"nodes": (0, 1), "distance": 10},
    {"nodes": (1, 2), "distance": 15},
    {"nodes": (0, 2), "distance": 20},
    {"nodes": (1, 3), "distance": 10},
    {"nodes": (2, 3), "distance": 5}
]

# Inicializar las feromonas en cada arista
pheromones = {tuple(sorted(edge["nodes"])): 1 for edge in edges}

# Función para actualizar las feromonas
def update_pheromones():
    global pheromones
    for edge in pheromones:
        pheromones[edge] *= 0.9  # Factor de evaporación

# Función principal del algoritmo de colonia de hormigas
def run_optimization():
    global pheromones
    for _ in range(3):  # Número de hormigas
        current_node = 0
        path = []

        while current_node != 3:
            choices = [edge for edge in edges if current_node in edge["nodes"]]
            if not choices:
                break  # Si no hay elecciones, salir del bucle
            next_edge = max(choices, key=lambda edge: pheromones[tuple(sorted(edge["nodes"]))])
            next_node = next_edge["nodes"][1] if next_edge["nodes"][0] == current_node else next_edge["nodes"][0]
            path.append(tuple(sorted(next_edge["nodes"])))
            current_node = next_node

        # Actualizar feromonas en el camino
        for edge_nodes in path:
            pheromones[edge_nodes] += 1

    # Actualizar feromonas después de todas las hormigas
    update_pheromones()

    # Mostrar resultados
    print("Feromonas después de la optimización:", pheromones)

# Ejecutar la optimización
run_optimization()
