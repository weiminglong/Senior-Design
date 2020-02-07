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

# similarity imports

from nltk.corpus import wordnet as wn
from itertools import product
import sys

# variables definitions

top5AllFiles = []
list_wo_rel = []
listFiles = []
listwords = []
listweights = []
lemmatizer = WordNetLemmatizer()
fullData = []
fullData2 = []
path = os.getcwd()
top5Final = []


def top5words():
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

    cv = CountVectorizer(analyzer='word', stop_words='english', lowercase=True)

    # this steps generates word counts for the words in your docs
    word_count_vector = cv.fit_transform(corpus)

    word_count_vector.shape

    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(word_count_vector)

    count_vector = cv.transform(corpus)
    tf_idf_vector = tfidf_transformer.transform(count_vector)

    feature_names = cv.get_feature_names()

    top10 = []

    # build dataframe of first document. Determined by the index od tf-idf_vector below

    corpusLength = len(corpus)

    for i in range(0, corpusLength):
        # print(i)
        df = pd.DataFrame(tf_idf_vector[i].T.todense(), index=feature_names, columns=["tfidf"])
        df.sort_values(by=["tfidf"], ascending=False)
        # get top 5 words
        top5 = df.nlargest(10, "tfidf")
        array = []
        data1 = []
        data2 = []
        for i, j in top5.iterrows():
            data1.append(i)
            data2.append(i)
            data1.append(j.tfidf)
        array.append(data1)
        list_wo_rel.append(data2)
        top10.append(array)

    # print(list_wo_rel)
    itr = 0
    top10size = len(top10)
    for i in list_wo_rel:
        no_duplicate = []
        newList5 = []
        hashed = {}
        rem_list = group_high_similarity(i, 0.85)
        no_duplicate = remove_duplicate(i, rem_list)
        # print(no_duplicate)
        if itr<top10size:
            hashed = hash_list(top10[itr])
        else:
            continue
        # print()
        for x in range(0, 5):
            #print(hashed[no_duplicate[x]])

            newList5.append(no_duplicate[x])
            #print(no_duplicate[x])
            try:
                newList5.append(hashed[no_duplicate[x]])
            except KeyError:
                newList5.append(0.7)

            #print(newList5)
        top5Final.append(newList5)
        itr += 1


def float_check(value):
    try:
        isinstance(float(value), float)
        return True
    except:
        # print(False)
        return False


def similarity(wordx, wordy):
    sem1 = wn.synsets(wordx)
    sem2 = wn.synsets(wordy)
    maxscore = 0
    for i, j in list(product(*[sem1, sem2])):
        score = i.path_similarity(j)  # Wu-Palmer Similarity
        if score == None:
            return 0
        maxscore = score if maxscore < score else maxscore
        # print(maxscore)
        # print(i,j)
    return maxscore


def group_high_similarity(target_list, lowerbound):
    duplicateToremove = []
    result = target_list[:]
    for x in range(0, len(target_list)):
        for y in range(x + 1, len(target_list)):
            wordx, wordy = target_list[x], target_list[y]
            # print()
            value = similarity(wordx, wordy)
            if value >= lowerbound:
                result[x] = wordx
                if wordy != wordx:
                    # print(wordy+"---> "+ wordx)
                    duplicateToremove.append(wordy)
    # return result
    return duplicateToremove


def remove_duplicate(target_list, remove_list):
    # using list comprehension to perform task
    res = [i for i in target_list if i not in remove_list]
    # printing result
    # print ("The list after performing remove operation is : " + str(res))
    return res


def hash_list(list_to_hash):
    # print('list to hash')
    # print()
    list = []
    list = list_to_hash[0]
    # print(list)
    data_value = {}
    for i in range(0, len(list)):
        if i % 2 == 0 and i != len(list):
            data_value[list[i]] = list[i + 1]
            #if list[i] == 'learning':
            #print(list[i])
            #print(list[i+1])
    # print('value of hashed \n')
    # print(data_value)
    return data_value


listFiles = []
testWord = []
listLinks = []
listCategory = []
listTitles = []

# this function get the start and end time from csv files that are all in a given list of words

def timeData(filename, stwords):
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
    category = []
    title = []

    for word in stwords:
        #print(link)
        lower = word.lower()
        count = 0
        for sentence in read:
            line = sentence.split()
            #print(line)
            for each in line:
                filesName = []
                linkName = []
                line4= each
                line2 = each.lower()
                line2 = line2.strip("!@#$%^&*(()_+=)")
                line3 = line2.split(":")
                # store dictionary in json file
                topword = []

                if len(line3)<=1:
                    continue
                comparedword = line3[1].lower()
                if line3[0] == "word" and lower == comparedword and lower not in foundWords:
                   # print(line3)
                    temptopword = []
                    name = lower
                    startTime = line[1]
                    start = startTime.split("start_time:")
                    startFin = start[1]
                    # print(k[1])
                    endTime = line[2]
                    end = endTime.split("end_time:")
                    endFin = end[1]
                    val2 = line3[0:2]
                    foundWords.append(lower)
                    temptopword.append(lower)
                    temptopword.append(startFin)
                    temptopword.append(endFin)
                    # tempfullData = tempfullData + temptopword
                    tempfullData.append(temptopword)
                    wordPresent = True
                    filesName.append(filename)

                if line3[0] == "link" and wordPresent == True and line[0] not in link:
                    lane = []
                    #print()
                    if(len(link)==0):
                        #link.append(line[0][5:])
                        lane = line4.split("word")
                        laneLink = line4.split("title:")
                        if len(laneLink) >= 2:
                            #print(laneLink[0])
                            link.append(laneLink[0])
                        elif len(lane)>=2 and len(lane[0]) <= len(lane[1]):
                            #print(line[0][5:])
                            link.append(line[0][5:])
                        else:
                           # print(lane[0][5:])
                            link.append(lane[0][5:])

                    elif(len(link)>0):
                        continue

                if line3[0] == "category" and wordPresent == True:
                    if(len(category)==0):
                            category.append(line3[1])
                            #print(category)
                    elif(len(category)>0):
                        continue

                if line3[0] == "title" and wordPresent == True:
                    #print(line)
                    #print()
                    if (len(title) == 0):
                        title.append(line[0][6:])
                    elif (len(title) > 0):
                        continue

    if len(foundWords) < 5:
        tempfullData = []
        return

    if foundWords in testWord:
        tempfullData = []
        return
    testWord.append(foundWords)
    if (len(tempfullData) <= 2):
        tempfullData = []
    if (len(tempfullData) < 5):
        tempfullData = []
    if link not in listLinks and len(tempfullData) >= 5:
        listLinks.append(link)
        #print(listLinks)
    if len(tempfullData) >= 5:
        listCategory.append(category)
        #print(listCategory)
    if  len(tempfullData) >= 5:
        listTitles.append(title)
    #print(listTitles)
    fullData.append(tempfullData)

# get the weight from tfidf data above
# listwords = []
listweights = []

def weights():
    for i in top5Final:
        size = len(i)
        temp = []
        tempfloat = []
        for j in range(0, size):
            # print(j)
            tempVar = []
            tempWeight = []
            if (j % 2 == 0 and j != len(i)):
                # print(i[0][j])
                weight = i[j + 1]
                tempVar.append(i[j])
                tempWeight.append(i[j + 1])
                temp = temp + tempVar
                tempfloat = tempfloat + tempWeight
        listwords.append(temp)
        listweights.append(tempfloat)


def words_time_weights():
    # parameter to be passed in time_data function
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
    index = 0

    lengthLimit = len(listweights)
    fulLeng = len(fullData2)
    for i in fullData2:
        # print(i)
        incr = 0
        for j in i:
            if (incr < sizeI and count < lengthLimit):
                weight = '%.3f' % (listweights[count][incr])
                j.append(weight)
                incr += 1
        count += 1
    # print(listFiles)
    count = 0
    my_dict = {}

    for i in fullData2:
        # if count == len(listFiles)-1:
        if count == len(listLinks) - 1:
            break
        indv_dict = {
            "words": "",
            "link": "",
            "category":"",
            "title":""
        }
        # print(listFiles[count])
        indv_dict["words"] = i
        # indv_dict["filename"] = listFiles[count]
        indv_dict["link"] = listLinks[count]
        indv_dict["category"] = listCategory[count]
        indv_dict["title"] = listTitles[count]
        my_dict[str(count)] = indv_dict
        count += 1

    # store dictionary in json file
    with open('top5Words.json', 'w') as filehandle:
        json.dump(my_dict, filehandle, indent=5)

    return my_dict

def TFIDF():
    top5 = {}
    top5words()
    weights()
    top5 = words_time_weights()
    #print(top5)
    return top5

#TFIDF()

