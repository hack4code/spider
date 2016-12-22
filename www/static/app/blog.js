import React from "react";
import {render, findDOMNode} from "react-dom";
import {SelectBox, EditBox, Button, Title, ErrMsg, Hr} from "./feed_component";

class SubmitForm extends React.Component {
  constructor(props) {
    super(props);
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = {category: "",
                  url: "",
                  entry: "",
                  item_title: "",
                  item_link: "",
                  item_content: "",
                  removed_xpath_nodes: ""}
  }

  submit(e) {
    e.preventDefault();

    var form = this.state;
    if (form["url"] == "" || form["entry"] == "" || form["item_title"] == "" || form["item_link"] == "" || form["item_content"] == "") {
      $("span").text("数据不能为空").show().fadeOut(2000);
    }
    else {
      $("span").text("正在提交 .....").show();
      $.ajax({type: "post",
              url: "/api/feed/blog",
              data: form,
              success: function(r){
                 if (r['err'] == 0) {
                  this.setState({url: "",
                                 entry:"",
                                 item_title: "",
                                 item_link: "",
                                 item_content: "",
                                 removed_xpath_nodes: ""
                                 });
                  $("span").text("成功").show().fadeOut(1500);
                 }
                else {
                  $("span").text("失败: " + r["msg"]).show().fadeOut(1500);
                }
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
      padding: 0,
      paddingLeft: "36px"
    };

    return (
      <div>
        <ErrMsg />
        <form style={style} onSubmit={this.submit}>
          <EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
          <SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
          <EditBox desc="文章Selector:" updateField={this.updateField} type="text" field="entry" value={this.state.entry} />
          <EditBox desc="标题Selector:" updateField={this.updateField} type="text" field="item_title" value={this.state.item_title} />
          <EditBox desc="链接Selector:" updateField={this.updateField} type="text" field="item_link" value={this.state.item_link} />
          <EditBox desc="内容Selector:" updateField={this.updateField} type="text" field="item_content" value={this.state.item_content} />
          <EditBox desc="清除xpath node 数组(选填):" updateField={this.updateField} type="text" field="removed_xpath_nodes" value={this.state.removed_xpath_nodes} />
          <Button ref="Submit" />
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
