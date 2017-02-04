import React from "react";
import {render, findDOMNode} from "react-dom";
import {SelectBox, EditBox, MEditBox, Button, Title, ErrMsg, Hr} from "./feed_component";
import "whatwg-fetch";

class SubmitForm extends React.Component {
  getInitialState() {
    return {
      url: "",
      category: "",
      entry_xpath: "",
      item_title_xpath: "",
      item_link_xpath: "",
      item_content_xpath: "",
      removed_xpath_nodes: ["", ]
    }
  }

  constructor(props) {
    super(props);
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = this.getInitialState();
  }

  submit(e) {
    e.preventDefault();

    let form = this.state;
    if (form["url"] == "" || form["entry_xpath"] == "" ||
        form["item_title_xpath"] == "" || form["item_link_xpath"] == "" ||
        form["item_content_xpath"] == "") {
      this.err.fadeIn("数据不能为空");
      setTimeout(() => {this.err.fadeOut()}, 1000);
    }
    else {
      this.err.fadeIn("正在提交 .....");

      let nodes = form["removed_xpath_nodes"].filter((node) => {node != ""});
      if (nodes.length > 0) {
        form["removed_xpath_nodes"] = JSON.stringify(nodes);
      }
      else {
        delete form["removed_xpath_nodes"];
      }
      let data  = new FormData();
      for (let k in form) {
        if (form[k] != "") {
          data.append(k, form[k]);
        }
      }

      let that = this;
      fetch("/submit/blog", {method: "POST",
                             body: data}
      )
      .then(function(response) {
        return response.json();
      })
      .then(function(r) {
        if (r['err'] == 0) {
          that.err.fadeIn("成功");
          setTimeout(() => {that.err.fadeOut()}, 1000);
          let state = that.getInitialState();
          state["category"] = that.state.category;
          that.setState(state);
        }
        else {
          that.err.fadeIn("失败: " + r["msg"]);
          setTimeout(() => {that.err.fadeOut()}, 1000);
        }
      })
      .catch(function(err) {
        this.err.fadeOut();
      })
    }
    findDOMNode(this.button).blur();
  }

  updateField(k, v) {
    this.setState({[k]: v});
  }

  render() {
    const style = {
      borderWidth: 0,
      padding: 0,
      paddingLeft: "36px"
    };

    return (
      <div>
        <ErrMsg ref={(com) => this.err = com} />
        <form style={style} onSubmit={this.submit}>
          <EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
          <SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
          <EditBox desc="文章Selector:" updateField={this.updateField} type="text" field="entry_xpath" value={this.state.entry_xpath} />
          <EditBox desc="标题Selector:" updateField={this.updateField} type="text" field="item_title_xpath" value={this.state.item_title_xpath} />
          <EditBox desc="链接Selector:" updateField={this.updateField} type="text" field="item_link_xpath" value={this.state.item_link_xpath} />
          <EditBox desc="内容Selector:" updateField={this.updateField} type="text" field="item_content_xpath" value={this.state.item_content_xpath} />
          <MEditBox desc="清除xpath node 数组(选填):" updateField={this.updateField} type="text" field="removed_xpath_nodes" value={this.state.removed_xpath_nodes} />
          <Button ref={(com) => this.button = com} />
        </form>
      </div>
    )
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
        <Title title="添加订阅源(Blog)" />
        <Hr />
        <SubmitForm />
      </div>
    )
  }
}

render(<App />, document.getElementById('content'));
