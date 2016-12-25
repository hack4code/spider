import React from "react";
import { render } from "react-dom";
import {Title, Hr, Entries} from "./entry_component";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {entries: []};
  }

  componentDidMount() {
    let that = this;
    fetch("/api/spiders").then(function(response) {
    	return response.json();
    })
    .then(function(data) {
      let err = data["err"];
      if (!err) {
        that.setState({entries: data["entries"]});
      }
    })
    .catch(function(err) {
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
