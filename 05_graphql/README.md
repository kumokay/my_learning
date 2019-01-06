# Getting Started with graphql

using nodejs v11.x,

## Concepts

see https://graphql.github.io/learn/

and https://code.fb.com/core-data/graphql-a-data-query-language/

for javascript, see [A_re-introduction_to_JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript)

for npm: [an-absolute-beginners-guide-to-using-npm](https://nodesource.com/blog/an-absolute-beginners-guide-to-using-npm/)

for npx: https://www.npmjs.com/package/npx

to enable es6 imports in node js: [how-to-enable-es6-imports-in-nodejs](https://timonweb.com/posts/how-to-enable-es6-imports-in-nodejs/)

## Environment setup

Use vagrant to create multiple VMs as the playground. See [00_vagrant](../00_vagrant) for how to use vagrant.

In Vagrantfile, use [ubuntu16_react](https://app.vagrantup.com/kumokay/boxes/ubuntu16_react) as the base box. This box is generated using the script in [react_box](../04_react/react_box).

In addition to nodejs v11.x and react v16.7.0 which are already installed in the base box, we will need to use npm to install other packages such as express, express-graphql, and graphql in the project folder later.

## Run sample code

The [graphql_helloworld](playground/graphql_helloworld) example is taken from [here](https://graphql.github.io/graphql-js/mutations-and-input-types/). It is one of the many in [graphql.js tutorial](https://graphql.github.io/graphql-js/).


The [graphql_helloworld_rewrite](playground/graphql_helloworld_rewrite) example
modified [graphql_helloworld](playground/graphql_helloworld) to javascript [es6](https://en.wikipedia.org/wiki/ECMAScript#6th_Edition_-_ECMAScript_2015).
In this example we also construct graphql object types by ourself; see [constructing-types](https://graphql.org/graphql-js/constructing-types/) for more details.


The [graphql_starwars](playground/graphql_starwars) is a much simpler version of the [starwars graphql wrapper](https://graphql.org/swapi-graphql/) that used by the [official tutorial](https://graphql.github.io/learn/). The corresponding source code is here (https://github.com/graphql/swapi-graphql).


We leveraged files (starWarsSchema.js and starWarsData.js) in [graphql-js github](https://github.com/graphql/graphql-js/tree/master/src/__tests__), made some modification, and implemented the mutation function `createReview`. It provides an alternative way to walk through the [official tutorial](https://graphql.github.io/learn/).


### start the box
```console
$ cd playground
$ vagrant up
$ vagrant ssh
```

### run graphql_helloworld

install packages
```console
vagrant@ubuntu-xenial:~/graphql_helloworld$ npm install
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN graphql_helloword@1.0.0 No description
npm WARN graphql_helloword@1.0.0 No repository field.

added 54 packages from 38 contributors and audited 145 packages in 7.208s
found 0 vulnerabilities
```

run the application
```console
vagrant@ubuntu-xenial:~/graphql_helloworld$ npm start

> graphql_helloword@1.0.0 start /home/vagrant/graphql_helloworld
> node index.js

Running a GraphQL API server at localhost:4000/graphql
```

Since we did port forwarding in the [Vagrantfile](playground/Vagrantfile),
we can access VM's port 4000 from host port 4444.
Open a web browser and you will see the GraphiQL UI at http://127.0.0.1:4444/graphql

Sample queries and mutations:
```
query {
  listMessageIDs
}

query {
  getMessage(id: "testid") {
    id
    author
    content
  }
}

mutation {
  createMessage(input: {
    author: "haha",
    content: "this is a new msg"
  }) {
    id
  }

}

mutation {
  updateMessage(id: "testid", input: {
    author: "testuser",
    content: "update test msg"
  }) {
    id
    content
  }
}

```

### run graphql_helloworld_rewrite

same as [run graphql_helloword](#run-graphql_helloworld).

### run graphql_starwars

install packages
```console
vagrant@ubuntu-xenial:~/graphql_starwars$ npm install
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN graphql_starwars@1.0.0 No description
npm WARN graphql_starwars@1.0.0 No repository field.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules/fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"linux","arch":"x64"})

added 313 packages from 161 contributors and audited 3657 packages in 13.18s
found 0 vulnerabilities
```

run the application
```console
vagrant@ubuntu-xenial:~/graphql_starwars$ npm start

> graphql_starwars@1.0.0 start /home/vagrant/graphql_starwars
> npm run build && node dist/index.js


> graphql_starwars@1.0.0 build /home/vagrant/graphql_starwars
> rimraf dist/ && babel ./ --out-dir dist/ --ignore ./node_modules,./.babelrc,./package.json,./npm-debug.log --copy-files

Successfully compiled 3 files with Babel.
Running a GraphQL API server at localhost:4000/graphql
```

Since we did port forwarding in the [Vagrantfile](playground/Vagrantfile),
we can access VM's port 4000 from host port 4444.
Open a web browser and you will see the GraphiQL UI at http://127.0.0.1:4444/graphql

sample queries and mutations
```
query {
  droid (id: "2001") {
    name
    friends {
      id
      name
    }
  }
}

mutation {
  createReview(episode: JEDI, review: {
    stars: 5
    commentary: "This is a great movie!"
  })
}

mutation {
  createReview(episode: EMPIRE, review: {
    stars: 87
    commentary: "best movie ever! 87 stars, cannot be higher."
  })
}

query {
  review {
    stars
  }
}
```
