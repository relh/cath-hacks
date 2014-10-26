import requests
import json

s = requests.session()

#---Analyzes tweets for news events
def analyze(tweets):
    print ""

#---Send information to database
def trigger(event):
    url = "https://luminous-fire-1209.firebaseio.com/events.json" 
    r = s.post(url, data=json.dumps(event))

