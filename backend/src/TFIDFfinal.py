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
fullData = []
fullData2 = []
#append each file with .txt extension to the corpus

for filename in sorted(glob.glob(os.path.join(path, '*.txt'))):
    with open(filename, 'r') as f:
        text = f.read()
        #print (filename)
        #print (len(text))
        corpus.append(text)

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

    # open output file for writing
    array.append(data1)
    top5AllFiles.append(array)



def timeData(filename, listwords):
    tempfullData = []
    foundWords= []
        #try:
    wordPresent = False
    file = open(filename,"r")
    read= file.readlines()
    file.close()
    #print(read)
    linkval=""
    linktemp = []
    link = []
   
    for word in listwords:
        lower = word.lower()
        count = 0
        for sentence in read:
            line = sentence.split()
            for each in line:
                line2 = each.lower()
                line2=line2.strip("!@#$%^&*(()_+=)")
                line3=line2.split(":")
                topword = []
                if line3[0]=="word" and lower == line3[1] and lower not in foundWords:
                    temptopword = []
                    name= lower
                    startTime = line[1]
                    endTime = line[2]
                    val2=line3[1]
                    foundWords.append(lower)
                    topword = "word: "+name+"  "+ startTime+"  "+ endTime
                    temptopword.append(topword)
                    tempfullData= tempfullData+temptopword
                    wordPresent= True
                    
                if line3[0]=="link" and wordPresent == True and line[0] not in link:
                    link.append(line[0])
 
    tempfullData =  tempfullData + link
    fullData.append(tempfullData)



#parse through top5words list and get weights and string in seperate list
    
listwords = []
listweights = []
for i in top5AllFiles:
    size = len(i[0])
    temp = []
    tempfloat = []
    for j in range(0,size):
        tempVar=[]
        tempWeight = []
        if(j%2==0):
            weight = i[0][j+1]
            tempVar.append(i[0][j])
            tempWeight.append(i[0][j+1])
            temp = temp+ tempVar
            tempfloat = tempfloat+tempWeight
    listwords.append(temp)
    listweights.append(tempfloat)

for i in listwords:
  
    #parse through file and get time stamp
    for filename in sorted(glob.glob(os.path.join(path, '*.csv'))):
        timeData(filename,i)

#stip empty list within a list
fullData2 = [e for e in fullData if e]


#variable definition
dictCorpus = {}
count = 0

for i in fullData2:
    myDict = {} 
    #print(i)
    size = len(listweights[count])
    #print(size)
    increment = 0
    for j in range(size):
        #print(len(i))
        test = []
        temper = []
        temper.append(listweights[count][j])
        test.append(i[j])
        myDict[increment] =test+temper
        if(j==size-1):
            myDict[increment].append(i[size])
        increment+=1
    dictCorpus[count]=myDict   
    count+=1
print(dictCorpus)

#write to json file
with open('top5Words.json', 'w') as filehandle:
        json.dump(dictCorpus, filehandle)
   