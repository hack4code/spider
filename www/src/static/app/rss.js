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
      };
  }

  constructor(props) {
    super(props);
    this.err = null;
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = this.getInitialState();
  }

  componentDidMount() {
    const href = window.location.href;
    const spid = href.split("/").slice(-1)
    if ((spid == "rss") || (spid == "xml")) {
      return;
    }

    let that = this;
    let url = new URL(window.location.protocol + "//" + window.location.hostname + "/api/spider");
    let params = {spid: spid};
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    fetch(url).then(function(response) {
      response.json().then(function(data) {
        if (response.status == 200) {
          that.setState({
            category: data["category"],
            url: data["start_urls"][0],
            item_content_xpath: data["item_content_xpath"],
            removed_xpath_nodes: data["removed_xpath_nodes"]
          });
        }
        else {
          console.log(data['message']);
        }
     });
   });
  }

  submit(e) {
    e.preventDefault();

    let feed = {}
    for (let key in this.state) {
      if (this.state[key].length > 0) {
        feed[key] = this.state[key];
      }
    }
    if (feed["url"] == null || feed["url"] == "") {
      this.err.fadeIn("需要网址数据");
      setTimeout(() => {this.err.fadeOut()}, 800);
    }
    else {
      this.err.fadeIn("正在提交 .....");

      let nodes = feed["removed_xpath_nodes"].filter((e) => {return e != "";});
      if (nodes.length == 0) {
         delete feed["removed_xpath_nodes"];
      }

      let that = this;
      fetch("/submit/rss", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(feed)
      })
      .then(function(response) {
        response.json().then(function(data) {
          if (response.status == 200) {
            that.err.fadeIn("成功");
            setTimeout(() => {that.err.fadeOut()}, 800);
            let state = that.getInitialState();
            state["category"] = that.state.category;
            that.setState(state);
          }
          else {
            that.err.fadeIn("失败: " + data["message"]);
            setTimeout(() => {that.err.fadeOut()}, 800);
          }
        })
      })
      .catch(function(err) {
        that.err.fadeIn("异常: fetch exception");
        setTimeout(() => {that.err.fadeOut()}, 800);
      })
    }
    findDOMNode(this.refs.Button).blur();
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
          <Button ref="Button"/>
        </form>
      </div>
    )
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
        <Title title="订阅源(rss|atom)" />
        <Hr />
        <SubmitForm />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
