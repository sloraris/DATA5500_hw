import networkx as nx

def how_many_nodes(G):

    # count nodes
    # I asked Claude: "How would I count the number of nodes in a NetworkX graph?"
    # Claude recommended using G.number_of_nodes(), but also offered using len(G.nodes())
    node_count = G.number_of_nodes()

    # prin and return results
    print("Number of nodes in graph:", node_count)
    return node_count
