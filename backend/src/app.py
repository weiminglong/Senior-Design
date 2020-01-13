from flask import Flask, request, jsonify

from flask_pymongo import PyMongo, MongoClient

import boto3

import urllib3

import json

import auto as auto
import TFIDFfinalwithlemmatization as nlp

from werkzeug.wrappers import Response

# handle requests and allow front end to access backend
from flask_cors import CORS
import os
# uuid - to generate id for videos to be stored
import uuid

app = Flask(__name__)

#config
app.config["MONGODB_NAME"] = "qa-classifier"
app.config["MONGO_URI"] = "mongodb+srv://rachell:leaf1234@cluster0-hu9je.mongodb.net/qa-classifier?retryWrites=true&w=majority"
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

        array = []
        for i in videos:
            print(i)
            array.append(i["filename"])

        print("array:")
        print(array)

    return json.dumps(array)


@app.route("/api/upload", methods=['GET', "POST"])
def upload_and_process():
    if request.method == "POST":
        print("here")
        video = request.files["video"]

        # prints received video
        print(video)

        print(request.url)

        with open("video/test-video.mp4", "wb") as f: # writes uploaded video object to .mp4 file
            f.write(video.read())


        # s3 = boto3.client('s3')
        # s3.upload_fileobj(video, 'qa-classifier', 'test-test-video')

        # text = request.json
        # tag = text["search"]

        # print(tag)

        # Call function to convert (existing) audio to text from offset.py file
        # auto.convert_auto()
        #
        # top5 = {}
        # top5 = nlp.TFIDF()
        #
        # tags_collection = mongo.db.tags
        #
        # for i in top5:
        #     # print(top5[i])
        #     tags_collection.insert_one(top5[i])

        return json.dumps("Successfully uploaded and processed video Taxonomy.mp4")


if __name__ == "__main__":
    app.run(debug=True)

