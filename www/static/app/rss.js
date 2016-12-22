import React from "react";
import {render, findDOMNode } from "react-dom";
import {SelectBox, EditBox, Button, Title, ErrMsg, Hr} from "./feed_component";

class SubmitForm extends React.Component {
  constructor(props) {
    super(props);
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = {category: "",
                  url: "",
                  item_content_xpath: "",
                  removed_xpath_nodes: ""}
  }

  submit(e) {
    e.preventDefault();

    var form = {}
    for (var k in this.state) {
      if (this.state[k].length > 0) {
        form[k] = this.state[k];
      }
    }

    if (form["url"] == "") {
      $("span").text("需要网址数据").show().fadeOut(1500);
    }
    else {
      $("span").text("正在提交 .....").show();
      $.ajax({type: "post",
              url: "/api/feed/rss",
              data: form,
              success: function(r){
                 if (r['err'] == 0) {
                  $("span").text("成功").show().fadeOut(1500);
                 }
                else {
                  $("span").text("失败: " + r["msg"]).show().fadeOut(1500);
                }
                this.setState({url: "", content: ""});
              }.bind(this)}
      );
    }
    findDOMNode(this.refs.Submit).blur();
  }

  updateField(k, v) {
    this.setState({[k]: v});
  }

  render() {
    var style = {
      borderWidth: 0,
      paddingLeft: "36px"
    };

    return (
      <div>
        <ErrMsg />
        <form onSubmit={this.submit} style={style}>
          <EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
          <SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
          <EditBox desc="内容selector[用于非全文输出的feed](选填):" updateField={this.updateField} type="text" field="item_content_xpath" value={this.state.content} />
          <EditBox desc="清除xpath node 数组(选填):" updateField={this.updateField} type="text" field="removed_xpath_nodes" value={this.state.removed_xpath_nodes} />
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

render(<App />, document.getElementById('content'));
