import datetime
import os

from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from youtube_api import YouTubeDataAPI

api_key =  os.environ['YOUTUBE_API_KEY']

yt = YouTubeDataAPI(api_key)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    video_id = request.form.get("search_query")
    comment_list = yt.get_video_comments(video_id)
    t = []
    for comment in comment_list:
        polarity = TextBlob(comment['text']).sentiment.polarity
        subjectivity = TextBlob(comment['text']).sentiment.subjectivity
        t.append([comment['text'],polarity,subjectivity])

    return jsonify({"success": True, "tweets": t})
