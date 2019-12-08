# Flask app imports
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS

# TFIDF imports
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


# path is that of the current directory
path = os.getcwd()
# print(location)
ps = PorterStemmer()
# empty list of corpus
corpus = []

fullData = []
fullData2 = []
# append each file with .txt extension to the corpus

for filename in sorted(glob.glob(os.path.join(path, '*.txt'))):
    with open(filename, 'r') as f:
        text = f.read()
        corpus.append(text)

vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus)

stop_words = set(stopwords.words('english'))

# ps = PorterStemmer()
analyzer = CountVectorizer().build_analyzer()

lemmatizer = WordNetLemmatizer()


# def stem_words(doc):
# return[port.stem(word) for word in analyzer(doc) if word not in stop_words]

def stem_words(doc):
    return [lemmatizer.lemmatize(word) for word in analyzer(doc) if word not in stop_words]



cv = CountVectorizer(analyzer=stem_words, stop_words='english', lowercase=True)

# cv=CountVectorizer(analyzer='word', stop_words = 'english',lowercase=True)

# this steps generates word counts for the words in your docs
word_count_vector = cv.fit_transform(corpus)

word_count_vector.shape

tfidf_transformer = TfidfTransformer()
tfidf_transformer.fit(word_count_vector)

count_vector = cv.transform(corpus)
tf_idf_vector = tfidf_transformer.transform(count_vector)

feature_names = cv.get_feature_names()

top5AllFiles = []

# build dataframe of first document. Determined by the index od tf-idf_vector below

corpusLength = len(corpus)

for i in range(0, corpusLength):
    # print(i)
    df = pd.DataFrame(tf_idf_vector[i].T.todense(), index=feature_names, columns=["tfidf"])
    df.sort_values(by=["tfidf"], ascending=False)
    # get top 5 words
    top5 = df.nlargest(5, "tfidf")
    # print(top5)
    array = []
    data1 = []
    for i, j in top5.iterrows():
        data1.append(i)
        data1.append(j.tfidf)

    array.append(data1)
    top5AllFiles.append(array)

# print(top5AllFiles)
# print()

listFiles = []

def timeData(filename, listwords):
    tempfullData = []
    foundWords = []
    # try:
    wordPresent = False
    file = open(filename, "r")
    read = file.readlines()
    file.close()
    linkval = ""
    linktemp = []
    link = []

    for word in listwords:
        lower = word.lower()
        count = 0
        for sentence in read:
            line = sentence.split()
            for each in line:
                filesName = []
                line2 = each.lower()
                line2 = line2.strip("!@#$%^&*(()_+=)")
                line3 = line2.split(":")
                topword = []
                comparedword = line3[1].lower()
                stemmedWord = lemmatizer.lemmatize(comparedword)
                # print(comparedword,":",stemmedWord)
                #if line3[0]=="word" and lower == line3[1].lower() and lower not in foundWords:
                if line3[0] == "word" and lower == stemmedWord and lower not in foundWords:
                    temptopword = []
                    name = lower
                    startTime = line[1]
                    start = startTime.split("start_time:")
                    startFin = start[1]
                    #print(k[1])
                    endTime = line[2]
                    end = endTime.split("end_time:")
                    endFin = end[1]
                    #print(endTime.split("end_time:"))
                    val2 = line3[1]
                    foundWords.append(lower)
                    topword = lower + ", " + startFin+ " , " + endFin
                    temptopword.append(topword)
                    #tempfullData = tempfullData + temptopword
                    tempfullData.append(temptopword)
                    wordPresent = True
                    filesName.append(filename)
                    # print(filename)
                    # print(tempfullData)
                    # print()
                if line3[0] == "link" and wordPresent == True and line[0] not in link:
                    link.append(line[0])
                if(len(tempfullData) >=5 and filesName not in listFiles and len(filesName)!=0):
                    listFiles.append(filesName)

    # if(len(tempfullData) <5 and len(tempfullData) >0):
    # continue
    # print(tempfullData)
    # print(listFiles)
    # print()
    tempfullData = tempfullData+ link
    if (len(tempfullData) <= 2):
        tempfullData = []
    if (len(tempfullData) < 5):
        tempfullData = []
    fullData.append(tempfullData)


    #tempfullData = tempfullData + filesName
    #fullData.append(tempfullData)



listwords = []
listweights = []
for i in top5AllFiles:
    size = len(i[0])
    temp = []
    tempfloat = []
    for j in range(0, size):
        tempVar = []
        tempWeight = []
        if (j % 2 == 0):
            weight = i[0][j + 1]
            tempVar.append(i[0][j])
            tempWeight.append(i[0][j + 1])
            temp = temp + tempVar
            tempfloat = tempfloat + tempWeight
    listwords.append(temp)
    listweights.append(tempfloat)


for i in listwords:
    # parse through file and get time stamp
    for filename in sorted(glob.glob(os.path.join(path, '*.csv'))):
        # print(filename)
        timeData(filename, i)


# stip empty list within a list
fullData2 = [e for e in fullData if e]
#print(fullData2)
# variable definition
dictCorpus = {}
#print(listFiles)
sizeI = len(fullData2[0])
count = 0
lengthLimit = len(listweights)
# print("size")
# print(sizeI)
# print(len(listweights)
# print(sizeI)
#incr = 0;
#for i in range(0,len(listFiles)):
     # lenght = len(listFiles[i])
     #k =
     #listFiles[i] = [x[x.index('c/'):] if 'src/' in x else x for x in listFiles[i]]
#print(fullData2)
print()
print()

#print(listweights[1])
print()
print()
dictCorpus = {}
counter = 0
incr = 0
count = 0
index=0

fulLeng= len(fullData2)
for i in fullData2:
    indexIn = 0
    incr = 0
    myDict = []
    test1 = []
    line = []
    for j in i:
        if (count<lengthLimit and incr<sizeI):
            #tester.append(listweights[0][incr])
           # print(j[0])
            weight = " ,"+'%.3f'%(listweights[count][incr])
           # print(weight)
            j[0] += weight
            incr+=1
        count+=1









print()
print(fullData2)
print("corpus: $$$$$$$$$$$$$$$$$$############")
#print(dictCorpus)
#print(listFiles)

# store dictionary in json file
#with open('top5Words.json', 'w') as filehandle:
    #json.dump(dictCorpus, filehandle)
# store json format in database
# json.dump(dictCorpus,sort_keys= True,indent = 5)

