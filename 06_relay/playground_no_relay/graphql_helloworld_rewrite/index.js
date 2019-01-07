import express from 'express';
import graphqlHTTP from 'express-graphql';
import { printSchema } from 'graphql';
import { mySchema } from './schema';


const app = express()

// add these to enable Cross Origin Resource Sharing
// reference: https://enable-cors.org/server_expressjs.html
// https://github.com/graphql/express-graphql/issues/14#issuecomment-298489529
app.use('/graphql', function (req, res, next) {
  res.header('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

app.use('/graphql', graphqlHTTP({
  schema: mySchema,
  graphiql: false,
  pretty: true,
}));

app.use('/schema', function(req, res, _next) {
    res.set('Content-Type', 'text/plain');
    res.send(printSchema(mySchema));
});

app.listen(4000, () => {
  console.log('Running a GraphQL API server at localhost:4000/graphql');
  console.log('To see the schema, go to localhost:4000/schema');
});
