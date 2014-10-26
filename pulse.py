# analyze and trigger must be blocking calls
import analyze
import canary
import time
from threading import Thread
from Queue import PriorityQueue

#---needs to be tested!
def tidapiobj_to_html(tweetid, apiobject):
    return json.loads(apiobject.get_oembed(id=tweetid))['html']

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
            event = analyze.analyze(queue)
        except:
            pass # BAD!
        if event:
            analyze.trigger(event)

class Pulse:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, geotags):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.geotags = geotags
    def start(self):
        self.queue = PriorityQueue()
        self.consumer = Thread(target = consume, args = (queue, ))
        self.consumer.start()
        self.operater = Thread(target = operate, args = (queue, ))
        self.operater.start()
        self.canary = canary.Canary(self.consumer_key, self.consumer_secret,\
                                    self.access_token, self.access_token_secret)
        self.canary.queue = self.queue
        def onData(canary, data):
            timestamp = time.time()
            twit = json.loads(data)
            tweet = {}
            tweet['timestamp'] = timestamp
            tweet['text'] = twit['text']
            tweet['id'] = twit['id_str']#does this actually work? must test!
            if 'coordinates' not in twit or 'coordinates' not in twit['coordinates']:
                print twit
                return#no coordinates in this tweet... somehow got in? we need to watch this!
            tweet['latlong'] = twit['coordinates']['coordinates'][::-1]#twitter returns these flipped
            canary.queue.put((0-timestamp, tweet))
        self.canary.data = onData
        self.canary.startStream(geotags)#may not work???

