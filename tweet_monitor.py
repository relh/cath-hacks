import os
import sys
import time
 
globals()['last_time'] = 0
 
if len(sys.argv)!=5:
 print 'Please run with consumer_key, consumer_secret, access_token, access_token_secret!'
 sys.exit(-1)
  
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
 
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=sys.argv[1]
consumer_secret=sys.argv[2]
 
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=sys.argv[3]
access_token_secret=sys.argv[4]
 
def clean(STRING):
 return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:100]
 
class StdOutListener(StreamListener):
 def on_data(self, data):
  if time.time() - globals()['last_time'] < 120:
   print 'Still waiting...'
   return True
  tweet_id = str(json.loads(data)['id'])
  cb1 = cleverbot.Cleverbot()
  our_tweet = '@' + json.loads(data)['user']['screen_name'] + ' ' + cb1.ask(clean(json.loads(data)['text']))
  api_object.update_status(status = our_tweet)
  print json.loads(data)['text']
  print "WE TWEETED:"
  print our_tweet
  print '\n\n'
  globals()['last_time'] = time.time()
  return True
 def on_error(self, status):
  print status
 
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api_object = API(auth)
stream = Stream(auth, l)
stream.filter(track=[str(raw_input('What keyword should we troll? '))])
