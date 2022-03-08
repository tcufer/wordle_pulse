#!/usr/bin/env python
# encoding: utf-8

import yaml
import json
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
import boto3


class Listener(Stream):
    def __init__(self, *args):
        super(Listener, self).__init__(*args)

    def send_tweet_to_kinesis(self, tweet_data):
        try:
            kinesis_client.put_record(
              StreamName=stream_name,
              Data=(json.dumps(tweet_data) + "\n").encode("utf-8"),
              PartitionKey=str(tweet_data['user']['screen_name'])
            )
        except Error as e:
            raise e

    def on_status(self, status):
        self.send_tweet_to_kinesis(status._json)

    def on_error(self, status_code):
        print(status_code)
        return False


config = ""
with open('secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

# string to track twitter topic
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

# create kinesis client
session = boto3.Session(profile_name="development")
kinesis_client = session.client("kinesis", region_name='eu-central-1')
stream_name = "twitter_wordle_stream"

stream = Listener(consumer_key, consumer_secret, access_key, access_secret)

try:
    print('Start streaming.')
    stream.filter(track=query_string, languages=['en'])
except KeyboardInterrupt:
    print("Stopped.")
finally:
    print('Done.')
    stream.disconnect()
