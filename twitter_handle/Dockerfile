# pull official base image
FROM python:3.9.5-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# copy project
COPY . /app/
COPY ./secrets.yml /app/
#start stream
CMD ["python", "stream_to_kinesis.py"]
