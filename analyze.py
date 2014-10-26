import requests
import json

s = requests.session()

#---Analyzes tweets for news events
def analyze(tweets):
    print ""

#---Send information to database
def trigger(event):
    r = s.post("https://luminous-fire-1209.firebaseio.com/events.json", 
                      data=json.dumps(event))

