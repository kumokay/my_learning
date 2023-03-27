#!/bin/bash

images=`ls dockerfile`
dockerhub="kumokay"

if [ $# != 1 ]; then
    echo "usage: $0 [<image_name>]"
else
    images=$1
fi

for image in ${images}; do
    echo ""
    echo "****************************************"
    echo "* build docker image: ${image}"
    echo "****************************************"
    echo ""
    docker build -t ${dockerhub}/${image}:latest -f dockerfile/${image}/Dockerfile .
    docker push ${dockerhub}/${image}:latest
done

