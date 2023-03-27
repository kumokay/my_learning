# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install grpcio
RUN pip3 install grpcio-tools
RUN pip3 install -U celery[redis]

# install app
WORKDIR /myapp/reader
COPY src/common ../common
COPY src/reader .
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. *.proto

# final configuration
CMD python3 async_reader_server.py

