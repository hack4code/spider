import React from "react";


class Hr extends React.Component {
  render() {
    const style = {
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
    const style = {
      fontFamily: "MiSans",
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
    const style = {
      fontWeight: "600",
      fontSize: "0.8em",
      fontFamily: "MiSans",
      lineHeight: "2em",
      textDecoration: "none"
    };
    let url = this.props.url;

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
    const style = {
      listStyle: "square",
      color: "red",
      marginLeft: "4em"
    };
    let prefix = this.props.prefix;
    let entries = this.props.entries;

    return (
      <ul style={style}>
        {entries.map(function(entry, index) {return <Entry key={index} url={prefix + entry[0]} title={entry[1]} />;})}
      </ul>
    )
  }
}

class SpiderButton extends React.Component {
  render () {
    const style = {
      fontWeight: "600",
      fontSize: "0.8em",
      fontFamily: "MiSans",
      textDecoration: "none",
      backgroundColor: "#EEEEEE",
      border: "1px solid #CCCCCC",
      borderRadius: "4px",
      padding: "2px 4px",
      marginLeft: "8px"
    };
    return (
      <a style={style} href={this.props.href} target="_blank">
        Edit
      </a>
    )
  }
}

class SpiderLink extends React.Component {
  render() {
    const style = {
      fontWeight: "600",
      fontSize: "0.8em",
      fontFamily: "MiSans",
      lineHeight: "2em",
      textDecoration: "none"
    };

    return (
      <a style={style} href={this.props.href} target="_blank">
        {this.props.title}
      </a>
    )
  }
}

class SpiderEntry extends React.Component {
  render() {
    const spider = this.props.spider;

    return (
      <li>
        <SpiderLink href={"/p/" + spider["id"]} title={spider["title"]} />
        <SpiderButton href={"/feed/" + spider["type"] + "/" + spider["id"]} />
      </li>
    )
  }
}

class SpiderEntries extends React.Component {
  static defaultProps = {
    spiders: []
  };

  render() {
    const style = {
      listStyle: "square",
      color: "red",
      marginLeft: "4em"
    };
    const spiders = this.props.spiders;

    return (
      <ul style={style}>
        {spiders.map(function(item, index) {return <SpiderEntry spider={item} />;})}
      </ul>
    )
  }
}


export {Title, Hr, SpiderEntries, Entries};
