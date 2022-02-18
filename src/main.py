from apscheduler.schedulers.blocking import BlockingScheduler
from makeSentences import make_sentences
from timelineTweets import fetch_timeline_tweets, get_tweets
from tweet import tweet
import logging
from replyStream import ReplyStreamListener, ReplyStream
from twitterAuth import auth
from flask_cors import CORS
from flask import Flask, jsonify
import os

logging.basicConfig(level=logging.DEBUG)

sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True


@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()


@sched.scheduled_job('interval', id='reply_stream', seconds=60)
def reply_stream():
    listener = ReplyStreamListener()
    stream = ReplyStream(auth, listener)
    stream.start()


app = Flask(__name__)
CORS(app)

@app.get("/api/make_sentence")
async def make_sentence():
    sentence_1, sentence_2 = make_sentences()
    if not get_tweets():
        fetch_timeline_tweets()
    return jsonify({'sentence': sentence_1})
    

if __name__ == "__main__":
    app.run (
          threaded=True,
          host = os.environ["HOST"], 
          port = os.environ["PORT"], 
          debug=False
    )
    sched.start()