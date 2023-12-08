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
        weight = random.randint(1, 40)
        G.add_edge(edge[0], edge[1], weight=weight)
    
    return G

def visualize_prim(graph, edges, node_colors, title="Prim's Algorithm"):
    pos = nx.spring_layout(graph)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [5, 1]})
    fig.suptitle(title, fontsize=20, style='oblique')

    visited_data = []  # List to store visited nodes and their total weight

    def update(frame, mst_edges, ax1, ax2):
        ax1.clear()

        # Initialize node colors to green
        node_colors = {node: 'g' for node in graph.nodes}

        # Highlight all visited nodes up to the current frame
        for edge in mst_edges[:frame + 1]:
            node_colors[edge[1]] = 'cyan'  # Color the visited node
            node_colors[edge[2]] = 'cyan'  # Color the visited node

        # Draw all edges in green
        nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=ax1, node_color=list(node_colors.values()))

        nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='green', width=2)


       # Add edge labels
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        #print("edge_labels", edge_labels)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        # Draw red edges for all visited edges
        for i in range(frame + 1):
            edge = mst_edges[i]
            nx.draw_networkx_edges(graph, pos, edgelist=[(edge[1], edge[2])], edge_color='r', width=2)

        visited_order_set = set()  # Initialize a set to track unique visited nodes
        total_weight = 0  # Initialize total weight

        # Create a dictionary to store cumulative weight for each node
        cumulative_weight = {node: 0 for node in graph.nodes}

        # Draw red edges for all visited edges and add edge labels
        for i in range(frame + 1):
            edge = mst_edges[i]

            # Update visited order set
            visited_order_set.add(edge[1])
            visited_order_set.add(edge[2])

            # Update cumulative weight
            total_weight += edge[0]
            cumulative_weight[edge[1]] += total_weight
            cumulative_weight[edge[2]] += total_weight

            # Add edge label
            #label_pos = (pos[edge[1]][0] + pos[edge[2]][0]) / 2, (pos[edge[1]][1] + pos[edge[2]][1]) / 2
            #ax1.text(label_pos[0], label_pos[1], str(edge[0]), color='black', fontweight='bold', ha='center', va='center')

        # Draw nodes with cyan color
        nx.draw_networkx_nodes(graph, pos, node_color=[node_colors[node] if node not in visited_order_set else 'cyan' for node in graph.nodes], node_size=700)

        # Add the visited data to the list
        visited_data.append((list(visited_order_set), cumulative_weight.copy()))

        # Draw the bar chart on ax2
        ax2.clear()
        unique_nodes = []  # Keep track of unique nodes
        current_x = 0
        for nodes, cumulative_weight in visited_data:
            for node in nodes:
                if node not in unique_nodes:
                    unique_nodes.append(node)
                    ax2.barh(0, 1, left=current_x, color='darkslategrey', alpha=0.7, height=0.6, edgecolor='black')
                    # Add label inside the bar with both the letter and cumulative weight
                    ax2.text(current_x + 0.5, 0, f"{node}\n{cumulative_weight[node]}", ha='center', va='center', color='white')
                    current_x += 1  # Move to the next "letter block"

        ax2.set_title('Visited Nodes Order')
        ax2.set_xlabel('Visit Order')
        ax2.set_yticks([])  # Remove y-axis ticks
        ax2.set_xlim(0, current_x)  # Set the x-axis limit based on the cumulative weight
        ax2.set_facecolor((0.9, 0.9, 0.9))  # Set the background color of the bar chart


    animation = FuncAnimation(fig, update, fargs=(edges, ax1, ax2), frames=len(edges), interval=400, repeat=False)
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
            #print("Visited Nodes:", visited_nodes)
            #print("MST Edges:", mst_edges)

    #print("Unvisited at end:", unvisited_nodes)
    #print("Visited at end: ", visited_nodes)
    return mst_edges, node_colors

# Example usage:
num_nodes = 12
num_edges = 30
print("START")
weighted_graph = create_weighted_graph(num_nodes, num_edges)
minimum_spanning_tree, node_colors = prim_algorithm(weighted_graph)
visualize_prim(weighted_graph, minimum_spanning_tree, node_colors)
print("DONE")