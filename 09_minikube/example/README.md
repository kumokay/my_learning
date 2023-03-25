# How to run

## folder structure
```
$ cd example
$ tree

.
├── application
│   ├── deployment
│   │   ├── celery-worker-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── redis-follower-deployment.yaml
│   │   ├── redis-leader-deployment.yaml
│   │   └── writer-deployment.yaml
│   └── service
│       ├── frontend-service.yaml
│       ├── redis-follower-service.yaml
│       ├── redis-leader-service.yaml
│       └── writer-service.yaml
├── dockerfile
│   ├── celeryworker
│   │   └── Dockerfile
│   ├── webserver
│   │   └── Dockerfile
│   └── writer
│       └── Dockerfile
└── src
    ├── celeryworker
    │   └── tasks.py -> ../common/tasks.py
    ├── common
    │   ├── hellostreamingworld.proto
    │   └── tasks.py
    ├── reader
    ├── webserver
    │   ├── async_greeter_client.py
    │   ├── flaskapp.py
    │   └── hellostreamingworld.proto -> ../common/hellostreamingworld.proto
    └── writer
        ├── async_greeter_server.py
        ├── hellostreamingworld.proto -> ../common/hellostreamingworld.proto
        └── tasks.py -> ../common/tasks.py

```

## Build docker image in each folder

```
$ cd example
$ export MYAPP=<folder-name>
$ docker build -t kumokay/$MYAPP:latest -f dockerfile/$MYAPP/Dockerfile .
$ docker run kumokay/$MYAPP:latest
$ docker ps
$ docker stop <container-id>
$ docker push kumokay/$MYAPP:latest
```

## Start minikube
```
screen1 $ start minikube
screen2 $ minikube dashboard
screen3 $ minikube tunnel
```

## create deployment and service
```
$ cd example/application

$ kubectl apply -f deployment/.
deployment.apps/celery-worker created
deployment.apps/frontend created
deployment.apps/redis-follower created
deployment.apps/redis-leader created
deployment.apps/writer created

$ kubectl apply -f service/.
service/frontend created
service/redis-follower created
service/redis-leader created
service/writer created
```

## delete deployment and service, stop minikube
```
$ cd example/application
$ kubectl delete deployment --all
$ kubectl delete service --all
$ stop minikube
```

