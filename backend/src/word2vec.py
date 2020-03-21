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


from nltk.corpus import wordnet as wn
from itertools import product
import sys
import time
import boto3




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


path = os.getcwd()

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
    string_list_value_dictionary()
    # print(fullData2)

    tempfullData2 = []
    for list in fullData2:
        tempfullData = []
        for words in list:
            temptopword = []
            # print(words[0])
            temptopword.append(words[0])
           # print(fullTime_dict)
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





def word_similarity(word):
    corpus = []
    article_text = ""
    result = []
    all_words = []
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
            #word2vec = Word2Vec(all_words, min_count=2)
            #word2vec = Word2Vec(all_words,min_count=1)
            #print(all_words)
            #word2vec= Word2Vec(all_words, min_count=1,sg=0)
            #word2vec = gensim.models.Word2Vec(all_words, size=150, window=10, min_count=1, workers=3, iter=10,sg=1)
            word2vec = gensim.models.Word2Vec(all_words,min_count=1, workers=3, iter=10, sg=1)
            #print(word2vec)
            result = word2vec.wv.most_similar(word,topn =5)
            #print(result)
            #print(result[0][0])
            #result = word2vec.wv.similar_by_word(word)
           # print(result)
            return word2vec, result


#model = list(model[0])
#print(type(model))
#print(cosine_distance('reaction',similar_elements,0.8))

if __name__ == '__main__':

    fullDiction = dict()
    fullDictionary = read_all_txt_files()

    dictionary_frequency = dict()
    input = 'yes'
    #print(fullDictionary)
    dictionary_frequency = frequency_word_infiles(input, fullDictionary)
    #print(dictionary_frequency)

    max_value = max(dictionary_frequency, key=dictionary_frequency.get)
    print('maximum key', max_value)
    print('maximum value', dictionary_frequency[max_value])
    print()
    print(sorted(dictionary_frequency))
    """
    max_value = max(dictionary_frequency, key=dictionary_frequency.get)
    print('maximum key', max_value)
    print('maximum value', dictionary_frequency[max_value])
     """
    # model = []
    input_word = 'glucose'
    model, output = word_similarity(input_word)
    print(output)
    similar_elements = []
    for el in output:
        similar_elements.append(el[0])

    maxWord, maxPercentage = closest_cosine_value(model, input_word, similar_elements, 0.8)
