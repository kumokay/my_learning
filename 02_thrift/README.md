# Getting Started with Apache Thrift


## Concepts

see https://thrift.apache.org/

Note: tried Apache Thrift v0.11.0 but cannot build the cpp example, so use v0.10.0 instead

## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_thrift](https://app.vagrantup.com/kumokay/boxes/ubuntu16_thrift) as the basebox.
This box is generated using the script in [thrift_box](thrift_box).

This setup will create a VM with thrift installed.

## Run sample code

### start the box
```console
$ cd playground
$ vagrant up
$ vagrant ssh
```

### code-gen and compile

code-gen and compile cpp
```console
vagrant@ubuntu-xenial:~/sample_code/cpp$ thrift -r --gen cpp ../tutorial.thrift
vagrant@ubuntu-xenial:~/sample_code/cpp$ ls
CMakeLists.txt  CppClient.cpp  CppServer.cpp  gen-cpp
vagrant@ubuntu-xenial:~/sample_code/cpp$ cmake .
-- The C compiler identification is GNU 5.4.0
-- The CXX compiler identification is GNU 5.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Boost version: 1.58.0
-- Configuring done
-- Generating done
-- Build files have been written to: /home/vagrant/sample_code/cpp
vagrant@ubuntu-xenial:~/sample_code/cpp$ ls
CMakeCache.txt  CMakeFiles  cmake_install.cmake  CMakeLists.txt  CppClient.cpp  CppServer.cpp  gen-cpp  Makefile
vagrant@ubuntu-xenial:~/sample_code/cpp$ make
Scanning dependencies of target tutorialgencpp
[  8%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/Calculator.cpp.o
[ 16%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/SharedService.cpp.o
[ 25%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/shared_constants.cpp.o
[ 33%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/shared_types.cpp.o
[ 41%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/tutorial_constants.cpp.o
[ 50%] Building CXX object CMakeFiles/tutorialgencpp.dir/gen-cpp/tutorial_types.cpp.o
[ 58%] Linking CXX static library libtutorialgencpp.a
[ 66%] Built target tutorialgencpp
Scanning dependencies of target TutorialServer
[ 75%] Building CXX object CMakeFiles/TutorialServer.dir/CppServer.cpp.o
[ 83%] Linking CXX executable TutorialServer
[ 83%] Built target TutorialServer
Scanning dependencies of target TutorialClient
[ 91%] Building CXX object CMakeFiles/TutorialClient.dir/CppClient.cpp.o
[100%] Linking CXX executable TutorialClient
[100%] Built target TutorialClient
vagrant@ubuntu-xenial:~/sample_code/cpp$ ls
CMakeCache.txt  cmake_install.cmake  CppClient.cpp  gen-cpp              Makefile        TutorialServer
CMakeFiles      CMakeLists.txt       CppServer.cpp  libtutorialgencpp.a  TutorialClient
```

code-gen for python
```console
vagrant@ubuntu-xenial:~/sample_code/py$ thrift -r --gen py ../tutorial.thrift
vagrant@ubuntu-xenial:~/sample_code/py$ ls
gen-py  PythonClient.py  PythonServer.py
```

### run sample case

run python server, try to use python client and cpp client to access
```console
vagrant@ubuntu-xenial:~/sample_code/py$ python -u PythonServer.py > server.log &
[1] 1855
vagrant@ubuntu-xenial:~/sample_code/py$ python PythonClient.py
ping()
1+1=2
InvalidOperation: InvalidOperation(whatOp=4, why=u'Cannot divide by 0')
15-10=5
Check log: 5
vagrant@ubuntu-xenial:~/sample_code/py$ ../cpp/TutorialClient
ping()
1 + 1 = 2
InvalidOperation: Cannot divide by 0
15 - 10 = 5
Received log: SharedStruct(key=1, value=5)
vagrant@ubuntu-xenial:~/sample_code/py$ cat server.log
Starting the server...
ping()
add(1,1)
calculate(1, Work(comment=None, num1=1, num2=0, op=4))
calculate(1, Work(comment=None, num1=15, num2=10, op=2))
getStruct(1)
ping()
add(1,1)
calculate(1, Work(comment=None, num1=1, num2=0, op=4))
calculate(1, Work(comment=None, num1=15, num2=10, op=2))
getStruct(1)
vagrant@ubuntu-xenial:~/sample_code/py$ kill 1855
```

run cpp server, try to use python client and cpp client to access
```console
vagrant@ubuntu-xenial:~/sample_code/py$ ../cpp/TutorialServer > cpp_server.log &
[1] 1864
vagrant@ubuntu-xenial:~/sample_code/py$ python PythonClient.py
ping()
1+1=2
InvalidOperation: InvalidOperation(whatOp=4, why=u'Cannot divide by 0')
15-10=5
Check log: 5
vagrant@ubuntu-xenial:~/sample_code/py$ ../cpp/TutorialClient
ping()
1 + 1 = 2
InvalidOperation: Cannot divide by 0
15 - 10 = 5
Received log: SharedStruct(key=1, value=5)
vagrant@ubuntu-xenial:~/sample_code/py$ cat cpp_server.log
Starting the server...
Incoming connection
	SocketInfo: <Host: ::ffff:127.0.0.1 Port: 59240>
	PeerHost: localhost
	PeerAddress: ::ffff:127.0.0.1
	PeerPort: 59240
ping()
add(1, 1)
calculate(1, Work(num1=1, num2=0, op=4, comment=<null>))
calculate(1, Work(num1=15, num2=10, op=2, comment=<null>))
getStruct(1)
Incoming connection
	SocketInfo: <Host: ::ffff:127.0.0.1 Port: 59242>
	PeerHost: localhost
	PeerAddress: ::ffff:127.0.0.1
	PeerPort: 59242
ping()
add(1, 1)
calculate(1, Work(num1=1, num2=0, op=4, comment=<null>))
calculate(1, Work(num1=15, num2=10, op=2, comment=<null>))
getStruct(1)
vagrant@ubuntu-xenial:~/sample_code/py$ kill 1864
```
