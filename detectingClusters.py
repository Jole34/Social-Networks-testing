import networkx as nx
from socialnetworking import loadingGraph

def components(gr):
    components = indetifyCmp(gr)
    return components

def indetifyCmp(gr):
    visited = set()
    components = set()
    print("Adding components ...")
    for v in gr.nodes:
        if v not in visited:
            components.add(bfs(v, visited, gr))
    number = str(len(components))
    print("Graph is made out of "+ number +" components")
    return frozenset(components)

def bfs(v, visited, gr):
    compSet = set()
    queue = list()
    compSet.add(v)
    visited.add(v)
    queue.append(v)
    while len(queue) != 0:
        current = queue.pop(0)
        neighbours = list(nx.neighbors(gr, current))
        for neighbour in neighbours[:]:
            afn1 = gr.get_edge_data(current, neighbour)
            afn2 = gr.get_edge_data(neighbour, current)
            if afn1['affinity'] == 'negative' or afn2['affinity'] == 'negative':
                neighbours.remove(neighbour)
        for neighbour in neighbours:
            if neighbour not in visited:
                compSet.add(neighbour)
                visited.add(neighbour)
                queue.append(neighbour)
    return frozenset(compSet)

def nodesAndEdgesinfo(gr):
    i = 0
    j = 0
    p = 0
    for v in gr.nodes:
        i = i+1
    for e in gr.edges:
        j = j+1
    for u, v, d in gr.edges(data=True):
        if (v, u) in gr.edges:
            af = gr[v][u]['affinity']
        if gr[u][v]['affinity'] == "positive" or af == "positive":
            p = p + 1
    k = p/j * 100
    print("Number of nodes is: "+ str(i))
    print("Number of edges is: "+ str(j))
    print("Percentage of positive edges is: "+ str(round(k, 2)) + "%")


def clusterNetworkCreate(clusters, gr):
    print("Making networks from clusters....")
    networks = set()
    for cl in clusters:
        allnodes = set()
        for v in cl:
            allnodes.add(v)
        newGraph = gr.copy()
        for v in list(newGraph.nodes)[:]:
            if v not in allnodes:
                newGraph.remove_node(v)
        networks.add(newGraph)
    return networks

def clusterNetworks(clusterNet):
    i = 0
    for gr in clusterNet:
        print("Cluster " + str(i) + ": ")
        i = i + 1
        if len(list(gr.edges)) is 0:
            print("Cluster has only one node and no edges")
        else:
            print("Cluster has  "+str(len(list(gr.edges)))+" edge/s")


def giantNetworkClusters(g, clusters):
    network = nx.Graph()
    i = 1
    for c in clusters:
        c.graph['name'] = "Claster "+ str(i)
        i = i + 1
        network.add_node(c)
 ##naming and adding clusters as nodes
    for c1 in clusters:
        for c2 in clusters:
            if c1 == c2:
                continue
            connected = False
            j = 0
            while not connected and j < len(c1.nodes):
                node = list(c1.nodes)[j]
                j = j+ 1
                #is node from cluster1 neighboor with some node in cluster2
                for node2 in c2:
                    if node in nx.neighbors(g, node2):
                        connected = True
            if connected:
                network.add_edge(c1, c2)
                ##edges between clusters are negative
    nx.set_edge_attributes(network, "negative", "affinity")
    return network
def isMyGraphClusterable(clusters):
    antiCoalitions = list()
    negativeEdges = list()
    coalitions = list()
    for cluster in clusters:
        for (u, v, d) in cluster.edges(data=True):
            if d['affinity'] == "negative":
                negativeEdges.append((u, v))
                antiCoalitions.append(cluster.nodes)
            else:
                coalitions.append((u, v))
    if len(antiCoalitions) == 0:
        print("Given graph is clusterable")
    else:
        print("Given graph is not clusterable")
        print ("Links for removal: ")
        for link in negativeEdges:
            print(link)

    return coalitions

def findGigantComponent(components):
    bigOne = set()
    max = 0
    for cm in components:
        if len(list(cm)) > max:
          max = len(list(cm))
          bigOne  = cm
    return max




