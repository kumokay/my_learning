import { randomBytes } from 'crypto'

var fakeDatabase = {
  "testid": {
    "author": "testuser",
    "content": "this is a test msg"
  }
};

export type MessageEntry = {
  author: string,
  content: string,
};

export type Message = {
  id: string,
} & MessageEntry;

export function createMessage(input: MessageEntry): Message {
  // Create a random id for our "database".
  var id = randomBytes(10).toString('hex');
  fakeDatabase[id] = input;
  return {
    id: id,
    author: input.author,
    content: input.content,
  };
}

export function getMessage(id: string): Message {
  if (!fakeDatabase[id]) {
    throw new Error('no message exists with id ' + id);
  }
  var msg_entry = fakeDatabase[id];
  return {
    id: id,
    author: msg_entry.author,
    content: msg_entry.content,
  };
}

export function listMessageIDs (): Array<string> {
  return Object.keys(fakeDatabase);
}

export function updateMessage(id: string, input: MessageEntry): Message {
  if (!fakeDatabase[id]) {
    throw new Error('no message exists with id ' + id);
  }
  // This replaces all old data, but some apps might want partial update.
  fakeDatabase[id] = input;
  return {
    id: id,
    author: input.author,
    content: input.content,
  };
}
