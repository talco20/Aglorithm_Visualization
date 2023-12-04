# Topological Sort
# BigO - O(n+m)
# Storage - O(n)

import networkx as nx

def top_sort(graph, start_node):
    indegree = {node: 0 for node in graph.nodes}
    
    # Calculate in-degrees for each node
    for edge in graph.edges:
        indegree[edge[1]] += 1

    # Initialize a queue with nodes having in-degree of 0
    queue = [node for node, degree in indegree.items() if degree == 0]

    result = []

    while queue:
        # Get a node with in-degree 0
        current_node = queue.pop(0)
        result.append(current_node)

        # Update in-degrees of adjacent nodes
        for neighbor in graph.neighbors(current_node):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(graph.nodes):
        print("The graph is not a Directed Acyclic Graph (DAG).")
        return []
    
    start_index = result.index(start_node)
    return result[start_index:]