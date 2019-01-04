# Getting Started with React

using nodejs v11.x, react v16.7.0

## Concepts

see https://reactjs.org/docs/hello-world.html

for javascript, see [A_re-introduction_to_JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript)

for npm: [an-absolute-beginners-guide-to-using-npm](https://nodesource.com/blog/an-absolute-beginners-guide-to-using-npm/)

for npx: https://www.npmjs.com/package/npx

## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_react](https://app.vagrantup.com/kumokay/boxes/ubuntu16_react) as the base box. This box is generated using the script in [react_box](grpc_box).

This setup will create a VM with nodejs v11.x and react v16.7.0 installed.

## Run sample code

The [sample code](react_box/sample_code) are taken from the [official tic-tac-toe tutorial](https://reactjs.org/tutorial/tutorial.html)

### start the box
```console
$ cd playground
$ vagrant up
$ vagrant ssh
```

### run the application

start application
```console
vagrant@ubuntu-xenial:~$ cd react_tictactoe
vagrant@ubuntu-xenial:~/react_tictactoe$ npm start
Compiled successfully!

You can now view react_tictactoe in the browser.

  Local:            http://localhost:3000/
  On Your Network:  http://10.0.2.15:3000/

Note that the development build is not optimized.
To create a production build, use npm run build.
```

Since we did port forwarding in the [Vagrantfile](playground/Vagrantfile),
we can access VM's port 3000 from host port 3333.
Open a web browser and you will see the tic-tac-toe at http://127.0.0.1:3333/
```console
$ curl http://127.0.0.1:3333
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <meta name="theme-color" content="#000000" />
    <!--
      manifest.json provides metadata used when your web app is added to the
      homescreen on Android. See https://developers.google.com/web/fundamentals/web-app-manifest/
    -->
    <link rel="manifest" href="/manifest.json" />
...
```
