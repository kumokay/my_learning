# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -U celery[redis]

# install app
COPY tasks.py /

# final configuration
CMD celery -A tasks worker --loglevel=INFO

