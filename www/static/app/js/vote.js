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

	var Voter = React.createClass({
		displayName: "Voter",

		getInitialState: function getInitialState() {
			var s = window.localStorage;
			var aid = this.props.aid;
			if (s.getItem(aid) != null) {
				return { voted: 1 };
			} else {
				return { voted: 0 };
			}
		},

		onClick: function onClick(e) {
			e.preventDefault();
			e.stopPropagation();

			var s = window.localStorage;
			var aid = this.props.aid;

			if (s.getItem(aid) != null) {
				return;
			} else {
				this.setState({ voted: 1 });
				$.post("/api/vote", { aid: aid }).done(function (data) {
					if (!data['err']) {
						s.setItem(aid, 1);
					} else {
						this.setState({ voted: 0 });
					}
				}.bind(this));
			}
		},


		render: function render() {
			var style = {
				fontSize: "1em",
				fontWeight: "bold"
			};
			style["color"] = this.state.voted ? "#004276" : "#999999";

			return React.createElement(
				"div",
				null,
				React.createElement(
					"a",
					{ style: style, href: "#", onClick: this.onClick },
					React.createElement("i", { className: "fa fa-thumbs-o-up" })
				)
			);
		}
	});

	var Footer = React.createClass({
		displayName: "Footer",

		render: function render() {
			var style = {
				color: "#888",
				fontSize: "x-small"
			};
			var url = "/p/" + this.props.spid;

			return React.createElement(
				"p",
				{ style: style },
				"\u672C\u6587\u7AE0\u6765\u81EA",
				React.createElement(
					"span",
					null,
					"[",
					React.createElement(
						"a",
						{ href: url, target: "_blank" },
						this.props.spname
					),
					"]"
				),
				", \u60A8\u53EF\u4EE5\u5BF9\u6587\u7AE0\u70B9\u8D5E"
			);
		}
	});

	var App = React.createClass({
		displayName: "App",

		render: function render() {
			var style = {
				display: "flex",
				flexDirection: "column",
				alignItems: "center"
			};
			var aid = $("#content").attr("aid");
			var spid = $("#content").attr("spid");
			var spname = $("#content").attr("spname");

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(Voter, { aid: aid }),
				React.createElement(Footer, { spid: spid, spname: spname })
			);
		}
	});

	ReactDOM.render(React.createElement(App, null), document.getElementById('content'));

/***/ }
/******/ ]);