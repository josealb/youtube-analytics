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

@app.route("/search_api", methods=["POST"])
def search_api():
    if request.content_type != 'application/json':
        return "ERROR: expects a json file"
    post_data = request.get_json()
    video_id = post_data.get('video_id')

    comment_list = yt.get_video_comments(video_id)
    t = []
    for comment in comment_list:
        polarity = TextBlob(comment['text']).sentiment.polarity
        subjectivity = TextBlob(comment['text']).sentiment.subjectivity
        t.append([comment['text'],polarity,subjectivity])
    stats = generate_stats(t)
    return stats

@app.route("/search", methods=["POST"])
def search():
    video_id = request.form.get("search_query")
    comment_list = yt.get_video_comments(video_id)
    t = []
    for comment in comment_list:
        polarity = TextBlob(comment['text']).sentiment.polarity
        subjectivity = TextBlob(comment['text']).sentiment.subjectivity
        t.append([comment['text'],polarity,subjectivity])
    stats = generate_stats(t)
    return stats

def generate_stats(comments):
    num_comments = len(comments)
    
    num_pos_comments = 0
    num_neg_comments = 0
    for comment in comments:
        if comment[1]>0:
            num_pos_comments+=1
        else:
            num_neg_comments+=1
    pos_percent = num_pos_comments / num_comments
    neg_percent = num_neg_comments / num_comments

    result = {
        'analyzed_comments': num_comments,
        'polarity': {
            'positive': {
                'amount': num_pos_comments,
                'percent': pos_percent
            },
            'negative': {
                'amount': num_neg_comments,
                'percent': neg_percent
            }
        }
    }
    return result