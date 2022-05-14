import yaml
from datetime import date

with open('secrets.yml', 'r') as file:
    CONFIG = yaml.safe_load(file)


WORDLE_START_DATE = date(2021, 6, 19)
