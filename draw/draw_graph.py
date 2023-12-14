import random
from matplotlib.lines import Line2D
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import string

def update(frame, order, G, pos, visited, ax1, ax2):
    node = order[frame]
    visited.append(node)

    ax1.clear()
    ax2.clear()

    # Draw the graph
    node_colors = ['cyan' if n in visited else 'g' for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', ax=ax1)
    ax1.set_title('Graph')

    # Add a legend to ax1
    ax1.legend(handles=[
        Line2D([0], [0], marker='o', color='w', markerfacecolor='cyan', markersize=10, label='Visited Node'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Unvisited Node')
    ], loc='upper right', bbox_to_anchor=(1.0, 1.0))

    # Update the bar chart
    visited_counts = {node: order.index(node) + 1 for node in string.ascii_uppercase if node in order}
    
    # Create a sorted version of visited_counts
    sorted_visited_counts = dict(sorted(visited_counts.items(), key=lambda x: x[1]))
    sorted_visited_counts = {node: 1 for node in sorted_visited_counts}

    # Create a stacked horizontal bar chart
    stacked_bar_colors = [[0, 0, 0] for _ in sorted_visited_counts]  # Initialize colors to black
    current_x = 0

    for node, width in sorted_visited_counts.items():
        ax2.barh(0, width, left=current_x, color='darkslategrey', alpha=0.7, height=0.6, edgecolor='black')  # Set color to blue
        current_x += width

        # Add label inside the bar
        ax2.text(current_x - width / 2, 0, node, ha='center', va='center', color='white')

    ax2.set_title('Visited Nodes Order')
    ax2.set_xlabel('Visit Order')
    ax2.set_yticks([])  # Remove y-axis ticks
    ax2.set_xlim(0, len(order))  # Set the x-axis limit based on the number of nodes
    ax2.set_facecolor((0.9, 0.9, 0.9))  # Set the background color of the bar chart

def visualize_search(order, title, G, pos, visited):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(title, fontsize=20, style='oblique')
    
    animation = FuncAnimation(fig, update, frames=len(order), fargs=(order, G, pos, visited, ax1, ax2), interval=200, repeat=False)
    
    # Delete the comment from the line below to save the animation as a gif
    #animation.save("animations/{}.gif".format(title), dpi=300, writer='pillow', fps=3)
    #plt.show()
    return ax1,ax2

# Randomize the creation of edges
def add_edges_rand(num):
    add_edges = []
    for _ in range(num):
        edge = (random.choice(string.ascii_uppercase), random.choice(string.ascii_uppercase))
        add_edges.append(edge)
    return add_edges

# Randomize the creation of edges to create a Directed Acyclic Graph (DAG)
def add_edges_dag(num_edges):
    # Create an empty directed graph
    G = nx.DiGraph()

    # Generate a list of uppercase letters as nodes
    nodes = list(string.ascii_uppercase)

    # Randomly shuffle the nodes
    random.shuffle(nodes)

    # Add edges to the graph while ensuring it remains a DAG
    for i in range(min(num_edges, len(nodes) - 1)):
        # Determine the number of outgoing edges for the current node
        num_outgoing_edges = random.randint(1, min(3, len(nodes) - i - 1))

        # Add outgoing edges from the current node
        for j in range(num_outgoing_edges):
            next_node_index = i + 1 + random.randint(0, len(nodes) - i - 2)
            G.add_edge(nodes[i], nodes[next_node_index])

    return G

# Returns the starting node of the graph
def get_start_node(graph):
    try:
        first_edge = next(iter(graph.edges))
        start_node = first_edge[0]
        return start_node
    except StopIteration:
        print("The graph is empty. Please add edges.")
        return None
