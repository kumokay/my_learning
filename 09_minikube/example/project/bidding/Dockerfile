# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install grpcio
RUN pip3 install grpcio-tools
RUN pip3 install -U celery[redis]
RUN pip3 install mysql-connector-python

# install app
WORKDIR /bidding
COPY src/ .
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. *.proto

# final configuration
CMD echo "hello world!"
