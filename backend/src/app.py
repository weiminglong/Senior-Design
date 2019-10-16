from flask import Flask, request, jsonify

from flask_pymongo import PyMongo, MongoClient

import json

# handle requests and allow front end to access backend
from flask_cors import CORS
import os
# uuid - to generate id for videos to be stored
import uuid

app = Flask(__name__)

#config
app.config["MONGODB_NAME"] = "qa-classifier"
app.config["MONGO_URI"] = "mongodb+srv://rachell:<password>@cluster0-hu9je.mongodb.net/qa-classifier?retryWrites=true&w=majority"
mongo = PyMongo(app)

# cluster = MongoClient("mongodb+srv://rachell:<password>@cluster0-hu9je.mongodb.net/test?retryWrites=true&w=majority", ssl=True)
# db = cluster["qa-classifier"]
# collection = db["tags"]


@app.route("/")
def index():
    return "<h1>Hello World</h1>"


@app.route("/tags")
def add_tags():

    # post = {"title": "harold the cat part 2", "duration": 120, "tags": "cat"}
    # collection.insert_one(post)

    tags_collection = mongo.db.tags
    tags_collection.insert_one({"title": "TESTING", "duration": 90, "tags": ["funny", "cat", "gag"]})
    return "<h1>added new video tags</h1>"


if __name__ == "__main__":
    app.run(debug=True)

