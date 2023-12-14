# Dijkstra's Algorithm 
# BigO - O(v^2)
# Storage - O(v + e log v)

import heapq
from draw.mst_builder_and_vis import *

def dijkstra_algorithm(graph, source):
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    previous_nodes = {node: None for node in graph.nodes}

    # Priority queue for nodes with their distances
    priority_queue = [(0, source)]

    algorithm_state = []  # Store the state at each step

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Check if the current path to the node is shorter than the known distance
        if current_distance > distances[current_node]:
            continue

        visited_nodes = [current_node]  # Track visited nodes at this step
        shortest_paths = {current_node: None}  # Track the shortest path at this step

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            new_distance = distances[current_node] + weight

            # Relaxation step
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

                visited_nodes.append(neighbor)
                shortest_paths[neighbor] = current_node

        algorithm_state.append((current_node, visited_nodes, shortest_paths))

    return distances, previous_nodes, algorithm_state

# Example usage:
#num_nodes = 15
#num_edges = 30
#weighted_graph = create_weighted_graph(num_nodes, num_edges)
#start_node = random.choice(list(weighted_graph.nodes))
#distances, previous_nodes, algorithm_state = dijkstra_algorithm(weighted_graph, start_node)

# Use the corrected function with algorithm_state
#visualize_dijkstra(weighted_graph, distances, previous_nodes, start_node, algorithm_state, "Dijkstra's Algorithm")