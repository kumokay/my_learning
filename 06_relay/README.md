# Getting Started with relay

using nodejs v11.x,

## Concepts


## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_react](https://app.vagrantup.com/kumokay/boxes/ubuntu16_react) as the base box. This box is generated using the script in [react_box](../04_react/react_box).

In addition to nodejs v11.x and react v16.7.0 which are already installed in the base box, we will need to use npm to install other packages such as express, express-graphql, and graphql in the project folder later.

## Run sample code

[playground_no_relay](playground_no_relay) illustrates how react_app talks to graphql-server.


### run playground_no_relay

start vagrant
```console
$ cd playground
$ vagrant up
```

then go to http://localhost:3000 for the react_app


### run playground_no_relay
