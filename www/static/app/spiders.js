import React from "react";
import { render } from "react-dom";
import {Title, Hr, Entries} from "./entry_component";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {entries: []};
  }

  componentDidMount() {
    $.getJSON("/api/spiders").done(function(data){
      var err = data["err"];
      if (!err) {
        this.setState({entries: data["entries"]});
      }
    }.bind(this))
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
