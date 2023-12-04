from dfs_algo import *
from bfs_algo import *
from top_sort import *
from draw_graph import *   
    
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
                        #G = add_edges_dag(10)
        else:
            G.add_edges_from(default_edges)
    return G

def search_and_visualize():
    print("******************************************************************************************************************")
    
    visited = []

    default_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('F', 'G'), ('E', 'G'),
                     ('B', 'G'), ('C', 'F'), ('B', 'H')]
    
    search_type = input("Choose search type (BFS or DFS or TOP): ").upper()

    if search_type == 'BFS':
        G = nx.Graph()
        pos = nx.spring_layout(G)
        G = choose_graph_size(G, default_edges, 'BFS')
        start_node = get_start_node(G)
        print("The start node is: ", start_node)
        pos = nx.spring_layout(G)  # Regenerate layout based on the updated graph

        order = order_bfs(G, start_node)
        visualize_search(order, 'BFS Visualization', G, pos, visited)

    elif search_type == 'DFS':
        G = nx.Graph()
        pos = nx.spring_layout(G)
        G = choose_graph_size(G, default_edges, 'DFS')
        start_node = get_start_node(G)
        print("The start node is: ", start_node)
        pos = nx.spring_layout(G)  # Regenerate layout based on the updated graph

        order = order_dfs(G, start_node)
        visualize_search(order, 'DFS Visualization', G, pos, visited)

    elif search_type == 'TOP':
        DAG = nx.DiGraph()
        DAG = choose_graph_size(DAG, default_edges, 'TOP')
        start_node = get_start_node(DAG)
        print("The start node is: ", start_node)
        pos = nx.spring_layout(DAG)

        order = top_sort(DAG, start_node)
        visualize_search(order, 'Topological Sort', DAG, pos, visited)
    else:
        print("Invalid search type. Please choose BFS, DFS or TOP.")

    visited.pop(0)

    if search_type == 'TOP':
        print("The graph's specs:", DAG)
    else:     
        print("The graph's specs:", G)
    
    print("Visited nodes:", visited)
    print("******************************************************************************************************************")
    
# Call the function
search_and_visualize()