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

top5AllFiles = []
fullData = []
fullData2 = []
lemmatizer = WordNetLemmatizer()
path = os.getcwd()

def top5words():

    # print(location)
    ps = PorterStemmer()
    # empty list of corpus
    corpus = []

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

    #print(top5AllFiles)
    # print()

listFiles = []
testWord = []

#this function get the start and end time from csv files that are all in a given list of words

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
                   # topword = str(lower) + ", " + str(startFin)+ " , " + str(endFin)
                   # temptopword.append(topword)
                    temptopword.append(lower)
                    temptopword.append(startFin)
                    temptopword.append(endFin)
                    #tempfullData = tempfullData + temptopword
                    tempfullData.append(temptopword)
                    wordPresent = True
                    filesName.append(filename)
                    # print(filename)
                    # print(tempfullData)
                    # print()
                #if line3[0] == "link" and wordPresent == True and line[0] not in link:
                   # link.append(line[0])
                if(len(tempfullData) >=5 and filesName not in listFiles and len(filesName)!=0):
                    listFiles.append(filesName)
    testWord = foundWords

    #tempfullData = tempfullData+ link
    if (len(tempfullData) <= 2):
        tempfullData = []
    if (len(tempfullData) < 5):
        tempfullData = []
    fullData.append(tempfullData)

#get the weight from tfidf data above
listwords = []
listweights = []


def weights():
    for i in top5AllFiles:
        size = len(i[0])
        temp = []
        tempfloat = []
        for j in range(0, size):
            #print(j)
            tempVar = []
            tempWeight = []
            if (j % 2 == 0):
                #print(i[0][j])
                weight = i[0][j + 1]
                tempVar.append(i[0][j])
                tempWeight.append(i[0][j + 1])
                temp = temp + tempVar
                tempfloat = tempfloat + tempWeight
        listwords.append(temp)
        listweights.append(tempfloat)

def words_time_weights():
    #parameter to be passed in time_data function
    for i in listwords:
        # parse through file and get time stamp
        for filename in sorted(glob.glob(os.path.join(path, '*.csv'))):
            # print(filename)
            timeData(filename, i)


    # stip empty list within a list
    fullData2 = [e for e in fullData if e]
    dictCorpus = {}
    sizeI = len(fullData2[0])
    counter = 0
    incr = 0
    count = 0
    index=0

    lengthLimit = len(listweights)
    fulLeng= len(fullData2)
    for i in fullData2:
       # print(i)
        incr = 0
        indexIn = 0
        myDict = []
        test1 = []
        line = []
        #print("printing j")
        for j in i:
          if (incr<sizeI and count<lengthLimit):
                weight ='%.3f'%(listweights[count][incr])
                j.append(weight)
                incr+=1
        count+=1
    #print(listFiles)
    count =0
    my_dict = {}

    for i in fullData2:
        if count == len(listFiles)-1:
            break
        indv_dict = {
            "words": "",
            "filename": ""
        }
       # print(listFiles[count])
        indv_dict["words"] = i
        indv_dict["filename"] = listFiles[count]
        my_dict[str(count)] = indv_dict
        count +=1

    # store dictionary in json file
    with open('top5Words.json', 'w') as filehandle:
        json.dump(my_dict,filehandle,indent =5)

    return my_dict

# store dictionary in json file
#with open('top5Words.json', 'w') as filehandle:
    #json.dump(dictCorpus, filehandle)
# store json format in database
# json.dump(dictCorpus,sort_keys= True,indent = 5)


def TFIDF():
    top5 = {}
    top5words()
    weights()
    top5 = words_time_weights()

    # for i in top5:
    #     print(top5[i])

    return top5

