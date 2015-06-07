#!/usr/bin/env python
import time
import json
import random
import re
from bottle import route, hook, response, run, static_file

@route('/')
def index():
    return static_file('index.html', root = '.')

@route('/maptweets.js')
def index_css():
    return static_file('maptweets.js', root = '.')

@route('/cross.jpg')
def index_css():
    return static_file('cross.jpg', root = '.')

@route('/light.png')
def index_css():
    return static_file('light.png', root = '.')

@route('/event.png')
def index_css():
    return static_file('event.png', root = '.')

run(host = '0.0.0.0', port = 80, server = 'tornado', debug = True)
