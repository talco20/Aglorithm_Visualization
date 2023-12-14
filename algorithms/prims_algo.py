# Prim's Algorithm 
# BigO - O(v^2)
# Storage - O(v+e)

from draw.mst_builder_and_vis import *

def prim_algorithm(graph):
    mst_edges = []
    visited_nodes = set()
    unvisited_nodes = set(graph.nodes)

    while unvisited_nodes:
        # Choose a random starting node not visited yet
        start_node = random.choice(list(unvisited_nodes))
        visited_nodes.add(start_node)
        unvisited_nodes.remove(start_node)

        while True:
            # Color the nodes based on whether they are visited or not
            node_colors = ['cyan' if n in visited_nodes else 'g' for n in graph.nodes]

            candidate_edges = []

            # Find edges connecting visited and unvisited nodes
            for node in visited_nodes:
                for neighbor in graph.neighbors(node):
                    if neighbor in unvisited_nodes:
                        candidate_edges.append((graph[node][neighbor]['weight'], node, neighbor))

            if not candidate_edges:
                break  # No more candidate edges, terminate the loop

            # Choose the minimum weight edge
            candidate_edges.sort()  # Sort edges by weight
            min_edge = candidate_edges.pop(0)  # Pop the minimum weight edge
            mst_edges.append(min_edge)

            # Add the new node to the visited set
            visited_nodes.add(min_edge[2])
            unvisited_nodes.remove(min_edge[2])

    return mst_edges, node_colors