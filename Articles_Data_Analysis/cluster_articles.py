import numpy as np
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt

import make_data
from transform import count_transform
from cluster_algos import kmeans, hcluster

def clustering(X, labels, algo='hcluster', n_clusters=5, figname='cluster_result.png'):
    """ Clustering data.
        Params:
            X: ndarray of n x d size (n samples, d features)
            labels: labels of samples, for visualizing result.
            algo: specify clustering algorithms, e.g., "hcluster", "kmeans"
            n_clusters: #.of.cluster in case of kmeans
            figname: file name to save figure
    """
    assert algo in ['hcluster', 'kmeans'], "Invalid algorithm!"
    
    if algo == 'hcluster':
        linkage_mat = hcluster(X, metric='correlation', method='average')
        fig = plt.figure(figsize=(30,20), dpi=100)
        fig.clf()
        hier.dendrogram(linkage_mat, labels=labels, leaf_rotation=90, leaf_font_size=20)
        plt.savefig(figname)
    else:
        labels = np.asarray(labels)
        result = kmeans(X, n_clusters=n_clusters)
        for cid in xrange(n_clusters):
            print 'Cluster %d:' %(cid+1)
            for a in labels[result == cid]:
                print a.encode('utf-8')
            print '-'*30
        
def main(url_file, use_tfidf=True):
    word_cnt, sites, site_urls = make_data.get_sites_words(url_file)
    sw_mat, word_list = make_data.make_site_by_word_mat(word_cnt, sites, freq=5, percent=0.7)
    X = sw_mat
    if use_tfidf:
        X = count_transform(sw_mat)
    labels = ['Normal Deviate', 'MLTheory', 'CNET', 'BBC', 'CNN', 'JP', 'CNN-Tech', 'TechReview', 'NYT-Tech', 'Time-World', 'Mark-Reid']
    
    clustering(X, labels, algo='hcluster', figname='hcluster_site_by_word_tfidf.png')
    
if __name__ == '__main__':
    main('txt/urls.txt', use_tfidf=True)