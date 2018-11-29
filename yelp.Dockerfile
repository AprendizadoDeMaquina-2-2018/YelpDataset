FROM python:2.7.15-alpine

ADD . /app
WORKDIR /app

RUN pip install simplejson