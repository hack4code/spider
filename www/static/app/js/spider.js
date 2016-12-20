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
			var url = "/p/" + this.props.spid;

			return React.createElement(
				"li",
				null,
				React.createElement(
					"a",
					{ style: style, href: url, target: "_blank" },
					this.props.name
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
					return React.createElement(Entry, { key: index, spid: entry[0], name: entry[1] });
				})
			);
		}
	});

	var App = React.createClass({
		displayName: "App",

		getInitialState: function getInitialState() {
			return { entries: [] };
		},

		componentDidMount: function componentDidMount() {
			$.getJSON("/api/spiders").done(function (data) {
				var err = data["err"];
				if (!err) {
					this.setState({ entries: data["entries"] });
				}
			}.bind(this));
		},

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(Title, { name: "\u6240\u6709\u8BA2\u9605\u7F51\u7AD9" }),
				React.createElement(Hr, null),
				React.createElement(Entries, { entries: this.state.entries })
			);
		}
	});

	ReactDOM.render(React.createElement(App, null), document.getElementById("content"));

/***/ }
/******/ ]);