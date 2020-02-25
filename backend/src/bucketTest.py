
import boto3
import  collections
import string



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
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('qac-txt-csv')
    csvFiles = []
    txtFiles = []
    # the key here represent the files names
    for obj in bucket.objects.all():
        key = obj.key
        # check for files that end with certain extension precisely .csv extension
        if key.endswith('.csv'):
            csvFiles.append(key)
            #print(type(csvFiles))
        elif key.endswith('.txt'):
            txtFiles.append(key)
    sortCaseIns(csvFiles)
    sortCaseIns(txtFiles)
    return csvFiles,txtFiles


#read all txt files and return a corpus of all the files read
def read_all_txt_files():
    corpus = []
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('qac-txt-csv')

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






    """
    for obj in bucket.objects.all():
        #the key here represent the files names
        key = obj.key
        #check for files that end with certain extension precisely .csv extension
        if key.endswith('.csv'):
            print(type(key))
    
            csvbody = obj.get()['Body'].read().decode('utf-8')
           # print(csvbody)
        else:
            txtbody = obj.get()['Body'].read().decode('utf-8')
            #print(txtbody)
        #body = obj.get()['Body'].read()
       # print(body)
       # print()
        #print()
    
    """

csvCollection, txtCollection = read_all_csv_txt_files()
finalCorpus = []

finalCorpus = read_all_txt_files()

for i in csvCollection:
    print(i)

