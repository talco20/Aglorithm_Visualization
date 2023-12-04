from dfs_algo import *
from bfs_algo import *
from draw_graph import *

def search_and_visualize():
    print("******************************************************************************************************************")
    G = nx.Graph()
    pos = nx.spring_layout(G)
    visited = []

    search_size = input("If you want a small graph, enter S; for a big graph, enter B: ").upper()

    if search_size == 'B':
        while True:
            additional_edges = input("Please enter the number of edges you want (max is 60): ")
            try:
                edges_count = int(additional_edges)
                if edges_count <= 60:
                    print(f"You entered {edges_count} edges. Proceeding...")
                    additional_edges = add_edges_rand(edges_count)
                    G.add_edges_from(additional_edges)
                    break  # Exit the loop if a valid value is provided
                else:
                    print("Invalid number of edges. Please enter a value below 60.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:
        G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('F', 'G'), ('E', 'G'),
                     ('B', 'G'), ('C', 'F'), ('B', 'H')])
    
    start_node = get_start_node(G)
    print("The start node is: ", start_node)
    if start_node is not None:
        pos = nx.spring_layout(G)  # Regenerate layout based on the updated graph

        search_type = input("Choose search type (BFS or DFS): ").upper()

        if search_type == 'BFS':
            order = order_bfs(G, start_node)
            visualize_search(order, 'BFS Visualization', G, pos, visited)
        elif search_type == 'DFS':
            order = order_dfs(G, start_node)
            visualize_search(order, 'DFS Visualization', G, pos, visited)
        else:
            print("Invalid search type. Please choose BFS or DFS.")

        print("The graph's specs:", G)
        visited.pop(0)
        print("Visited nodes:", visited)
        print("******************************************************************************************************************")
    
# Call the function
search_and_visualize()