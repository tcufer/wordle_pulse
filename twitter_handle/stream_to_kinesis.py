#!/usr/bin/env python
# encoding: utf-8
from functools import cache
import json
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
import boto3
import time
from datetime import datetime
import constants as const

class Listener(Stream):
    def __init__(self, *args):
        super(Listener, self).__init__(*args)

    # create kinesis client
    @cache
    def _kinesis_client(self):
        kinesis_client = boto3.client(
            "kinesis",
            aws_access_key_id=const.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=const.AWS_SECRET_ACCESS_KEY,
            region_name=const.AWS_REGION_NAME
        )
        return kinesis_client

    def send_tweet_to_kinesis(self, tweet_data):
        try:
            self._kinesis_client().put_record(
                StreamName=const.KINESIS_STREAM_NAME,
                Data=(json.dumps(tweet_data) + "\n").encode("utf-8"),
                PartitionKey=str(tweet_data['user']['screen_name'])
            )
        except UnicodeEncodeError as e:
            # pass on possible encoding problem to avoid breaking the stream
            pass

    def on_status(self, status):
        self.send_tweet_to_kinesis(status._json)

    def on_error(self, status_code):
        print(status_code)
        return True


def _prepare_filter_keywords():
    wordle_id = (datetime.utcnow().date() - const.WORDLE_START_DATE).days
    stream_filter = [f"Wordle {wordle_id}"]
    return stream_filter

def _stream_tweets(stream):
    stream.filter(track=_prepare_filter_keywords(), languages=['en'], threaded=False)
    current_date = datetime.utcnow().date()
    while True:
        if datetime.utcnow().date() > current_date:
            stream.disconnect()
            current_date = datetime.utcnow().date()
            time.sleep(10)
            stream.filter(track=_prepare_filter_keywords(), languages=['en'], threaded=True)


def main():
    # authorize twitter, initialize stream
    auth = OAuthHandler(const.TWITTER_CONSUMER_KEY, const.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(const.TWITTER_ACCESS_KEY, const.TWITTER_ACCESS_SECRET)
    api = API(auth, wait_on_rate_limit=True)
    stream = Listener(const.TWITTER_CONSUMER_KEY, const.TWITTER_CONSUMER_SECRET, const.TWITTER_ACCESS_KEY, const.TWITTER_ACCESS_SECRET)
    try:
        print('Start streaming.')
        _stream_tweets(stream)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        print('Done.')
        stream.disconnect()

if __name__ == '__main__':
    main()

