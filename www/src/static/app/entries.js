require("whatwg-fetch");

var React = require("react");
var ReactDOM = require("react-dom");
var EntryComponent = require("./entry_component");


class AidLink extends React.Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();

    this.props.onAidClick();
  }

  render() {
    let cn = "";
    let style = {};

    if (this.props.handType == "handright") {
      cn = "fa fa-hand-o-right";
      style = {
        float: "right"
      }
    }
    else {
      cn = "fa fa-hand-o-left";
      style = {
        float: "left"
      }
    }

    return (
      <span style={style}>
        <a href="#" onClick={this.onClick}>
          <i className={cn} aria-hidden="true"></i>
        </a>
      </span>
    )
  }
}

class AidLinkDiv extends React.Component {
  render() {
    const style = {
      paddingLeft: "40%",
      paddingRight: "40%"
    };

    return (
      <div style={style}>
        <AidLink handType="handleft" onAidClick={this.props.onLeftClick} />
        <AidLink handType="handright" onAidClick={this.props.onRightClick} />
      </div>
    )
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.getEntries = this.getEntries.bind(this);
    this.onLeftClick = this.onLeftClick.bind(this);
    this.onRightClick = this.onRightClick.bind(this);
    let node = document.getElementById("content");
    let spid = node.getAttribute("spid");
    let name = node.getAttribute("name");
    this.state = {spid: spid, name: name, entries: []};
  }

  getEntries(aid, q) {
    let url = new URL(window.location.protocol + "//" + window.location.hostname + "/api/entries");
    let params = {spid: this.state.spid};
    if (aid != null) {
      params["aid"] = aid;
      params["q"] = q;
    }
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    let that = this;

    fetch(url)
    .then(function(response) {
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

  onLeftClick() {
    let entries = this.state.entries;
    if (entries.length == 0) {
      return;
    }
    let aid = entries[0][0];
    this.getEntries(aid, "p");
  }

  onRightClick() {
    let entries = this.state.entries;
    if (entries.length == 0) {
      return;
    }
    let aid = entries[entries.length-1][0];
    this.getEntries(aid, "n");
  }

  componentDidMount() {
    this.getEntries();
  }

  render() {
    return (
      <div>
        <EntryComponent.Title name={this.state.name} />
        <EntryComponent.Hr />
        <EntryComponent.ArticleEntries prefix="/a/" entries={this.state.entries} />
        <EntryComponent.Hr />
        <AidLinkDiv onLeftClick={this.onLeftClick} onRightClick={this.onRightClick} />
      </div>
    )
  }
}

const node = document.getElementById("content");
const root = ReactDOM.createRoot(node);
root.render(<App />);
