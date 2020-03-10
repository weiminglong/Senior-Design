from flask import Flask, request, jsonify

from flask_pymongo import PyMongo, MongoClient

import boto3

import urllib3

import json

import auto as auto
import TFIDFfinal as nlp
import jsonCheck

from werkzeug.wrappers import Response

# handle requests and allow front end to access backend
from flask_cors import CORS
import os
# uuid - to generate id for videos to be stored
import uuid

app = Flask(__name__)

#config
app.config["MONGODB_NAME"] = "qa-classifier"
#app.config["MONGO_URI"] = "mongodb+srv://Larissa:spring2020@cluster0-nkghg.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://longweiming:leaf1234@cluster0-i1gqv.mongodb.net/test?retryWrites=true&w=majority"
<<<<<<< Updated upstream
=======
#app.config["MONGO_URI"] = "mongodb+srv://rachell:leaf1234@cluster0-hu9je.mongodb.net/qa-classifier?retryWrites=true&w=majority"
>>>>>>> Stashed changes
mongo = PyMongo(app)

CORS(app)
# cluster = MongoClient("mongodb+srv://rachell:<password>@cluster0-hu9je.mongodb.net/test?retryWrites=true&w=majority", ssl=True)
# db = cluster["qa-classifier"]
# collection = db["tags"]



@app.route("/")
def index():
    #return "<h1>Hello World</h1>"
    categories = mongo.db.categories
    result = categories.find({"categories": {}})
    print("final categories array:")
    print(result)

    return json.dumps(result)


@app.route("/test")
def add_tags():

    # post = {"title": "harold the cat part 2", "duration": 120, "tags": "cat"}
    # collection.insert_one(post)

    tags_collection = mongo.db.tags
    tags_collection.insert_one({"title": "Physics 2: Electromagnetism, Lecture 3", "duration": 90, "tags": ["charge", "force", "work"]})
    return "<h1>added new video tags</h1>"


@app.route("/api/tags", methods=['GET', "POST"])
def search_tags():
    if request.method == "POST":
        text = request.json
        tag = text["search"]
        print()

        tags_collection = mongo.db.tags
        videos = tags_collection.find({"words": {"$elemMatch": {"$elemMatch": {"$in": [tag]}}}})

        linkArray = []
        wordArray = []
        for i in videos:
            # append video link and keywords/timestamps to create 2D array
            linkArray.append(i["link"])
            wordArray.append(i["words"])

        array = []
        array.append(linkArray)
        array.append(wordArray)

        print("final array:")
        print(array)

    return json.dumps(array)

@app.route("/api/toolbar", methods=['GET', "POST"])
def get_categories():
    if 1:#request.method == "POST":
        # text = request.json
        # tag = text["search"]
        # print()

        categories = mongo.db.categories
        result = categories.find({"categories": {}}) #{"words": {"$elemMatch": {"$elemMatch": {"$in": [tag]}}}})

        # linkArray = []
        # wordArray = []
        # for i in videos:
        #     # append video link and keywords/timestamps to create 2D array
        #     linkArray.append(i["link"])
        #     wordArray.append(i["words"])
        #
        # array = []
        # array.append(linkArray)
        # array.append(wordArray)

        # categoriesList = []
        # for i in result:


        print("final categories array:")
        print(result)

    return json.dumps(result)

@app.route("/api/upload", methods=['GET', "POST"])
def upload_and_process():
    if request.method == "POST":
        print("here")
        video = request.files["video"]
        title = request.form["title"].replace(" ", "")
        video_name = video.filename.replace(" ", "")
        category = request.form["category"]

        # prints received video
        print(video)
        print(request.url)
        print(title)
        print(video_name)
        print(category)


        # retrieve_video()

        filename = "video/" + video_name

        with open(filename, "wb") as f: # writes uploaded video object to .mp4 file
            f.write(video.read())

        s3 = boto3.client('s3')
        s3.upload_file(filename, 'qa-classifier2', video_name, ExtraArgs={'ACL':'public-read'})

        # get object url
        video_url = "https://qa-classifier2.s3.amazonaws.com/%s" % (video_name)
        print(video_url)

        # ************************************
        # text = request.json
        # tag = text["search"]

        # print(tag)

        '''JSON CATEGORY'''
        #Call function to check if the category exist or not in the json file
        cats_data = jsonCheck.categoriesJsonCheck(category)
        # cats_data = "categories.json"
        cats_collection = mongo.db.categories

        cats_collection.insert_one(cats_data)

        for i in cats_data['categories']:
            #cats_collection.insert_one(categoryJsonArray[i])
            print(i)#cats_data['categories'][i])

        # Call function to convert (existing) audio to text  from offset.py file
        auto.convert_auto(title, video_name, video_url, category)
        #
        top5 = {}
        top5 = nlp.TFIDF()

        tags_collection = mongo.db.tags
        print("printing the top5 in app.py")
        print()
        print(top5)
        print()
        print()
        print("inside of the app.py, testing the values of top5 being inserted")
        print()
        print()
        for i in top5:
            print(top5[i])
            tags_collection.insert_one(top5[i])
        # ************************************

        return json.dumps("Successfully uploaded and processed video " + video.filename)


def retrieve_video():

    s3 = boto3.client('s3')

    with open("testing-download.mp4", "wb") as video:
        s3.download_fileobj("qa-classifier2", "test-video.mp4", video)

    print(video)

    return 0


@app.route("/api/play", methods=['GET', "POST"])
def get_video():

    # get object url
    video_url = "https://qa-classifier2.s3.amazonaws.com/IntroductiontoWorkandEnergy.mp4"
    print("sending link...")
    return json.dumps(video_url)


if __name__ == "__main__":
    app.run(debug=True)

