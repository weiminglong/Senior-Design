
import gensim
import os
import json
from nltk.stem import WordNetLemmatizer
import boto3
from nltk.corpus import stopwords



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
    file_words_diction = dict()
    corpus = []
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.txt'):
            texRead = obj.get()['Body'].read().decode('utf-8')
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
        occurence_dictionay[key] = freq_word
    sorted_x = {k: v for k, v in sorted(occurence_dictionay.items(), key=lambda item: item[1],reverse = True)}
    occurence_dictionay = sorted_x
    reverse_dict = dict()
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


def words_time_weights(input_word,filename):
    print('inputword is: \n', input_word)
    csvCorpora = []
    csvCollection, txtCollection, csvCorpora = read_all_csv_txt_files()
    timeData(filename, input_word)
    fullData3 = []
    fullData2 = [e for e in fullData if e]
    if len(fullData2) >1:
        lengthData = len(fullData2)
        tempfull2 = fullData2[lengthData -1]
        fullData2 = []
        fullData2.append(tempfull2)

    tempfullData2 = []
    for list in fullData2:
        tempfullData = []
        for words in list:
            temptopword = []
            print(words[0])
            temptopword.append(words[0])
            time_data1 = fullTime_dict[words[0]]
            time_data = remove_redundant_elements(time_data1)
            print('time_data no redundant',time_data)
            temptopword.append(time_data)
            tempfullData.append(temptopword)
        tempfullData2.append(tempfullData)
    if len(tempfullData2)>1 :
        fullData3.append(tempfullData2[0])
    fullData3.append(tempfullData2)
    dictCorpus = {}
    sizeI = len(fullData2[0])
    count = 0
    lengthLimit = len(listweights)
    fulLeng = len(fullData2)

    count = 0
    counter = 500
    my_dict = {}

    for i in fullData3[0]:
        indv_dict = {
            "words": "",
            "link": "",
            "category": "",
            "title": ""
        }

        if type(i[0][0][0]) == None:
             array = []
             array.append(i)
             indv_dict["words"] = array
        else:
            indv_dict["words"] = i
        size = len(listLinks)
        indv_dict["link"] = listLinks[size-1]
        indv_dict["category"] = listCategory[size-1]
        indv_dict["title"] = listTitles[size-1]
        counter +=1
        count += 1

    # store dictionary in json file
    with open('foundWord.json', 'w') as filehandle:
        json.dump(indv_dict, filehandle, indent=5)
    return indv_dict


# this function get the start and end time from csv files that are all in a given list of words
listFiles = []
listLinks = []
listCategory = []
listTitles = []
testWord = []
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
                    # lowers = lower
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
    if len(foundWords) < 1:
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
        return

    elif foundWords in testWord:
        print('test word',testWord)
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
        return
    if (len(tempfullData) < 1):
        tempfullData = []
        remove_key_value(temp_dictionary, stwords)
    if link not in listLinks and len(tempfullData) >= 1:
        listLinks.append(link)
        print('the list of links is: ',listLinks)

    if len(tempfullData) >= 1:
        listCategory.append(category)
        listTitles.append(title)
    removedup = [tempfullData[i] for i in range(len(tempfullData)) if i == 0 or tempfullData[i] != tempfullData[i - 1]]
    fullData.append(removedup)
    fullTime_dict.update(temp_dictionary)


def listToString(s):
    # initialize an empty string
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

# remove empty elements from a list
def remove_emptyEl_list(test_list):
    while ("" in test_list):
        test_list.remove("")
        return test_list

def remove_redundant_elements(duplicate):
    if isinstance(duplicate, str):
        li = list(duplicate.split(" "))
        duplicate = []
        duplicate = li
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    final_list = list(filter(None, final_list))
    return final_list


def remove_key_value(dictionary_delete,key_list):
    for word in key_list:
        dictionary_delete.pop(word,None)


def string_list_value_dictionary():
    k = " "
    value = []
    for i in fullTime_dict:
        print('the full list in loop is: ',fullTime_dict[i],'\n')
        k = listToString(fullTime_dict[i])
        value = k.split(" ")
        value = remove_emptyEl_list(value)
        fullTime_dict[i] = value

def word_similarity(word,all_words):
            model2 = gensim.models.Word2Vec([all_words], min_count=1,size=50,sg=1)
            result = model2.wv.most_similar(word,topn =3)
            return model2, result

def first_elem_value(dictionary):

    for key in dictionary.keys():
        return key,dictionary[key]

def txt_string_to_csv_str(txt_name):
    string1 = txt_name[:-4]
    string2 = ".csv"
    string3 = f"{string1}{string2}"
    return string3

def  get_data_of_word(word_input,csv_name):
    top5 = {}
    data = word_input.split(" ")
    top5 = words_time_weights(data,csv_name)
    return top5


def remove_stop_words_list(list_with_sw):
    filtered_words = [word for word in list_with_sw if word not in stopwords.words('english')]
    return filtered_words

def word2vec(input):

    fullDiction = dict()
    corpus = []
    fullDictionary,corpus = read_all_txt_files()

    dictionary_frequency = dict()

    dictionary_frequency = frequency_word_infiles(input, fullDictionary)
    firstEle, firstValue = first_elem_value(dictionary_frequency)
    csvname = txt_string_to_csv_str(firstEle)
    dataFound = {}
    if firstValue>0:
        dataFound= get_data_of_word(input,csvname)
        return input,dataFound
    else:
        corpus1 = corpus[0]
        corpus1 = corpus1[:-1]
        corpus1.insert(len(corpus1), input)
        corpus1 = remove_stop_words_list(corpus1)
        model, output = word_similarity(input, corpus1)
        new_input = output[0][0]
        dictionary_frequency = frequency_word_infiles(new_input, fullDictionary)
        firstEle, firstValue = first_elem_value(dictionary_frequency)
        csvname = txt_string_to_csv_str(firstEle)
        dataFound = get_data_of_word(new_input, csvname)
        with open('similarFound.json', 'w') as filehandle:
            json.dump(dataFound, filehandle, indent=5)
        return new_input, dataFound


data_els = {}
firstEl = ""
input = 'data'
