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
import codecs
# similarity imports

from nltk.corpus import wordnet as wn
from itertools import product
import sys
import time
import boto3
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
s3 = boto3.resource('s3')
bucket = s3.Bucket('qac-txt-csv')


#function that takes in parameter a list and sort its elements in alphabetical order
#ignores the case sensitive
def sortCaseIns(lst):
    lst2 = [[x for x in range(0, 2)] for y in range(0, len(lst))]
    for i in range(0, len(lst)):
        lst2[i][0] = lst[i].lower()
        lst2[i][1] = lst[i]
    lst2.sort()
    for i in range(0, len(lst)):
        lst[i] = lst2[i][1]


#read the files names in a bucket both csv and txt file and return two lists
#of all the csv and txt files in the bucket in alphabetical order
def read_all_csv_txt_files():

    csvFiles = []
    txtFiles = []
    csvCorpus = []
    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        #print(type(key))
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.csv'):
            csvFiles.append(key)
            csvRead = obj.get()['Body'].read().decode('utf-8')
          #  print(csvRead)
            csvCorpus.append(csvRead)
            #print()
            #print()
            #print(type(csvFiles))
        elif key.endswith('.txt'):
            txtFiles.append(key)
    sortCaseIns(csvFiles)
    sortCaseIns(txtFiles)
    return csvFiles,txtFiles,csvCorpus


#read all txt files and return a corpus of all the files read
def read_all_txt_files():
    corpus = []
   # s3 = boto3.resource('s3')
    #bucket = s3.Bucket('qac-txt-csv')

    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.txt'):
            texRead = obj.get()['Body'].read().decode('utf-8')
            #print(texRead)
            #print()
            #print()
            #print()
            corpus.append(texRead)
    return corpus





def top5words():
    ps = PorterStemmer()
    # empty list of corpus
    corpus = []

    # append each file with .txt extension to the corpus
    """
    for filename in sorted(glob.glob(os.path.join(path, '*.txt'))):
        with open(filename, 'r') as f:
            text = f.read()
            corpus.append(text)
            
    """
    corpus = read_all_txt_files()
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

#remove empty elements from a list
def remove_emptyEl_list(test_list):
    while ("" in test_list):
        test_list.remove("")
        return test_list

listFiles = []
testWord = []
listLinks = []
listCategory = []
listTitles = []

# this function get the start and end time from csv files that are all in a given list of words
fullTime_dict = dict()


# this function get the start and end time from csv files that are all in a given list of words

def timeData(filename,stwords):
    #timeData(csvCorpora, i, word)
    #print('filename is:',filename)
    tempfullData = []
    foundWords = []
    # try:
    wordPresent = False
    read = ""
    #file = open(filename, "r")
    #read = file.readlines()
    #file.close()
    for obj in bucket.objects.all():
        # the key here represent the files names
        key = obj.key
        #print('key or filename is:',key)
        # check for files that end with certain extension precisely .csv extension
        if key.endswith(filename) == False:
            continue
            #print()
            #read = open(filename, encoding='utf-8')
       # print(key, filename)
    linkval = ""
    linktemp = []
    link = []
    #print(read)
    word_time_array = {}
    category = []
    title = []
    #print(read)
    #print()

    for word in stwords:
        #print(link)
        lower = word.lower()
        count = 0
        #print(open(filename, encoding='utf-8'))
        #print(filename)
        f = codecs.open(filename, 'r', 'UTF-8')
        for sentence in f:
            #print(line)
        #print(f)
        #for sentence in open(filename, encoding='utf-8'):
            #print(sentence)
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
                    start = startTime[11:]
                   # print(start)
                    startFin = start
                    #print(startFin)
                    if lower in fullTime_dict:
                        # append the new number to the existing array at this slot
                        #fullTime_dict[lower].append(startFin+" ")
                        #fullTime_dict[lower] +=""
                        #original = ""+fullTime_dict[lower]
                        fullTime_dict[lower] = startFin+" "
                        #fullTime_dict[lower] = original
                        #continue
                    else:
                        # create a new array in this slot
                        fullTime_dict[lower] = startFin+" "
                        #print('from the root',fullTime_dict[lower])

                    endTime = line[2]
                    end = endTime.split("end_time:")
                    endFin = end[1]
                    val2 = line3[0:2]
                    foundWords.append(lower)
                    temptopword.append(lower)
                    tempfullData.append(temptopword)
                    wordPresent = True
                    filesName.append(filename)

                if line3[0] == "link" and wordPresent == True and line[0] not in link:
                    lane = []
                    laneLink = []
                    #print()
                    if(len(link)==0):
                        #link.append(line[0][5:])
                        lane = line4.split("word")
                        if len(lane)>=2 and len(lane[0]) <= len(lane[1]):
                            laneLink = line4.split("link:")
                        if len(laneLink) >= 2:
                            link.append(line4[7:])
                        elif len(lane)>=2 and len(lane[0]) <= len(lane[1]):
                            link.append(line4[6:])
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
                    if (len(title) == 0):
                        title.append(sentence[6:])
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

    if len(tempfullData) >= 5:
        listCategory.append(category)
        #print(listCategory)
    if  len(tempfullData) >= 5:
        listTitles.append(title)
    #print(listTitles)
    fullData.append(tempfullData)
   # print(fullData)

# get the weight from tfidf data above
# listwords = []
listweights = []
"""
def dictionary_cleanup(wordArray):
    k = fullTime_dict["vector"]
    #print(k)
    #print(type(k))
    for lword in wordArray:
        for w in lword:
           #print(type(w))
           time_array = []
           times = " "
           times = fullTime_dict[w]
           temp = []
           if(type(times) == list):
               temp = times
           else:
               temp = times.split(" ")
           time_array = temp
           time_array = list(dict.fromkeys(time_array))
           time_array = [i for i in time_array if i]
           #sorted((time.strptime(d, "%M:%S") for d in time_array), reverse=True)
           time_array = sorted(time_array)
           fullTime_dict[w] = time_array
           
"""
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
        if temp not in listwords:
            listwords.append(temp)
        else:
            continue
        listweights.append(tempfloat)
"""
def string_List_dictionary_key():
    for i in fullTime_dict:
        print(i)
"""
new_list = []
def new_map():
    #print()
    #cnt = 0
    for i in listwords:
        tmpmap = []
        for w in i:
            tmpmap.append(w)
            print('final list:',fullTime_dict[w])
            tmpmap.append(fullTime_dict[w])
            new_list.append(tmpmap)
            #cnt +=1

def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


def string_list_value_dictionary():
    k = " "
    value = []
    for i in fullTime_dict:
        print(fullTime_dict[i])
        k = listToString(fullTime_dict[i])
        value = k.split(" ")
        value = remove_emptyEl_list(value)
        fullTime_dict[i] = value
        #print(fullTime_dict[i])
        #print()

    # print(type(k[0][1]))
def words_time_weights():
    csvCorpora = []
    csvCollection, txtCollection, csvCorpora = read_all_csv_txt_files()
    #print(fullTime_dict)
    # parameter to be passed in time_data function

    for i in listwords:
        # parse through file and get time stamp
        for filename in csvCollection:
            # print(filename)
            timeData(filename, i)
    """
    for word in listwords:
        for i in range(len(csvCorpora)):
            timeData(csvCorpora,i,word,csvCollection[i])
    """
    #print(listLinks)
    # stip empty list within a list
    fullData3 =[]
    fullData2 = [e for e in fullData if e]
    string_list_value_dictionary()
    #print(fullData2)

    tempfullData2 = []
    for list in fullData2:
        tempfullData = []
        for words in list:
            temptopword = []
           # print(words[0])
            temptopword.append(words[0])
            time_data = fullTime_dict[words[0]]
            print(time_data)
            #print()
            temptopword.append(time_data)
            #tempdata2.append(temptopword)
            tempfullData.append(temptopword)
        tempfullData2.append(tempfullData)
        #print(tempfullData2)
    fullData3.append(tempfullData2)
    #print(fullData3)
    dictCorpus = {}
    sizeI = len(fullData2[0])
    count = 0

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

    for i in fullData3[0]:
        if count == len(listLinks) - 1:
            break
        indv_dict = {
            "words": "",
            "link": "",
            "category":"",
            "title":""
        }
        # print(listFiles[count])
        #print(i)
        indv_dict["words"] = i
        print(i)
        print()
        # indv_dict["filename"] = listFiles[count]
        indv_dict["link"] = listLinks[count]
        indv_dict["category"] = listCategory[count]
        indv_dict["title"] = listTitles[count]
        my_dict[str(count)] = indv_dict
        count += 1

    # store dictionary in json file
    with open('top5Words.json', 'w') as filehandle:
        json.dump(my_dict, filehandle, indent=5)
    #print(my_dict)
    return my_dict

def TFIDF():
    top5 = {}
    top5words()
    weights()
    top5 = words_time_weights()
    new_map()
    print(top5)
    return top5

TFIDF()

