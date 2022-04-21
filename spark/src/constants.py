import configparser
import yaml
import os

with open('../secrets.yml', 'r') as file:
    CONFIG = yaml.safe_load(file)

s3_conf = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
s3_conf.read(config_path)
AWS_ACCESS_KEY_ID = s3_conf.get('development', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = s3_conf.get('development', 'aws_secret_access_key')
