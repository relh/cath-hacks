#from analyze import find_event?

class Tweet():
    info = {} 	#fields: latlong, text, id, timestamp
    def init(self, data):
	decoded = json.loads(data)
	info['latlong'] = decoded[]
	info['text'] = clean(decoded[])
	info['id'] = decoded[]
	info['timestamp'] = decoded[]
	
def clean(STRING):
    return (''.join([c for c in STRING if c.lower() in 'abcdefghijklmnopqrstuvwxyz ']))[:100]


#---needs to be tested!
def tidapiobj_to_html(tweetid, apiobject):
    return json.loads(apiobject.get_oembed(id=tweetid))['html']

#---streams tweets into queue
def stream_thread(queue):
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_object = API(auth)
    stream = Stream(auth, l)

#---removes tweets from the bottom of the queue
def remove_thread(queue):
    #remove old tweets
    return

#---analyzes queue for news events
def analysis_thread(queue):
    #analyze current queue
    return

