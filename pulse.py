# analyze and trigger must be blocking calls
from analyze import analyze, trigger
import time

def clean(STRING):
    return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:140]

#---needs to be tested!
def tidapiobj_to_html(tweetid, apiobject):
    return json.loads(apiobject.get_oembed(id=tweetid))['html']

#---removes tweets from the bottom of the queue
def remove_thread(queue):
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
def analysis_thread(queue):
    while True:
        time.sleep(0.25)
        #analyze current queue
        try:
            event = analyze(queue)
        except:
            pass # BAD!
        if event:
            trigger(event)

