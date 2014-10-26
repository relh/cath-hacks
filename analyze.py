FIREBASE_EVENTS_ENDPOINT = "https://e-pulse.firebaseio.com/events.json"

import requests
import json
import re
import random

analyze_session = requests.session()

#---Gets rid of extra punctuation, not latin characters, and urls
def clean(STRING):
    STRING = re.sub(r'(http|https):\/\/.*?[\s]', '', STRING)
    return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:140]

#---Analyzes tweets for news events
def analyze(tweets):
    event = None
    
    for tweet in tweets:
        print clean(tweet['text'])
        if 'obama' in tweet['text'] or random.random() > 0.8:
            if not event:event = {}
            event[str(tweet['id'])] = {'Lat':tweet['latlong'][0], 'Long':tweet['latlong'][1],\
                                       'Timestamp':tweet['timestamp'],'Data':tweet['id']}
    
    # SET EVENT DESCRIPTION IN VAR DESCRIPTION
    description = 'beautiful weather'
    # EVENT MUST CONTAIN TWEETS WITH LAT,LONG,TIMESTAMP,DATA
    if event:
        print 'event detected!'
        tweets = [event[x] for x in event if isinstance(event[x], dict)]
        avg_lat = sum(map(lambda x:x['Lat'], tweets))/float(len(tweets))
        avg_long = sum(map(lambda x:x['Long'], tweets))/float(len(tweets))
        avg_time = sum(map(lambda x:x['Timestamp'], tweets))/float(len(tweets))
        event['Lat'] = avg_lat
        event['Long'] = avg_long
        event['Keywords'] = description
        event['Timestamp'] = avg_time
        analyze_session.post(FIREBASE_EVENTS_ENDPOINT, data=json.dumps(event))
