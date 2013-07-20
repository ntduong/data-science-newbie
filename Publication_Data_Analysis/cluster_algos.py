""" Clustering methods: k-means(++), hierarchical agglomerative clustering, etc.
    Refactoring code for later reuse
    @Todo: Add more clustering methods 
    
    (c) Duong Nguyen @TokyoTech - CS
    Email: ntduong268(at)gmail.com
"""

import numpy as np
import scipy
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as hier
from sklearn.cluster import KMeans

def kmeans(X, n_clusters=5):
    """ K-means clustering method
        Params: 
            X: ndarray of n x d matrix (n samples, d-dimension)
            n_clusters: #.of.clusters
        Returns:
    """
    a_kmeans = KMeans(n_clusters=n_clusters, init='k-means++')
    return a_kmeans.fit_predict(X)
    
def hcluster(X, metric="correlation", method="average"):
    """ Bottom-up hierarchical clustering method.
        Params: 
            X: ndarray of n x d matrix (n samples, d-dimension)
            metric: For computing sample-pairwise distance matrix, e.g., "euclidean", "correlation", etc.
            method: linkage method, e.g., "single", "complete", "average", etc.
        Returns:
            linkage-matrix for dendrogram plot
            See scipy.cluster.hierarchy for more details. 
    """
    distance_mat = dist.pdist(X, metric) # condensed matrix form
    linkage_mat = hier.linkage(distance_mat, method=method, metric='euclidean')
    return linkage_mat
    
