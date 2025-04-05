import React from "react";
import "whatwg-fetch";

class Title extends React.Component {
  render() {
    const style = {
      fontFamily: "MiSans, sans-serif",
      fontSize: "1.6em",
      fontWeight: "normal",
      textAlign: "center"
    };

    return (
      <div>
        <p style={style}>{this.props.title}</p>
      </div>
    )
  }
}

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

class ErrMsg extends React.Component {
  constructor(props) {
    super(props);
    this.fadeIn = this.fadeIn.bind(this);
    this.fadeOut = this.fadeOut.bind(this);
    this.state = {show: false, message: ""};
  }

  fadeIn(msg) {
    this.setState({show: true, message: msg});
  }

  fadeOut() {
    this.setState({show: false});
  }

  render() {
    const style = {
        textAlign: "center",
        fontSize: "0.5em",
        marginBottom: "1em",
        color: "#aaa",
    };

    if (this.state.show) {
      return (
        <div style={style}>{this.state.message}</div>
      )
    }
    else {
      return null;
    }
  }
}

class Input extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    let v = e.target.value;
    this.props.updateField(this.props.field, v);
  }

  render() {
    const style = {
      backgroundColor: "transparent",
      border: "0.1rem solid #d1d1d1",
      borderRadius: "1px",
      boxShadow: "none",
      boxSizing: "border-box",
      height: "3.2em",
      width: "42em",
      margin: "0em 0em 1.2em 0em",
    };

    return (
      <input style={style} value={this.props.value} onChange={this.handleChange} type={this.props.type}/>
    )
  }
}

class IButton extends React.Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
  }

  onClick(e) {
    this.props.onClick(e);
  }

  render() {
    const style = {
      backgroundColor: "transparent",
      border: "0rem",
      borderRadius: "0.4rem",
      boxSizing: "borderBox",
      cursor: "pointer",
      display: "inlineBlock",
      fontSize: "0.4rem",
      fontWeight: "700",
      height: "3.2em",
      width: "1em",
      textAlign: "center",
      textDecoration: "none",
      whiteSpace: "nowrap",
      display: this.props.show ? "inline" : "none"
    };

    return (
      <button style={style} type="button" onClick={this.onClick}>+</button>
    )
  }
}

class Label extends React.Component {
  render() {
    const style = {
      fontFamily: "MiSans, sans-serif",
      fontSize: "1.0em",
      fontWeight: "normal",
      marginBottom: "0.5em",
      display: "block"
    };

    return (
      <label style={style}>{this.props.desc}</label>
    )
  }
}

class EditBox extends React.Component {
  render() {
    return (
      <div>
        <Label desc={this.props.desc} />
        <Input type={this.props.type} updateField={this.props.updateField} field={this.props.field} value={this.props.value} />
      </div>
    )
  }
}

class MEditBox extends React.Component {
  constructor(props) {
    super(props);
    this.addField = this.addField.bind(this);
    this.updateValues = this.updateValues.bind(this);
  }

  addField(e) {
    e.preventDefault();
    e.stopPropagation();

    let arr = this.props.value;
    arr.length = arr.length + 1;
    arr[arr.length-1] = "";
    this.props.updateField(this.props.field, arr);
  }

  updateValues(index, v) {
    let arr = this.props.value;
    arr[index] = v;
    this.props.updateField(this.props.field, arr);
  }

  render() {
    const style = {
      display: "inlineBlock",
    };
    let arr = this.props.value;
    let n = arr.length;
    let type = this.props.type;
    let updateValues = this.updateValues;
    let onClick = this.addField;

    return (
      <div>
        <Label desc={this.props.desc} />
        {
          arr.map(function(value, index) {
            return (
            <div key={index.toString()} style={style}>
              <Input type={type} updateField={updateValues} field={index} value={value} />
              <IButton show={index == n-1} onClick={onClick} />
            </div>
            )
          })
        }
      </div>
    )
  }
}
class Select extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = {list: []};
  }

  componentDidMount() {
    let that = this;

    fetch(this.props.url)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      let err = data["err"];
      if (!err) {
        let list = data["data"];
        that.setState({list: list});
      }
    })
    .catch(function(err) {
      console.log("get items list failed");
    })
  }

  handleChange(e) {
    let val = e.target.value;
    this.props.updateField(this.props.field, val);
  }

  render() {
    const style = {
      backgroundColor: "transparent",
      border: "0.1rem solid #d1d1d1",
      borderRadius: "1px",
      boxShadow: "none",
      boxSizing: "border-box",
      height: "3.2em",
      width: "42em",
      margin: "0em 0em 1.2em 0em",
      display: "block"
    };
    let list = this.state.list;

    return (
      <div>
        <input list="options" name="options" value={this.props.value} style={style} onChange={this.handleChange} />
        <datalist id="options">
        {
          list.map(function(val, index) {return <option value={val} key={index}/>;})
        }
        </datalist>
      </div>
    )
  }
}

class SelectBox extends React.Component {
  render() {
    return (
      <div>
        <Label desc={this.props.desc} />
        <Select updateField={this.props.updateField} value={this.props.value} url={this.props.url} field={this.props.field} />
      </div>
    )
  }
}

class TextArea extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    let v = e.target.value;
    this.props.updateField(this.props.field, v);
  }

  render() {
    const style = {
      backgroundColor: "transparent",
      border: "0.1rem solid #d1d1d1",
      borderRadius: "4px",
      boxSizing: "border-box",
      width: "47em",
      margin: "0em 0em 1.2em 0em"
    };

    return (
      <textarea style={style} rows="16" value={this.props.value} onChange={this.handleChange} field={this.props.field} ></textarea>
    )
  }
}

class TextBox extends React.Component {
  render() {
    return (
      <div>
        <Label desc={this.props.desc} />
        <TextArea updateField={this.props.updateField} value={this.props.value} field={this.props.field} />
      </div>
    )
  }
}

class Button extends React.Component {
  render() {
    const style = {
      backgroundColor: "transparent",
      border: "0.1rem solid #d1d1d1",
      borderRadius: "0.4rem",
      boxSizing: "borderBox",
      cursor: "pointer",
      display: "inlineBlock",
      fontSize: "0.4rem",
      fontWeight: "700",
      height: "3.2em",
      letterSpacing: "0.3em",
      textAlign: "center",
      textDecoration: "none",
      textTransform: "uppercase",
      whiteSpace: "nowrap"
    };

    return (
      <input style={style} type="submit" value="提交" />
    )
  }
}

export {TextBox, SelectBox, EditBox, MEditBox, Button, Title, ErrMsg, Hr};
