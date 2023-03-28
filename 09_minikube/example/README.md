# How to run

## Start minikube
```
screen1 $ start minikube
screen2 $ minikube dashboard
screen3 $ minikube tunnel
```

## Build docker image in each folder

```
$ cd example/project/${project}/
$ docker build -t ${dockerhub}/${project}:latest -f Dockerfile .
$ docker push ${dockerhub}/${project}:latest

or

$ cd example
$ ./update_images.sh ${project}
```

## create deployment and service
```
$ kubectl apply -f project/bidding/kube/
```

## debug pod
```
$ kubectl get pods
NAME                               READY   STATUS        RESTARTS      AGE
webapp-6bbd95b5f5-t5dxr            1/1     Running       0             7s
...

$ kubectl logs -f webapp-6bbd95b5f5-t5dxr
```

## re-deploy deployment
```
$ kubectl rollout restart deployment/${project}
```

## delete deployment and service, stop minikube
```
$ cd example/application
$ kubectl delete deployment --all
$ kubectl delete service --all
$ stop minikube
```
