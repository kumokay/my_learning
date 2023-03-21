# Using Minikube
Environment: 
- ubuntu 16.04
- virtualbox 5.1.38
- minikube v1.29.0
Reference: 
- https://minikube.sigs.k8s.io/docs/start/

## Installation

### Install VirtualBox
```
$ sudo apt-get install virtualbox virtualbox-ext-pack
```
Note: May need to turn off secure boot to make it work.

### Install Minikube
https://minikube.sigs.k8s.io/docs/start/
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Install kubectl (pronounce "kube-cuttle")
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Getting Started 

### Start your cluster with Minikube
```
$ minikube start --driver=virtualbox
😄  minikube v1.29.0 on Ubuntu 16.04
✨  Using the virtualbox driver based on user configuration
💿  Downloading VM boot image ...
    > minikube-v1.29.0-amd64.iso....:  65 B / 65 B [---------] 100.00% ? p/s 0s
    > minikube-v1.29.0-amd64.iso:  276.35 MiB / 276.35 MiB  100.00% 27.05 MiB p
👍  Starting control plane node minikube in cluster minikube
💾  Downloading Kubernetes v1.26.1 preload ...
    > preloaded-images-k8s-v18-v1...:  397.05 MiB / 397.05 MiB  100.00% 31.33 M
🔥  Creating virtualbox VM (CPUs=2, Memory=3900MB, Disk=20000MB) ...
🐳  Preparing Kubernetes v1.26.1 on Docker 20.10.23 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
💡  kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

```

### Interact with your cluster with kubectl
```
$ kubectl get po -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
kube-system   coredns-787d4945fb-gsbnj           1/1     Running   0             11m
kube-system   etcd-minikube                      1/1     Running   0             11m
kube-system   kube-apiserver-minikube            1/1     Running   0             11m
kube-system   kube-controller-manager-minikube   1/1     Running   0             11m
kube-system   kube-proxy-rps5m                   1/1     Running   0             11m
kube-system   kube-scheduler-minikube            1/1     Running   0             11m
kube-system   storage-provisioner                1/1     Running   1 (10m ago)   11m
```

### Show dashboard (in another window)
```
$ minikube dashboard
🔌  Enabling dashboard ...
    ▪ Using image docker.io/kubernetesui/dashboard:v2.7.0
    ▪ Using image docker.io/kubernetesui/metrics-scraper:v1.0.8
💡  Some dashboard features require the metrics-server addon. To enable all features please run:

	minikube addons enable metrics-server	


🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:35147/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...

## Deploying an application

Modify the official example and use Flask + Redis instead of PHP + Redis:
https://kubernetes.io/docs/tutorials/stateless-application/guestbook/

```
### How to build docker images
Ref: https://devopscube.com/build-docker-image/

```
$ cd ~/github/my_learning/09_minikube/dockerfiles/helloworld
$ docker build -t kumokay/flask-helloworld:latest .
$ docker push kumokay/flask-helloworld:latest
```

### Start up a Redis leader.
```
$ cd ~/github/my_learning/09_minikube/application/helloworld
$ kubectl apply -f redis-leader-deployment.yaml
deployment.apps/redis-leader created
$ kubectl apply -f redis-leader-service.yaml
service/redis-leader created
```
### Start up two Redis followers.
```
$ kubectl apply -f redis-follower-deployment.yaml
deployment.apps/redis-follower created
$ kubectl apply -f redis-follower-service.yaml
service/redis-follower created
```
### Start up the frontend.
```
$ kubectl apply -f frontend-deployment.yaml 
deployment.apps/frontend created
$ kubectl apply -f frontend-service.yaml 
service/frontend created
```
### Query the list of Pods
```
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
frontend-68bd8c8b85-h9s22         1/1     Running   0          22s
frontend-68bd8c8b85-jpnfp         1/1     Running   0          22s
frontend-68bd8c8b85-xqhbm         1/1     Running   0          22s
redis-follower-74d9c98c76-nxphc   1/1     Running   0          43s
redis-follower-74d9c98c76-ptmwq   1/1     Running   0          43s
redis-leader-5596fc7b68-sl9vv     1/1     Running   0          90s
```
### Query the list of Services and start the tunnel 
Frontend's external-IP is still pending.
```
$ kubectl get service
NAME             TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
frontend         LoadBalancer   10.103.201.214   <pending>     8080:30044/TCP   30s
kubernetes       ClusterIP      10.96.0.1        <none>        443/TCP          30h
redis-follower   ClusterIP      10.102.254.141   <none>        6379/TCP         50s
redis-leader     ClusterIP      10.108.156.152   <none>        6379/TCP         85s
```
In another window, start the tunnel to create a routable IP for the frontend deployment:
```
$ minikube tunnel
Status:	
	machine: minikube
	pid: 21792
	route: 10.96.0.0/12 -> 192.168.59.100
	minikube: Running
	services: [frontend]
    errors: 
		minikube: no errors
		router: no errors
		loadbalancer emulator: no errors
```
Now we have frontend's external-IP:
```
$ kubectl get services
NAME             TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
frontend         LoadBalancer   10.103.201.214   10.103.201.214   8080:30044/TCP   7m9s
kubernetes       ClusterIP      10.96.0.1        <none>           443/TCP          30h
redis-follower   ClusterIP      10.102.254.141   <none>           6379/TCP         7m29s
redis-leader     ClusterIP      10.108.156.152   <none>           6379/TCP         8m4s
```
### Test the deployment

```
$ curl http://10.103.201.214:8080
Hello World!

$ curl http://10.103.201.214:8080/get_from_redis
[{}]

$ curl -X POST -H "Content-Type: application/json" -d '{"key1": 12345}' http://10.103.201.214:8080/add_to_redis
[{"key1":"12345"}]

$ curl http://10.103.201.214:8080/get_from_redis
[{"key1":"12345"}]
```

### Debug the deployment
We can get inside a pod / container to check if there's something wrong.
For example, debugging hello-minikube1 running the container image built from here: https://github.com/kumokay/my_learning/tree/master/09_minikube/dockerfiles/helloworld
```
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
hello-minikube1-c799c86d-4vvzc    1/1     Running   0          4m4s

$ kubectl exec -it hello-minikube1-c799c86d-4vvzc -- bash

root@hello-minikube1-c799c86d-4vvzc:/# flask shell

Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
App: hello [production]
Instance: /instance
>>> from hello import get_from_redis
>>> get_from_redis()
Traceback (most recent call last):
  File "/hello.py", line 40, in get_from_redis
    return jsonify([dict(zip(keys, vals))])
  File "/usr/local/lib/python3.8/dist-packages/flask/json/__init__.py", line 302, in jsonify
    f"{dumps(data, indent=indent, separators=separators)}\n",
  File "/usr/local/lib/python3.8/dist-packages/flask/json/__init__.py", line 132, in dumps
    return _json.dumps(obj, **kwargs)
  File "/usr/lib/python3.8/json/__init__.py", line 234, in dumps
    return cls(
  File "/usr/lib/python3.8/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib/python3.8/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
TypeError: keys must be str, int, float, bool or None, not bytes
```

### Scale the web frontend 
Scale up the number of frontend Pods:
```
$ kubectl scale deployment frontend --replicas=5
$ kubectl get pods
```
Scale down the number of frontend Pods:

```
$ kubectl scale deployment frontend --replicas=2
$ kubectl get pods
```

### Clean up deployments and services
```
$ kubectl delete deployment -l app=redis
$ kubectl delete service -l app=redis
$ kubectl delete deployment frontend
$ kubectl delete service frontend
```
### Clean up minikube
```
$ minikube stop
✋  Stopping node "minikube"  ...
🛑  1 node stopped.

$ minikube delete --all
🔥  Deleting "minikube" in virtualbox ...
💀  Removed all traces of the "minikube" cluster.
🔥  Successfully deleted all profiles
```



