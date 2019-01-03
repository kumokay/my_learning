#!/usr/bin/env bash

apt-get update

# install thrift 0.10.0
# https://thrift-tutorial.readthedocs.io/en/latest/installation.html
sudo apt-get -y install \
  automake bison flex g++ git libboost-all-dev libevent-dev libssl-dev \
  libtool make pkg-config
wget http://archive.apache.org/dist/thrift/0.10.0/thrift-0.10.0.tar.gz
tar -xvf thrift-0.10.0.tar.gz
cd thrift-0.10.0
./bootstrap.sh
./configure
make
sudo make install
thrift -version

# install language support
cd lib/py
sudo python setup.py install
sudo apt-get -y install python-pip cmake
pip --disable-pip-version-check install six

# clean up
sudo apt-get clean
cd ~
sudo rm -rf thrift-0.10.0*
