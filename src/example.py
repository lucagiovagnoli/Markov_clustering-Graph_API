"""
Created on Apr 29, 2014

@author: luca
"""

import numpy 
import Graph
import MarkovClustering
        
f = open("../input_graph.txt","r")

grafo = Graph.Graph()
for line in f:
    edges = line.split()
    grafo.addNode(edges[0], edges[0])
    grafo.addNode(edges[1], edges[1])
    grafo.addEdge(edges[0], edges[1])


print "Graph adjacency list representation: \n",grafo    

matrix, mapBackToKeys = grafo.getGraphMatrix()
numpymat = numpy.array(matrix)
print "Graph matrix representation: \n",numpymat
print "\nMapping matrix indexes to keys: ", mapBackToKeys

alg = MarkovClustering.MarkovClustering(matrix,e=2,r=2)
clusters = alg.computeClusters(T=40)

print "\nClusters after MCL algorithm: "
for cluster in clusters:
    print [mapBackToKeys[x] for x in cluster]

#===============================================================================
# print "\nNumber of nodes: ",grafo.nodesCount
# print "\nValue node 1:", grafo.getNodeValue('1')
# print "\nAll nodes (key, value): \n", grafo.getAllNodes()
# print "\nNeighbors of node '0' (key, value): \n", grafo.getNeighbours('0')
#===============================================================================
