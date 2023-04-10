#!/bin/bash

projects=`ls project`

if [ $# != 1 ]; then
    echo "usage: $0 [<project_name>]"
else
    projects=$1
fi

for project in ${projects}; do
    echo ""
    echo "****************************************"
    echo "* rollout deployment/${project}"
    echo "****************************************"
    echo ""
    kubectl apply -f project/${project}/kube
    kubectl rollout restart deployment/${project}
done