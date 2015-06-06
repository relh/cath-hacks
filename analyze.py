import copy
import requests
import json
import re
import random
import firebase

#---Gets rid of extra punctuation, not latin characters, and urls
def clean(message):
    out = ''
    words = message.replace('\n',' ').split()
    bad_words = [u'hour',u'are',u'here',u'much',u'things',u'than',u'there',u'much',u'from',u'still',u'being',u'into',u'out',u'every',u'they',u'now',u'were',u'very',u'after',u'would',u'could',u'can',u'can',u'will',u'doe',u'thats',u'why',u'take',u'cant',u'well',u'look',u'know',u'all',u'ur',u'what',u'who',u'where',u'or',u'do',u'got',u'when',u'no',u'u',u'im',u'dont',u'how',u'if',u'as',u'nd',u'up',u'by',u'what',u'about',u'was',u'',u'its',u'in',u'too',u'a',u'an',u'i',u'he',u'me',u'she',u'we',u'the',u'to',u'are',u'you',u'him',u'her',u'my',u'and',u'is',u'of',u'to',u'rt',u'for',u'on',u'it',u'that',u'this',u'be',u'just',u'like',u'lol',u'rofl',u'lmao',u'your',u'have',u'but',u'you',u'not',u'get',u'so',u'at',u'with']
    for word in words:
        if word.lower() in bad_words:
            continue
        if word[0] is '@' or word[:2] is '.@':
            continue
        if word.lower()[:4] == 'http':
            continue
        if word == 'RT':
            return ''
        if len(word) < 3:
            continue
        out += ''.join([c for c in word if c.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789 ./,;\'[]<>?:"{}~!@#$%^&*()_+=-`'])
        out += ' '
    return out.lower().strip()

def good(tweet):
    if tweet['text'][:2].lower() == 'rt':
        return False
    return True

def analyze(tweets):
    tweets = copy.deepcopy(tweets)
    for tweet in tweets:
        if not good(tweet):
            continue
        text = tweet['text'] # clean(tweet['text'])
        lat = tweet['latlong'][0]
        long = tweet['latlong'][1]
        timestamp = tweet['timestamp']
        tweet_id = tweet['id']
        firebase.push('prepel', {'ID':tweet_id, 'Lat':lat,
                      'Long':long, 'Text':text, 'Timestamp':timestamp})

