import tweepy
import json
import os
import sys
import time
from analyze import clean

def __main__():
    if len(sys.argv) != 5:
        print "python fetch_data.py <c_key> <c_secret> <a_token> <a_token_s>"
        sys.exit(-1)

    c_key = sys.argv[1]
    c_secret = sys.argv[2]
    a_token = sys.argv[3]
    a_token_s = sys.argv[4]

    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_token_s)

    api = tweepy.API(auth)

    #tweets = api.search("",rpp=100,page=1,geocode="40.915256,-74.259088,25km")
    #tweets = api.search("",geocode="[[[-74.259088,40.915256],[-73.700272,40.915256],[-73.700272,40.495996],[-74.259088,40.495996]]]")
    #print tweets[0]
    for tweet in tweepy.Cursor(api.search, q="",
                           geocode="47.734145,-122.435908,20km",
                           since="2014-10-23",
                           until="2014-10-25",
                           lang="en").items():
        time.sleep(.3)
        t = {}
        t['text'] = clean(tweet.text)
        t['latlong'] = tweet.coordinates
        t['id'] = tweet.id
        t['timestamp'] = tweet.created_at
        print t
__main__()
