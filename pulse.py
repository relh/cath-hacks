from analyze import analyze, trigger

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

