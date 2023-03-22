# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install grpcio
RUN pip3 install grpcio-tools

# install app
COPY hellostreamingworld.proto /
COPY async_greeter_server.py /
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. hellostreamingworld.proto

# final configuration
CMD python3 async_greeter_server.py

