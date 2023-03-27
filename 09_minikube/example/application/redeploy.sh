#!/bin/bash

if [ $# != 1 ]; then
    echo "usage: $0 [<image_name>]"
    exit 1
fi

kubectl delete deployment $1
kubectl apply -f deployment

