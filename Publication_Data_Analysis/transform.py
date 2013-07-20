""" Transform from occurence matrix to tf, tf-idf matrix
    A wrapper of sklearn's Tf-idf transformer.
    See sklearn.feature_extraction.text.TfidfTransformer for details.
    
    Tf: term-frequency
    Tf-idf: term-frequency x (document-frequency)^{-1}
    See IR book for more details.
    
    (c) Duong Nguyen @TokyoTech - CS
    Email: ntduong268(at)gmail.com
"""

from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

def count_transform(counter_mat, use_idf=True):
    """ Transform counter (occurence) matrix to tf/tf-idf matrix.
        Params: 
            counter_mat: n x d matrix (n samples, d features)
                        E.g. Matrix of term counts for articles
            use_itf: use idf reweighting scheme.
    """
    transformer = TfidfTransformer(norm='l2', use_idf=use_idf, smooth_idf=True).fit(counter_mat)
    new_mat = transformer.transform(counter_mat)
    sz = new_mat.shape
    ret = np.zeros(sz, dtype="float64")
    for r in xrange(sz[0]):
        for c in xrange(sz[1]):
            ret[r,c] = new_mat[r,c]
    return ret


