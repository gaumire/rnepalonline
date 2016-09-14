

from flask import Flask
from flask import render_template
import praw
from pymongo import MongoClient
import os
import datetime
import simplejson as json
from bson import json_util

app = Flask(__name__, static_url_path='/static')


@app.route("/insertdata")
def record_active_users():
    """
    returns active users in r/Nepal
    """
    mongo_url = os.environ.get(
        'MONGODB_URI', "mongodb://127.0.0.1:27017/redditor")
    mc = MongoClient(mongo_url)
    db = getattr(mc, mongo_url.rsplit('/',1)[1])
    user_agent = "r/Nepal active user count"
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit('Nepal')
    active_users = subreddit.accounts_active
    result = db.active_user.insert_one(dict(
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        online=active_users))
    return "SUCCESS"


@app.route("/getrawdata")
def get_active_user():
    mongo_url = os.environ.get(
        'MONGODB_URI', "mongodb://127.0.0.1:27017/redditor")
    mc = MongoClient(mongo_url)
    db = getattr(mc, mongo_url.rsplit('/',1)[1])
    json_data = [doc for doc in db.active_user.find({}, {'_id': False})]
    json_data = json.dumps(json_data, default=json_util.default)
    return json_data


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # record_active_users()
    # get_active_user()
    app.run(host='0.0.0.0', port=port, debug=True)
