import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def nodes(n,start,max_age):
    #define array and start value
    node_tab = np.zeros((max_age,n))
    node_tab[start-1][0] = 1

    #find all nodes in the network
    for i in range(0,n-1):
        for j in range(0,max_age):
            if node_tab[j][i] == 1:
                if j == max_age-1:
                    node_tab[0][i+1] = 1
                else:
                    node_tab[0][i+1] = 1
                    node_tab[j+1][i+1] =1
    return node_tab


def networkViz(node_tab,max_age,n):

    def takeSecond(elem):
        return elem[0]

    ## Get all points for graph
    result = np.where(node_tab==1)
    result = [x +1 for x in result]
    points = list(zip(result[1],result[0]))
    points.sort(key=takeSecond)

    #Create edges for graph

    edges = []
    for x in points:
        age = x[1]
        decisionYear = x[0]
        if decisionYear == n:
            break
        if age >= max_age:
            pos_edge1 = (decisionYear+1,1)
            e1 = (points.index(x),points.index(pos_edge1),"R")
            edges.append(e1)
        else:
            pos_edge1 = (decisionYear+1,1)
            pos_edge2 = (decisionYear+1,age+1)
            e1 = (points.index(x),points.index(pos_edge1),"R")
            edges.append(e1)
            e1 = (points.index(x),points.index(pos_edge1),"R")
            e2 = (points.index(x),points.index(pos_edge2),"K")
            edges.append(e1)
            edges.append(e2)
            

    def add_edge_to_graph(G, e1, e2, w):
        G.add_edge(e1, e2, weight=w)


    G = nx.Graph()

    for i in range(len(edges)):
        add_edge_to_graph(G, points[edges[i][0]], points[edges[i][1]], edges[i][2])

    # you want your own layout
    # pos = nx.spring_layout(G)
    pos = {point: point for point in points}
    labels = {point: point[1] for point in points}
    # add axis
    fig, ax = plt.subplots()
    nx.draw(G, pos=pos, node_color='k', ax=ax)
    nx.draw(G, pos=pos, node_size=250, ax=ax)  # draw nodes and edges
    nx.draw_networkx_labels(G, pos=pos,labels=labels,font_size=8)  # draw node labels/names
    # draw edge weights
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    plt.axis("on")
    plt.xlabel("Decision year")
    plt.ylabel("Machine age")
    plt.xticks(np.arange(0,n+3,1))
    plt.yticks(np.arange(0,max_age+1,1))
    #ax.set_xlim(0.5, n+3)
    #ax.set_ylim(0,max_age+5)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

    return fig