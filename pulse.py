from analyze import analyze, trigger

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
    #remove old tweets
    return

#---analyzes queue for news events
def analysis_thread(queue):
    #analyze current queue
    return

