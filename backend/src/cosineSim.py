
import pandas as pd, numpy as np, re, sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import time
#need to install package with command pip install sparse_dot_topn


def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape

    idx_dtype = np.int32

    nnz_max = M * ntop

    indptr = np.zeros(M + 1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data, indices, indptr), shape=(M, N))

def get_matches_df(sparse_matrix, A, B, top=100):
    non_zeros = sparse_matrix.nonzero()

    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = A[sparserows[index]]
        right_side[index] = B[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]

    return pd.DataFrame({'left_side': left_side,
                         'right_side': right_side,
                         'similairity': similairity})
"""
df_dirty = {"name":["gogle","bing","amazn","facebook","fcbook","abbasasdfzz","zsdfzl"]}

df_clean = {"name":["google","bing","amazon","facebook"]}
"""
df_dirty = {"name":["told","hello","choreography","facebook","fcbook","abbasasdfzz","zsdfzl","Barack Obama"]}

df_clean = {"name":["told","dance","amazon","book","Barack"]}

print (df_dirty["name"])
print (df_clean["name"])

vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
tf_idf_matrix_clean = vectorizer.fit_transform(df_clean['name'])
tf_idf_matrix_dirty = vectorizer.transform(df_dirty['name'])

t1 = time.time()
matches = awesome_cossim_top(tf_idf_matrix_dirty, tf_idf_matrix_clean.transpose(), 1, 0)
t = time.time()-t1
print("SELFTIMED:", t)

matches_df = get_matches_df(matches, df_dirty['name'], df_clean['name'], top=0)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(matches_df)


