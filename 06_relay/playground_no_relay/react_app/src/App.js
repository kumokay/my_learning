import React, { Component } from 'react';
import './App.css';


function doGraphQLQuery(query_str) {
  var url = 'http://localhost:4000/graphql';
  return fetch(
    url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query_str, //.replace(/\s+/g, ''),
      }),
    }
  ).then(response => {
    console.log(response);
    return response.json();
  })
}


class MessageInputForm extends React.Component {
  constructor(props) {
    super(props);
    this.actionCompleteHandler = (
      props.actionCompleteHandler ? props.actionCompleteHandler : (json) => {
        console.log(JSON.stringify(json.data, null, 2));
      });
    this.state = {
      msgId: props.msgId,
      author: props.author ? props.author : '',
      content: props.content ? props.content : '',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const name = event.target.name;
    this.setState({
      [name]: event.target.value,
    });
  }

  handleSubmit(event) {
    const query_str = (this.state.msgId) ? (
      `mutation {
        updateMessage(id: "${this.state.msgId}", input: {
          author: "${this.state.author}",
          content: "${this.state.content}",
        }) {
          id
        }
      }`
    ) : (`
      mutation {
        createMessage(input: {
          author: "${this.state.author}",
          content: "${this.state.content}",
        }) {
          id
        }
      }
    `);
    const json = doGraphQLQuery(query_str).then(json => {
      console.log(JSON.stringify(json, null, 2));
      return json;
    });
    this.actionCompleteHandler(json);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        author:
        <input name="author" type="text" value={this.state.author} onChange={this.handleChange} />
        message:
        <textarea name="content" type="text" value={this.state.content} onChange={this.handleChange} />
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

class MessageEntry extends React.Component {
  constructor(props) {
    super(props);
    this.msgId = props.msgId;
    this.state = {
      isContentVisible: false,
      isEditOn: false,
      author: '',
      content: '',
    };
    // This binding is necessary to make `this` work in the callback
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleContentClick = this.handleContentClick.bind(this);
    this.handleSubmitted = this.handleSubmitted.bind(this);
  }
  updateContent() {
    var query_str = `
      query {
        getMessage(id: "${ this.msgId }") {
          author
          content
        }
      }
    `;
    return doGraphQLQuery(query_str).then(json => {
      console.log(JSON.stringify(json, null, 2));
      console.log(json.data.getMessage.author)
      this.setState({
        author: json.data.getMessage.author,
        content: json.data.getMessage.content,
      });
    });
  }
  handleButtonClick() {
    if (!this.state.isContentVisible)
      this.updateContent();
    this.setState(state => ({
      isContentVisible: !state.isContentVisible
    }));
  }
  handleSubmitted(json) {
    // trigger content display if isContentVisible
    console.log(JSON.stringify(json, null, 2));
    this.setState({
      isEditOn: false,
      isContentVisible: false,
    });
  }
  handleContentClick() {
    this.setState(state => ({
      isEditOn: !state.isEditOn
    }));
  }
  render() {
    if (!this.state.isContentVisible) {
      return (
        <button onClick={ this.handleButtonClick }>
          { this.msgId }
        </button>);
    }
    else if (!this.state.isEditOn) {
      return (
        <div>
          <button onClick={ this.handleButtonClick }>
            { this.msgId }
          </button>
          <span onDoubleClick={ this.handleContentClick }>
            <p>{this.state.author} says: {this.state.content}</p>
          </span>
        </div>);
    } else {
      return (
        <div>
          <button onClick={ this.handleButtonClick }>
            { this.msgId }
          </button>
          <MessageInputForm
            actionCompleteHandler={this.handleSubmitted}
            msgId={this.msgId}
            author={this.state.author}
            content={this.state.content} />
        </div>);
    }
  }
}


class QueryUI extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      msgList: [],
    };

    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    var query_str = `
      query {
        listMessageIDs
      }
    `;
    doGraphQLQuery(query_str).then(json => {
      this.setState({
        msgList: json.data.listMessageIDs,
      });
    })
  }

  render() {
    const listItems = this.state.msgList.map((msgId) =>
      <li key={msgId.toString()}>
        <MessageEntry msgId={ msgId } />
      </li>
    );
    return (
      <div>
        <button onClick={ this.handleClick }>
          get message list
        </button>
        <ul>{ listItems }</ul>
      </div>
    );
  }
}


class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
        </header>
        <div className="App-panel">
          <MessageInputForm />
          <QueryUI />
        </div>
      </div>
    );
  }
}

export default App;
