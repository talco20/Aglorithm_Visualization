# Kruskal's Algorithm 
# BigO - O(e log v)
# Storage - O(e+v)

def kruskal_algorithm(graph):
    mst_edges = []
    visited_nodes = set()

    # Sort all edges in ascending order by weight
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])

    # Create a disjoint set data structure for tracking connected components
    disjoint_set = {node: {node} for node in graph.nodes}

    for edge in edges:
        weight = edge[2]['weight']
        node1, node2 = edge[0], edge[1]

        # Check if adding this edge creates a cycle
        if disjoint_set[node1] != disjoint_set[node2]:
            mst_edges.append((weight, node1, node2))

            # Merge the sets of the two connected components
            set1 = disjoint_set[node1]
            set2 = disjoint_set[node2]
            new_set = set1.union(set2)

            # Update the disjoint set data structure
            for node in new_set:
                disjoint_set[node] = new_set

            # Add the new nodes to the visited set
            visited_nodes.add(node1)
            visited_nodes.add(node2)

    return mst_edges, visited_nodes
