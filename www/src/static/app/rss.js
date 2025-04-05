import React, { createRef } from "react";
import {createRoot} from 'react-dom/client';
import {TextBox, SelectBox, EditBox, MEditBox, Button, Title, ErrMsg, Hr} from "./feed_component";
import "whatwg-fetch";

class SubmitForm extends React.Component {

    getInitialState() {
        return {
            category: "",
            url: "",
            item_content_xpath: "",
            removed_xpath_nodes: ["",],
            css: ""
        };
    }

    constructor(props) {
        super(props);
        this.err = null;
        this.submit = this.submit.bind(this);
        this.updateField = this.updateField.bind(this);
        this.state = this.getInitialState();
        this.buttonRef = createRef();
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
                    });

                    if (("item_content_xpath" in data) && data["item_content_xpath"]) {
                        that.setState({
                            item_content_xpath: data["item_content_xpath"]
                        });
                    };

                    if (("removed_xpath_nodes" in data) && data["removed_xpath_nodes"]) {
                        that.setState({
                            removed_xpath_nodes: data["removed_xpath_nodes"]
                        });
                    };

                    if (("css" in data) && data["css"]) {
                        that.setState({
                            css: data["css"]
                        });
                    };
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

            let item_content_xpath = feed["item_content_xpath"];
            if (!item_content_xpath) {
                delete feed["item_content_xpath"];
            }

            let nodes = feed["removed_xpath_nodes"]
            if (!nodes) {
                delete feed["removed_xpath_nodes"];
            }
            let css = feed["css"];
            if (!css) {
                delete feed["css"]
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
        this.buttonRef.current.blur();
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
            <TextBox desc="CSS:(选填):" updateField={this.updateField} type="text" field="css" value={this.state.css} />
            <Button ref={this.buttonRef}/>
            </form>
            </div>
        )
    }
}

class App extends React.Component {
    render() {
        return (
            <div>
            <Title title="源(rss|atom)" />
            <Hr />
            <SubmitForm />
            </div>
        )
    }
}

const node = document.getElementById("content");
const root = createRoot(node);
root.render(<App />);


/* vim: set ts=4 sw=4 sts=4 ft=javascript et: */
