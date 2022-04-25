import configparser
import yaml
import os
from datetime import date

with open('../secrets.yml', 'r') as file:
    CONFIG = yaml.safe_load(file)

s3_conf = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
s3_conf.read(config_path)

# read credentials
consumer_key = CONFIG['consumer_key']
consumer_secret = CONFIG['consumer_secret']
access_key = CONFIG['access_key']
access_secret = CONFIG['access_secret']

WORDLE_START_DATE = date(2021,6,20)
