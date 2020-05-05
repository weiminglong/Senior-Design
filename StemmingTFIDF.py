#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import os,glob
import numpy as np
import json
from textblob import TextBlob
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse.csr import csr_matrix #need this if you want to save tfidf_matrix

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


#path is that of the current directory
path = os.getcwd()
#print(location)

#empty list of corpus
corpus = []

fullData = []
fullData2 = []
#append each file with .txt extension to the corpus

for filename in sorted(glob.glob(os.path.join(path, '*.txt'))):
    with open(filename, 'r') as f:
        text = f.read()
        #print (filename)
        #print (len(text))
        corpus.append(text)


        
stop_words = set(stopwords.words('english'))
    
port = PorterStemmer()
analyzer = CountVectorizer().build_analyzer()

def stem_words(doc):
    return[port.stem(word) for word in analyzer(doc) if word not in stop_words]



cv=CountVectorizer(analyzer=stem_words,stop_words = 'english',lowercase=True)

# this steps generates word counts for the words in your docs
word_count_vector=cv.fit_transform(corpus)

word_count_vector.shape


tfidf_transformer=TfidfTransformer()
tfidf_transformer.fit(word_count_vector)


count_vector=cv.transform(corpus)
tf_idf_vector=tfidf_transformer.transform(count_vector)


feature_names = cv.get_feature_names()

top5AllFiles = []


#build dataframe of first document. Determined by the index od tf-idf_vector below

corpusLength = len(corpus)

for i in range(0,corpusLength):
    #print(i)
    df = pd.DataFrame(tf_idf_vector[i].T.todense(), index=feature_names, columns= ["tfidf"])
    df.sort_values(by=["tfidf"],ascending=False)
    #get top 5 words
    top5=df.nlargest(5, "tfidf")
    #print(top5)
    array = []
    data1=[]
    for i, j in top5.iterrows():
        data1.append(i)
        data1.append(j.tfidf)

    #print(data1)
    # open output file for writing
    array.append(data1)
    top5AllFiles.append(array)

print(top5AllFiles)
print()
print()
print()








# In[ ]:




