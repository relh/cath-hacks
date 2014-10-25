import os
import sys
import time
from Queue import Queue
from threading import Thread

globals()['last_time'] = 0
globals()['queue_size'] = 10000		#tinker with this
globals()['queue'] = Queue(globals()['queue_size'])
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
   decoded = json.loads(data)
   #push onto end of queue
  globals()['last_time'] = time.time()
  return True
 def on_error(self, status):
  print status

#thread #1: streams tweets into queue
#thread #2: removes tweets from the bottom of the queue
#thread #3: periodically analyzes queue - looks for news

# NEEDS TO BE TESTED!
def tidapiobj_to_html(tweetid, apiobject):
 return json.loads(apiobject.get_oembed(id=tweetid))['html']

def stream_thread(queue):
 l = StdOutListener()
 auth = OAuthHandler(consumer_key, consumer_secret)
 auth.set_access_token(access_token, access_token_secret)
 api_object = API(auth)
 stream = Stream(auth, l)

def remove_thread(queue):
 #remove old tweets
 return

def analysis_thread(queue):
 #analyze current queue
 return

#---start threads
feeder = Thread(Target=stream_thread, args=(queue,))
consumer = Thread(Target=remove_thread, args=(queue,))
#analyzer = Thread(Target=analysis_thread, args=(queue,))

feeder.start()
consumer.start()
#analyzer.start()
