""" Publication Bibtex Data Analysis
    Clustering publication data (e.g., authors, terms, etc.)
    @Todo: Revise and clean code  
  
    (c) Duong Nguyen @TokyoTech - CS
    Email: ntduong268(at)gmail.com
"""

from pybtex.database.input import bibtex
import bib_parser

from collections import defaultdict
import re

import numpy as np
import scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from sklearn.decomposition import PCA
import simpleLPP

from git_mds import mds
from transform import count_transform
from cluster_algos import kmeans

# regex pattern to split words
SPLITTER = re.compile(r'\W+')

#*********************#
#   COMMON FUNCTIONS  #
#*********************#
def get_stop_words(fname='txt/english_stop.txt'):
    """ Load stop-word list from a file."""
    stop_words = []
    with open(fname, 'rt') as fin:
        for line in fin:
            stop_words.append(line.strip().lower())	
    return stop_words

def get_terms(title, stop_words):
    """ Get terms from a given pub title."""
    tokens = SPLITTER.split(title)
    terms = [t.lower() for t in tokens] # convert to lowercase
    terms = [t for t in terms if t not in stop_words] # remove stop words
    return terms

def get_bib_data(fname='txt/sugiyama.bib.txt'):
    """ Parse given bibtex file and return parsed data."""
    parser = bibtex.Parser()
    bib_data = parser.parse_file(fname)
    return bib_data

def h_clustering(mat, labels, fig_name, show=False):
    """ Hierarchical clustering A based on B given A by B matrix.
        Params:
            mat: ndarray A by B
            labels: A labels
            fig_name: file name to save figure
            show: show figure flag interactively. Default: False.
    """
    distance_mat = dist.pdist(mat, "euclidean")
    # Euclidean-based average linkage hierarchical clustering
    linkage_mat = hier.linkage(distance_mat, method="average", metric="euclidean")
    fig = plt.figure(figsize=(30,20), dpi=100)
    fig.clf()
    hier.dendrogram(linkage_mat, labels=labels, leaf_rotation=90, leaf_font_size=15)
    plt.savefig(fig_name)
    if show:
        plt.show()
    
def bib_cluster_A_by_B(mat, A_labels, fname):
    """ Clustering A (years, authors, etc.) by B (terms, etc.)."""
    h_clustering(mat, A_labels, fname)

# OBSOLETE
def mds_bib_data_with_sklearn(fname):
    
    bib_data = get_bib_data()
    mat, years, term_list, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    
    # Euclidean-based MDS
    aMDS = MDS(n_components=2, dissimilarity='euclidean')
    coords = aMDS.fit_transform(mat)
    fig = plt.figure()
    fig.clf()
    for label, x, y in zip(years, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x,y))
    
    plt.savefig(fname)

#**************#
# YEAR - TERM  #
#**************#    
def get_year_by_term_mat(bib_data, freq=5):
    """ Make year-by-term matrix: mat.
        Each element of mat, e.g., mat[y][t] := the frequency of term t in year y.
        
        Params:
            bib_data: parsed bibtex data
            freq: the thresholding value to filter terms that appear not less than freq times.
    """
    stop_words = get_stop_words()
    entries = bib_data.entries # entries is dict-like ds {key:value}
    term_cnt = defaultdict(int) # term counter for all pub entries: {term: counter}
    year_title = defaultdict(list) # dict { year:[titles in year] }
    for k in entries:
        e = entries[k] # get the value of entry corresponding to key k
        f = e.fields
        try:
            year = f['year']
            title = f['title']
            terms = get_terms(title, stop_words)
            for t in terms:
                term_cnt[t] += 1
            year_title[year].append(title)
        except KeyError:
            continue
    
    years = [] # year list, e.g. ['2008', '2009',...]
    years_cnt = [] # years_cnt[i] := a dict {term:cnt} for all pubs in the i-th year
    for year in year_title:
        years.append(year)
        year_dict = defaultdict(int)
        titles = year_title[year]
        for title in titles:
            terms = get_terms(title, stop_words)
            for t in terms:
                year_dict[t] += 1
        years_cnt.append(year_dict)
    
    # Make a list of terms from term_cnt: only choose term that appear >= freq times
    term_list = [t for t in term_cnt if term_cnt[t] >= freq]
    
    # Make year-by-term matrix (year <-> row, term <-> column)
    mat = [ [0 if t not in y_cnt else y_cnt[t] for t in term_list] for y_cnt in years_cnt]
    mat = np.asarray(mat, dtype="float64") # convert to ndarray
    return mat, years, term_list, years_cnt

def mds_year_term(fname1='corr_2d_mds_years_by_terms.png', fname2='corr_2d_mds_terms_by_years.png'):
    bib_data = get_bib_data()
    mat, years, term_list, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    ydist = dist.squareform(dist.pdist(mat, 'correlation'))
    coords,_ = mds(ydist, dim=2)
    
    mat = mat.T
    tdist = dist.squareform(dist.pdist(mat, 'correlation'))
    coords, _ = mds(tdist, dim=2)
    fig = plt.figure()
    fig.clf();
    plt.xlim(-80,100)
    plt.ylim(-100,100)
    for label, x, y in zip(term_list, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x*100,y*100))
    plt.axis('off')
    plt.savefig(fname2)
    
def mds_author_term(fname1='corr_2d_mds_authors_by_terms.png', fname2='corr_2d_mds_terms_by_authors.png'):
    bib_data = get_bib_data()
    mat, authors, term_list, authors_cnt = get_author_by_term_mat(bib_data, tfreq=5, afreq=10)
    adist = dist.squareform(dist.pdist(mat, 'correlation'))
    coords,_ = mds(adist, dim=2)
    
    fig = plt.figure()
    fig.clf()
    plt.xlim(-15, 20)
    plt.ylim(-15, 20)
    for label, x, y in zip(authors, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x*20,y*20))
    plt.axis('off')
    plt.savefig(fname1)
    
    
    mat = mat.T
    tdist = dist.squareform(dist.pdist(mat, 'correlation'))
    coords, _ = mds(tdist, dim=2)
    #fig = plt.figure()
    fig.clf();
    plt.xlim(-80,100)
    plt.ylim(-100,100)
    for label, x, y in zip(term_list, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x*500,y*500))
    plt.axis('off')
    plt.savefig(fname2)
    
    
def main_year_term():
    bib_data = get_bib_data()
    mat, years, term_list, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    
    # Clustering years by terms
    bib_cluster_A_by_B(mat, years, './cluster_res/hcluster_years_by_terms.png')
    
    # Clustering terms by years
    mat = mat.T
    bib_cluster_A_by_B(mat, term_list, './cluster_res/hcluster_terms_by_years.png')
    
def get_hot_term_in_year(year_list=None, freq=5):
    """ Find the most frequent title terms that appear >= freq times in given years. """
    bib_data = get_bib_data()
    _, years, _, years_cnt = get_year_by_term_mat(bib_data, freq=0)
    if not year_list:
        year_list = years
    for y in year_list:
        ind = years.index(y)
        year_cnt = years_cnt[ind]
        tmp = {t : year_cnt[t] for t in year_cnt if (t and year_cnt[t] >= freq)}
        bib_parser.bar_plot(tmp, 'Hot terms', 'Term', 'Frequency', './simple/hot_terms/hot_terms_%s.png' %y, show=False, sorted_by_key=True)

#***************# 
#  AUTHOR-TERM  #
#***************#
def get_author_by_term_mat(bib_data, tfreq=5, afreq=10):
    """ Make author by term matrix mat.
        Each element, e.g., mat[a][t] := how many times term t appears in a title of pub written by author a.
        
        Params:
            bib_data: parsed bibtex data
            tfreq: threshold value to filter only terms that appear  >= tfreq times
            afreq: threshold value to filter only authors that have >= afreq pubs
    """
    stop_words = get_stop_words()
    entries = bib_data.entries
    term_cnt = defaultdict(int)
    author_title = defaultdict(list)
  
    for k in entries:
        e = entries[k]
        if 'author' not in e.persons: 
            continue
        f = e.fields
        if 'title' not in f: 
            continue
        title = f['title']
        terms = get_terms(title, stop_words)
        for t in terms:
            term_cnt[t] += 1
        for au in e.persons['author']:
            name = au.last()[0]
            if au.first(): name += ' ,' + au.first()[0]
            author_title[name].append(title)	
                
    authors = []
    authors_cnt = []
    
    # Filter only authors with >= afreq pubs
    freq_author_title = {name:author_title[name] for name in author_title if len(author_title[name]) >= afreq}
    
    # Make term list from term_cnt: only choose term that appear >= tfreq times
    term_list = [t for t in term_cnt if term_cnt[t] >= tfreq]
    
    for au in freq_author_title:
        authors.append(au)
        tmp = defaultdict(int)
        for title in author_title[au]:
            terms = get_terms(title, stop_words)
            for t in terms:
                tmp[t] += 1
        authors_cnt.append(tmp)
    
    # make author-by-term matrix
    mat = [ [0 if t not in au else au[t] for t in term_list] for au in authors_cnt]
    mat = np.asarray(mat, dtype="float64") # convert to ndarray
    return mat, authors, term_list, authors_cnt
    
def main_author_term():
    bib_data = get_bib_data()
    mat, authors, term_list, authors_cnt = get_author_by_term_mat(bib_data, tfreq=5, afreq=10)
    
    # Clustering authors by terms
    bib_cluster_A_by_B(mat, authors, './cluster_res/hcluster_authors_by_terms.png')
    
    # Clustering terms by authors
    mat = mat.T
    bib_cluster_A_by_B(mat, term_list, './cluster_res/hcluster_terms_by_authors.png')
    
def get_hot_term_in_author(author_list=None, freq=5):
    """ Find relevant terms for each author in given author list.
        Here, term t is relevant to author a if term t appears more than freq times in all pubs of author a. 
    """
    bib_data = get_bib_data()
    _, authors, _, authors_cnt = get_author_by_term_mat(bib_data, tfreq=0, afreq=10)
    if not author_list:
        author_list = authors
    for au in author_list:
        ind = authors.index(au)
        au_cnt = authors_cnt[ind]
        tmp = {t : au_cnt[t] for t in au_cnt if (t and au_cnt[t] >= freq)}
        dot_ind = au.find(' ')
        au_name = au[:dot_ind]
        if au_name == 'M{\\"u}ller': # fix latex name error!
            au_name = 'Muller'
        bib_parser.bar_plot(tmp, 'Relevant terms', 'Term', 'Frequency', './simple/hot_terms/rel_terms_%s.png' %au_name.encode('utf-8'), show=False, sorted_by_key=True)
 
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

#****************************
#  Dimensionality reduction *
#****************************
def MDS_A_by_B(mat, labels, fname):
    adist = dist.squareform(dist.pdist(mat, 'correlation'))
    coords,_ = mds(adist, dim=2)
    
    fig = plt.figure()
    fig.clf()
    plt.xlim(-15, 20)
    plt.ylim(-15, 20)
    for label, x, y in zip(labels, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x*20,y*20))
    #plt.axis('off')
    plt.savefig(fname)
    
def main_MDS(tfidf=True):
    bib_data = get_bib_data()
    at_mat, authors, term_list1, authors_cnt = get_author_by_term_mat(bib_data, tfreq=5, afreq=10)
    yt_mat, years, term_list2, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    if tfidf:
        at_mat = count_transform(at_mat)
        yt_mat = count_transform(yt_mat)
    MDS_A_by_B(at_mat, authors, 'mds_author_by_term.png')

def PCA_A_by_B(mat, labels, fname):
    aPCA = PCA(n_components=2, whiten=True).fit(mat)
    coords = aPCA.transform(mat)
    print coords
    fig = plt.figure()
    fig.clf()
    plt.xlim(-30, 30)
    plt.ylim(-30, 30)
    for label, x, y in zip(labels, coords[:,0], coords[:,1]):
        plt.annotate(label, xy=(x*10,y*10))
    plt.axis('off')
    plt.savefig(fname)

def main_PCA(tfidf=True):
    bib_data = get_bib_data()
    at_mat, authors, term_list1, authors_cnt = get_author_by_term_mat(bib_data, tfreq=5, afreq=10)
    yt_mat, years, term_list2, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    if tfidf:
        at_mat = count_transform(at_mat)
        yt_mat = count_transform(yt_mat)
    PCA_A_by_B(at_mat, authors, "pca_author_by_term.png")

def main(tfidf=True):
    bib_data = get_bib_data()
    at_mat, authors, term_list1, authors_cnt = get_author_by_term_mat(bib_data, tfreq=5, afreq=10)
    yt_mat, years, term_list2, years_cnt = get_year_by_term_mat(bib_data, freq=5)
    
    if tfidf:
        at_mat = count_transform(at_mat)
        yt_mat = count_transform(yt_mat)
    
    #bib_cluster_A_by_B(at_mat, authors, 'hcluster_authors_by_terms_2.png')
    #bib_cluster_A_by_B(yt_mat, years, 'hcluster_years_by_terms_2.png')   
    #at_mat = at_mat.T
    #yt_mat = yt_mat.T
    #bib_cluster_A_by_B(at_mat, term_list1, 'hcluster_terms_by_authors_2.png')
    #bib_cluster_A_by_B(yt_mat, term_list2, 'hcluster_terms_by_years_2.png')
    #clustering(at_mat, authors, algo='kmeans', n_clusters=3)
    #clustering(yt_mat, years, algo='kmeans', n_clusters=4)
    #at_mat = at_mat.T
    #yt_mat = yt_mat.T
    #clustering(at_mat, term_list1, algo='kmeans', n_clusters=5)
    #clustering(yt_mat, term_list2, algo='kmeans', n_clusters=10)
        
if __name__ == '__main__': 
    pass