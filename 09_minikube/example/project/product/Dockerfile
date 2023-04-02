# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# install app
WORKDIR /product
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .
COPY tmp/product.proto .
RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. *.proto

# final configuration
CMD echo "hello world!"
