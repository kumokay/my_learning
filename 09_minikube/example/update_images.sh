#!/bin/bash

images=`ls dockerfile`
dockerhub="kumokay"

for image in ${images}; do
    echo "****************************************"
    echo "* build docker image: ${image}"
    echo "****************************************"
    docker build -t ${dockerhub}/${image}:latest -f dockerfile/${image}/Dockerfile .
    docker push ${dockerhub}/${image}:latest
done

