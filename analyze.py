FIREBASE_EVENTS_ENDPOINT = "https://e-pulse.firebaseio.com/events.json"

import requests
import json
import re

analyze_session = requests.session()

#---Gets rid of extra punctuation, not latin characters, and urls
def clean(STRING):
    STRING = re.sub(r'(http|https):\/\/.*?[\s]', '', STRING)
    return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:140]

#---Analyzes tweets for news events
def analyze(tweets):
    print 'got these tweets to analyze:'
    print tweets
    event = None
    for tweet in tweets:
        print 'analyzing tweet!'
        print clean(tweet['text'])
        if 'obama' in tweet['text']:
            if not event:event = {'tweets':[]}
            event['tweets'].append({'latlong':tweet['latlong'], 'timestamp':tweet['timestamp'],\
                                    'id':tweet['id']})
    if event:
        print 'event detected!'
        avg_lat = sum(map(lambda x:x['latlong'][0], event['tweets']))/float(len(event['tweets']))
        avg_long = sum(map(lambda x:x['latlong'][1], event['tweets']))/float(len(event['tweets']))
        avg_time = sum(map(lambda x:x['timestamp'], event['tweets']))/float(len(event['tweets']))
        keywords = 'description'
        event['latlong'] = str([avg_lat, avg_long])
        event['keywords'] = 'keywords'
        event['timestamp'] = avg_time
        analyze_session.post(FIREBASE_EVENTS_ENDPOINT, data=json.dumps(event))
