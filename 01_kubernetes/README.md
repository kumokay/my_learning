# How to use kubernetes

using kubernetes v1.13.1

## Concepts

This article explains different pieces that make up the Kubernetes: [ref](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16).

## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_kubeadm](https://app.vagrantup.com/kumokay/boxes/ubuntu16_kubeadm) as the basebox. This box is generated using the script in [00_vagrant/kubeadm_box](../../00_vagrant/kubeadm_box/).

This setup will create a cluster of 2 workers.

### start VMs
```console
$ cd playground
$ vagrant up
$ vagrant ssh master
```

### setup cluster

setup kubectl
``` console
vagrant@master$ mkdir -p $HOME/.kube
        sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

check cluster status
```console
vagrant@master:~$ kubectl get nodes
NAME      STATUS     ROLES    AGE     VERSION
master    NotReady   master   15m     v1.13.1
worker1   NotReady   <none>   2m16s   v1.13.1
worker2   NotReady   <none>   85s     v1.13.1
```

install a pod network add-on so that your pods can communicate with each other.
See [pod-network](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#pod-network)
and information about [flannel network](https://kubernetes.io/docs/concepts/cluster-administration/networking/#flannel)

```console
vagrant@master:~$ wget https://raw.githubusercontent.com/kumokay/my_learning/master/01_kubernetes/files/kube-flannel.yml
vagrant@master:~$ kubectl apply -f kube-flannel.yml
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds-amd64 created
daemonset.extensions/kube-flannel-ds-arm64 created
daemonset.extensions/kube-flannel-ds-arm created
daemonset.extensions/kube-flannel-ds-ppc64le created
daemonset.extensions/kube-flannel-ds-s390x created
```

## Deploy applications
ref: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

create a deployment
```console
vagrant@master:~$ wget https://raw.githubusercontent.com/kumokay/my_learning/master/01_kubernetes/playground/files/nginx-app/run-my-nginx.yaml
vagrant@master:~$ kubectl apply -f run-my-nginx.yaml
deployment.apps/my-nginx created
```

check deployment status
```console
vagrant@master:~$ kubectl get deployments -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES   SELECTOR
my-nginx   2/2     2            2           9m10s   my-nginx     nginx    run=my-nginx

```

check pod status in this deployment
```console
vagrant@master:~$ kubectl get pods -l run=my-nginx -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP           NODE      NOMINATED NODE   READINESS GATES
my-nginx-64fc468bd4-9w69x   1/1     Running   0          9m57s   10.244.1.4   worker1   <none>           <none>
my-nginx-64fc468bd4-fr4wp   1/1     Running   0          9m57s   10.244.2.2   worker2   <none>           <none>
```

check more deployment details
```console
vagrant@master:~$ kubectl describe deployment my-nginx
Name:                   my-nginx
Namespace:              default
CreationTimestamp:      Wed, 02 Jan 2019 18:44:09 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
                        kubectl.kubernetes.io/last-applied-configuration:
                          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"name":"my-nginx","namespace":"default"},"spec":{"replicas":2,"se...
Selector:               run=my-nginx
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  run=my-nginx
  Containers:
   my-nginx:
    Image:        nginx
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   my-nginx-64fc468bd4 (2/2 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  6m17s  deployment-controller  Scaled up replica set my-nginx-64fc468bd4 to 2
```

## Connecting applications with services

ref: https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/

### create a Service object that exposes the deployment

There are multiple ways to do it. The easiest way is to use NodePort. Here is an article about different ways to get external traffic into your cluster [ref](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0)

create a service
```console
vagrant@master:~$ wget https://raw.githubusercontent.com/kumokay/my_learning/master/01_kubernetes/playground/files/nginx-app/nginx-svc.yaml
vagrant@master:~$ kubectl create -f nginx-svc.yaml
service/my-nginx created
```

check service status
```console
vagrant@master:~$  kubectl get svc my-nginx -o wide
NAME       TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE     SELECTOR
my-nginx   NodePort   10.100.213.194   <none>        8080:31839/TCP   4m56s   run=my-nginx
```

check service details
```console
vagrant@master:~$ kubectl describe service my-nginx
Name:                     my-nginx
Namespace:                default
Labels:                   run=my-nginx
Annotations:              <none>
Selector:                 run=my-nginx
Type:                     NodePort
IP:                       10.100.213.194
Port:                     http  8080/TCP
TargetPort:               80/TCP
NodePort:                 http  31839/TCP
Endpoints:                10.244.1.4:80,10.244.2.2:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

### use the Endpoints' public IP and NodePort to access the service

check pod status in this deployment

10.244.1.4:80,10.244.2.2:80 corresponds to worker1 and worker2 respectively.
```console
vagrant@master:~$ kubectl get pods -l run=my-nginx -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP           NODE      NOMINATED NODE   READINESS GATES
my-nginx-64fc468bd4-9w69x   1/1     Running   0          9m57s   10.244.1.4   worker1   <none>           <none>
my-nginx-64fc468bd4-fr4wp   1/1     Running   0          9m57s   10.244.2.2   worker2   <none>           <none>
```

The private network IPs of worker1 and worker2 are 10.11.0.101, 10.11.0.102 respectively.
(see Vagrantfile: `node.vm.network :private_network, ip:"#{VAR_NW_PREFIX}.#{100+i}"`)

```console
vagrant@master~$ curl http://10.11.0.101:31839
vagrant@master~$ curl http://10.11.0.102:31839
```

## Clean-up the applications

```
vagrant@master:~$ kubectl delete deployments,svc my-nginx
deployment.extensions "my-nginx" deleted
service "my-nginx" deleted
```

## Create deployment and service in one step

Option 1: write everything in one file
```console
vagrant@master:~$ cat nginx-svc.yaml run-my-nginx.yaml > nginx-app.yaml
vagrant@master:~$ kubectl create -f nginx-app.yaml
service/my-nginx created
deployment.apps/my-nginx created
vagrant@master:~$ kubectl delete -f nginx-app.yaml
service "my-nginx" deleted
deployment.apps "my-nginx" deleted

```

Option 2: put everything in one folder
```console
vagrant@master:~$ mkdir nginx-app
vagrant@master:~$ mv nginx-svc.yaml nginx-app/.
vagrant@master:~$ mv run-my-nginx.yaml nginx-app/.
vagrant@master:~$ kubectl create -f nginx-app
service/my-nginx created
deployment.apps/my-nginx created
vagrant@master:~$ kubectl delete -f nginx-app
service "my-nginx" deleted
deployment.apps "my-nginx" deleted
```
