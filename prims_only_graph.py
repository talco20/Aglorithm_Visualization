import networkx as nx
import matplotlib.pyplot as plt
import random
import string
from matplotlib.animation import FuncAnimation

def create_weighted_graph(num_nodes, num_edges):
    G = nx.Graph()
    nodes = list(string.ascii_uppercase)[:num_nodes]
    G.add_nodes_from(nodes)
    
    for _ in range(num_edges):
        edge = random.sample(nodes, 2)
        weight = random.randint(1, 10)
        G.add_edge(edge[0], edge[1], weight=weight)
    
    return G

def visualize_prim(graph, edges, node_colors, title="Prim's Algorithm"):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle(title, fontsize=16)
    
    def update(frame, mst_edges):
        ax.clear()

        # Initialize node colors to green
        node_colors = {node: 'g' for node in graph.nodes}

        # Highlight all visited nodes up to the current frame
        for edge in mst_edges[:frame + 1]:
            node_colors[edge[1]] = 'cyan'  # Color the visited node
            node_colors[edge[2]] = 'cyan'  # Color the visited node

        # Draw all edges in green
        nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=ax, node_color=list(node_colors.values()))

        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)

        # Draw red edges for all visited edges
        for i in range(frame + 1):
            edge = mst_edges[i]
            nx.draw_networkx_edges(graph, pos, edgelist=[(edge[1], edge[2])], edge_color='r', width=2)

        # Draw nodes with cyan color
        nx.draw_networkx_nodes(graph, pos, node_color=[node_colors[node] for node in graph.nodes], node_size=700)

    animation = FuncAnimation(fig, update, fargs=(edges,), frames=len(edges), interval=300, repeat=False)
    plt.show()

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

            # Print information for debugging
            print("Visited Nodes:", visited_nodes)
            print("MST Edges:", mst_edges)

    print("Unvisited at end:", unvisited_nodes)
    print("Visited at end: ", visited_nodes)
    return mst_edges, node_colors

# Example usage:
num_nodes = 12
num_edges = 30
print("START")
weighted_graph = create_weighted_graph(num_nodes, num_edges)
print("MID")
minimum_spanning_tree, node_colors = prim_algorithm(weighted_graph)
print("Minimum Spanning Tree:", minimum_spanning_tree)
visualize_prim(weighted_graph, minimum_spanning_tree, node_colors)
print("DONE")