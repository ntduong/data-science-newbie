""" Make blog/feed text dataset from a list of seed urls
    
    (c) Duong Nguyen @TokyoTech - CS
    Email: ntduong268(at)gmail.com
"""

import feedparser
from utils.porter_stemmer import PorterStemmer
from collections import defaultdict
import re
import numpy as np

HTML_TAG_STRIPPER = re.compile(r'<[^>]+>')
TEXT_SPLITTER = re.compile(r'\W+')

# Initialize stemmer
aStemmer = PorterStemmer()

# Load stop words
STOP_WORDS_FILE = 'txt/english_stop.txt'
stop_words = []
with open(STOP_WORDS_FILE, 'rt') as fin:
    for line in fin:
        stop_words.append(line.strip().lower())

def get_words(html):
    """ Get words (terms) from an article's html text.
        Stem words using Porter stemming algorithm and remove also common words.
    """
    text = HTML_TAG_STRIPPER.sub('', html) # stripping off HTML tags
    tokens = TEXT_SPLITTER.split(text) # split text into tokens with non-alphabetical delimiters
    words = [w.lower() for w in tokens if w != ''] # convert all token to lowercase
    words = [w for w in words if w not in stop_words] # remove stop (common) words
    #words = [aStemmer.stem(w, 0, len(w)-1) for w in words] # stemming
    return words

def get_articles_words(url_file='txt/urls.txt'):
    """ Process all articles from a given feed list.
        Compute the word count for all articles,
                the word counts for each articles,
                articles' titles.
    """
    word_cnt = defaultdict(int) # counters of words in all articles
    a_ind = 0 # article index
    articles = [] # articles[i] := word count for the i-th article (articles is a list of dicts) 
    article_titles = [] # list of articles' titles
    
    with open(url_file, 'rt') as urls:
        for url in urls:
            feed = feedparser.parse(url)
            for e in feed.entries:
                if e.title in article_titles: continue
                # get words from the title and description of article
                words = get_words(e.title.encode('utf-8') + " " + e.description.encode('utf-8'))
                article_titles.append(e.title)
                articles.append(defaultdict(int))
                for word in words:
                    word_cnt[word] += 1
                    articles[a_ind][word] += 1
                a_ind += 1
    
    return word_cnt, articles, article_titles
                
def make_mat(word_cnt, articles, threshold=0.6):
    """ Make an article-by-word matrix: aw_mat (ndarray)
        aw_mat[a][w] := freq of word w in article a
        Intuitively, each article is represented as a bag of words, along with their frequencies.
        We assume that similar articles should have similar bags of words's frequencies.
    """
    n_articles = len(articles)
    word_list = [] # list of words that appear more than 3 times, but not too much, say threshold % of # articles
    for w in word_cnt:
        if word_cnt[w] >= 3 and word_cnt[w] < threshold * n_articles:
            word_list.append(w)
            
    aw_mat = [[ (w in a and a[w] or 0) for w in word_list ] for a in articles]
    aw_mat = np.asarray(aw_mat, dtype="float64") # convert to ndarray
    return aw_mat, word_list

def get_sites_words(url_file='txt/feedlist.txt'):
    word_cnt = defaultdict(int) # counters of words in all articles
    site_ind = 0 
    sites = []  
    site_urls = [] 
    with open(url_file, 'rt') as urls:
        for url in urls:
            site_urls.append(url)
            sites.append(defaultdict(int))
            feed = feedparser.parse(url)
            for e in feed.entries:
                # get words from the title and description of article
                words = get_words(e.title.encode('utf-8') + " " + e.description.encode('utf-8'))
                for word in words:
                    word_cnt[word] += 1
                    sites[site_ind][word] += 1
            site_ind += 1
    
    return word_cnt, sites, site_urls
    
def make_site_by_word_mat(word_cnt, sites, freq=5, percent=0.7):
    n_sites = len(sites)
    total_cnt = sum(word_cnt.values())
    word_list = [] # list of words that appear more than 3 times, but not too much, say threshold % of # articles
    for w in word_cnt:
        if word_cnt[w] >= freq and word_cnt[w] <= percent * total_cnt:
            word_list.append(w)
            
    sw_mat = [[ (w in s and s[w] or 0) for w in word_list ] for s in sites]
    sw_mat = np.asarray(sw_mat, dtype="float64") # convert to ndarray
    return sw_mat, word_list

if __name__ == '__main__':
    pass