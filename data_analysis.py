import pulse
from analyze import clean
import os
import sys
import tweepy
import json
import datetime
import copy

#keywords = [u'tragedy',u'shooting',u'shooter',u'shoot',u'concert',u'game']

def prune(d):
    #keywords = [u'tragedy',u'shooting',u'shooter',u'shoot',u'concert',u'game']

    badwords = [u'hour',u'are',u'here',u'much',u'things',u'than',u'there',u'much',u'from',u'still',u'being',u'into',u'out',u'every',u'they',u'now',u'were',u'very',u'after',u'would',u'could',u'can',u'can',u'will',u'doe',u'thats',u'why',u'take',u'cant',u'well',u'look',u'know',u'all',u'ur',u'what',u'who',u'where',u'or',u'do',u'got',u'when',u'no',u'u',u'im',u'dont',u'how',u'if',u'as',u'nd',u'up',u'by',u'what',u'about',u'was',u'',u'its',u'in',u'too',u'a',u'an',u'i',u'he',u'me',u'she',u'we',u'the',u'to',u'are',u'you',u'him',u'her',u'my',u'and',u'is',u'of',u'to',u'rt',u'for',u'on',u'it',u'that',u'this',u'be',u'just',u'like',u'lol',u'rofl',u'lmao',u'your',u'have',u'but',u'you',u'not',u'get',u'so',u'at',u'with']
#return {x for x in d if x not in badwords}
    di = {}
    for w in d:
        if w not in badwords:
            di[w] = d[w]

    return di

def analyze_test(tweets):
    #keywords = [u'tragedy',u'shooting',u'shooter',u'shoot',u'concert',u'game']
    keywords = [u'rain',u'rainy',u'storm',u'stormy',u'sunny',u'snow',u'snowy',u'cloudy',u'clear',u'windy',u'wind',u'bright']
    temperature_words = [u'cold',u'freezing',u'frigid',u'chilly',u'mild',u'warm',u'hot',u'scorching',u'scorcher',u'heat']
    all_tweets = copy.copy(tweets)      #copy of tweets
    event = None
    word_freq = {}      #frequency list
    for tweet in tweets:
        #print clean(tweet['text'])
        if tweet['text'][:2].lower() == 'rt':continue
        #---Your code goes here! Try stuff to find events!
        #^- frequency analysis?
        txt = clean(tweet['text'])
        #txt = tweet['text']
        words = txt.split(' ')	#wordlist
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
        if f in keywords:	#tweak
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
        #---Your code goes above this. Try to find events!

    if event:
        print("event found:")
        #avg_lat = sum(map(lambda x:x['latlong'][0], event['tweets']))/float(len(event['tweets']))
        #avg_long = sum(map(lambda x:x['latlong'][1], event['tweets']))/float(len(event['tweets']))
        #avg_time = sum(map(lambda x:x['timestamp'], event['tweets']))/float(len(event['tweets']))
        #event['latlong'] = str([avg_lat, avg_long])
        #event['keywords'] = keywords
        #event['timestamp'] = avg_time
        print event
        print ""
        #analyze_session.post("https://luminous-fire-1209.firebaseio.com/events.json",data=json.dumps(event))

#----

num = 100    #number of tweets to parse at a time
f = open('./tweets/20-24_sea_10km', 'r')
lines = f.readlines();
t = []
for l in lines:
    tweet = eval(l)
    t.append(tweet)
tweets = t[::-1]
f.close()

for i in range(0,len(tweets)/num):
    if (i+1)*num > len(tweets):
        analyze_test(tweets[i*num:len(tweets)])
    else:
        analyze_test(tweets[i*num:(i+1)*num])

print "done"
