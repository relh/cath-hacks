from analyze import analyze, trigger
import time

def clean(STRING):
    return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:100]

#---needs to be tested!
def tidapiobj_to_html(tweetid, apiobject):
    return json.loads(apiobject.get_oembed(id=tweetid))['html']

#---streams tweets into queue
def stream_thread(queue):
    return

#---removes tweets from the bottom of the queue
def remove_thread(queue):
    time = time.time() * -1
    try:
	(t_time, tweet) = queue.get()
        while t_time - time > 60*15:
	    (t_time, tweet) = queue.get()
	queue.put((t_time,tweet))

    except Queue.Empty:
	return

    return

#---analyzes queue for news events
def analysis_thread(queue):
    #analyze current queue
    event = analyze(queue)
    if event:
	trigger(event)
    return

