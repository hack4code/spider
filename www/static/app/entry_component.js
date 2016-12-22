import React from "react";

class Hr extends React.Component {
  render() {
    var style = {
      border: "none",
      height: 1,
      color: "#EEE",
      backgroundColor: "#EEE",
      marginBottom: "1em",
      clear: "both"
    };

    return (
      <hr style={style} />
    )
  }
}

class Title extends React.Component {
  render() {
    var style = {
      fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
      fontSize: "normal",
      fontWeight: "bold",
      textAlign: "center"
    };

    return (
      <div>
        <p style={style}>{this.props.name}</p>
      </div>
    )
  }
}

class Entry extends React.Component {
  render() {
    var style = {
      fontWeight: "600",
      fontSize: "0.8em",
      fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
      lineHeight: "2em",
      textDecoration: "none"
    };
    var url = this.props.url;

    return (
      <li>
        <a style={style} href={url} target="_blank">{this.props.title}</a>
      </li>
    )
  }
}

class Entries extends React.Component {
  static defaultProps = {
    prefix: "",
    entries: []
  };

  render() {
    var style = {
      listStyle: "square",
      color: "red",
      marginLeft: "4em"
    };
    var prefix = this.props.prefix;
    var entries = this.props.entries;

    return (
      <ul style={style}>
        {entries.map(function(entry, index) {return <Entry key={index} url={prefix + entry[0]} title={entry[1]} />;})}
      </ul>
    )
  }
}


export {Title, Hr, Entries};
