import React from "react";
import { render } from "react-dom";
import {Title, Hr, Entries} from "./entry_component";
import "whatwg-fetch";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {entries: []};
  }

  componentDidMount() {
    let that = this;
    fetch("/api/spiders").then(function(response) {
      response.json().then(function(data) {
        if (response.status == 200) {
          that.setState({entries: data["entries"]});
        }
        else {
          console.log(data['message']);
        }
      })
    })
    .catch(function(err) {
      console.log("fetch error");
    })
  }

  render() {
    return (
      <div>
        <Title name="所有订阅网站" />
        <Hr />
        <Entries prefix="/p/" entries={this.state.entries} />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
