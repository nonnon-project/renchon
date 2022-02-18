import random
from urllib import response
import MeCab
import numpy as np

from makeTweetSentences import make_tweet_sentences
from timelineTweets import tweets, fetch_timeline_tweets
from filters import normalize_text

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def make_reply_sentence(status):
    screen_name = status.user.screen_name
    text = status.text.replace(",", "")
    text = normalize_text(text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace('@nyanpassnanon', "")
    response = None
    # 占い
    if "占って" in text or "おみくじ" in text:
        response = "@{} {}なん！".format(screen_name, random.choice(("凶", "大凶", "末吉", "吉", "小吉", "中吉", "大吉")))
    # じゃんけん
    if "グー" in text or "チョキ" in text or "パー" in text or "ぐー" in text or "ちょき" in text or "ぱー" in text:
        result = random.choice(("グー", "チョキ", "パー"))
         # あいこ
        if result == text: 
            response = "@{} {}なん！あいこなん！".format(screen_name, result)
        # 勝ちパターン
        elif result == "グー" and text == "チョキ":
            response = "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        elif result == "チョキ" and text == "パー": 
            response = "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        elif result == "パー" and text == "グー": 
            response = "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        # 負けパターン
        elif result == "グー" and text == "パー":
            response = "@{} {}なん！うちの負けなん！".format(screen_name, result)
        elif result == "チョキ" and text == "グー":
            response = "@{} {}なん！うちの負けなん！".format(screen_name, result)
        elif result == "パー" and text == "チョキ":
            response = "@{} {}なん！うちの負けなん！".format(screen_name, result)
    else:
        if len(tweets) == 0:
            fetch_timeline_tweets()
        sentence_1, sentence_2 = make_tweet_sentences() 
        response = "@{} {}".format(screen_name, sentence_1)
    return response