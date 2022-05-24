Data Engineering project for capturing and parsing Wordle results from Twitter Stream.
[Blog post](https://tcufer.github.io/wordle_pulse/).

## Objective

The objective is to capture messages with Wordle daily puzzle results on Twitter and store them in a form that enables analysis and exploration of results. 

## High level architecture

  https://whimsical.com/wordle-pulse-pipeline-design-LNV8hCKdRDbuud5q8gYR77

  ![Whimsical diagram](static/whimsical_diagram.png?raw=true)

## Results

![Streamlit dashboard](static/dashboard_printscreen.png?raw=true)


## Live demo dashboard

[http://ec2-3-126-209-227.eu-central-1.compute.amazonaws.com:8000/](http://ec2-3-126-209-227.eu-central-1.compute.amazonaws.com:8000/)


## Setup
### Requirements
  - AWS account
  - Twitter API credentials
  - Docker & docker-compose
  - Terraform

### Setup instructions

1. Install Docker, docker-compose and Terraform
2. Create new App on [Twitter Developer portal](https://developer.twitter.com/en/portal/projects-and-apps) to obtain credentials
3. Install Terraform, navigate to `wordle_pulse/kinesis_ds_firehose/` and run `terraform plan` and `terraform apply`
4. You need to fill in the following variables to your `.env` file:
```
# AWS credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# S3 settings
S3_BUCKET=
S3_FOLDER=

# Kinesis settings
KINESIS_STREAM_NAME=
KINESIS_ENDPOINT_URL=
AWS_REGION_NAME=eu-central-1

# Twitter credentials
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_KEY=
TWITTER_ACCESS_SECRET=

# Postgres settings
PG_DBNAME=
PG_USER=
PG_PASSWORD=
PG_HOST=
PG_PORT=

# Streamlit port settings
PORT=8000
```

5. To run tests, navigate to `wordle_pulse/` and run:
  - `docker-compose -f docker-compose-test.yml build`
  - `docker-compose -f docker-compose-test.yml up`

6. To run all containers (Twitter handle, Spark, Airflow, Streamlit), navigate to `wordle_pulse/` and run:
  - `docker-compose -f docker-compose.yml build` and
  - `docker-compose -f docker-compose.yml up`
