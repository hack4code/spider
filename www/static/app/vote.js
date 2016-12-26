import React from "react";
import { render } from "react-dom";
import "whatwg-fetch";

class Voter extends React.Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
    let s = window.localStorage;
    let aid = this.props.aid;
    if (s.getItem(aid) != null) {
      this.state =  {voted: 1};
    }
    else {
      this.state = {voted: 0};
    }
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();

    let s = window.localStorage;
    let aid = this.props.aid;

    if (s.getItem(aid) != null) {
      return;
    }
    else {
      this.setState({voted: 1});

      let form = new FormData();
      form.append("aid", aid);
      let that = this;
      fetch("/api/vote", {method: "POST",
                          credentials: "same-origin",
                          body: form}
      )
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        console.log(data);
        if (!data["err"]) {
          s.setItem(aid, 1);
        }
        else {
          that.setState({voted: 0});
        }
      })
      .catch(function(err) {
      })
    }
  }

  render() {
    let style = {
      fontSize: "1em",
      fontWeight: "bold"
    };
    style["color"] = this.state.voted ? "#004276" : "#999999";

    return (
      <div>
        <a style={style} href="#" onClick={this.onClick}>
          <i className="fa fa-thumbs-o-up"></i>
        </a>
      </div>
    )
  }
}

class Footer extends React.Component {
  render() {
    const style = {
      color: "#888",
      fontSize: "x-small",
    };
    let url = "/p/" + this.props.spid;

    return (
      <p style={style}>
        本文章来自
        <span>[<a href={url} target="_blank">{this.props.spname}</a>]</span>
        , 您可以对文章点赞
      </p>
    )
  }
}

class App extends React.Component {
  render() {
    const style = {
      display: "flex",
      flexDirection: "column",
      alignItems: "center"
    };

    let node = document.getElementById("content");
    let aid = node.getAttribute("aid");
    let spid = node.getAttribute("spid");
    let spname = node.getAttribute("spname");
    return (
      <div style={style}>
        <Voter aid={aid} />
        <Footer spid={spid} spname={spname} />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
