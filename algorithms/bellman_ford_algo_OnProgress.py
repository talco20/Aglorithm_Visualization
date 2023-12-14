from draw.mst_builder_and_vis import *

import heapq

def bellman_ford_algorithm(graph, source):
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    previous_nodes = {node: None for node in graph.nodes}

    algorithm_state = []  # Store the state at each step

    # Relax edges repeatedly |V| - 1 times
    for _ in range(len(graph.nodes) - 1):
        for edge in graph.edges:
            current_node, neighbor = edge
            weight = graph[current_node][neighbor]['weight']
            new_distance = distances[current_node] + weight

            # Relaxation step
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

                visited_nodes = [current_node, neighbor]  # Track visited nodes at this step
                shortest_paths = {neighbor: current_node}  # Track the shortest path at this step

                algorithm_state.append((current_node, visited_nodes, shortest_paths))

    # Check for negative weight cycles during the last iteration
    for edge in graph.edges:
        current_node, neighbor = edge
        weight = graph[current_node][neighbor]['weight']
        new_distance = distances[current_node] + weight

        # Relaxation step
        if new_distance < distances[neighbor]:
            print("Graph contains a negative weight cycle")
            #raise ValueError("Graph contains a negative weight cycle")

    return distances, previous_nodes, algorithm_state