# analyze and trigger must be blocking calls
import analyze
import canary
import time
import copy
import json
from threading import Thread
from Queue import PriorityQueue

#---removes tweets from the bottom of the queue
def consume(queue):
    while True:
        time.sleep(0.25)
        timer = time.time() * -1
        try:
            (t_time, tweet) = queue.get()
            while t_time - timer > 60*15:  #15 minute expiry
                (t_time, tweet) = queue.get()
            queue.put((t_time,tweet))
        except Queue.Empty:
            continue

#---analyzes queue for news events
def operate(queue):
    while True:
        time.sleep(0.25)
        #analyze current queue
        try:
            print 'sent to analyze'
            analyze.analyze(copy.copy(map(lambda x:x[1],queue.queue)))
        except Exception,e:
            print 'whoa not analyzed'
            print str(e)
            pass # BAD!

class Pulse:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, geotags):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.geotags = geotags
    def start(self):
        self.queue = PriorityQueue()
        self.consumer = Thread(target = consume, args = (self.queue, ))
        self.consumer.start()
        self.operater = Thread(target = operate, args = (self.queue, ))
        self.operater.start()
        self.canary = canary.Canary(self.consumer_key, self.consumer_secret,\
                                    self.access_token, self.access_token_secret)
        self.canary.queue = self.queue
        def onData(canary, data):
            try:
                timestamp = time.time()
                twit = json.loads(data)
                print 'THIS IS OUR TWIT:'
                print twit
                try:
                    tweet = {}
                    tweet['timestamp'] = timestamp
                    tweet['text'] = twit['text']
                    tweet['id'] = str(twit['id'])#does this actually work? must test!
                    tweet['latlong'] = twit['coordinates']['coordinates'][::-1]#twitter returns these flipped
                    self.canary.queue.put((0-timestamp, tweet))
                except Exception,e:
                    print "LOLWAT"
                    print str(e)
            except Exception,e:
                print 'EXCEPTION!'
                print str(e)
        self.canary.onData = onData
        self.canary.startStream(self.geotags)#may not work???

