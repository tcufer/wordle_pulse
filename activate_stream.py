#!/usr/bin/env python
# encoding: utf-8

import yaml
import re
import sys
import json
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from datetime import datetime
import socket
import re
import json

class Listener(Stream):
    def __init__(self, *args, **kwargs):
        self.tcp_conn = kwargs['conn']
        super(Listener, self).__init__(*args)


    def send_tweet_to_spark(self, tweet_data):
        try:
            self.tcp_conn.send((json.dumps(tweet_data) + "\n").encode("utf-8"))
        except:
            e = sys.exc_info()
            print("Error: %s" % e)


    def on_status(self, status):
        # ts = datetime.fromtimestamp(int(status.timestamp_ms)/1000)

        wordle_score = re.search(r"Wordle\s22.\s\d\/\d", status.text)
        if wordle_score is None:
            # print("Couldn't parse tweet text.")
            pass
        else:
            self.send_tweet_to_spark(status._json)
            # print(status.text[0:160])


    def on_error(self, status_code):
        print(status_code)
        return False


config = ""
with open('secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

# string to query twitter stream
query_string = config['query_string']
# read credentials
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_key = config['access_key']
access_secret = config['access_secret']

# authorize twitter, initialize tweepy
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = API(auth, wait_on_rate_limit=True)


TCP_IP = "localhost"
TCP_PORT = 9008
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")

stream = Listener(consumer_key, consumer_secret, access_key, access_secret, conn = conn)

try:
    print('Start streaming.')
    stream.filter(track=query_string, languages=['en'])
except KeyboardInterrupt:
    print("Stopped.")
finally:
    print('Done.')
    stream.disconnect()
