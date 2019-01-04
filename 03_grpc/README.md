# Getting Started with Apache Thrift

using grpc v1.17.1, protobuf v3.6.1

## Concepts

see https://grpc.io/docs/guides/concepts.html

similar to thrift.


## How files are generated

see Protocol Buffer tutorial in [cpp](https://developers.google.com/protocol-buffers/docs/cpptutorial) and [python](https://developers.google.com/protocol-buffers/docs/pythontutorial)

## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_grpc](https://app.vagrantup.com/kumokay/boxes/ubuntu16_grpc) as the base box. This box is generated using the script in [grpc_box](grpc_box).

This setup will create a VM with grpc v1.17.1 installed. The VM can run python and cpp.

To enable more programming languages, follow the instructions in [thrift/lib/<language>](https://github.com/apache/thrift/tree/master/lib)

## Run sample code

The [sample code](grpc_box/sample_code) are taken from the [official helloworld tutorial](https://grpc.io/docs/tutorials/).

### start the box
```console
$ cd playground
$ vagrant up
$ vagrant ssh
```

### code-gen and compile

see the Makefile in each folder.
```console
vagrant@ubuntu-xenial:~/sample_code/cpp/helloworld$ make
protoc -I ../../protos --cpp_out=. ../../protos/helloworld.proto
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o helloworld.pb.o helloworld.pb.cc
protoc -I ../../protos --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../../protos/helloworld.proto
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o helloworld.grpc.pb.o helloworld.grpc.pb.cc
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o greeter_client.o greeter_client.cc
g++ helloworld.pb.o helloworld.grpc.pb.o greeter_client.o -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl -o greeter_client
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o greeter_server.o greeter_server.cc
g++ helloworld.pb.o helloworld.grpc.pb.o greeter_server.o -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl -o greeter_server
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o greeter_async_client.o greeter_async_client.cc
g++ helloworld.pb.o helloworld.grpc.pb.o greeter_async_client.o -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl -o greeter_async_client
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o greeter_async_client2.o greeter_async_client2.cc
g++ helloworld.pb.o helloworld.grpc.pb.o greeter_async_client2.o -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl -o greeter_async_client2
g++ -std=c++11 `pkg-config --cflags protobuf grpc`  -c -o greeter_async_server.o greeter_async_server.cc
g++ helloworld.pb.o helloworld.grpc.pb.o greeter_async_server.o -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl -o greeter_async_server

vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ make
python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto
python -m compileall .
Listing . ...
Compiling ./greeter_client.py ...
Compiling ./greeter_client_with_options.py ...
Compiling ./greeter_server.py ...
Compiling ./greeter_server_with_reflection.py ...
Compiling ./helloworld_pb2.py ...
Compiling ./helloworld_pb2_grpc.py ...
```

### run sample case

run python server, try to use python client and cpp client to access
```console
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ python greeter_server.py >/dev/null &
[1] 1680
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ python greeter_client.py
Greeter client received: Hello, you!
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ ../../cpp/helloworld/greeter_client
Greeter received: Hello, world!
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ kill 1680
```

run cpp server, try to use python client and cpp client to access
```console
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ ../../cpp/helloworld/greeter_server >/dev/null &
[1] 1695
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ python greeter_client.py
Greeter client received: Hello you
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ ../../cpp/helloworld/greeter_client
Greeter received: Hello world
vagrant@ubuntu-xenial:~/sample_code/python/helloworld$ kill 1695
```
