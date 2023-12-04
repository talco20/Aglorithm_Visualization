# Topological Sort
# BigO - O(n+m)
# Storage - O(n)

import networkx as nx

def top_sort(graph, start_node):
    try:
        order = list(nx.topological_sort(graph))
        start_index = order.index(start_node)
        return order[start_index:]
    except nx.NetworkXError:
        print("The graph is not a Directed Acyclic Graph (DAG).")
        return []