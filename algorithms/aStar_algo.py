import heapq
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from draw.mst_builder_and_vis import *
from draw.draw_graph import *

def astar_algorithm(graph, start, goal, heuristic_func):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}

    # Priority queue for nodes with their distances
    priority_queue = [(0 + heuristic_func(graph, start, goal), 0, start)]

    algorithm_state = []  # Store the state at each step

    while priority_queue:
        _, current_distance, current_node = heapq.heappop(priority_queue)

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
                heapq.heappush(priority_queue, (new_distance + heuristic(graph, neighbor, goal), new_distance, neighbor))

                visited_nodes.append(neighbor)
                shortest_paths[neighbor] = current_node

        algorithm_state.append((current_node, visited_nodes, shortest_paths))

    return distances, previous_nodes, algorithm_state

def heuristic(G, node, goal):
    # Simple heuristic function (number of edges between nodes)
    return nx.shortest_path_length(G, source=node, target=goal)

# def visualize_astar(graph, distances, previous_nodes, start, goal, algorithm_state, title="A* Algorithm"):
#     pos = nx.spring_layout(graph)
#     fig, ax = plt.subplots(figsize=(8, 8))
#     fig.suptitle(f"{title} \n Start Node is: {start}, Goal node is: {goal}", fontsize=16)

#     def update(frame):
#         current_node, visited_nodes, shortest_paths = algorithm_state[frame]

#         # Color the nodes based on whether they are part of the shortest path
#         node_colors = ['cyan' if node in visited_nodes else 'yellow' if node == start else 'darkgoldenrod' if node == goal else 'g' for node in graph.nodes]

#         # Draw all edges in green
#         nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=ax, node_color=node_colors)

#         # Draw edge weights
#         edge_labels = nx.get_edge_attributes(graph, "weight")
#         nx.draw_networkx_edge_labels(graph, pos, edge_labels)

#         # Draw green edges for the final shortest path
#         if goal in shortest_paths and shortest_paths[goal] is not None:
#             shortest_path_nodes = nx.shortest_path(graph, source=start, target=goal, weight='weight')
#             shortest_path_edges = [(shortest_path_nodes[i], shortest_path_nodes[i+1]) for i in range(len(shortest_path_nodes)-1)]
#             nx.draw_networkx_edges(graph, pos, edgelist=shortest_path_edges, edge_color='green', width=4)

#             # Add distance label next to the nodes on the final shortest path
#             for node in shortest_path_nodes:
#                 label_pos = pos[node] - 0.05
#                 ax.text(
#                     label_pos[0], label_pos[1],
#                     f"{distances[node]}",
#                     color='blue',
#                     fontweight='bold',
#                     ha='center',
#                     va='center'
#                 )

#     animation = FuncAnimation(fig, update, frames=len(algorithm_state), interval=500, repeat=False)
#     plt.show()

# Example usage:
# num_nodes = 10
# num_edges = 22
# graph = create_weighted_graph(num_nodes, num_edges)
# start_node = get_start_node(graph)
# goal_node = random.choice(list(graph.nodes))
# distances, previous_nodes, algorithm_state = astar_algorithm(graph, start_node, goal_node, heuristic)
# print(graph.edges)
# print(graph.degree)
# # Use the corrected function with algorithm_state
# visualize_astar(graph, distances, previous_nodes, start_node, goal_node, algorithm_state, "A* Algorithm")
