from draw.draw_graph import *  
from draw.mst_builder_and_vis import *
from algorithms.dfs_algo import *
from algorithms.bfs_algo import *
from algorithms.top_sort import *
from algorithms.prims_algo import * 
from algorithms.kruskal_algo import *
from algorithms.dijkstra_algo import *
from algorithms.bellman_ford_algo_OnProgress import *
    
def choose_graph_size(G, default_edges, type):
    search_size = input("If you want a small graph, enter S; for a big graph, enter B: ").upper()

    if search_size == 'B':
        while True:
            additional_edges = input("Please enter the number of edges you want (max is 60): ")
            try:
                edges_count = int(additional_edges)
                if edges_count <= 60:
                    print(f"You entered {edges_count} edges. Proceeding...")
                    if type == 'TOP':
                        G = add_edges_dag(edges_count)
                    else:
                        additional_edges = add_edges_rand(edges_count)
                        G.add_edges_from(additional_edges)
                    break  # Exit the loop if a valid value is provided
                else:
                    print("Invalid number of edges. Please enter a value below 60.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:
        if type == 'TOP':
                        dag_default_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('E', 'G'),
                                             ('B', 'F'), ('C', 'F'), ('B', 'H')]
                        G.add_edges_from(dag_default_edges)
        else:
            G.add_edges_from(default_edges)
    return G

def get_data_for_mst_algos():
    node_user = 0
    edge_user = 0
    while True:
        node_input = input("Enter number of nodes: ").upper()
        edge_input = input("Enter number of edges: ").upper()
        try:
            node_user = int(node_input)
            edge_user = int(edge_input)
            if edge_user >= 2*node_user:
                print(f"You entered {node_user} nodes and {edge_user} edges. Proceeding...")
                break  # Exit the loop if a valid value is provided
            else:
                print("Invalid number of nodes and edges.")
        except ValueError:
                print("Invalid input. Please enter a valid number.")
    return node_user, edge_user

def search_and_visualize():
    print("******************************************************************************************************************")
    
    visited = []

    default_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('F', 'G'), ('E', 'G'),
                     ('B', 'G'), ('C', 'F'), ('B', 'H')]
    
    while True:
        try:
            search_type = input("Choose search type (BFS or DFS or TOP or PRIM or KRUSKAL or DIJKSTRA[DIJ] or BELLMAN-FORD[BF]): ").upper()

            if search_type == 'BFS':
                G = nx.Graph()
                pos = nx.spring_layout(G)
                G = choose_graph_size(G, default_edges, 'BFS')
                start_node = get_start_node(G)
                print("The start node is: ", start_node)
                pos = nx.spring_layout(G)  # Regenerate layout based on the updated graph

                order = order_bfs(G, start_node)
                visualize_search(order, 'BFS Visualization', G, pos, visited)
                break

            elif search_type == 'DFS':
                G = nx.Graph()
                pos = nx.spring_layout(G)
                G = choose_graph_size(G, default_edges, 'DFS')
                start_node = get_start_node(G)
                print("The start node is: ", start_node)
                pos = nx.spring_layout(G)  # Regenerate layout based on the updated graph

                order = order_dfs(G, start_node)
                visualize_search(order, 'DFS Visualization', G, pos, visited)
                break

            elif search_type == 'TOP':
                DAG = nx.DiGraph()
                DAG = choose_graph_size(DAG, default_edges, 'TOP')
                start_node = get_start_node(DAG)
                print("The start node is: ", start_node)
                pos = nx.spring_layout(DAG)

                order = top_sort(DAG, start_node)
                visualize_search(order, 'Topological Sort', DAG, pos, visited)
                break

            elif search_type == 'PRIM':
                print("For Prim's algorithm please enter number of nodes and edges,\nedges should be more than 2 times the number of nodes.")
                node_user, edge_user = get_data_for_mst_algos()

                G = create_weighted_graph(node_user, edge_user)
                minimum_spanning_tree, node_colors = prim_algorithm(G)
                visualize_prim(G, minimum_spanning_tree, node_colors, title="Prim's Algorithm")
                break

            elif search_type == 'KRUSKAL':
                print("For Kruskal's algorithm please enter number of nodes and edges,\nedges should be more than 2 times the number of nodes.")
                node_user, edge_user = get_data_for_mst_algos()

                G = create_weighted_graph(node_user, edge_user)
                minimum_spanning_tree, node_colors = kruskal_algorithm(G)
                visualize_prim(G, minimum_spanning_tree, node_colors, title="Kruskal's Algorithm")
                break

            elif search_type == 'DIJKSTRA' or search_type == 'DIJ':
                print("For Dijkstra's algorithm please enter number of nodes and edges,\nedges should be more than 2 times the number of nodes.")
                node_user, edge_user = get_data_for_mst_algos()

                G = create_weighted_graph(node_user, edge_user)
                start_node = random.choice(list(G.nodes))
                distances, previous_nodes, algorithm_state = dijkstra_algorithm(G, start_node)

                # Use the corrected function with algorithm_state
                visualize_dijkstra(G, distances, previous_nodes, start_node, algorithm_state, "Dijkstra's Algorithm")
                break

            elif search_type == 'BELLMAN-FORD' or search_type == 'BF':
                print("For Bellman-Ford's algorithm please enter number of nodes and edges,\nedges should be more than 2 times the number of nodes.")
                node_user, edge_user = get_data_for_mst_algos()

                G = create_weighted_graph_negatives(node_user, edge_user)
                start_node = random.choice(list(G.nodes))
                distances, previous_nodes, algorithm_state = bellman_ford_algorithm(G, start_node)

                # Use the corrected function with algorithm_state
                visualize_dijkstra(G, distances, previous_nodes, start_node, algorithm_state, "Bellman-Ford's Algorithm")
                break
        except ValueError as ve:
            print(f"ValueError: {ve}")
            print("Invalid input. Please enter a valid value.")    
    
    if search_type != 'PRIM' and search_type != 'KRUSKAL' and search_type != 'DIJKSTRA' and search_type != 'DIJ' and search_type != 'BELLMAN-FORD' and search_type != 'BF':
        visited.pop(0)
        print("Visited nodes:", visited)

    if search_type == 'TOP':
        print("The graph's specs:", DAG)
    else:     
        print("The graph's specs:", G)
        
    print("******************************************************************************************************************")
    
# Call the function
#search_and_visualize()