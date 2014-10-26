import pulse
from analyze import clean
import os
import sys
import tweepy
import json
import datetime

def analyze_test(tweets):
    event = None
    for tweet in tweets:
        #print clean(tweet['text'])
        
        #---Your code goes here! Try stuff to find events!
        if '' in tweet['text']:
            if not event:event = {'tweets':[]}
            event['tweets'].append({'latlong':tweet['latlong'], 'timestamp':tweet['timestamp'],'id':tweet['id']})
        #---Your code goes above this. Try to find events!

    if event:
        print("event found:\n")
        avg_lat = sum(map(lambda x:x['latlong'][0], event['tweets']))/float(len(event['tweets']))
        avg_long = sum(map(lambda x:x['latlong'][1], event['tweets']))/float(len(event['tweets']))
        avg_time = sum(map(lambda x:x['timestamp'], event['tweets']))/float(len(event['tweets']))
        keywords = 'description'
        event['latlong'] = str([avg_lat, avg_long])
        event['keywords'] = 'keywords'
        event['timestamp'] = avg_time
        #analyze_session.post("https://luminous-fire-1209.firebaseio.com/events.json",data=json.dumps(event))

#----

f = open('./tweets/23-25_seattle_10km', 'r')
lines = f.readlines();
t = []
for l in lines:
    tweet = eval(l)
    t.append(tweet)
tweets = t[::-1]
f.close()

for i in range(0,len(tweets)/100):
    if (i+1)*100 > len(tweets):
        analyze_test(tweets[i*100:len(tweets)])
    else:
        analyze_test(tweets[i*100:(i+1)*100])

print "done"
