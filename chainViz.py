import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def ChainViz(chain):
    G = nx.DiGraph()
    nodes = np.arange(0, len(chain)).tolist()

    labels = {nodes [i]: chain[i] for i in range(len(chain))}

    size  = []
    for i in chain:
        if i == "K" or i== "R":
            size.append(500)
        else:
            size.append(500)

    G.add_nodes_from(nodes)
    G.add_edges_from([(0,1), (1,2), (2,3)])
    pos = {pos: (pos,1) for pos in range(len(chain))}

    fig,ax = plt.subplots()
    plt.figure(figsize=(7,3))
    plt.title("Decision Chain")
    nx.draw_networkx(G, pos = pos, labels = labels,font_size=8, arrows = True, node_shape = "s",node_size= size, node_color = "white",edgecolors ="grey",ax=ax)
    
    
    
    return fig