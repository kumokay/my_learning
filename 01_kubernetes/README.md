# How to use kubernetes

## Environment setup

Use vagrant to create multiple vms as the playground. See 00_vagrant [../00_vagrant] for more details.

In Vagrantfile, use vagrant box generated in 00_vagrant/kubeadm_box [../../00_vagrant/kubeadm_box/] as the basebox.

This setup will create a cluster of 2 workers.

## Deploy applications

### first make sure we have a cluster setup correctly
```
$ cd playground
$ vagrant up
$ vagrant ssh master

# setup kubectl
master$ mkdir -p $HOME/.kube
        sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config

# check node status
master$ kubectl get nodes
NAME      STATUS     ROLES    AGE     VERSION
master    NotReady   master   7m57s   v1.13.1
worker1   NotReady   <none>   7m5s    v1.13.1
worker2   NotReady   <none>   6m11s   v1.13.1
```

### then create a pod
ref: https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/
```
master$ wget https://raw.githubusercontent.com/coreos/flannel/bc79dd1505b0c8681ece4de4c0d86c5cd2643275/Documentation/kube-flannel.yml
master$ kubectl apply -f kube-flannel.yml
master$ kubectl get pods --all-namespaces
NAMESPACE     NAME                             READY   STATUS    RESTARTS   AGE
kube-system   coredns-86c58d9df4-7k992         1/1     Running   0          5m2s
kube-system   coredns-86c58d9df4-wlnm6         1/1     Running   0          5m2s
kube-system   etcd-master                      1/1     Running   0          4m2s
kube-system   kube-apiserver-master            1/1     Running   0          4m27s
kube-system   kube-controller-manager-master   1/1     Running   0          4m28s
kube-system   kube-flannel-ds-amd64-5lkrl      1/1     Running   0          71s
kube-system   kube-flannel-ds-amd64-k46lf      1/1     Running   0          71s
kube-system   kube-flannel-ds-amd64-zpwtp      1/1     Running   0          71s
kube-system   kube-proxy-9wnrg                 1/1     Running   0          4m30s
kube-system   kube-proxy-dk662                 1/1     Running   0          5m2s
kube-system   kube-proxy-nt5lm                 1/1     Running   0          3m37s
kube-system   kube-scheduler-master            1/1     Running   0          4m15s
```

### deploy applications
ref: https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/

```
master$ wget https://k8s.io/examples/application/deployment.yaml
master$ kubectl apply -f deployment.yaml
```

### check pod IPs
```
master$ kubectl get pods -l app=nginx -o wide
NAME                                READY   STATUS    RESTARTS   AGE   IP           NODE      NOMINATED NODE   READINESS GATES
nginx-deployment-76bf4969df-jhmzd   1/1     Running   0          19m   10.244.1.2   worker1   <none>           <none>
nginx-deployment-76bf4969df-rb76j   1/1     Running   0          19m   10.244.2.2   worker2   <none>           <none>

```

### check deployment status
```
master$ kubectl describe deployment nginx-deployment
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Tue, 01 Jan 2019 00:52:54 +0000
...
  Containers:
   nginx:
    Image:        nginx:1.7.9
    Port:         80/TCP
    Host Port:    0/TCP
...
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-76bf4969df (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  25s   deployment-controller  Scaled up replica set nginx-deployment-76bf4969df to 2
```

## Access applications

There are multiple ways. Here we create a service to access it.

ref: https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

### create a Service object that exposes the deployment
```
master$ kubectl expose deployments nginx-deployment --type=NodePort --name=nginx-service

# get the exposed port
master$ kubectl describe services nginx-service | grep NodePort
Type:                     NodePort
NodePort:                 <unset>  30735/TCP                   <none>
```

### check which nodes are running the application
```
master$ kubectl get pods -l app=nginx -o wide
NAME                                READY   STATUS    RESTARTS   AGE   IP           NODE      NOMINATED NODE   READINESS GATES
nginx-deployment-76bf4969df-jhmzd   1/1     Running   0          19m   10.244.1.2   worker1   <none>           <none>
nginx-deployment-76bf4969df-rb76j   1/1     Running   0          19m   10.244.2.2   worker2   <none>           <none>
```

### use the node's public ip and NodePort to access the service
```
master$ curl http://10.11.0.101:30735
master$ curl http://10.11.0.102:30735



```








