require("whatwg-fetch");

var React = require("react");
var ReactDOM = require("react-dom/client");
var EntryComponent = require("./entry_component");


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
        <EntryComponent.Title name="所有订阅" />
        <EntryComponent.Hr />
        <EntryComponent.SpiderEntries spiders={this.state.spiders} />
        <EntryComponent.Hr />
      </div>
    )
  }
}

const node = document.getElementById("content");
const root = ReactDOM.createRoot(node);
root.render(<App />);
