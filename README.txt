
Graph Structure in the test.py example:

   0            4
  /|\          /|\
 1---2 ------ 6---5  
  \|/          \|/
   3            7
  
Output clusters of the Markov Clustering Algorithm after only 14 iterations:
['1', '0', '3', '2']
['5', '4', '7', '6']
  

The Graph is represented using the adjacency list method. For the example above: 
1: 0->3->2->
0: 1->3->2->
3: 1->0->2->
2: 1->0->3->6->
5: 4->7->6->
4: 5->7->6->
7: 5->4->6->
6: 2->5->4->7->

It is slower than the matrix representation but better from a memory point of view if the graph is sparse. Matrix 
representation for the example above (indexes mapping to keys: ['1', '0', '3', '2', '5', '4', '7', '6']):
[[0 1 1 1 0 0 0 0]
 [1 0 1 1 0 0 0 0]
 [1 1 0 1 0 0 0 0]
 [1 1 1 0 0 0 0 1]
 [0 0 0 0 0 1 1 1]
 [0 0 0 0 1 0 1 1]
 [0 0 0 0 1 1 0 1]
 [0 0 0 1 1 1 1 0]]


The list of nodes is a python dictionary in order to be able to retrieve node's information and list of neighbors in 
O(1). The lists of neighbors are python dictionaries too, so it takes O(1) to retrieve a edge's weight.  
The methods have been partially implemented, more details can be found in the docstrings inside the code.






GRAPH ALGORITHMS - High level Concepts

Depth First Search
DFS is a search algorithm that takes two nodes of a graph as input and returns a path between them. Depth-First is 
referred to the visiting order of the neighbor nodes. A stack is used in order to store all nodes to be visited (a 
queue is used in BFS). Instead of visiting all neighbor nodes at current level before processing the next level (Breadth 
First Search), we keep going deep level after level visiting always the last node added to the stack (pop operation).
Steps:
1) Push neighbors on a stack data structure.
2) Pop node and visit it.
4) Repeat the process until stack is empty or visited node is the one we were looking for.

Dijkstra
Computes the shortest path from a node to all other nodes. 
The starting node has a distance of zero, all others start with an infinite distance value. The idea is to scan 
through all nodes in the graph updating these distances until at the end each of them will have the minimum 
possible distance from the starting node. 
Relaxation is obtained checking all possible ways of arriving to a certain node and saving the minimum. To be sure 
that the distances of the previous nodes in the path are already definitive we need to visit the nodes of the graph in a 
certain way. Hence nodes are put in a priority queue and processed in ascending value of distance. 

Kruskal
Computes the minimum spanning tree of the graph. The minimum spanning tree is a tree composed by all nodes of the graph 
so that the sum of the arc costs connecting these nodes is the minimum.
Input is the list of all edges. 
We keep track of two sets, the connected nodes and the nodes yet to be visited. 
We process the edges in order of ascending weight. 
For each processed edge, we mark the two nodes as visited and we add the edge to the solution. The algorithm stop after 
processing all edges or when the set nodes-yet-to-be-visited is empty. We can use a connectivity algorithm like the 
union-find for the connectivity purposes of the algorithm.
At the end there will be a list of edges representing the minimum spanning tree. 

Centrality
There are many ways of defining centrality. Degree centrality is a measure of how likely is for a node to “catch” a 
flow going through the network. Higher the node’s degree, higher the centrality. The degree of a node is the number of 
adjacent edges to which it is connected. We can keep track of this number each time we add or remove edges and nodes 
from the graph. The algorithm simply returns a list of nodes associated to their degrees.
For example in a social network graph, the degree of a node could be the friends of a person. Higher the number of 
friends, higher Its centrality.

Connectivity (Union-Find)
Union-find is an algorithm for computing connectivity of a graph. There are two main connectivity algorithms. The 
quick-find allows lookup for connectivity in O(1) and connecting (union) of nodes in O(n). Once connectivity computation 
is completed, using the data structure will be very fast. The alternative is the quick-union algorithm where we can 
connect nodes in O(1) but lookup takes O(n) time.
Input is a list of all edges in the graph. Each time we process an edge, we make sure to connect the nodes clusters 
together. An auxiliary hash table is used for this purpose. At each hashed node corresponds a value that is equal for 
all nodes connected together. To connect two nodes together we scan through the data structure putting the same value to 
all nodes belonging to either the clusters of the two edge’s nodes.





MARKOV CLUSTERING ALGORITHM

MCL algorithm. 
Unlike some other clustering techniques like K-means clustering, in MCL 
the number of clusters is not predetermined. The idea is to operate random walks through the graph. 
While walking inside a cluster the probability of staying inside the same cluster is high. 
Numpy library is used in order to speed up matrix operations.

Arguments:
matrix -- a square matrix representation of a graph. Matrix should be symmetric.
         'The reason that mcl dislikes uni-directed graphs is not very mcl specific, it has more to do with the  
          clustering problem itself. Somehow, directionality thwarts the notion of cluster structure.' (Stijn van       
          Dongen)
e -- power parameter. The matrix is multiplied by itself e times each iteration
r -- inflation parameter. Increasing r will make inflation stronger and will 
     increase granularity/tightness of clusters).
    
Algorithm - steps:
1) column normalize the matrix
2) raise the matrix to the e-th power (simulates the random walk)
3) raise each element to the r-th power and column normalize. It strengthens more likely currents 
    while weakening the less likely (faster convergence).
4) repeat steps 2 and 3 until we are in a steady state or max number of iterations T is reached
5) interpret clusters (non-zero elements along rows)
    
A possible future improvement could be the pruning of cells in case of huge graphs. It is similar
to inflation, we set little matrix values directly to zero to speed up the process. 

Sources: 
http://www.micans.org/mcl/ 
http://www.cs.ucsb.edu/~xyan/classes/CS595D-2009winter/MCL_Presentation2.pdf
