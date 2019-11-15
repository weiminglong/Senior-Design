import pandas as pd
import os,glob
import numpy as np
import json

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse.csr import csr_matrix #need this if you want to save tfidf_matrix



#path is that of the current directory
path = os.getcwd()
#print(location)

#empty list of corpus
corpus = []

#append each file with .txt extension to the corpus

for filename in sorted(glob.glob(os.path.join(path, '*.txt'))):
    with open(filename, 'r') as f:
        text = f.read()
        #print (filename)
        #print (len(text))
        corpus.append(text)

    
vectorizer = TfidfVectorizer(analyzer='word',stop_words = 'english', sublinear_tf=True)
tfidf_matrix = vectorizer.fit_transform(corpus)
#prints the tfidf MATRIX 
#print(tfidf_matrix)

#print(docs)


#feature_names = vectorizer.get_feature_names()
#corpus_index = [n for n in corpus]
#df = pd.DataFrame(tfidf_matrix.T.todense(), index=feature_names, columns=corpus_index)
#print(df)

#remove stopwords 
#maxfeatures is to only get the top 5 relevant data
cv=CountVectorizer(analyzer='word', stop_words = 'english',lowercase=True,strip_accents='unicode')

# this steps generates word counts for the words in your docs
word_count_vector=cv.fit_transform(corpus)

word_count_vector.shape


tfidf_transformer=TfidfTransformer(smooth_idf=True)
tfidf_transformer.fit(word_count_vector)


count_vector=cv.transform(corpus)
tf_idf_vector=tfidf_transformer.transform(count_vector)

feature_names = cv.get_feature_names()

top5AllFiles = []


#build dataframe of first document. Determined by the index od tf-idf_vector below

corpusLength = len(corpus)-1

dataFile = {}
dataFile['Document'] = []

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
    
    top5AllFiles.append(array)
    array.append(data1)
    #print(array)

with open('top5Words.json', 'w') as filehandle:
        json.dump(top5AllFiles, filehandle)

        
#parse through file and get time stamp

tscorpus = []
for filename in sorted(glob.glob(os.path.join(path, '*.csv'))):
    with open(filename, 'r') as f:
        text = f.read()
        #print (filename)
        #print (len(text))
        tscorpus.append(text)
        #print(tscorpus)


#print(corpus)
print()
print()
print()
print()
#print(tscorpus)


