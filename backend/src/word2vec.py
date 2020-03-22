#import bs4 as bs
import urllib.request
import re
import nltk
import gensim
from gensim.models import Word2Vec
import pandas as pd
import os, glob
import numpy as np
import  numpy
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
import operator
import collections
from nltk.corpus import wordnet as wn
from itertools import product
import sys
import time
import boto3



#global variable definition
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
bucket = s3.Bucket('qac-txt-csv2')


#path = os.getcwd()

def cosine_distance (model,wa,wb):
   similar_percentage = model.wv.similarity(wa, wb)
   return  similar_percentage

def closest_cosine_value(model,word,similarity_list,lowerbound):
    dictionary_percentage = dict()
    max_val = 0
    for el in similarity_list:
        return_percentage = cosine_distance(model,word,el)
        dictionary_percentage[el] = return_percentage
    max_key = max(dictionary_percentage, key=dictionary_percentage.get)
    print('maximum key', max_key)
    print('maximum value', dictionary_percentage[max_key])
    #if dictionary_percentage[max_key] >=lowerbound:
    return max_key,dictionary_percentage[max_key]
# read the files names in a bucket both csv and txt file and return two lists
# of all the csv and txt files in the bucket in alphabetical order
def read_all_csv_txt_files():
    csvFiles = []
    txtFiles = []
    csvCorpus = []
    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        # print(type(key))
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.csv'):
            csvFiles.append(key)
            csvRead = obj.get()['Body'].read().decode('utf-8')
            #  print(csvRead)
            csvCorpus.append(csvRead)
            # print()
            # print()
            # print(type(csvFiles))
        elif key.endswith('.txt'):
            txtFiles.append(key)
    sortCaseIns(csvFiles)
    sortCaseIns(txtFiles)
    return csvFiles, txtFiles, csvCorpus

# read all txt files and return a corpus of all the files read
def read_all_txt_files():
    file_words_diction = dict()
    corpus = []
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.txt'):
            texRead = obj.get()['Body'].read().decode('utf-8')
            #print(key)
            #print(list(texRead))
            list_words_files = texRead.split('\n')
            file_words_diction[key] = list_words_files
            corpus.append(list_words_files)

    return file_words_diction,corpus


def frequency_word_infiles(word,files_dictionary):

    occurence_dictionay = dict()
    sorted_x = dict()
    for key in files_dictionary:
        file_words = files_dictionary[key]
        freq_word = file_words.count(word)
        #print(freq_word)
        occurence_dictionay[key] = freq_word
    #sorted_x = sorted(occurence_dictionay.items(), key=lambda kv: kv[1])
    sorted_x = {k: v for k, v in sorted(occurence_dictionay.items(), key=lambda item: item[1],reverse = True)}
    occurence_dictionay = sorted_x
    #for key in occurence_dictionay.keys():
        #print(key,occurence_dictionay[key])
    reverse_dict = dict()
    #reverse_dict = sorted_x.reverse()



    return occurence_dictionay

# function that takes in parameter a list and sort its elements in alphabetical order
# ignores the case sensitive
def sortCaseIns(lst):
    lst2 = [[x for x in range(0, 2)] for y in range(0, len(lst))]
    for i in range(0, len(lst)):
        lst2[i][0] = lst[i].lower()
        lst2[i][1] = lst[i]
    lst2.sort()
    for i in range(0, len(lst)):
        lst[i] = lst2[i][1]


def words_time_weights(listwords):
    csvCorpora = []
    csvCollection, txtCollection, csvCorpora = read_all_csv_txt_files()
    # print(fullTime_dict)
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
    # print(listLinks)
    # stip empty list within a list
    fullData3 = []
    fullData2 = [e for e in fullData if e]
    #print('full data####', fullData2)
    #print('full data2', fullData2)
    string_list_value_dictionary()
    # print(fullData2)

    tempfullData2 = []
    for list in fullData:
        print('list',list)
        tempfullData = []
        for words in list:
            temptopword = []
            # print(words[0])
            temptopword.append(words[0])
            print('full time dicitonary 2',fullTime_dict)
            time_data1 = fullTime_dict[words[0]]
            time_data = remove_redundant_elements(time_data1)
            # print(time_data)
            # print()
            temptopword.append(time_data)
            # tempdata2.append(temptopword)
            tempfullData.append(temptopword)
        tempfullData2.append(tempfullData)
        # print(tempfullData2)
    fullData3.append(tempfullData2)
    # print(fullData3)
    dictCorpus = {}
    # print("value of full data 2 is:")
    # print(fullData2)
    sizeI = len(fullData2[0])
    count = 0

    lengthLimit = len(listweights)
    fulLeng = len(fullData2)
    """
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
    """
    count = 0
    my_dict = {}

    for i in fullData3[0]:
        if count == len(listLinks) - 1:
            break
        indv_dict = {
            "words": "",
            "link": "",
            "category": "",
            "title": ""
        }
        # print(listFiles[count])
        # print(i)
        indv_dict["words"] = i
        # print(i)
        # print()
        # indv_dict["filename"] = listFiles[count]
        indv_dict["link"] = listLinks[count]
        indv_dict["category"] = listCategory[count]
        indv_dict["title"] = listTitles[count]
        my_dict[str(count)] = indv_dict
        count += 1

    # store dictionary in json file
    with open('top5Words.json', 'w') as filehandle:
        json.dump(my_dict, filehandle, indent=5)
    # print(my_dict)
    return my_dict


def words_time_weights(input_word,filename):
    csvCorpora = []
    csvCollection, txtCollection, csvCorpora = read_all_csv_txt_files()

    #for filename in csvCollection:
        # print(filename)
    timeData(filename, input_word)
    """
    for word in listwords:
        for i in range(len(csvCorpora)):
            timeData(csvCorpora,i,word,csvCollection[i])
    """
    # print(listLinks)
    # stip empty list within a list
    fullData3 = []
    fullData2 = [e for e in fullData if e]
    string_list_value_dictionary()
    print('full data2\n',fullData2[0][0])

    tempfullData2 = []
    for list in fullData2:
        print('list',list)
        tempfullData = []
        for words in list:
            print('words',words)
            temptopword = []
            # print(words[0])
            temptopword.append(words[0])
            print('temptopword',temptopword)
            time_data1 = fullTime_dict[words[0]]
            print('time_data1',time_data1)
            time_data = remove_redundant_elements(time_data1)
            # print(time_data)
            print('time_data no redundant',time_data)
            temptopword.append(time_data)
            # tempdata2.append(temptopword)
            tempfullData.append(temptopword)
        tempfullData2.append(tempfullData)
        print('temp full data 2',tempfullData2)
    fullData3.append(tempfullData2)
    print('full data 3', fullData3)
    # print(fullData3)
    dictCorpus = {}
    # print("value of full data 2 is:")
    # print(fullData2)
    sizeI = len(fullData2[0])
    count = 0

    lengthLimit = len(listweights)
    fulLeng = len(fullData2)
    """
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
    """
    count = 0
    my_dict = {}

    for i in fullData3[0]:
        print('i',i)
        #if count == len(listLinks) - 1:
          #  print()
          #  break

        indv_dict = {
            "words": "",
            "link": "",
            "category": "",
            "title": ""
        }
        # print(listFiles[count])
        # print(i)
        indv_dict["words"] = i
        # print(i)
        # print()
        # indv_dict["filename"] = listFiles[count]
        indv_dict["link"] = listLinks[count]
        indv_dict["category"] = listCategory[count]
        indv_dict["title"] = listTitles[count]
        my_dict[str(count)] = indv_dict
        count += 1

    # store dictionary in json file
    with open('foundWord.json', 'w') as filehandle:
        json.dump(my_dict, filehandle, indent=5)
    # print(my_dict)
    return my_dict


# this function get the start and end time from csv files that are all in a given list of words
listFiles = []
testWord = []
listLinks = []
listCategory = []
listTitles = []

fullTime_dict = dict()

def get_contents(filename):
    contents = ""
    for obj in bucket.objects.all():
        # the key here represent the files names
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith(filename) == False:
            continue
        contents = obj.get()['Body'].read().decode(encoding="utf-8", errors="ignore")
    return contents

def timeData(filename, stwords):

    temp_dictionary = dict()
    tempfullData = []
    foundWords = []
    # try:
    wordPresent = False
    read = ""
    contents = ""
    contents = get_contents(filename)

    linkval = ""
    linktemp = []
    link = []
    # print(read)
    word_time_array = {}
    category = []
    title = []
    # print(read)
    # print()

    for word in stwords:
        # print(link)
        lower = word.lower()
        count = 0
        # print(open(filename, encoding='utf-8'))
        # print(filename)
        # print(filename)
        # f = codecs.open(filename, 'r3', encoding='utf-8')
        # print("value of f is:", f)
        # for sentence in f:
        sentences_list = []
        sentences_list = contents.splitlines()
        for sentence in sentences_list:
            lowers = []
            # print(type(contents.splitlines()))
            # for sentence in open(filename, encoding='utf-8'):
            # print(sentence)
            line = sentence.split()
            # print(line)
            for each in line:
                filesName = []
                linkName = []
                line4 = each
                line2 = each.lower()
                line2 = line2.strip("!@#$%^&*(()_+=)")
                line3 = line2.split(":")
                # print(line3)
                # store dictionary in json file
                topword = []

                if len(line3) <= 1:
                    continue
                comparedword = line3[1].lower()

                if line3[0] == "word" and lower == comparedword:
                    # print(comparedword)
                    temptopword = []
                    name = lower
                    startTime = line[1]
                    start = startTime[11:]
                    # print(start)
                    startFin = start
                    # print(type)
                    # print(startFin)
                    # fullTime_dict[lower] = startFin + " "

                    if lower in temp_dictionary.keys():
                        # if lower in fullTime_dict.keys():
                        # print(lower)
                        # print(fullTime_dict.keys())
                        # append the new number to the existing array at this slot
                        # fullTime_dict[lower].append(startFin+" ")
                        # fullTime_dict[lower] += startFin + " "  #\
                        # ""
                        temp_dictionary[lower] += startFin + " "

                    else:
                        # create a new array in this slot
                        # fullTime_dict[lower] = startFin+" "
                        # fullTime_dict[lower] = startFin + " "
                        temp_dictionary[lower] = startFin + " "
                        # print(temp_dictionary)
                    # print("first time adding time is:",fullTime_dict[lower])
                    # print('from the root',fullTime_dict[lower])

                    endTime = line[2]
                    end = endTime.split("end_time:")
                    endFin = end[1]
                    val2 = line3[0:2]
                    # lowers = lower
                    foundWords.append(lower)
                    temptopword.append(lower)
                    tempfullData.append(temptopword)
                    wordPresent = True
                    filesName.append(filename)

                if line3[0] == "link" and wordPresent == True and line[0] not in link:
                    lane = []
                    laneLink = []
                    # print()
                    if (len(link) == 0):
                        # link.append(line[0][5:])
                        lane = line4.split("word")
                        if len(lane) >= 2 and len(lane[0]) <= len(lane[1]):
                            laneLink = line4.split("link:")
                        if len(laneLink) >= 2:
                            link.append(line4[7:])
                        elif len(lane) >= 2 and len(lane[0]) <= len(lane[1]):
                            link.append(line4[6:])
                        else:
                            # print(lane[0][5:])
                            link.append(lane[0][5:])

                    elif (len(link) > 0):
                        continue

                if line3[0] == "category" and wordPresent == True:
                    if (len(category) == 0):
                        category.append(line3[1])
                        # print(category)
                    elif (len(category) > 0):
                        continue

                if line3[0] == "title" and wordPresent == True:
                    if (len(title) == 0):
                        # print(sentence[6:])
                        title.append(sentence[6:])
                    elif (len(title) > 0):
                        continue
    foundWords = remove_redundant_elements(foundWords)
    print(foundWords)
    if len(foundWords) < 1:
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
        return

    elif foundWords in testWord:
        print('test word',testWord)
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
        return
    testWord.append(foundWords)
    #print(testWord)
    if (len(tempfullData) < 1):
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
    if link not in listLinks and len(tempfullData) >= 1:
        listLinks.append(link)

    if len(tempfullData) >= 1:
        listCategory.append(category)
        # print(listCategory)
    if len(tempfullData) >= 1:
        listTitles.append(title)
    # print(listTitles)
    print('tempfulldata',tempfullData)
    removedup = [tempfullData[i] for i in range(len(tempfullData)) if i == 0 or tempfullData[i] != tempfullData[i - 1]]
    fullData.append(removedup)
    fullTime_dict.update(temp_dictionary)
    print('full dictionary',fullTime_dict)


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele
        # return string
    return str1

# remove empty elements from a list
def remove_emptyEl_list(test_list):
    while ("" in test_list):
        test_list.remove("")
        return test_list

def remove_redundant_elements(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def remove_key_value(dictionary_delete,key_list):
    for word in key_list:
        dictionary_delete.pop(word,None)


def string_list_value_dictionary():
    k = " "
    value = []
    for i in fullTime_dict:
        k = listToString(fullTime_dict[i])
        value = k.split(" ")
        value = remove_emptyEl_list(value)
        fullTime_dict[i] = value

def word_similarity(word,all_words):

            #cleprint(all_words)
            #word2vec = Word2Vec(all_words, min_count=2)
            #word2vec = Word2Vec(all_words,min_count=1)
            #print(all_words)
            #word2vec= Word2Vec(all_words, min_count=1,sg=0)
            #word2vec = gensim.models.Word2Vec(all_words, size=150, window=10, min_count=1, workers=3, iter=10,sg=1)
            print(all_words)
            print()
            #word2vec = gensim.models.Word2Vec(all_words,min_count=1,workers=3, iter=10, sg=1)
            word2vec = gensim.models.Word2Vec(all_words, window=10, min_count=1, workers=3, iter=10, sg=1)
            #print(word2vec)
            result = word2vec.wv.most_similar(word,topn =5)
            #print(result)
            #print(result[0][0])
            #result = word2vec.wv.similar_by_word(word)
           # print(result)
            print()
            print()
            print()
            print('results')
            print()
            print()
            print('result%%%%%%%%%%%%%',result)
            return word2vec, result

def first_elem_value(dictionary):

    for key in dictionary.keys():
        return key,dictionary[key]

def txt_string_to_csv_str(txt_name):
    string1 = txt_name[:-4]
    print('string1',string1)
    string2 = ".csv"
    string3 = f"{string1}{string2}"
    print(string3)
    return string3

def  get_data_of_word(word_input,csv_name):
    top5 = {}
    data = word_input.split(" ")
    #print(data)
    top5 = words_time_weights(data,csv_name)
    return top5
    #print(top5)
if __name__ == '__main__':

    fullDiction = dict()
    corpus = []
    fullDictionary,corpus = read_all_txt_files()

    dictionary_frequency = dict()
    input = 'migrant'
    #print(fullDictionary)
    dictionary_frequency = frequency_word_infiles(input, fullDictionary)
    firstEle, firstValue = first_elem_value(dictionary_frequency)
    #print('first element',firstEle,'first value',firstValue)

    csvname = txt_string_to_csv_str(firstEle)
    #print('csvname of first element',csvname)
    dataFound = {}
    if firstValue>0:
       dataFound= get_data_of_word(input,csvname)
       print()
       print()
       print(dataFound)
    else:
        print(corpus)
       # a.insert(len(a), 5)
        corpus1 = corpus[0]
        corpus1 = corpus1[:-1]
        corpus1.insert(len(corpus1),input)
        #print(corpus1)
        model, output = word_similarity(input, corpus1)
        #print(output)
        similar_elements = []
        for el in output:
            similar_elements.append(el[0])


    """
    max_value = max(dictionary_frequency, key=dictionary_frequency.get)
    print('maximum key', max_value)
    print('maximum value', dictionary_frequency[max_value])
    """
    """
    # model = []
    input_word = 'history'
    #print(corpus)
    model, output = word_similarity(input_word,corpus)
    print(output)
    similar_elements = []
    for el in output:
        similar_elements.append(el[0])

    maxWord, maxPercentage = closest_cosine_value(model, input_word, similar_elements, 0.8)

   """
