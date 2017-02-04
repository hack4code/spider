import React from "react";
import {render, findDOMNode } from "react-dom";
import {SelectBox, EditBox, MEditBox, Button, Title, ErrMsg, Hr} from "./feed_component";
import "whatwg-fetch";

class SubmitForm extends React.Component {
  getInitialState() {
    return {
      category: "",
      url: "",
      item_content_xpath: "",
      removed_xpath_nodes: ["",]
    }
  }

  constructor(props) {
    super(props);
    this.err = null;
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = this.getInitialState();
  }

  submit(e) {
    e.preventDefault();

    let form = {}
    for (let k in this.state) {
      if (this.state[k].length > 0) {
        form[k] = this.state[k];
      }
    }
    if (form["url"] == null || form["url"] == "") {
      this.err.fadeIn("需要网址数据");
      setTimeout(() => {this.err.fadeOut()}, 800);
    }
    else {
      this.err.fadeIn("正在提交 .....");

      let nodes = form["removed_xpath_nodes"].filter((node) => {node != ""});
      if (nodes.length > 0) {
        form["removed_xpath_nodes"] = JSON.stringify(nodes);
      }
      else {
        delete from["removed_xpath_nodes"];
      }
      let data  = new FormData();
      for (let k in form) {
        data.append(k, form[k]);
      }

      let that = this;
      fetch("/submit/rss", {method: "post",
                            body: data}
      )
      .then(function(response) {
        return response.json();
      })
      .then(function(r) {
        if (r['err'] == 0) {
          that.err.fadeIn("成功");
          setTimeout(() => {that.err.fadeOut()}, 800);
          let state = that.getInitialState();
          state["category"] = that.state.category;
          that.setState(state);
        }
        else {
          that.err.fadeIn("失败: " + r["msg"]);
          setTimeout(() => {that.err.fadeOut()}, 800);
        }
      })
      .catch(function(err) {
        console.log("Error in fetch post function");
      })
    }

    findDOMNode(this.refs.Submit).blur();
  }

  updateField(k, v) {
    this.setState({[k]: v});
  }

  render() {
    const style = {
      borderWidth: 0,
      paddingLeft: "36px"
    };

    return (
      <div>
        <ErrMsg ref={(com) => this.err = com} />
        <form onSubmit={this.submit} style={style}>
          <EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
          <SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
          <EditBox desc="内容selector[用于非全文输出的feed](选填):" updateField={this.updateField} type="text" field="item_content_xpath" value={this.state.item_content_xpath} />
          <MEditBox desc="清除xpath node 数组(选填):" updateField={this.updateField} type="text" field="removed_xpath_nodes" value={this.state.removed_xpath_nodes} />
          <Button ref="Submit"/>
        </form>
      </div>
    )
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
        <Title title="添加订阅源(rss|atom)" />
        <Hr />
        <SubmitForm />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
