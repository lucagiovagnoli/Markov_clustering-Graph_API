"""
Created on Apr 29, 2014

@author: luca
"""

class Node(object):
    
    def __init__(self, value):
        self.value = value
        # A dictionary is used for neighbors. keys are neighbor nodes keys, 
        # values are weights of arcs between nodes
        self.neighbors = {}
        self.inDegree = 0
        self.outDegree = 0
    
    def updateEdgeWeight(self, key):
        pass
        
    def getEdgeWeight(self, key):
        if self.isConnectedTo(key):
            return self.neighbors[key]
        return None
    
    def connectTo(self, key, weight):
        self.neighbors[key] = weight

    def isConnectedTo(self, key):
        return key in self.neighbors
        
class Graph(object):
    """
    The Graph is represented using the adjacency list method. It is slower than
    the matrix representation but better from a memory point of view if the
    graph is sparse. The list of nodes is a python dictionary in order to be
    able to retrieve node's information and list of neighbors in O(1). The
    lists of neighbors are python dictionaries too, so it takes O(1) to
    retrieve a edge's weight.  
    """

    def __init__(self, directedGraph=False):
        """
        Arguments:
        directedGraph - must be True for creating a directed graph, False
                        otherwise.  default is False (undirected graph).
        """
        
        self.directedGraph = directedGraph
        self.nodes = {}
        self.nodesCount = 0
        self.edgeCount = 0
        
    ## Graph modification ##
    def addNode(self, key, value):
        """
        addNode required before calling addEdge.
        Nodes are represented by key, value pairs.
        
        Arguments:
        key -- identifier of the node, used for indexing it in the dictionary. 
        value -- information to store in the node
        """
        
        if not self.hasNode(key):
            self.nodes[key] = Node(value)
            self.nodesCount += 1         
            
    def addEdge(self, key1, key2, weight=1): 
        """
        Requires the two nodes to be already inserted in the graph. So call addNode on each of them first.
        Adds an edge to the graph from node with key1 to the node with key2, and viceversa if graph is undirected.
        Updates inDegree and outDegree properties of the node. 
        Returns None if the two nodes are not already in the graph.
        
        Arguments:
        key1 -- key of the first node
        key2 -- key of the node to connect to the first
        weight -- The edge can contain a weight for various purposes (useful in shortest path algorithms 
                  like Bellman-Ford, Dijkstra or minimum spanning-tree like Kruskal or Prim)
        """
        
        #add the nodes to the list if not already there
        if not self.hasNode(key1) or not self.hasNode(key2):
            return None
        
        #add the edge if not already existing
        if not self.hasEdge(key1, key2):
            self.nodes[key1].connectTo(key2, weight)
            self.edgeCount += 1
        
        if not self.directedGraph:
            if not self.hasEdge(key2, key1):
                self.nodes[key2].connectTo(key1, weight)
 
    def updateNodeValue(self, key):
        pass
    def updateEdge(self, key1, key2, newWeight):
        pass
    def removeNode(self, key):       
        pass
    def removeEdge(self,node1,node2):
        pass

    
    ## Graph properties ##
    def getNodeValue(self, key):
        """
        Returns value of node with 'key' key, or None if the node is not in the graph
        """
        if (self.hasNode(key)):
            return self.nodes[key].value 
        return None
    
    def getEdgeWeight(self, key1, key2):
        """
        Returns the weight of the edge between key1 and key2
        """
        if self.hasNode(key1):
            return self.nodes[key1].getEdgeWeight(key2)
        return None
    
    def getAllNodes(self):
        """
        Returns a list of (key, value) pairs representing all the nodes in the graph
        """
        
        res = []
        for k in self.nodes:
            res.append((k,self.getNodeValue(k)))            
        return res
    
    def getAllEdges(self):
        res = []
        for k in self.nodes:
            for k1 in self.nodes[k].neighbors:
                if self.directedGraph: 
                    res.append((k,k1))
                else:
                    if (k1, k) not in res:
                        res.append((k, k1))
        return res
        
    def getNeighbours(self, key):
        """
        Returns a list of nodes connected to the node with 'key' key.
        """
        
        if self.hasNode(key):
            return [(x, self.getNodeValue(x)) for x in self.nodes[key].neighbors]
        return None
    
    def hasNode(self, key):
        """
        Returns Tru
        e if node with 'key' is in the graph
        """
        return key in self.nodes
        
    def hasEdge(self, key1, key2):
        """
        Returns True if nodes with key1 and key2 are connected.
        """
        
        if self.hasNode(key1):
            return self.nodes[key1].isConnectedTo(key2)
        return False
    
    def nodesCount(self):
        return self.nodesCount
        
    def inDegree(self, key):
        pass
    def outDegree(self, key):
        pass


    # ALGORITHMS
        
    def DepthFirstSearch(self, key1, key2):
        """
        Computes a path from node with key1 to node with key2 using depth first
        search.  Returns the path as a list of node's keys.
        """
        pass 
    
    def Dijkstra(self, key1):
        """
        Computes the shortest path between node with key1 and all other nodes.
        Returns a dictionary. Every node's key in the dictionary stores the
        cost of the path and the last node traversed to get there (part of the
        best path). It is possible to build a shortest path from the starting
        node to all others using this information. 
        """
        pass
        
    def Kruskal(self):
        """
        Computes minimum spanning tree of the graph. 
        Returns a list of edges (the minimum tree).
        """
        pass
    
    def degreeCentrality(self, key):   
        """
        Computes centrality of all nodes in the graph as the number of inDegree
        connections.  Returns a dictionary of keys associated to inDegree
        values (key:inDegree)
        """
        pass
        
    def UnionFind(self):
        """
        Computes connectivity between nodes in the graph. Implemented with the
        quick-find method, it takes time for getting the result but then the
        connectivity lookup is O(1).  Returns a dictionary where each key
        corresponds to a value (equal for elements connected together).
        """
        pass

    def getGraphMatrix(self):
        """
        Computes the matrix representation of the graph to be used in the 
        MarkovClustering algorithm or any other possible future algorithm 
        implementation needing a matrix representation. 

        :returns: a tuple (matrix, mapIndexesToKeys) where mapIndexesToKeys 
        is needed to map back the row and column indexes to keys values. 
        """
        mapKeysToIndexes = {}
        mapIndexesToKeys = [None] * self.nodesCount
        c = 0
        for k in self.nodes:
            mapKeysToIndexes[k] = c 
            mapIndexesToKeys[c] = k
            c += 1
        
        matrix = [[0 for _ in range(self.nodesCount)] 
                for _ in range(self.nodesCount)]
        for k in self.nodes:
            for k1 in self.nodes[k].neighbors:
                matrix[mapKeysToIndexes[k]][mapKeysToIndexes[k1]] = \
                        self.nodes[k].neighbors[k1]
         
        return (matrix, mapIndexesToKeys)
                
     
    ## DEBUG ##     
    def __str__(self):
        """
        Adjacency list representation of the graph for debug purposes.
        """
        
        s = ""
        for n1 in self.nodes:
            s += str(n1) + ": "
            for n2 in self.nodes[n1].neighbors:
                s+= str(n2) + "->"
            s += "\n"
        return s
               
               
           
    
        
        
        
