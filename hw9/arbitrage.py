import networkx as nx
import os
import requests
from itertools import combinations
import time

# txt file with crypto to arbitrage
filepath = os.getcwd()
file = open(f"{filepath}/crypto.txt", "r")

# Create pairs from file
coins = []
for line in file.readlines():
    name, symbol = line.split(",")
    name = name.strip()
    symbol = symbol.strip()
    coins.append((name, symbol))

# Create graph
g = nx.DiGraph()

# Get all combinations and make API calls
for coin1, coin2 in combinations(coins, 2):
    name1, symbol1 = coin1
    name2, symbol2 = coin2
    req = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={name1},{name2}&vs_currencies={symbol1},{symbol2}")
    data = req.json()
    print(data)
    time.sleep(20)

    # Add edges to graph if values succeed, skip if not
    try:
        g.add_weighted_edges_from([(symbol1, symbol2, data[name1][symbol2]), (symbol2, symbol1, data[name2][symbol1])])
    except KeyError:
        continue

# Calculate simple paths and weights, print results
for coin1, coin2 in combinations(coins, 2):
    name1, symbol1 = coin1
    name2, symbol2 = coin2
    for path in nx.all_simple_paths(g, source=symbol1, target=symbol2):
        print(path)
        forward = 1
        for i in range(len(path)-1):
            node1 = path[i]
            node2 = path[i+1]
            forward *= g[node1][node2]['weight']
        rpath = path[::1]
        print(rpath)
        backward = 1
        for i in range(len(path)-1):
            node1 = path[i]
            node2 = path[i+1]
            backward *= g[node1][node2]['weight']
        total_weight = forward * backward
        print(total_weight)
