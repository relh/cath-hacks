FIREBASE_EVENTS_ENDPOINT = "https://e-pulse.firebaseio.com/events.json"

import requests
import json
import re
import random
from data_analysis import prune

analyze_session = requests.session()

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
        out += ''.join([c for c in word if c.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789 '])
        out += ' '
    return out.lower().strip()

#---Analyzes tweets for news events
def analyze(tweets):
    event = None
    
    keywords = [u'rain',u'rainy',u'storm',u'stormy',u'sunny',u'snow',u'snowy',u'cloudy',u'clear',u'windy',u'wind',u'bright']
    temperature_words = [u'cold',u'freezing',u'frigid',u'chilly',u'mild',u'warm',u'hot',u'scorching',u'scorcher',u'heat']
    all_tweets = copy.copy(tweets)      #copy of tweets
    word_freq = {}      #frequency list
    for tweet in tweets:
        #print clean(tweet['text'])
        if tweet['text'][:2].lower() == 'rt':continue
        #---Your code goes here! Try stuff to find events!
        #^- frequency analysis?
        txt = clean(tweet['text'])
        #txt = tweet['text']
        words = txt.split(' ')  #wordlist
        #print txt
        #print words
        for w in words:
            if not w.lower() in word_freq:
                word_freq[w.lower()] = 1
            else:
                word_freq[w.lower()] += 1
    freq = prune(word_freq)
    freq2 = sorted(freq, key=freq.get)
    freq = freq2[len(freq2)-30:len(freq2)]  #top 30 current words
    #print freq
    i = 0
    for f in freq:
        if f in keywords:       #tweak
            #print "keyword found: "+f
            #print len(all_tweets)
            for t in all_tweets:
                if t['text'][:2].lower() == 'rt':continue
                if f in clean(t['text']).split(' '):
                    if not event:
                        event = {}
                        event['tweets'] = []
                    event['tweets'].append({'latlong':t['latlong'],'timestamp':t['timestamp'],'id':t['id']})
                    event['keywords'] = [f]
                    for temp in temperature_words:
                        if temp in clean(t['text']).split(' '):
                            event['keywords'].append(temp)

            break
        i += 1


    
    # SET EVENT DESCRIPTION IN VAR DESCRIPTION
    description = 'weather'
    # EVENT MUST CONTAIN TWEETS WITH LAT,LONG,TIMESTAMP,DATA
    if event:
        print 'event detected!'
        print event
        tweets = [event[x] for x in event if isinstance(event[x], dict)]
        #avg_lat = sum(map(lambda x:x['Lat'], tweets))/float(len(tweets))
        #avg_long = sum(map(lambda x:x['Long'], tweets))/float(len(tweets))
        #avg_time = sum(map(lambda x:x['Timestamp'], tweets))/float(len(tweets))
        #event['Lat'] = avg_lat
        #event['Long'] = avg_long
        #event['Keywords'] = description
        #event['Timestamp'] = avg_time
        #analyze_session.post(FIREBASE_EVENTS_ENDPOINT, data=json.dumps(event))
