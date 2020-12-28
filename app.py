import pymongo
from pymongo import MongoClient
from bson import json_util
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
plt.rcdefaults()

#MongoClient for connecting MongoDB with Flask
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration
mongostring = MongoClient("mongodb://admin:school@127.0.0.1:27017")
#database-Donor
db = mongostring.donor
#Aggregates-ProjectStats & DonorStats
projectCollection = db.ProjectStats
donorCollection = db.DonorStats

#Webpage - running
@app.route('/')
def Index():
    return render_template('index.html')

# publish wordcloud
@app.route('/search', methods=['GET', 'POST'])
def search():

    all_top_words = []
    category = request.form['category']

    # TopWords column has an array of 25 words extracted from each donor essay
    # List 25 such topwords(array of 25 words) for each resource category
    top_words = [task for task in projectCollection.find({"ProjectResourceCategory": category}, {
                                                         "TopWords": 1}).sort('DonationStrength', pymongo.DESCENDING).limit(25)]
    for i in range(0, len(top_words)):
        all_top_words.extend(x for x in top_words)

    # Get top 40 words with their count
    t = Counter(str(all_top_words).split()).most_common(40)

    # Extract just the words from top 40
    final_words = [w[0] for w in t]

    #Reduce noise
    final_words = (str(final_words).replace("',", ""))

    # Use wordcloud library to generate the wordcloud with required attributes
    wcloud = WordCloud(max_words=100, colormap='cool', background_color='white',
                       normalize_plurals=True).generate((str(final_words).replace("'", "")))

    plt.figure(figsize=(15, 15))
    plt.imshow(wcloud)
    plt.axis('off')
    plt.title('')
    plt.show()
    return render_template('index.html')

 # Search Maximum Donors
@app.route('/donors', methods=['GET', 'POST'])
def donors():
    category = request.form['category']
    # Get top 30 donors for selected category
    donorlist = [task for task in donorCollection.find({"ProjectResourceCategory": category}, {
                                                       "DonorId": 1, "DonationSum": 1, "DonationCount": 1, "City": 1, "State": 1, "Zip": 1}).sort('DonationSum', pymongo.DESCENDING).limit(30)]

    col_names = ['_id', 'Donor ID', 'Donor City',
                 'Donor State', 'Donor Zip', 'sum', 'count']
    donor_list = pd.DataFrame(list(donorlist))
    donor_list.columns = col_names

    return render_template('maxdonors.html', maxdonor=list(donor_list.values))

# Search Maximum Utilized Resource Category
@app.route('/resource', methods=['GET', 'POST'])
def resource():
    category = request.form['category']

    # List max donation for each category
    #maxdonorlist=[task for task in projectCollection.find({"Category" : category},{"Category" : 1, "Strength" : 1})]
    maxdonorlist = [task for task in projectCollection.aggregate([{"$match": {"ProjectResourceCategory": category}}, {
                                                                 "$group": {"_id": "$ProjectResourceCategory", "AvgStrength": {"$avg": "$DonationStrength"}}}])]

    col_names = ['Category', 'Strength']
    maxdonor_list = pd.DataFrame(list(maxdonorlist))
    maxdonor_list.columns = col_names

    return render_template('maxdonationlist.html', maxdonation=list(maxdonor_list.values))

# insert data into database
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        category = request.form['category']
        projectname = request.form['pname']
        cost = request.form['ecost']
        essay = request.form['essay']

        mydict = {"ProjectName": projectname, "ProjectResourceCategory": category,
                  "ProjectCost": cost, "Essay":  essay}

        x = projectCollection.insert_one(mydict)
        return jsonify("Added Project:" + projectname)

#Delete Projects
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        category = request.form['category']
        projectname = request.form['pname']

        x = projectCollection.remove(
            {"ProjectName": projectname, "ProjectResourceCategory": category})

        return jsonify("Deleted Project:" + projectname)


if __name__ == '__main__':
    app.run(debug=True)
