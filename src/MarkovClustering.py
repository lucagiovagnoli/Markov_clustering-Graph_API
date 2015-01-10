'''
Created on Apr 29, 2014

@author: luca
'''

import numpy

class MarkovClustering(object):
    """
    MCL algorithm. 
    Unlike some other clustering techniques like K-means clustering, in MCL the
    number of clusters is not predetermined. The idea is to operate random
    walks through the graph.  While walking inside a cluster the probability of
    staying inside the same cluster is high. 
    
    Algorithm - steps:
        1) column normalize the matrix
        2) raise the matrix to the e-th power (simulates the random walk)
        3) raise each element to the r-th power and column normalize. It
            strengthens more likely currents while weakening the less likely
            (faster convergence).
        4) repeat steps 2 and 3 until we are in a steady state or max number of
            iterations T is reached
        5) interpret clusters (non-zero elements along rows)
    
    A possible future improvement could be the pruning of cells in case of huge
    graphs. It is similar to inflation, we set little matrix values directly to
    zero to speed up the process. 
    Sources: 
        http://www.micans.org/mcl/ 
        http://www.cs.ucsb.edu/~xyan/classes/CS595D-2009winter/MCL_Presentation2.pdf
    """

    def __init__(self, matrix, e, r):
        """
        Arguments:
        matrix -- a square matrix representation of a graph. Matrix should be
            symmetric.  'The reason that mcl dislikes uni-directed graphs is not
            very mcl specific, it has more to do with the clustering problem
            itself.  Somehow, directionality thwarts the notion of cluster
            structure.' (Stijn van Dongen)
        e -- power parameter. The matrix is multiplied by itself e times each
                iteration
        r -- inflation parameter. Increasing r will make inflation stronger and
            will increase granularity/tightness of clusters).
        """
        
        # numpy library is used in order to speed up matrix operations.
        self.matrix = numpy.array(matrix,dtype=numpy.float64)
        self.e = e
        self.r = r
        
    def computeClusters(self, T = 100):
        """
        Returns a list of clusters. Each cluster is represented by a list of indexes.

        Parameter:
        T -- max iterations, MCL can be experimentally shown to usually
            converge in less than ~100 steps
        """
 
        self.addSelfLoops()
        self.normalizeColumns()
        
        t = 0
        while(t<T):
            lastMatrix = numpy.copy(self.matrix)
            self.powerStep()
            self.inflationStep()
            if self.steadyState(lastMatrix)==True:
                break
            t += 1

        return self.interpretClusters()
        
        
    def addSelfLoops(self):
        """
        Useful for convergence purposes.
        """
        for i in range(self.matrix.shape[0]):
            self.matrix[i][i] = 1
            
    def normalizeColumns(self):
        # Note: after column normalization, matrix is no longer symmetric
        s = self.matrix.sum(axis=0)
        for (x,y), _ in numpy.ndenumerate(self.matrix):
            if s[y] != 0:
                self.matrix[x][y] /= float(s[y])
        
    def powerStep(self):      
        """
        The matrix is raised to the e-th power (simulates the random walk)
        """
        temp = self.matrix
        for _ in range(self.e-1):
            temp = temp.dot(self.matrix) 
        self.matrix = temp
            
    def inflationStep(self):
        """
        Executes inflation on the matrix. Inflation:
        1) every element is raised to the r-th power
        2) matrix is column normalized
        The inflation is responsible for strengthening and weakening of current.
        """
        self.matrix **= self.r 
        self.normalizeColumns();
    
    def steadyState(self, lastMatrix):
        """
        Returns True if current self.matrix is equal to  lastMatrix 
        that is the matrix of the last iteration. False otherwise. 
        """
        for (x,y), _ in numpy.ndenumerate(self.matrix):
            if self.matrix[x][y]-lastMatrix[x][y] != 0:
                return False
        return True
        
    def interpretClusters(self):
        """
        Return a list of clusters. Each cluster is a list of indexes. 
        Interpreting clusters is achieved examining non-zero elements along rows.
        """
        res = []
        for i in range(self.matrix.shape[0]):
            cluster = []
            flag = 0
            for z in range(self.matrix.shape[0]):
                if self.matrix[i][z] > 0:
                    cluster.append(z)
                    flag = 1
            if flag==1:
                res.append(cluster)
        return res
