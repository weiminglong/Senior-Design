from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import MongoClient

import boto3
import json
import auto as auto
import TFIDFfinal as nlp
import jsonCheck
import word2vec as wv3

app = Flask(__name__)

# configure database
app.config["MONGODB_NAME"] = "qa-classifier"
app.config["MONGO_URI"] = "<Add Mongo URI>"
mongo = PyMongo(app)

CORS(app)


@app.route("/api/tags", methods=['GET', "POST"])
def search_tags():
    if request.method == "POST":
        text = request.json
        tag = text["search"]

        tags_collection = mongo.db.tags
        videos = tags_collection.find({"words": {"$elemMatch": {"$elemMatch": {"$in": [tag]}}}})

        # if there aren't videos in the database for the word searched
        if videos.count() == 0:
            firstElement, eleData = wv3.word2vec(tag)

            # store the videoData in the database
            tags_collection.insert_one(eleData)
            tags_collection.save(eleData)

            # FirstElement is either the same value of tag or the word most similar to tag
            tag = firstElement
            videos = tags_collection.find({"words": {"$elemMatch": {"$elemMatch": {"$in": [tag]}}}})

        link_array = []
        word_array = []
        title_array = []
        for i in videos:
            # append video link and keywords/timestamps to create 2D array
            link_array.append(i["link"])
            word_array.append(i["words"])
            title_array.append(i["title"])

        array = []
        array.append(link_array)
        array.append(word_array)
        array.append(title_array)

    return json.dumps(array)


@app.route("/api/toolbar", methods=['GET', "POST"])
def get_categories():
    if 1:#request.method == "POST":

        categories = mongo.db.categories
        result = categories.find({"categories": {}})

        print("final categories array:")
        print(result)

    return json.dumps(result)


@app.route("/api/upload", methods=['GET', "POST"])
def upload_and_process():
    if request.method == "POST":
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

        filename = "video/" + video_name

        with open(filename, "wb") as f: # writes uploaded video object to .mp4 file
            f.write(video.read())

        s3 = boto3.client('s3')
        s3.upload_file(filename, 'qa-classifier2', video_name, ExtraArgs={'ACL':'public-read'})

        # get object url
        video_url = "https://qa-classifier2.s3.amazonaws.com/%s" % (video_name)

        '''JSON CATEGORY'''
        # Call function to check if the category exist or not in the json file
        cats_data = jsonCheck.categoriesJsonCheck(category)
        # cats_data = "categories.json"
        cats_collection = mongo.db.categories

        cats_collection.insert_one(cats_data)

        for i in cats_data['categories']:
            # cats_collection.insert_one(categoryJsonArray[i])
            print(i)  # cats_data['categories'][i])

        # Call function to convert (existing) audio to text  from offset.py file
        auto.convert_auto(title, video_name, video_url, category)

        top5 = nlp.TFIDF()

        client = MongoClient("<Add Mongo URI>", ssl=True)
        client.drop_database("qa-classifier")

        tags_collection = mongo.db.tags
        for i in top5:
            print(top5[i])
            tags_collection.insert_one(top5[i])

        return json.dumps("Successfully uploaded and processed video " + video.filename)


if __name__ == "__main__":
    app.run(debug=True)

