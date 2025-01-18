import React from "react";
import { createRoot } from 'react-dom/client';
import {Title, Hr, SpiderEntries} from "./entry_component";
import "whatwg-fetch";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {spiders: []};
  }

  componentDidMount() {
    let that = this;
    fetch("/api/spiders").then(function(response) {
      response.json().then(function(data) {
        if (response.status == 200) {
          that.setState({"spiders": data});
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
        <Title name="所有订阅" />
        <Hr />
        <SpiderEntries spiders={this.state.spiders} />
        <Hr />
      </div>
    )
  }
}

const node = document.getElementById("content");
const root = createRoot(node);
root.render(<App />);
