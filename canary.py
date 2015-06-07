import time
import datetime
import random
import traceback

try:
    import tweepy
except ImportError:
    import os
    os.system('curl https://bootstrap.pypa.io/get-pip.py -o pip.py')
    os.system('python pip.py')
    os.system('rm pip.py')
    os.system('pip install tweepy')
    os.system('pip install requests')
    import tweepy

def printHelp():
    print 'Usage example: '
    print '>>> from canary import Canary'
    print '>>> import json, time'
    print '>>> watcher = Canary("consumer_api_key", "consumer_api_secret",'
    print '                     "access_token", "access_secret")'
    print '>>> def onData(watcher, data):print "\\n"+json.loads(data)["text"]'
    print '>>> watcher.onData = onData'
    print '>>> watcher.startStream(["obama"])'
    print '>>> time.sleep(15)'
    print '>>> watcher.stopStream()'

class OnDataListener(tweepy.streaming.StreamListener):
    def __init__(self, parent):
        self.parent = parent
    def on_data(self, data):
        self.parent.onData(self.parent, data)
        return True
    def on_error(self, status):
        self.parent.onError(status)
        return True

class Canary:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.listener = OnDataListener(self)
        self.stream = tweepy.Stream(auth, self.listener)
    def onData(self, data):
        print 'DEFAULT ONDATA'
        print '\n'+str(data).strip()
        print 'DEFAULT ONDATA'
    def onError(self, error):
        traceback.print_exc()
    def startStream(self, locations = ['pancake']):
        if self.stream.running:
            self.stream.disconnect()
        self.stream.filter(track = locations, async = True)
    def stopStream(self):
        self.stream.disconnect()

# comment this out in prod
# printHelp()
