import yaml

with open('../secrets.yml', 'r') as file:
    CONFIG = yaml.safe_load(file)

CHECKPOINT_BUCKET = "s3a://" + CONFIG['bucket'] + "/" + CONFIG['folder'] + "/"
