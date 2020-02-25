from flask import Flask, request, jsonify

from flask_pymongo import PyMongo, MongoClient

import boto3

import urllib3

import json

import auto as auto
import TFIDFfinal as nlp

from werkzeug.wrappers import Response

# handle requests and allow front end to access backend
from flask_cors import CORS
import os
# uuid - to generate id for videos to be stored
import uuid

app = Flask(__name__)

#config
app.config["MONGODB_NAME"] = "qa-classifier"
# app.config["MONGO_URI"] = "mongodb+srv://Larissa:spring2020@cluster0-nkghg.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://longweiming:leaf1234@cluster0-i1gqv.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

CORS(app)
# cluster = MongoClient("mongodb+srv://rachell:<password>@cluster0-hu9je.mongodb.net/test?retryWrites=true&w=majority", ssl=True)
# db = cluster["qa-classifier"]
# collection = db["tags"]


@app.route("/")
def index():
    return "<h1>Hello World</h1>"


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
        s3.upload_file(filename, 'qa-classifier', video_name, ExtraArgs={'ACL':'public-read'})

        # get object url
        video_url = "https://qa-classifier.s3.amazonaws.com/%s" % (video_name)
        print(video_url)

        # ************************************
        # text = request.json
        # tag = text["search"]

        # print(tag)

        # Call function to convert (existing) audio to text  from offset.py file
        auto.convert_auto(title, video_name, video_url, category)
        #
        top5 = {}
        top5 = nlp.TFIDF()

        tags_collection = mongo.db.tags

        for i in top5:
            # print(top5[i])
            tags_collection.insert_one(top5[i])
        # ************************************

        return json.dumps("Successfully uploaded and processed video " + video.filename)


def retrieve_video():

    s3 = boto3.client('s3')

    with open("testing-download.mp4", "wb") as video:
        s3.download_fileobj("qa-classifier", "test-video.mp4", video)

    print(video)

    return 0


@app.route("/api/play", methods=['GET', "POST"])
def get_video():

    # get object url
    video_url = "https://qa-classifier.s3.amazonaws.com/IntroductiontoWorkandEnergy.mp4"
    print("sending link...")
    return json.dumps(video_url)


if __name__ == "__main__":
    app.run(debug=True)

