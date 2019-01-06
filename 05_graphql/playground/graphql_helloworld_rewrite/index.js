import express from 'express';
import graphqlHTTP from 'express-graphql';
import { printSchema } from 'graphql';
import { mySchema } from './schema';


const app = express()
app.get('/graphql', graphqlHTTP({
  schema: mySchema,
  graphiql: true,
}));
app.get('/schema', function(req, res, _next) {
    res.set('Content-Type', 'text/plain');
    res.send(printSchema(mySchema));
});
app.listen(4000, () => {
  console.log('Running a GraphQL API server at localhost:4000/graphql');
  console.log('To see the schema, go to localhost:4000/schema');
});
