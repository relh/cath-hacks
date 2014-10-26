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
        analyze_session.post("https://luminous-fire-1209.firebaseio.com/events.json",\
                             data=json.dumps(event))

'''
t1 = {"latlong":"40.7127, -74.0059", "text":"ahh bees be all up in my http://google.com beesniss", "id":"1", "timestamp":"1414287284.405456"}
t2 = {"latlong":"40.7123, -74.0051", "text":"The!! http://www.x.com bees are attacking", "id":"2", "timestamp":"1414287284.415456"}
t3 = {"latlong":"40.7130, -74.0063", "text":"Don't $#$#( like getting stung none", "id":"3", "timestamp":"1414287289.408456"}
t4 = {"latlong":"40.7117, -74.0049", "text":"The hive exploded and the bees are out", "id":"4", "timestamp":"1414287294.408456"}
tweets = [t1, t2, t3, t4]
analyze(tweets)
'''
