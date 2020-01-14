import bs4 as bs
import urllib.request
import re
import nltk
from gensim.models import Word2Vec
import pandas as pd
import os, glob
import numpy as np
import json
from textblob import TextBlob
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse.csr import csr_matrix  # need this if you want to save tfidf_matrix

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer


path = os.getcwd()

def text_preprocessing():
    

def word_similarity(word, lower_bound):
    corpus = []
    article_text = ""

    # append each file with .txt extension to the corpus

    for filename in sorted(glob.glob(os.path.join(path, 'e.txt'))):
        #filename = sorted(glob.glob(os.path.join(path, 'e.txt')
        with open(filename, 'r') as f:
            text = f.read()
            corpus.append(text)
            article_text += text

            # Cleaing the text
            processed_article = article_text.lower()
            processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
            processed_article = re.sub(r'\s+', ' ', processed_article)

            # Preparing the dataset
            all_sentences = nltk.sent_tokenize(processed_article)

            all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

            # Removing Stop Words
            from nltk.corpus import stopwords
            for i in range(len(all_words)):
                all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
            #cleprint(all_words)
            word2vec = Word2Vec(all_words, min_count=2)
            word2vec.most_similar(word,topn =5)

            """
            vocabulary = word2vec.wv.vocab
            #print(vocabulary)
            #model.wv.vocab
            param = word
            v1 = word2vec.wv[param]
            print()
            #print('v1')
           # v1 = word2vec.wv.vocab
            #print(v1)
            print('value of param is:'+param)
            print()
            print()
            sim_words = word2vec.wv.most_similar(param)
            print(sim_words)
            print()
            print()
            break
            """
            """
            print(sim_words[0][0])
            print()
            print()
            weight = sim_words[0][1]
            if weight >= 0.7:
                return 
            print(sim_words[0][1])
            #print(v1)
            """
            
word_similarity('cellular',0.5)

"""
from gensim.models import Word2Vec

# define training data
sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
			['this', 'is', 'the', 'second', 'sentence'],
			['yet', 'another', 'sentence'],
			['one', 'more', 'sentence'],
			['and', 'the', 'final', 'sentence']]
# train model
model = Word2Vec(sentences, min_count=1)
# summarize the loaded model
print(model)
print()
# summarize vocabulary
words = list(model.wv.vocab)
print(words)
print()
# access vector for one word
print(model['more'])
print()
# save model
model.save('model.bin')
# load model
new_model = Word2Vec.load('model.bin')
print(new_model)
print()
print()
print(dir(model))
print()
print(model.wv.vocab)
print()

from sklearn.decomposition import PCA
from matplotlib import pyplot


"""
"""
# fit a 2d PCA model to the vectors
X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
"""



