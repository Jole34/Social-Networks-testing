from socialnetworking import  loadingGraph
from socialnetworking import  detectingClusters


graph = loadingGraph.loadGraph()
comp = detectingClusters.components(graph)
detectingClusters.nodesAndEdgesinfo(graph)
detectingClusters.findGigantComponent(comp)
clusterNets = detectingClusters.clusterNetworkCreate(comp, graph)
detectingClusters.isMyGraphClusterable(clusterNets)
detectingClusters.clusterNetworks(clusterNets)
net = detectingClusters.giantNetworkClusters(graph, clusterNets)
