import tkinter as tk
import tkinter.messagebox
import customtkinter as ck
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from draw.mst_builder_and_vis import *

from algo_vis_terminal import *
from draw.draw_graph import *  
from draw.mst_builder_and_vis import *
from algorithms.dfs_algo import *
from algorithms.bfs_algo import *
from algorithms.top_sort import *
from algorithms.prims_algo import * 
from algorithms.kruskal_algo import *
from algorithms.dijkstra_algo import *
from algorithms.bellman_ford_algo_OnProgress import *

ck.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ck.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ck.CTk):
    def __init__(self):
        super().__init__()
        self.visited = []
        
        # configure window
        self.title("CustomTkinter Algorithm Visualization.py")
        self.geometry(f"{1100}x{620}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        
        # create sidebar frame with widgets
        self.sidebar_frame = ck.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(12, weight=1)
        self.logo_label = ck.CTkLabel(self.sidebar_frame, text="The Algorithm Vizualizer", font=ck.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.graph_type_label = ck.CTkLabel(self.sidebar_frame, text="Choose Graph Type:", font=ck.CTkFont(size=16, weight="bold"))
        self.graph_type_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Create a option menu for selecting the graph type
        #self.graph_types = ["BFS", "DFS", "Topological Sort", "Prim", "Kruskal", "Dijkstra", "Bellman-Ford"]
        self.graph_types = ["BFS", "DFS", "Topological Sort", "Prim", "Kruskal", "Dijkstra"]
        self.graph_type_var = tk.StringVar()
        self.graph_type_optionemenu = ck.CTkOptionMenu(self.sidebar_frame, values=self.graph_types,
                                                                       command=self.graph_type_var_changed)
        self.graph_type_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Num nodes and edges
        self.nodes_num_label = ck.CTkLabel(self.sidebar_frame, text="Choose Number Of Nodes:", font=ck.CTkFont(size=12, weight="bold"))
        self.nodes_num_label.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.nodes_box_optionmenu = ck.CTkOptionMenu(self.sidebar_frame, values=[str(x) for x in [10, 15, 20, 25]])
        self.nodes_box_optionmenu.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.edges_num_label = ck.CTkLabel(self.sidebar_frame, text="Choose Number Of Edges:", font=ck.CTkFont(size=12, weight="bold"))
        self.edges_num_label.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.edges_box_optionmenu = ck.CTkOptionMenu(self.sidebar_frame, values=[str(x) for x in [20, 25, 30, 35, 40, 45, 50]])
        self.edges_box_optionmenu.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")

        # Run Algorithm Button
        self.sidebar_button_runApp = ck.CTkButton(self.sidebar_frame, command=self.run_algorithm, text="Run Algorithm", textvariable='bold',
                                                   fg_color='red', hover_color='darkred')
        self.sidebar_button_runApp.grid(row=7, column=0, padx=20, pady=20, sticky="nsew")

        # Sidebar lower actions
        self.appearance_mode_label = ck.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.appearance_mode_optionemenu = ck.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.scaling_label = ck.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.scaling_optionemenu = ck.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # create plot frame
        self.plot_frame = ck.CTkFrame(self, corner_radius=0)
        self.plot_frame.grid(row=0, column=1, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)

    def validate_int(self, new_value):
        if new_value == "":
            return True
        return new_value.isdigit()
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ck.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ck.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def graph_type_var_changed(self, *args):
        if self.graph_type_optionemenu.get():
            print(f"Succeed to take the type, is: {self.graph_type_optionemenu.get()}")
        else:
             print("Failed to take the type")

    def update(self, frame, order, G, pos, visited, ax1, ax2):
        node = order[frame]
        visited.add(node)

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

    def visualize_prim(self, graph, edges, node_colors, title):
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.suptitle(title, fontsize=16)
        pos = nx.spring_layout(graph)
        
        visited_data = []

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

            visited_order_set = set()  # Initialize a set to track unique visited nodes
            total_weight = 0  # Initialize total weight

            # Create a dictionary to store cumulative weight for each node
            cumulative_weight = {node: 0 for node in graph.nodes}

            for i in range(frame + 1):
                edge = mst_edges[i]

                # Update visited order set
                visited_order_set.add(edge[1])
                visited_order_set.add(edge[2])

                # Update cumulative weight
                total_weight += edge[0]
                cumulative_weight[edge[1]] += total_weight
                cumulative_weight[edge[2]] += total_weight

            visited_data.append((list(visited_order_set), cumulative_weight.copy()))

            unique_nodes = []  # Keep track of unique nodes
            current_x = -0.8
            for nodes, cumulative_weight in visited_data:
                for node in nodes:
                    if node not in unique_nodes:
                        unique_nodes.append(node)
                        ax.text(current_x, -1.1, f"{node}\n{cumulative_weight[node]}", ha='left', va='bottom', color='blue')
                        current_x += 0.13

        animation = FuncAnimation(fig, update, fargs=(edges,), frames=len(edges), interval=300, repeat=False)
        # Delete the comment from the line below to save the animation as a gif
        #animation.save("animations/{}.gif".format(title), dpi=300, writer='pillow', fps=3)
        self.scatter1 = FigureCanvasTkAgg(fig, master=self)
        self.scatter1.get_tk_widget().grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.scatter1.draw()
        self.update_idletasks()

    def visualize_dijkstra(self, graph, distances, previous_nodes, start_node, algorithm_state, title="Dijkstra's Algorithm"):
        pos = nx.spring_layout(graph)
        fig, ax = plt.subplots(figsize=(8, 8))
        fixed_title = f"{title}\nStart Node: {start_node}"
        fig.suptitle(fixed_title, fontsize=16)

        visited_nodes_accumulated = set()

        def update(frame):
            current_node, visited_nodes, shortest_paths = algorithm_state[frame]

            # Add current visited nodes to the accumulated set
            visited_nodes_accumulated.update(visited_nodes)

            # Color the nodes based on whether they are part of the shortest path
            node_colors = ['cyan' if node in visited_nodes_accumulated else 'g' for node in graph.nodes]

            # Draw all edges in green
            nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=ax, node_color=node_colors)
            
            edge_labels = nx.get_edge_attributes(graph, "weight")
            nx.draw_networkx_edge_labels(graph, pos, edge_labels)

            # Draw red edges for the shortest paths
            for node, path_info in shortest_paths.items():
                if path_info is not None:
                    nx.draw_networkx_edges(graph, pos, edgelist=[(node, path_info)], edge_color='r', width=3.5)

                    # Add distance label next to the node
                    label_pos = pos[node] - 0.05
                    ax.text(
                        label_pos[0], label_pos[1],
                        f"{distances[node]}",
                        color='blue',
                        fontweight='bold',
                        ha='center',
                        va='center'
                    )

            # Add text for the start node with updated distance
            ax.text(
                pos[start_node][0]-0.05, pos[start_node][1]-0.05,
                f"0",
                color='blue',
                fontweight='bold',
                ha='center',
                va='center'
            )

        animation = FuncAnimation(fig, update, frames=len(algorithm_state), interval=1000, repeat=False)
        # Delete the comment from the line below to save the animation as a gif
        #animation.save("animations/{}.gif".format(title), dpi=300, writer='pillow', fps=3)
        self.scatter1 = FigureCanvasTkAgg(fig, master=self)
        self.scatter1.get_tk_widget().grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.scatter1.draw()
        self.update_idletasks()

    
    def visualize_search(self, order, title, G, pos, visited):
        self.fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        self.fig.suptitle(title, fontsize=20, style='oblique')

        self.animation = FuncAnimation(self.fig, self.update, frames=len(order),
                                       fargs=(order, G, pos, visited, ax1, ax2), interval=200, repeat=False)
        
        self.scatter1 = FigureCanvasTkAgg(self.fig, master=self)
        self.scatter1.get_tk_widget().grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.scatter1.draw()
        self.update_idletasks()

    def run_algorithm(self):
        # Get the selected graph type, nodes and edges
        self.nodes_entered = int(self.nodes_box_optionmenu.get())
        self.edges_entered = int(self.edges_box_optionmenu.get())
        graph_type_tmp = self.graph_type_optionemenu.get()
        graph_type = graph_type_tmp.upper()
        
        default_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('F', 'G'), ('E', 'G'),
                     ('B', 'G'), ('C', 'F'), ('B', 'H')]
        
        # Initialize the graph and run the selected algorithm
        if graph_type == 'BFS':
            self.run_bfs_algorithm()

        elif graph_type == 'DFS':
            self.run_dfs_algorithm()
                
        elif graph_type == 'TOPOLOGICAL SORT':
            self.run_topologic_sort()
                
        elif graph_type == 'PRIM':
            self.run_prim_algorithm()
                
        elif graph_type == 'KRUSKAL':
            self.run_kruskal_algorithm()
                
        elif graph_type == 'DIJKSTRA' or graph_type == 'DIJ':
            self.run_dijkstra_algorithm()
                
        elif graph_type == 'BELLMAN-FORD' or graph_type == 'BF':
            self.run_bellman_ford_algorithm()

    def run_bfs_algorithm(self):
        self.graph = nx.Graph()
        pos = nx.spring_layout(self.graph)
        additional_edges = add_edges_rand(self.edges_entered)
        self.graph.add_edges_from(additional_edges)
        start_node = get_start_node(self.graph)
        pos = nx.spring_layout(self.graph)  # Regenerate layout based on the updated graph

        order = order_bfs(self.graph, start_node)
        self.visited = set()
        vis = self.visualize_search(order, 'BFS Visualization', self.graph, pos, self.visited)
        
    def run_dfs_algorithm(self):
        self.graph = nx.Graph()
        pos = nx.spring_layout(self.graph)
        additional_edges = add_edges_rand(self.edges_entered)
        self.graph.add_edges_from(additional_edges)
        start_node = get_start_node(self.graph)
        pos = nx.spring_layout(self.graph)  # Regenerate layout based on the updated graph

        order = order_dfs(self.graph, start_node)
        visited = set()
        vis = self.visualize_search(order, 'DFS Visualization', self.graph, pos, visited)

    def run_topologic_sort(self):
        self.graph = nx.DiGraph()
        self.graph = add_edges_dag(self.edges_entered)
        start_node = get_start_node(self.graph)
        pos = nx.spring_layout(self.graph)

        order = top_sort(self.graph, start_node)
        visited = set()
        vis = self.visualize_search(order, 'Topological Sort',  self.graph, pos, visited)

    def run_prim_algorithm(self):
        node_user = self.nodes_entered
        edge_user = self.edges_entered

        self.graph = create_weighted_graph(node_user, edge_user)
        minimum_spanning_tree, node_colors = prim_algorithm(self.graph)
        vis = self.visualize_prim(self.graph, minimum_spanning_tree, node_colors, title="Prim's Algorithm")

    def run_kruskal_algorithm(self):
        node_user = self.nodes_entered
        edge_user = self.edges_entered

        self.graph = create_weighted_graph(node_user, edge_user)
        minimum_spanning_tree, node_colors = kruskal_algorithm(self.graph)
        vis = self.visualize_prim(self.graph, minimum_spanning_tree, node_colors, title="Kruskal's Algorithm")

    def run_dijkstra_algorithm(self):
        node_user = self.nodes_entered
        edge_user = self.edges_entered

        self.graph = create_weighted_graph(node_user, edge_user)
        start_node = random.choice(list(self.graph.nodes))
        distances, previous_nodes, algorithm_state = dijkstra_algorithm(self.graph, start_node)

        # Use the corrected function with algorithm_state
        vis = self.visualize_dijkstra(self.graph, distances, previous_nodes, start_node, algorithm_state, "Dijkstra's Algorithm")

    # def run_bellman_ford_algorithm(self):
    #     node_user = self.nodes_entered
    #     edge_user = self.edges_entered

    #     self.graph = create_weighted_graph_negatives(node_user, edge_user)
    #     start_node = random.choice(list(self.graph.nodes))
    #     distances, previous_nodes, algorithm_state = bellman_ford_algorithm(self.graph, start_node)

    #     # Use the corrected function with algorithm_state
    #     visualize_dijkstra(self.graph, distances, previous_nodes, start_node, algorithm_state, "Bellman-Ford's Algorithm")

    
if __name__ == "__main__":
    app = App()
    app.mainloop()