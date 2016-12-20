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

	function decodeEntities(encodedString) {
		var textArea = document.createElement('textarea');
		textArea.innerHTML = encodedString;
		return textArea.value;
	}

	var NavSector = React.createClass({
		displayName: "NavSector",

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					null,
					"\u5BFC\u822A"
				),
				React.createElement(
					"ul",
					null,
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"/d/Y-M-D: \u6309\u65E5\u671F\u663E\u793A\u6587\u7AE0"
						)
					),
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"/l/p: \u6240\u6709\u8BA2\u9605\u6E90"
						)
					),
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"/f/atom: \u6DFB\u52A0rss\u8BA2\u9605\u6E90"
						)
					),
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"/f/blog: \u6DFB\u52A0blog\u8BA2\u9605\u6E90"
						)
					)
				)
			);
		}
	});

	var DeclareSector = React.createClass({
		displayName: "DeclareSector",

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					null,
					"\u58F0\u660E"
				),
				React.createElement(
					"ul",
					null,
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"\u6240\u6709\u6587\u7AE0\u6807\u9898\u5904\u5747\u9644\u6709\u539F\u6587\u94FE\u63A5"
						)
					),
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"\u6240\u6709\u5185\u5BB9\u6765\u81EA\u4E92\u8054\u7F51\uFF0C\u4EFB\u4F55\u5546\u4E1A\u7528\u9014\u8BF7\u8054\u7CFB\u539F\u4F5C\u8005"
						)
					)
				)
			);
		}
	});

	var SpiderButton = React.createClass({
		displayName: "SpiderButton",

		render: function render() {
			var style = {
				backgroundColor: "#eff6fa",
				border: "0.1em solid #eff6fa",
				borderRadius: "0.4em",
				boxSizing: "border-box",
				color: "#259",
				cursor: "pointer",
				display: "inline-block",
				fontSize: "0.6em",
				fontWeight: "bold",
				height: "3em",
				width: "92%",
				letterSpacing: "0.1rem",
				lineHeight: "3em",
				padding: "1 4em",
				textAlign: "center",
				textDecoration: "none"
			};

			return React.createElement(
				"li",
				null,
				React.createElement(
					"div",
					null,
					React.createElement(
						"p",
						null,
						this.props.desc
					),
					React.createElement(
						"a",
						{ style: style, href: this.props.url, target: "_blank" },
						this.props.title
					)
				)
			);
		}
	});

	var SubmitSector = React.createClass({
		displayName: "SubmitSector",

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					null,
					"Spider"
				),
				React.createElement(
					"ul",
					null,
					React.createElement(SpiderButton, { desc: "\u6DFB\u52A0rss\u6E90\uFF0C\u652F\u6301rss\u4E0Eatom", url: "/f/rss", title: "\u751F\u6210RSS Spider" }),
					React.createElement(SpiderButton, { desc: "\u6DFB\u52A0blog,\u7528\u4E8E\u6CA1\u6709rss\u8F93\u51FA\u7684blog", url: "/f/blog", title: "\u751F\u6210Blog Spider" })
				)
			);
		}
	});

	var AddressSector = React.createClass({
		displayName: "AddressSector",

		render: function render() {
			var style = {
				color: "#888",
				textDecoration: "none"
			};

			return React.createElement(
				"div",
				null,
				React.createElement(
					"p",
					null,
					"\u8054\u7CFB\u65B9\u5F0F"
				),
				React.createElement(
					"ul",
					null,
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"email: ",
							React.createElement(
								"a",
								{ style: style, href: "mailto:code4hack@gmail.com" },
								"code4hack@gmail.com"
							)
						)
					)
				),
				React.createElement(
					"p",
					null,
					"\u9879\u76EE\u5730\u5740"
				),
				React.createElement(
					"ul",
					null,
					React.createElement(
						"li",
						null,
						React.createElement(
							"p",
							null,
							"github: ",
							React.createElement(
								"a",
								{ style: style, href: "https://github.com/alone-walker/BlogSpider", target: "_blank" },
								"BlogSpider"
							)
						)
					)
				)
			);
		}
	});

	var FloatSide = React.createClass({
		displayName: "FloatSide",

		render: function render() {
			var style = {
				float: "right",
				width: "300px",
				padding: "0 32px",
				fontFamily: "sans-serif",
				fontSize: "0.7em",
				fontWeight: "bold",
				color: "dimgray"
			};

			if (screen.width < 600) {
				style["display"] = "none";
			} else {
				style["display"] = "block";
			}

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(NavSector, null),
				React.createElement(Hr, null),
				React.createElement(DeclareSector, null),
				React.createElement(Hr, null),
				React.createElement(SubmitSector, null),
				React.createElement(Hr, null),
				React.createElement(AddressSector, null)
			);
		}
	});

	var Rank = React.createClass({
		displayName: "Rank",

		render: function render() {
			var style = {
				color: "#c6c6c6",
				textAlign: "right",
				fontFamily: "arial",
				fontSize: "medium",
				fontWeight: "bold",
				width: "40px",
				paddingRight: "25px",
				flexShrink: 0
			};

			return React.createElement(
				"span",
				{ style: style },
				this.props.rank
			);
		}
	});

	var ArticleLink = React.createClass({
		displayName: "ArticleLink",

		render: function render() {
			var style = {
				fontFamily: "verdana, helvetica, Pingfang SC, Microsoft YaHei, arial, sans-serif",
				fontSize: "0.9em",
				fontWeight: "normal"
			};
			var url = "/a/" + this.props.aid;
			var title = decodeEntities(this.props.title);

			return React.createElement(
				"span",
				{ className: "articlelink" },
				React.createElement(
					"a",
					{ style: style, href: url, target: "_blank" },
					title
				)
			);
		}
	});

	var OrginalLink = React.createClass({
		displayName: "OrginalLink",

		render: function render() {
			var style = {
				padding: "0 6px",
				fontSize: "x-small"
			};

			return React.createElement(
				"span",
				{ className: "articlelink" },
				React.createElement(
					"a",
					{ style: style, href: this.props.url, target: "_blank" },
					React.createElement("i", { className: "fa fa-paper-plane-o", "aria-hidden": "true" })
				)
			);
		}
	});

	var DomainLink = React.createClass({
		displayName: "DomainLink",

		render: function render() {
			var style = {
				color: "#888",
				fontSize: "x-small",
				whiteSpace: "nowrap",
				textDecoration: "none"
			};
			var url = "http://" + this.props.domain;

			return React.createElement(
				"span",
				null,
				React.createElement(
					"a",
					{ style: style, href: url, target: "_blank" },
					"(",
					this.props.domain,
					")"
				)
			);
		}
	});

	var EntryTitle = React.createClass({
		displayName: "EntryTitle",

		render: function render() {
			var style = {
				margin: 0,
				padding: 0,
				lineHeight: 1
			};

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(ArticleLink, { aid: this.props.aid, title: this.props.title }),
				React.createElement(OrginalLink, { url: this.props.url }),
				React.createElement(DomainLink, { domain: this.props.domain })
			);
		}
	});

	var SpiderTag = React.createClass({
		displayName: "SpiderTag",

		render: function render() {
			var style = {
				color: "#999",
				fontSize: "x-small",
				fontWeight: "bold",
				marginRight: "4px",
				marginBottom: "2px",
				textDecoration: "none"
			};
			var spid = this.props.spider.spid;
			var spname = this.props.spider.spname;
			var url = "/p/" + spid;

			return React.createElement(
				"span",
				null,
				React.createElement(
					"a",
					{ style: style, href: url, target: "_blank" },
					"[",
					spname,
					"]"
				)
			);
		}
	});

	var ArticleTag = React.createClass({
		displayName: "ArticleTag",

		render: function render() {
			var style = {
				fontWeight: "normal",
				fontSize: "x-small",
				color: "#999",
				backgroundColor: "#eee",
				borderRadius: "30px",
				padding: "1px 10px",
				marginRight: "4px",
				marginBottom: "2px",
				whiteSpace: "nowrap"
			};

			return React.createElement(
				"span",
				{ style: style },
				this.props.tag
			);
		}
	});

	var EntryTags = React.createClass({
		displayName: "EntryTags",

		render: function render() {
			var style = {
				display: "flex",
				flexDirection: "row",
				flexWrap: "wrap",
				alignItems: "baseline"
			};
			var spider = this.props.spider;
			var tags = this.props.tags;

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(SpiderTag, { spider: spider }),
				tags.map(function (tag, index) {
					return React.createElement(ArticleTag, { key: index, tag: tag });
				})
			);
		}
	});

	var Entry = React.createClass({
		displayName: "Entry",

		render: function render() {
			var style = {
				display: "flex",
				alignItems: "center",
				marginBottom: "12px"
			};

			var index = this.props.index;
			var entry = this.props.entry;
			var spider = { spid: entry[5], spname: entry[3] };
			var tags = entry[4] == null ? [] : entry[4];

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(Rank, { rank: index }),
				React.createElement(
					"div",
					null,
					React.createElement(EntryTitle, { aid: entry[0], title: entry[1], url: entry[7], domain: entry[6] }),
					React.createElement(EntryTags, { spider: spider, tags: tags })
				)
			);
		}
	});

	var Entries = React.createClass({
		displayName: "Entries",

		render: function render() {
			var entries = this.props.entries;
			return React.createElement(
				"div",
				null,
				entries.map(function (entry, index) {
					return React.createElement(Entry, { key: index, index: index, entry: entry });
				})
			);
		}
	});

	var Category = React.createClass({
		displayName: "Category",

		onClick: function onClick(e, category) {
			e.preventDefault();
			e.stopPropagation();

			this.props.onCategoryClick(category);
		},

		render: function render() {
			var _this = this;

			var listyle = {
				display: "inline-block",
				marginRight: "1.6em"
			};

			var astyle = {
				fontFamily: "Pingfang SC, Microsoft YaHei",
				fontWeight: "bold",
				fontSize: "1.0em",
				color: "#666666",
				textDecoration: "none"
			};

			if (this.props.focus) {
				astyle["color"] = "#222222";
			}

			return React.createElement(
				"li",
				{ style: listyle },
				React.createElement(
					"a",
					{ href: "#", style: astyle, onClick: function onClick(event) {
							return _this.onClick(event, _this.props.category);
						} },
					this.props.category
				)
			);
		}
	});

	var CategoryDiv = React.createClass({
		displayName: "CategoryDiv",

		render: function render() {
			var style = {
				listStyle: "none",
				marginBottom: 0,
				marginLeft: "2em"
			};
			var categories = this.props.categories;
			var onCategoryClick = this.props.onCategoryClick;
			var categoryFocused = this.props.categoryFocused;

			return React.createElement(
				"div",
				null,
				React.createElement(
					"ul",
					{ style: style },
					categories.map(function (category, index) {
						var focus = categoryFocused == category;
						return React.createElement(Category, { key: index, focus: focus, category: category, onCategoryClick: onCategoryClick });
					})
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

	var ContentDiv = React.createClass({
		displayName: "ContentDiv",

		getCategories: function getCategories(data) {
			var categories = [];
			$.each(data, function (key, val) {
				categories.push(key);
			});
			return categories.sort(function (a, b) {
				var sortList = {
					"技术": 0,
					"数据库": 1,
					"安全": 2,
					"科技": 3,
					"新闻": 4
				};
				return sortList[a] > sortList[b] ? 1 : -1;
			});
		},

		getDefaultProps: function getDefaultProps() {
			return { data: { "新闻": [],
					"技术": [],
					"科技": [],
					"数据库": [],
					"安全": [] }
			};
		},

		getInitialState: function getInitialState() {
			var categories = this.getCategories(this.props.data);
			return { category: categories[0] };
		},

		componentWillReceiveProps: function componentWillReceiveProps(nextProps) {
			this.setState({ category: this.getCategories(nextProps.data)[0] });
		},

		onCategoryClick: function onCategoryClick(category) {
			this.setState({ category: category });
		},

		render: function render() {
			var data = this.props.data;
			var categories = this.getCategories(data);
			var entries = data[this.state.category];

			return React.createElement(
				"div",
				null,
				React.createElement(CategoryDiv, { categoryFocused: this.state.category, categories: categories, onCategoryClick: this.onCategoryClick }),
				React.createElement(Hr, null),
				React.createElement(FloatSide, null),
				React.createElement(Entries, { entries: entries }),
				React.createElement(Hr, null)
			);
		}
	});

	var DayLink = React.createClass({
		displayName: "DayLink",

		onClick: function onClick(e, day) {
			e.preventDefault();
			e.stopPropagation();

			this.props.onDayLinkClick(day);
		},

		render: function render() {
			var _this2 = this;

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
					{ href: "#", onClick: function onClick(e) {
							return _this2.onClick(e, _this2.props.day);
						} },
					React.createElement("i", { className: cn, "aria-hidden": "true" })
				)
			);
		}
	});

	var DayLinkDiv = React.createClass({
		displayName: "DayLinkDiv",

		render: function render() {
			var style = {
				paddingLeft: "40%",
				paddingRight: "40%"
			};

			return React.createElement(
				"div",
				{ style: style },
				React.createElement(DayLink, { handType: "handleft", day: this.props.day_after, onDayLinkClick: this.props.onDayLinkClick }),
				React.createElement(DayLink, { handType: "handright", day: this.props.day_before, onDayLinkClick: this.props.onDayLinkClick })
			);
		}
	});

	var App = React.createClass({
		displayName: "App",

		getInitialState: function getInitialState() {
			return { day_before: null,
				day_after: null };
		},

		setDay: function setDay(day) {
			$.getJSON("/api/day", { day: day }).done(function (data) {
				var err = data["err"];

				if (!err) {
					var nstate = { day_before: data["day_before"],
						day_after: data["day_after"] };

					if (data["data"]) {
						nstate["data"] = data["data"];
					}

					if (nstate["data"] == null) {
						var now = new Date(document.title);
						var t = new Date();
						var today = new Date(t.getFullYear(), t.getMonth(), t.getDate());
						if (now >= today && nstate["day_before"] != null) {
							this.setDay(nstate["day_before"]);
							return;
						}
					} else {
						document.title = day;
						window.history.pushState(day, day, "/d/" + day);
						this.setState(nstate);
					}
				}
			}.bind(this));
		},

		onDayLinkClick: function onDayLinkClick(day) {
			if (day) {
				this.setDay(day);
			}
		},

		componentDidMount: function componentDidMount() {
			this.setDay(document.title);
		},

		render: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(ContentDiv, { data: this.state.data }),
				React.createElement(DayLinkDiv, { day_after: this.state.day_after, day_before: this.state.day_before, onDayLinkClick: this.onDayLinkClick })
			);
		}
	});

	ReactDOM.render(React.createElement(App, null), document.getElementById('content'));

/***/ }
/******/ ]);