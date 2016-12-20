/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	"use strict";

	function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

	var Title = React.createClass({
		displayName: "Title",

		render: function render() {
			var style = {
				fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
				fontSize: "1.6em",
				fontWeight: "normal",
				textAlign: "center"
			};

			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					{ style: style },
					this.props.title
				)
			);
		}
	});

	var Hr = React.createClass({
		displayName: "Hr",

		render: function render() {
			var style = {
				border: "none",
				height: 1,
				color: "#EEE",
				backgroundColor: "#EEE",
				marginBottom: "1em",
				clear: "both"
			};

			return React.createElement("hr", { style: style });
		}
	});

	var ErrMsg = React.createClass({
		displayName: "ErrMsg",

		render: function render() {
			var style = {
				textAlign: "center",
				fontSize: "0.5em",
				color: "#888",
				marginBottom: "1em"
			};

			return React.createElement(
				"div",
				{ style: style },
				React.createElement("span", null)
			);
		}
	});

	var Input = React.createClass({
		displayName: "Input",

		handleChange: function handleChange(e) {
			var v = e.target.value;
			this.props.updateField(this.props.field, v);
		},

		render: function render() {
			var style = {
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

			return React.createElement("input", { style: style, value: this.props.value, onChange: this.handleChange, type: this.props.type });
		}
	});

	var Label = React.createClass({
		displayName: "Label",

		render: function render() {
			var style = {
				fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
				fontSize: "1.0em",
				fontWeight: "normal",
				marginBottom: "0.5em",
				display: "block"
			};

			return React.createElement(
				"label",
				{ style: style },
				this.props.desc
			);
		}
	});

	var EditBox = React.createClass({
		displayName: "EditBox",

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(Label, { desc: this.props.desc }),
				React.createElement(Input, { type: this.props.type, updateField: this.props.updateField, field: this.props.field, value: this.props.value })
			);
		}
	});

	var Select = React.createClass({
		displayName: "Select",

		getInitialState: function getInitialState() {
			return { list: ["null"] };
		},

		componentDidMount: function componentDidMount() {
			$.getJSON(this.props.url).done(function (data) {
				var err = data["err"];
				if (!err) {
					var list = data["data"];
					this.setState({ list: list });
					this.props.updateField(this.props.field, list[0]);
				}
			}.bind(this));
		},

		handleChange: function handleChange(e) {
			var v = e.target.value;
			this.props.updateField(this.props.field, v);
		},

		render: function render() {
			var style = {
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
			var list = this.state.list;

			return React.createElement(
				"select",
				{ style: style, value: this.props.value, onChange: this.handleChange },
				list.map(function (v, index) {
					return React.createElement(
						"option",
						{ key: index, value: v },
						v
					);
				})
			);
		}
	});

	var SelectBox = React.createClass({
		displayName: "SelectBox",

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(Label, { desc: this.props.desc }),
				React.createElement(Select, { updateField: this.props.updateField, url: this.props.url, field: this.props.field, value: this.props.value })
			);
		}
	});

	var Button = React.createClass({
		displayName: "Button",

		render: function render() {
			var style = {
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

			return React.createElement("input", { style: style, type: "submit", value: "\u63D0\u4EA4" });
		}
	});

	var SubmitForm = React.createClass({
		displayName: "SubmitForm",

		getInitialState: function getInitialState() {
			return { category: "",
				url: "",
				item_content_xpath: "",
				removed_xpath_nodes: "" };
		},

		submit: function submit(e) {
			e.preventDefault();

			var form = {};
			for (var k in this.state) {
				if (this.state[k].length > 0) {
					form[k] = this.state[k];
				}
			}

			if (form["url"] == "") {
				$("span").text("需要网址数据").show().fadeOut(1500);
			} else {
				$("span").text("正在提交 .....").show();
				$.ajax({ type: "post",
					url: "/api/feed/rss",
					data: form,
					success: function (r) {
						if (r['err'] == 0) {
							$("span").text("成功").show().fadeOut(1500);
						} else {
							$("span").text("失败: " + r["msg"]).show().fadeOut(1500);
						}
						this.setState({ url: "", content: "" });
					}.bind(this) });
			}
			ReactDOM.findDOMNode(this.refs.Submit).blur();
		},

		updateField: function updateField(k, v) {
			this.setState(_defineProperty({}, k, v));
		},

		render: function render() {
			var style = {
				borderWidth: 0,
				paddingLeft: "36px"
			};

			return React.createElement(
				"div",
				null,
				React.createElement(ErrMsg, null),
				React.createElement(
					"form",
					{ onSubmit: this.submit, style: style },
					React.createElement(EditBox, { desc: "\u7F51\u5740:", updateField: this.updateField, type: "url", field: "url", value: this.state.url }),
					React.createElement(SelectBox, { desc: "\u7C7B\u522B:", updateField: this.updateField, field: "category", url: "/api/categories", value: this.state.category }),
					React.createElement(EditBox, { desc: "\u5185\u5BB9selector[\u7528\u4E8E\u975E\u5168\u6587\u8F93\u51FA\u7684feed](\u9009\u586B):", updateField: this.updateField, type: "text", field: "item_content_xpath", value: this.state.content }),
					React.createElement(EditBox, { desc: "\u6E05\u9664xpath node \u6570\u7EC4(\u9009\u586B):", updateField: this.updateField, type: "text", field: "removed_xpath_nodes", value: this.state.removed_xpath_nodes }),
					React.createElement(Button, { ref: "Submit" })
				)
			);
		}
	});

	var App = React.createClass({
		displayName: "App",


		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(Title, { title: "\u6DFB\u52A0\u8BA2\u9605\u6E90(rss|atom)" }),
				React.createElement(Hr, null),
				React.createElement(SubmitForm, null)
			);
		}
	});

	ReactDOM.render(React.createElement(App, null), document.getElementById('content'));

/***/ }
/******/ ]);