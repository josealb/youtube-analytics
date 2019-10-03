import os
import tweepy

from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

from twitter_sentiment_analysis.utils import utils


api_key =  os.environ['YOUTUBE_API_KEY']

api = tweepy.API(auth)
yt = YouTubeDataAPI(api_key)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    search_words = request.form.get("search_query")
    t = []
    interval = datetime.timedelta(days=1)
    search_end = datetime.datetime.now() # TODO make this user selectable
    search_start = datetime.datetime.now() - datetime.timedelta(days=7) # Twitter API limitation

    search_intervals = utils.get_time_intervals(search_start,search_end,interval)

    for search_interval in search_intervals:
        interval_start = search_interval[0]
        interval_end = search_interval[1]
        tweets = tweepy.Cursor(api.search,
                q = search_words,
                lang = 'en',
                since=interval_start,
                until=interval_end).items(20)

        for tweet in tweets:
            polarity = TextBlob(tweet.text).sentiment.polarity
            subjectivity = TextBlob(tweet.text).sentiment.subjectivity
            t.append([tweet.text,polarity,subjectivity])

    return jsonify({"success": True, "tweets": t})
