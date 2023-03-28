#!/bin/bash

projects=`ls project`
dockerhub="kumokay"
current_dir=`pwd`

if [ $# != 1 ]; then
    echo "usage: $0 [<image_name>]"
else
    projects=$1
fi

for project in ${projects}; do
    echo ""
    echo "****************************************"
    echo "* build docker image: ${project}"
    echo "****************************************"
    echo ""
    cp ${current_dir}/common/* ${current_dir}/project/${project}/
    cd ${current_dir}/project/${project}
    docker build -t ${dockerhub}/${project}:latest -f Dockerfile .
    docker push ${dockerhub}/${project}:latest
done
