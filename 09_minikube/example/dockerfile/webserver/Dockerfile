# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask[async]
RUN pip3 install redis
RUN pip3 install grpcio
RUN pip3 install grpcio-tools

# install app
WORKDIR /myapp/webserver
COPY src/common ../common
COPY src/webserver .
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. *.proto

# final configuration
ENV FLASK_APP=flaskapp
EXPOSE 8080
CMD flask run --host 0.0.0.0 --port 8080

