# imports
import pandas as pd
import os
import json
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from itertools import product
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
bucket = s3.Bucket('qac-txt-csv2')


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


# read the files names in a bucket both csv and txt file and return two lists
# of all the csv and txt files in the bucket in alphabetical order
def read_all_csv_txt_files():
    csvFiles = []
    txtFiles = []
    csvCorpus = []
    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.csv'):
            csvFiles.append(key)
            csvRead = obj.get()['Body'].read().decode('utf-8')
            csvCorpus.append(csvRead)
        elif key.endswith('.txt'):
            txtFiles.append(key)
    sortCaseIns(csvFiles)
    sortCaseIns(txtFiles)
    return csvFiles, txtFiles, csvCorpus


# read all txt files and return a corpus of all the files read
def read_all_txt_files():
    corpus = []
    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.txt'):
            texRead = obj.get()['Body'].read().decode('utf-8')
            corpus.append(texRead)
    return corpus


def top5words():
    ps = PorterStemmer()
    # empty list of corpus
    corpus = []
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

    itr = 0
    top10size = len(top10)
    for i in list_wo_rel:
        no_duplicate = []
        newList5 = []
        hashed = {}
        rem_list = group_high_similarity(i, 0.85)
        no_duplicate = remove_duplicate(i, rem_list)
        if itr < top10size:
            hashed = hash_list(top10[itr])
        else:
            continue
        for x in range(0, 5):
            newList5.append(no_duplicate[x])
            try:
                newList5.append(hashed[no_duplicate[x]])
            except KeyError:
                newList5.append(0.7)
        top5Final.append(newList5)
        itr += 1


def float_check(value):
    try:
        isinstance(float(value), float)
        return True
    except:
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
    return maxscore

def group_high_similarity(target_list, lowerbound):
    duplicateToremove = []
    result = target_list[:]
    for x in range(0, len(target_list)):
        for y in range(x + 1, len(target_list)):
            wordx, wordy = target_list[x], target_list[y]
            value = similarity(wordx, wordy)
            if value >= lowerbound:
                result[x] = wordx
                if wordy != wordx:
                    duplicateToremove.append(wordy)
    return duplicateToremove


def remove_duplicate(target_list, remove_list):
    # using list comprehension to perform task
    res = [i for i in target_list if i not in remove_list]
    return res


def hash_list(list_to_hash):
    list = []
    list = list_to_hash[0]
    data_value = {}
    for i in range(0, len(list)):
        if i % 2 == 0 and i != len(list):
            data_value[list[i]] = list[i + 1]
    return data_value


# remove empty elements from a list
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

def timeData(filename, stwords):
    temp_dictionary = dict()
    tempfullData = []
    foundWords = []
    wordPresent = False
    read = ""
    contents = ""
    for obj in bucket.objects.all():
        # the key here represent the files names
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith(filename) == False:
            continue
        contents = obj.get()['Body'].read().decode(encoding="utf-8", errors="ignore")
    linkval = ""
    linktemp = []
    link = []
    word_time_array = {}
    category = []
    title = []
    for word in stwords:
        lower = word.lower()
        count = 0
        sentences_list = []
        sentences_list = contents.splitlines()
        for sentence in sentences_list:
            lowers = []
            line = sentence.split()
            for each in line:
                filesName = []
                linkName = []
                line4 = each
                line2 = each.lower()
                line2 = line2.strip("!@#$%^&*(()_+=)")
                line3 = line2.split(":")
                # store dictionary in json file
                topword = []

                if len(line3) <= 1:
                    continue
                comparedword = line3[1].lower()

                if line3[0] == "word" and lower == comparedword:
                    temptopword = []
                    name = lower
                    startTime = line[1]
                    start = startTime[11:]
                    startFin = start

                    if lower in temp_dictionary.keys():
                        temp_dictionary[lower] += startFin + " "

                    else:

                        temp_dictionary[lower] = startFin + " "

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
                    if (len(link) == 0):
                        lane = line4.split("word")
                        if len(lane) >= 2 and len(lane[0]) <= len(lane[1]):
                            laneLink = line4.split("link:")
                        if len(laneLink) >= 2:
                            link.append(line4[7:])
                        elif len(lane) >= 2 and len(lane[0]) <= len(lane[1]):
                            link.append(line4[6:])
                        else:
                            link.append(lane[0][5:])

                    elif (len(link) > 0):
                        continue

                if line3[0] == "category" and wordPresent == True:
                    if (len(category) == 0):
                        category.append(line3[1])
                    elif (len(category) > 0):
                        continue

                if line3[0] == "title" and wordPresent == True:
                    if (len(title) == 0):
                        title.append(sentence[6:])
                    elif (len(title) > 0):
                        continue
    foundWords = remove_redundant_elements(foundWords)
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
    if len(tempfullData) >= 5:
        listTitles.append(title)
    removedup = [tempfullData[i] for i in range(len(tempfullData)) if i == 0 or tempfullData[i] != tempfullData[i - 1]]
    fullData.append(removedup)
    fullTime_dict.update(temp_dictionary)

# get the weight from tfidf data above
listweights = []

def remove_key_value(dictionary_delete,key_list):
    for word in key_list:
        dictionary_delete.pop(word,None)


def weights():
    for i in top5Final:
        size = len(i)
        temp = []
        tempfloat = []
        for j in range(0, size):
            tempVar = []
            tempWeight = []
            if (j % 2 == 0 and j != len(i)):
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

new_list = []


def new_map():
    for i in listwords:
        tmpmap = []
        for w in i:
            tmpmap.append(w)
            tmpmap.append(fullTime_dict[w])
            new_list.append(tmpmap)


def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    return str1

def remove_redundant_elements(duplicate):
    if(type(duplicate) == 'None'):
        return
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def string_list_value_dictionary():
    k = " "
    value = []

def string_to_list(dict):
    k = " "
    value = []
    for i in dict:
        k = listToString(dict[i])
        value = k.split(" ")
        value = remove_emptyEl_list(value)
        dict[i] = value
        print(dict[i])
        print()

def words_time_weights():
    csvCorpora = []
    csvCollection, txtCollection, csvCorpora = read_all_csv_txt_files()
    # parameter to be passed in time_data function

    for i in listwords:
        # parse through file and get time stamp
        for filename in csvCollection:
            timeData(filename, i)

    # stip empty list within a list
    fullData3 = []
    fullData2 = [e for e in fullData if e]
    print(fullData2)
    string_to_list(fullTime_dict)

    tempfullData2 = []
    for list in fullData2:
        tempfullData = []
        for words in list:
            temptopword = []
            temptopword.append(words[0])
            time_data1 = fullTime_dict[words[0]]
            if(type(time_data1)) == None:
                continue
            time_data = remove_redundant_elements(time_data1)
            temptopword.append(time_data)
            tempfullData.append(temptopword)
        tempfullData2.append(tempfullData)
    fullData3.append(tempfullData2)
    dictCorpus = {}
    sizeI = len(fullData2[0])
    count = 0
    lengthLimit = len(listweights)
    fulLeng = len(fullData2)

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
        indv_dict["words"] = i
        indv_dict["link"] = listLinks[count]
        indv_dict["category"] = listCategory[count]
        indv_dict["title"] = listTitles[count]
        my_dict[str(count)] = indv_dict
        count += 1

    # store dictionary in json file
    with open('top5Words.json', 'w') as filehandle:
        json.dump(my_dict, filehandle, indent=5)
    print()
    print()
    print(my_dict)
    return my_dict


def TFIDF():
    top5 = {}
    top5words()
    weights()
    top5 = words_time_weights()
    new_map()
    return top5


