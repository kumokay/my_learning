/**
 * In this file, follow the example to construct object types
 *   - define graphql object types according to schema.graphql
 *      - ref: https://graphql.org/graphql-js/constructing-types/
 *   - create graphql schema object in the end
 */

import {
  GraphQLInputObjectType,
  GraphQLList,
  GraphQLNonNull,
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLString,
} from 'graphql';

import {
  createMessage,
  getMessage,
  listMessageIDs,
  updateMessage,
} from './database';

/*
input MessageInput {
  content: String
  author: String
}
*/
const MessageInputType = new GraphQLInputObjectType({
  name: 'MessageInput',
  fields: {
    author: {
      description: 'who is writing this message?',
      type: GraphQLString,
    },
    content: {
      description: 'your message goes here',
      type: GraphQLString,
    },
  },
});

/*
type Message {
  id: ID!
  content: String
  author: String
}
*/
const MessageType = new GraphQLObjectType({
  name: 'Message',
  fields: {
    id: {
      description: 'message id (hex string)',
      type: new GraphQLNonNull(GraphQLString),
    },
    author: {
      description: 'masked username',
      type: GraphQLString,
      resolve: root => root.author.substring(0, 2) + '*****'
    },
    content: {
      description: 'all content',
      type: GraphQLString,
    },
  },
});

/*
type Query {
  getMessage(id: ID!): Message
  listMessageIDs: [ID]
}
*/
const QueryType = new GraphQLObjectType({
  name: 'Query',
  fields: {
    getMessage: {
      description: 'your message goes here',
      type: MessageType,
      args: {
        id: {
          type: new GraphQLNonNull(GraphQLString),
        },
      },
      resolve: (_, { id }) => getMessage(id),
    },
    listMessageIDs: {
      description: 'list all message IDs in the database',
      type: new GraphQLList(GraphQLString),
      resolve: () => listMessageIDs(),
    },
  },
});

/*
type Mutation {
  createMessage(input: MessageInput): Message
  updateMessage(id: ID!, input: MessageInput): Message
}
*/
const MutationType = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    createMessage: {
      description: 'create a new message',
      type: MessageType,
      args: {
        input: {
          type: MessageInputType,
        },
      },
      resolve: (_, { input }) => createMessage(input),
    },
    updateMessage: {
      description: 'update a message',
      type: MessageType,
      args: {
        id: {
          type: new GraphQLNonNull(GraphQLString),
        },
        input: {
          type: MessageInputType,
        },
      },
      resolve: (_, { id, input }) => updateMessage(id, input),
    },
  },
});

/*
Construct the schema
*/
export const mySchema = new GraphQLSchema({
  query: QueryType,
  mutation: MutationType,
});
