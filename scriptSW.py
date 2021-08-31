# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:59:04 2021

@author: aimedb
"""



import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from networkx.algorithms.community import greedy_modularity_communities


def get_value(name, maps):
    for nodes in maps:
        if nodes["name"] == name:
            return nodes["value"]

def get_info(data):
    connections = defaultdict(int)
    interactions = defaultdict(int)
    for link in data["links"]:
        connections[data["nodes"][link["source"]]["name"]] += 1
        connections[data["nodes"][link["target"]]["name"]] += 1
        interactions[data["nodes"][link["source"]]["name"]] += link["value"]
        interactions[data["nodes"][link["target"]]["name"]] += link["value"]
    return connections, interactions
   
def get_communities(G):
    partition = greedy_modularity_communities(G)
    pos = nx.spring_layout(G)
    node_groups = []
    node_groups = list(partition)
    color_map = []
    for node in G:
        if node in node_groups[0]:
            color_map.append('blue')
        else: 
            if node in node_groups[1]:
                color_map.append('yellow')
            else: 
                if node in node_groups[2]:
                    color_map.append('red')
                else: 
                    if node in node_groups[3]:
                        color_map.append('grey')
                    else:
                        color_map.append('green')
    nx.draw(G,pos, alpha=0.5,node_size=50,node_color=color_map,with_labels=True)
    plt.savefig(f'results/graphs/Episode_{episode}_Graph_communities.png')
    plt.show()
    plt.close()

def get_graph(data, episode):
    nodes = [ node['name'] for node in data["nodes"] ]
    edges = [ (nodes[link['source']], nodes[link['target']]) for link in data["links"] ]
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    for edge in edges:
        G.add_edge(edge[0],edge[1])
    nb_nodes = G.number_of_nodes()
    nb_edges = G.number_of_edges()
    plt.figure(figsize=(30,15))
    plt.subplot(121)
    nx.draw(G,with_labels=True)
    plt.savefig(f'results/graphs/Episode_{episode}_Graph.png')
    plt.show()
    plt.close()
    G = get_communities(G)
    return G,nb_nodes,nb_edges

def get_episode(episode, feature):
    e = "episode-" + str(episode)
    if episode == 0:
        e = "full"
    with open(f'data/starwars-{e}-{feature}.json') as f:
        data = json.load(f)    
    connections, interractions = get_info(data)
    Graph,nb_nodes,nb_edges  = get_graph(data, episode)
        
    temp = set()
    for i,j in zip(connections.items(), interractions.items()):
        temp.add((i[0], i[1], j[1], get_value(i[0], data["nodes"])))
    temp = sorted(temp, key = lambda x: x[1])[::-1]
    plt.figure(figsize=(25,10))
    plt.title(f'Episode-{episode} {feature}')
    plt.plot(list(zip(*temp))[0], list(zip(*temp))[1], list(zip(*temp))[0], list(zip(*temp))[2], list(zip(*temp))[0], list(zip(*temp))[3])
    plt.xticks(list(zip(*temp))[0][::1],  rotation='vertical')
    plt.savefig(f'results/images/Episode_{episode}_{feature}.png')
    plt.show()
    plt.close()
    
    return Graph,nb_nodes,nb_edges, (connections, interractions)


if __name__ == "__main__":
    if not os.path.exists('results'):
        os.makedirs('results')
        os.makedirs('results/images')
        os.makedirs('results/graphs')
    feature = "interactions-allCharacters"
    episode = 4
    task = get_episode(episode, feature)
    print(f"Nombre de sommets :{task[1]}, Nombre de noeuds : {task[2]}")