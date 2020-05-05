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
bucket = s3.Bucket('qac-txt-csv2')

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
            corpus.append(texRead)
    return file_words_diction

def frequency_word_infiles(word,files_dictionary):
    occurence_dictionay = dict()
    for key in files_dictionary:
        file_words = files_dictionary[key]
        freq_word = file_words.count(word)
        #print(freq_word)
        occurence_dictionay[key] = freq_word
    return occurence_dictionay


# this function get the start and end time from csv files that are all in a given list of words

def timeData(filename, stwords):
    temp_dictionary = dict()
    # timeData(csvCorpora, i, word)
    # print('filename is:',filename)
    tempfullData = []
    foundWords = []
    # try:
    wordPresent = False
    read = ""
    # file = open(filename, "r")
    # read = file.readlines()
    # file.close()
    contents = ""
    for obj in bucket.objects.all():
        # the key here represent the files names
        key = obj.key
        # print('key or filename is:',key)
        # check for files that end with certain extension precisely .csv extension
        if key.endswith(filename) == False:
            continue
            # print()
            # read = open(filename, encoding='utf-8')
        # print(key, filename)
        contents = obj.get()['Body'].read().decode(encoding="utf-8", errors="ignore")
    # print("value of content is:",contents)
    # print()
    # print()
    # for line in contents.splitlines():
    # print(line)

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
            #print(line)
            for each in line:
                filesName = []
                linkName = []
                line4 = each
                line2 = each.lower()
                line2 = line2.strip("!@#$%^&*(()_+=)")
                line3 = line2.split(":")
                #print(line3)
                # store dictionary in json file
                topword = []

                if len(line3) <= 1:
                    continue
                comparedword = line3[1].lower()

                if line3[0] == "word" and lower == comparedword:
                    #print(comparedword)
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
                    #if lower in fullTime_dict.keys():
                        # print(lower)
                        #print(fullTime_dict.keys())
                        # append the new number to the existing array at this slot
                        # fullTime_dict[lower].append(startFin+" ")
                        #fullTime_dict[lower] += startFin + " "  #\
                                                           #""
                        temp_dictionary[lower] += startFin + " "

                    else:
                        # create a new array in this slot
                        # fullTime_dict[lower] = startFin+" "
                        #fullTime_dict[lower] = startFin + " "
                        temp_dictionary[lower] = startFin + " "
                        #print(temp_dictionary)
                    # print("first time adding time is:",fullTime_dict[lower])
                    # print('from the root',fullTime_dict[lower])

                    endTime = line[2]
                    end = endTime.split("end_time:")
                    endFin = end[1]
                    val2 = line3[0:2]
                    #lowers = lower
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
                        #print(sentence[6:])
                        title.append(sentence[6:])
                    elif (len(title) > 0):
                        continue
    foundWords = remove_redundant_elements(foundWords)
    #print(foundWords)
    if len(foundWords) < 5:
        tempfullData = []
        remove_key_value(temp_dictionary,stwords)
        return

    elif foundWords in testWord:
        tempfullData = []
        remove_key_value(temp_dictionary,stwords)
        return
    testWord.append(foundWords)
    if (len(tempfullData) <= 2):
        tempfullData = []
        remove_key_value(temp_dictionary,stwords)
    if (len(tempfullData) < 5):
        tempfullData = []
        remove_key_value(temp_dictionary,stwords)
    if link not in listLinks and len(tempfullData) >= 5:
        listLinks.append(link)

    if len(tempfullData) >= 5:
        listCategory.append(category)
        # print(listCategory)
    if len(tempfullData) >= 5:
        listTitles.append(title)
    # print(listTitles)
    removedup = [tempfullData[i] for i in range(len(tempfullData)) if i == 0 or tempfullData[i] != tempfullData[i - 1]]
    fullData.append(removedup)
    fullTime_dict.update(temp_dictionary)

fullDiction = dict()
fullDictionary = read_all_txt_files()
#print(fullDictionary.keys())
#print(fullDiction['BO.txt'])
dictionary_frequency = dict()
dictionary_frequency = frequency_word_infiles('what',fullDictionary)
#print('frequency')
print(dictionary_frequency)
"""
max_value = max(dictionary_frequency, key=dictionary_frequency.get)
print('maximum key',max_value)
print('maximum value',dictionary_frequency[max_value])
"""
