var express = require('express');
var graphqlHTTP = require('express-graphql');
var { buildSchema } = require('graphql');
var { StarWarsSchema } = require('./starWarsSchema');

var app = express();
app.use('/graphql', graphqlHTTP({
  schema: StarWarsSchema,
  graphiql: true,
}));
app.use('/schema', function(req, res, _next) {
    var printSchema = require('graphql/utilities/schemaPrinter').printSchema;
    res.set('Content-Type', 'text/plain');
    res.send(printSchema(StarWarsSchema));
});
app.listen(4000, () => {
  console.log('Running a GraphQL API server at localhost:4000/graphql');
});
