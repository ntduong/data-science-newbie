""" Publication Bibtex Data Analysis
    Compile some simple statistics from bibtex data.
    
    (c) Duong Nguyen @TokyoTech - CS
    Email: ntduong268(at)gmail.com
"""

from pybtex.database.input import bibtex
from collections import defaultdict
import re
import numpy as np

import matplotlib
# Matplotlib plot setting
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}
matplotlib.rc('font', **font)
import matplotlib.pyplot as plt

def get_year_stats(bibdata):
    """ Compute #.of.pubs per year stats."""
    entries = bibdata.entries
    year_cnt = defaultdict(int)
    year_paper = defaultdict(list)
    for bib_key in entries:
        f = entries[bib_key].fields
        try:
            year = f['year']
            title = f['title']
            year_cnt[year] += 1
            year_paper[year].append(title)
        except KeyError: 
            continue
    
    return year_cnt, year_paper

def get_journal_stats(bibdata):
    """ Compute #.of.pubs per journal stats."""
    entries = bibdata.entries
    journal_cnt = defaultdict(int)
    journal_paper = defaultdict(list)
    short_jn_map = defaultdict(list)
    for k in entries:
        e = entries[k]
        if e.type != 'article': continue # journal is of type 'article'
        f = e.fields
        try:
            jn = f['journal']
            title = f['title']
            
            short_jn = k.split(':')[0]
            short_jn_map[short_jn].append(jn)
            
            journal_cnt[short_jn] += 1
            journal_paper[jn].append(title)
        except KeyError:
            continue
        
    return journal_cnt, journal_paper, short_jn_map
    
def get_conf_stats(bibdata):
    """ Compute #.of.pubs per conference stats."""
    entries = bibdata.entries
    conf_cnt = defaultdict(int)
    for k in entries:
        e = entries[k]
        if e.type == 'conference':
            conf_name = k.split(':')[0]
            conf_cnt[conf_name] += 1
            
    return conf_cnt

def get_type_stats(bibdata):
    """ Compute #.of.pubs per pub-type (conference, journal, techrep, etc) stats."""
    entries = bibdata.entries
    type_cnt = defaultdict(int)
    for k in entries:
        e = entries[k]
        type_cnt[e.type] += 1
        
    return type_cnt
                    
def get_author_stats(bibdata, threshold=10):
    """ Computer #.of.pubs per author stats."""
    entries = bibdata.entries
    author_cnt = defaultdict(int)
    first_authors = defaultdict(int)
    for k in entries:
        e = entries[k]
        if 'author' not in e.persons: 
            continue
        first_au = False
        for au in e.persons['author']:	
            name = au.last()[0]
            if au.first(): name += ' ,' + au.first()[0]
            author_cnt[name] += 1
            if not first_au:
                first_authors[name] += 1
                first_au = True
            
    # filter authors with >= threshold pubs
    freq_authors = dict()
    for au in author_cnt:
        if author_cnt[au] >= threshold:
            freq_authors[au] = author_cnt[au]
    
    maxv = float(max(freq_authors.values()))
    for au in freq_authors:
        freq_authors[au] /= maxv
    
    
    return author_cnt, freq_authors, first_authors

#### TITLE TERM RELATED ###
def get_stop_words(fname='txt/english_stop.txt'):
    stop_words = []
    with open(fname, 'rt') as fin:
        for line in fin:
            stop_words.append(line.strip())
    return stop_words

SPLITTER = re.compile(r'\W+')
def get_terms_from_title(title, stop_words):
    tokens = SPLITTER.split(title)
    terms = [t.lower() for t in tokens] # lowercase
    terms = [t for t in terms if t not in stop_words] # remove stop words
    return terms
    
def get_term_stats(bib_data, threshold=10):
    """ Get term frequency from publication titles."""
    
    term_cnt = defaultdict(int) # term counter for all publications.	
    stop_words = get_stop_words()
    entries = bib_data.entries
    for key in entries:
        e = entries[key]
        f = e.fields
        if 'title' not in f: 
            continue
        title = f['title']
        terms = get_terms_from_title(title, stop_words)
        for t in terms:
            term_cnt[t] += 1
    
    freq_term = {} # terms that appear more than *threshold* times
    for t in term_cnt:
        if term_cnt[t] >= threshold:
            freq_term[t] = term_cnt[t]
    return term_cnt, freq_term
    
def bar_plot(aDict, title, xlabel, ylabel, figname, show=False, sorted_by_key=False):
    n_keys = len(aDict.keys())
    ind = np.arange(n_keys)
    
    if sorted_by_key:
        x_val = sorted(aDict.keys())
        y_val = [aDict[k] for k in x_val]
    else:
        x_val = aDict.keys()
        y_val = aDict.values()
    
    width = 0.5
    fig = plt.figure(figsize=(50, 30), dpi=100)
    fig.clf()
    ax = fig.add_subplot(111)
    ax.bar(ind, y_val, width, color='blue')
    ax.set_xlim(-width, len(ind)+width)
    ax.set_ylim(0, 100)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_val, rotation=90, fontsize=30)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.savefig(figname)
    if show:
        plt.show()
    
def main(fname="txt/sugiyama.bib.txt"):
    parser = bibtex.Parser()
    bib_data = parser.parse_file(fname)
    '''
    sorted_year_cnt, year_paper = get_year_stats(bib_data)
    bar_plot(sorted_year_cnt, 'Publication per Year Statistic', 'Year', 'Number of publications', './simple/pub_year.png', show=False, sorted_by_key=True)
    
    journal_cnt, journal_paper, short_jn_map = get_journal_stats(bib_data)
    bar_plot(journal_cnt, 'Publication per Journal Statistic', 'Journal', 'Number of publications', './simple/pub_journal.png', show=False, sorted_by_key=True)
    
    type_cnt = get_type_stats(bib_data)
    bar_plot(type_cnt, 'Publication per Type Statistic', 'Type', 'Number of publications', './simple/pub_type.png', show=False, sorted_by_key=True)
    conf_cnt = get_conf_stats(bib_data)
    bar_plot(conf_cnt, 'Publication per Conference Statistic', 'Conference', 'Number of publications', './simple/pub_conf.png', show=False, sorted_by_key=True)
    author_cnt, freq_authors, first_authors = get_author_stats(bib_data, threshold=5)
    bar_plot(freq_authors, 'Publication per Author Statistic', 'Author', 'Publications rate', './simple/pub_freq_author.png', show=False, sorted_by_key=True)
    '''
    term_cnt, freq_term = get_term_stats(bib_data, threshold=10)
    bar_plot(freq_term, 'Frequent Terms Statistic', 'Term', 'Frequency', './simple/term_freq.png', show=False, sorted_by_key=True)
    
if __name__ == '__main__':
    main()