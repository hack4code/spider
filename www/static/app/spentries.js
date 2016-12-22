import React from "react";
import { render } from "react-dom";
import {Title, Hr, Entries} from "./entry_component";

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
    var cn;
    var style;

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
    var style = {
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
    var spid = $("#content").attr("spid");
    var name = $("#content").attr("name");
    this.state = {spid: spid, name: name, entries: []};
  }

  getEntries(aid, q) {
    var spid = this.state.spid;
    var args = {spid: spid};
    if (aid != null) {
      args['aid'] = aid;
      args['q'] = q;
    }

    $.getJSON("/api/spider", args).done(function(data){
      var err = data["err"];
      if (!err) {
        this.setState({entries: data["entries"]});
      }
    }.bind(this));
  }

  onLeftClick() {
    var entries = this.state.entries;
    if (entries.length == 0) {
      return;
    }
    var aid = entries[0][0];
    this.getEntries(aid, "p");
  }

  onRightClick() {
    var entries = this.state.entries;
    if (entries.length == 0) {
      return;
    }
    var aid = entries[entries.length-1][0];
    this.getEntries(aid, "n");
  }

  componentDidMount() {
    this.getEntries();
  }

  render() {
    return (
      <div>
        <Title name={this.state.name} />
        <Hr />
        <Entries prefix="/a/" entries={this.state.entries} />
        <Hr />
        <AidLinkDiv onLeftClick={this.onLeftClick} onRightClick={this.onRightClick} />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
