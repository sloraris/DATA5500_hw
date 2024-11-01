import networkx as nx

def nodes_degree_over_5(G):

    # tracking variable
    node_count = 0

    # check nodes and add to count if degree > 5
    # I asked Claude: "How would I count the number of nodes in a graph with more than 5 degrees?"
    # Claude suggested using the G.degree() function to get a node and it's degree
    # then iterate through the results and increase the count if the degree > 5
    for node, degree in G.degree():
        if degree > 5:
            node_count += 1

    # return count
    return node_count
