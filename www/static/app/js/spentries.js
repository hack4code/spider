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

	var Title = React.createClass({
		displayName: "Title",

		render: function render() {
			var style = {
				fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
				fontSize: "normal",
				fontWeight: "bold",
				textAlign: "center"
			};

			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					{ style: style },
					this.props.name
				)
			);
		}
	});

	var Entry = React.createClass({
		displayName: "Entry",

		render: function render() {
			var style = {
				fontWeight: "600",
				fontSize: "0.8em",
				fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
				lineHeight: "2em",
				textDecoration: "none"
			};
			var url = "/a/" + this.props.aid;

			return React.createElement(
				"li",
				null,
				React.createElement(
					"a",
					{ style: style, href: url, target: "_blank" },
					this.props.title
				)
			);
		}
	});

	var Entries = React.createClass({
		displayName: "Entries",

		render: function render() {
			var style = {
				listStyle: "square",
				color: "red",
				marginLeft: "4em"
			};
			var entries = this.props.entries;

			return React.createElement(
				"ul",
				{ style: style },
				entries.map(function (entry, index) {
					return React.createElement(Entry, { key: index, aid: entry[0], title: entry[1] });
				})
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

	var AidLink = React.createClass({
		displayName: "AidLink",

		onClick: function onClick(e) {
			e.preventDefault();
			e.stopPropagation();

			this.props.onAidClick();
		},

		render: function render() {
			var cn;
			var style;

			if (this.props.handType == "handright") {
				cn = "fa fa-hand-o-right";
				style = {
					float: "right"
				};
			} else {
				cn = "fa fa-hand-o-left";
				style = {
					float: "left"
				};
			}

			return React.createElement(
				"span",
				{ style: style },
				React.createElement(
					"a",
					{ href: "#", onClick: this.onClick },
					React.createElement("i", { className: cn, "aria-hidden": "true" })
				)
			);
		}
	});

	var AidLinkDiv = React.createClass({
		displayName: "AidLinkDiv",

		render: function render() {
			var style = {
				paddingLeft: "40%",
				paddingRight: "40%"
			};

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(AidLink, { handType: "handleft", onAidClick: this.props.onLeftClick }),
				React.createElement(AidLink, { handType: "handright", onAidClick: this.props.onRightClick })
			);
		}
	});

	var App = React.createClass({
		displayName: "App",

		getEntries: function getEntries(aid, q) {
			var spid = this.state.spid;
			var args = { spid: spid };
			if (aid != null) {
				args['aid'] = aid;
				args['q'] = q;
			}

			$.getJSON("/api/spider", args).done(function (data) {
				var err = data["err"];
				if (!err) {
					this.setState({ entries: data["entries"] });
				}
			}.bind(this));
		},

		onLeftClick: function onLeftClick() {
			var entries = this.state.entries;
			if (entries.length == 0) {
				return;
			}
			var aid = entries[0][0];
			this.getEntries(aid, "p");
		},

		onRightClick: function onRightClick() {
			var entries = this.state.entries;
			if (entries.length == 0) {
				return;
			}
			var aid = entries[entries.length - 1][0];
			this.getEntries(aid, "n");
		},

		getInitialState: function getInitialState() {
			var spid = $("#content").attr("spid");
			var name = $("#content").attr("name");
			return { spid: spid, name: name, entries: [] };
		},

		componentDidMount: function componentDidMount() {
			this.getEntries();
		},

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(Title, { name: this.state.name }),
				React.createElement(Hr, null),
				React.createElement(Entries, { entries: this.state.entries }),
				React.createElement(Hr, null),
				React.createElement(AidLinkDiv, { onLeftClick: this.onLeftClick, onRightClick: this.onRightClick })
			);
		}
	});

	ReactDOM.render(React.createElement(App, null), document.getElementById("content"));

/***/ }
/******/ ]);