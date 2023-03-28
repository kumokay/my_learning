#!/bin/bash

projects=`ls project`
dockerhub="kumokay"

if [ $# != 1 ]; then
    echo "usage: $0 [<image_name>]"
else
    images=$1
fi

for project in ${projects}; do
    echo ""
    echo "****************************************"
    echo "* build docker image: ${project}"
    echo "****************************************"
    echo ""
    cp common/* project/${project}/
    docker build -t ${dockerhub}/${project}:latest -f ${project}/Dockerfile project/${project}
    docker push ${dockerhub}/${project}:latest
done
