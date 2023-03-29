# Setup python virtual env

## Install pyenv
ubuntu 16.04
```
sudo apt-get update
sudo apt-get install build-essential git libreadline-dev zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
# may need this, but install script above should handle it; and yeah, you can do multiline inserts with awk/sed or whatever
echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.9
```
## Setup python virtual env for each project
```
$ cd ${project}
$ source ~/.bashrc
$ pyenv virtualenv 3.9.16 ${project}
$ echo -e "${project}\n3.9.16\n" > .python-version
(${project}) $ 
```

## Generate requirements.txt
First create your requirement.in
```
(${project}) $ cat requirement.in
grpcio
grpcio-tools
celery[redis]
mysql-connector-python
```
Then compile
```
(${project}) $ pip install pip-tools
(${project}) $ pip-compile --resolver=backtracking
```

## Install from requirements.txt
```
(${project}) pip install -r requirements.txt
```

# Setup deployment

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
