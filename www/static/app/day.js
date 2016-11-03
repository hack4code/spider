var NavSector = React.createClass({
	render: function() {
		return (
			<div>
				<p>导航</p>
				<ul>
					<li><p>/d/Y-M-D: 按日期显示文章</p></li>
					<li><p>/l/p: 所有订阅源</p></li>
					<li><p>/f/atom: 添加rss订阅源</p></li>
					<li><p>/f/blog: 添加blog订阅源</p></li>
				</ul>
			</div>
		)
	}
});

var DeclareSector = React.createClass({
	render: function() {
		return (
			<div>
				<p>声明</p>
				<ul>
					<li><p>所有文章标题处均附有原文链接</p></li>
					<li><p>所有内容来自互联网，任何商业用途请联系原作者</p></li>
				</ul>
			</div>
		)
	}
});

var SpiderButton = React.createClass({
	render: function() {
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

		return (
			<li><div>
				<p>{this.props.desc}</p>
				<a style={style} href={this.props.url} target="_blank">{this.props.title}</a>
			</div></li>
		)
	}
});

var SubmitSector = React.createClass({
	render: function() {
		return (
			<div>
				<p>Spider</p>
				<ul>
					<SpiderButton desc="添加rss源，支持rss与atom" url="/f/rss" title="生成RSS Spider" />
					<SpiderButton desc="添加blog,用于没有rss输出的blog" url="/f/blog" title="生成Blog Spider" />
				</ul>
			</div>
		)
	}
});

var AddressSector = React.createClass({
	render: function() {
		var style = {
			color: "#888",
			textDecoration: "none"
		};

		return (
			<div>
			<p>联系方式</p>
			<ul>
				<li>
				<p>email: <a style={style} href="mailto:code4hack@gmail.com">wartalker@gmail.com</a></p>
				</li>
				<li>
				<p>github: <a style={style} href="https://github.com/alone-walker/BlogSpider" target="_blank">BlogSpider</a></p>
				</li>
			</ul>
			</div>
		)
	}
});

var FloatSide = React.createClass({
	render: function() {
		var style = {
			display: "block",
			float: "right",
			width: "300px",
			padding: "0 32px",
			fontFamily: "sans-serif",
			fontSize: "0.7em",
			fontWeight: "bold",
			color: "dimgray"
		};

		return (
			<div style={style}>
				<NavSector />
				<Hr />
				<DeclareSector />
				<Hr />
				<SubmitSector />
				<Hr />
				<AddressSector />
			</div>
		)
	}
});

var Rank = React.createClass({
	render: function() {
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

		return (
			<span style={style}>
				{this.props.rank}
			</span>
		)
	}
});

var ArticleLink = React.createClass({
	render: function() {
		var style = {
			fontFamily: "verdana, helvetica, Pingfang SC, Microsoft YaHei, arial, sans-serif",
			fontSize: "0.9em",
			fontWeight: "normal",
		};
		var url = "/a/" + this.props.aid;

		return (
			<span className="articlelink">
				<a style={style} href={url} target="_blank">{this.props.title}</a>
			</span>
		)
	}
});

var OrginalLink = React.createClass({
	render: function() {
		var style = {
			padding: "0 6px",
		  fontSize: "x-small",
		};

		return (
			<span className="articlelink">
				<a style={style} href={this.props.url} target="_blank">
				<i className="fa fa-paper-plane-o" aria-hidden="true"></i>
				</a>
			</span>
		)
	}
});

var DomainLink = React.createClass({
	render: function() {
		var style = {
			color: "#888",
			fontSize: "x-small",
			whiteSpace: "nowrap",
			textDecoration: "none"
		};
		var url = "http://" + this.props.domain;

		return (
			<span>
				<a style={style} href={url} target="_blank">({this.props.domain})</a>
			</span>
		)
	}
});

var EntryTitle = React.createClass({
	render: function() {
		var style = {
			margin: 0,
			padding: 0,
			lineHeight: 1
		};

		return (
			<div style={style}>
				<ArticleLink aid={this.props.aid} title={this.props.title} />
				<OrginalLink url={this.props.url} />
				<DomainLink domain={this.props.domain} />
			</div>
		)
	}
});

var SpiderTag = React.createClass({
	render: function() {
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

		return (
			<span>
				<a style={style} href={url} target="_blank">[{spname}]</a>
			</span>
		)
	}
});

var ArticleTag = React.createClass({
	render: function() {
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

		return (
			<span style={style}>
				{this.props.tag}
			</span>
	  )
	}
});

var EntryTags = React.createClass({
	render: function() {
		var style = {
			display: "flex",
			flexDirection: "row",
			flexWrap: "wrap",
			alignItems: "baseline"
		};
		var spider = this.props.spider;
		var tags = this.props.tags;

		return (
			<div style={style}>
				<SpiderTag spider={spider} />
				{tags.map(function(tag, index) { return <ArticleTag key={index} tag={tag} />; })}
			</div>
		)
	}
});

var Entry = React.createClass({
	render: function() {
		var style = {
			display: "flex",
			alignItems: "center",
			marginBottom: "12px"
		};

		var index = this.props.index;
		var entry = this.props.entry;
		var spider = {spid: entry[5], spname: entry[3]};
		var tags = (entry[4] == null) ? [] : entry[4];

		return (
				<div style={style}>
					<Rank rank={index} />
					<div>
						<EntryTitle aid={entry[0]} title={entry[1]} url={entry[7]} domain={entry[6]} />
						<EntryTags spider={spider} tags={tags} />
					</div>
				</div>
		)
	}
});

var Entries = React.createClass({
	render: function() {
		var entries = this.props.entries;
		return (
			<div>
				{entries.map(function(entry, index) {
					return <Entry key={index} index={index} entry={entry} />
				})}
			</div>
		)
	}
});

var Category = React.createClass({
	onClick: function(e, category) {
		e.preventDefault();
		e.stopPropagation();

		this.props.onCategoryClick(category);
	},

	render: function() {
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

		return (
			<li style={listyle}>
				<a href="#" style={astyle} onClick={(event)=>this.onClick(event, this.props.category)}>{this.props.category}</a>
			</li>
		)
	}
});

var CategoryDiv = React.createClass({
	render: function() {
		var style = {
			listStyle: "none",
			marginBottom: 0,
			marginLeft: "2em"
		};
		var categories = this.props.categories;
		var onCategoryClick = this.props.onCategoryClick;
		var categoryFocused = this.props.categoryFocused;

		return (
			<div>
				<ul style={style}>
					{categories.map(function(category, index) {
						var focus = (categoryFocused == category);
						return <Category key={index} focus={focus} category={category} onCategoryClick={onCategoryClick} />;
					})}
				</ul>
			</div>
		)
	}
});

var Hr = React.createClass({
	render: function() {
		var style = {
			border: "none",
			height: 1,
			color: "#EEE",
			backgroundColor: "#EEE",
			marginBottom: "1em",
			clear: "both"
		};

		return (
			<hr style={style} />
		)
	}
});

var ContentDiv = React.createClass({
	getCategories: function(data) {
		var categories = [];
		$.each(data, function(key, val) {
			categories.push(key);
		});
		return categories.sort(function(a, b) {
			var sortList = {
				"技术": 0,
				"数据库": 1,
				"安全": 2,
				"科技": 3,
				"新闻": 4
			};
			return sortList[a] > sortList[b];
		});
	},

	getDefaultProps: function() {
	   return { data: {"新闻": [],
						 				 "技术": [],
						         "科技": [],
										 "数据库": [],
						         "安全": []},
					  }
	},

	getInitialState: function() {
		var categories = this.getCategories(this.props.data);
		return {category: categories[0]};
	},

	componentWillReceiveProps: function(nextProps) {
		this.setState({category: this.getCategories(nextProps.data)[0]});
	},

	onCategoryClick: function(category) {
		this.setState({category: category});
	},

	render: function() {
		var data = this.props.data;
		var categories = this.getCategories(data);
		var entries = data[this.state.category];

		return (
			<div>
				<CategoryDiv categoryFocused={this.state.category} categories={categories} onCategoryClick={this.onCategoryClick} />
				<Hr />
				<FloatSide />
				<Entries entries={entries} />
				<Hr />
			</div>
		)
	}
});

var DayLink = React.createClass({
	onClick: function(e, day) {
		e.preventDefault();
		e.stopPropagation();

		this.props.onDayLinkClick(day);
	},

	render: function() {
		var cn;
		var style;

		if (this.props.handType == "handright") {
			cn = "fa fa-hand-o-right";
			style = {
				float: "right"
			}
		}
		else {
			cn = "fa fa-hand-o-left";
			style = {
				float: "left"
			}
		}

		return (
			<span style={style}>
				<a href="#" onClick={(e)=>this.onClick(e, this.props.day)}>
					<i className={cn} aria-hidden="true"></i>
		  	</a>
			</span>
		)
	}
});

var DayLinkDiv = React.createClass({
	render: function() {
		var style = {
			paddingLeft: "40%",
			paddingRight: "40%"
		};

		return (
			<div style={style}>
				<DayLink handType="handleft" day={this.props.day_after} onDayLinkClick={this.props.onDayLinkClick} />
				<DayLink handType="handright" day={this.props.day_before} onDayLinkClick={this.props.onDayLinkClick} />
			</div>
		)
	}
});

var App = React.createClass({
	getInitialState: function() {
		return {day_before: null,
						day_after: null}
	},

	setDay: function(day) {
		$.getJSON("/api/day", {day: day}).done(function(data) {
			var err = data["err"];

			if (!err) {
				var nstate = {day_before: data["day_before"],
										  day_after: data["day_after"]};

				if (data["data"]) {
					nstate["data"] = data["data"];
				}

				document.title = day;
				window.history.pushState(day, day, "/d/" + day);
				this.setState(nstate);
			}
		}.bind(this));
	},

	onDayLinkClick: function(day) {
		if (day) {
			this.setDay(day);
		}
	},

	componentDidMount: function() {
		this.setDay(document.title);
	},

	render: function() {
			return (
				<div>
					<ContentDiv data={this.state.data} />
					<DayLinkDiv day_after={this.state.day_after} day_before={this.state.day_before} onDayLinkClick={this.onDayLinkClick} />
				</div>
			)
		}
});

ReactDOM.render(<App />, document.getElementById('content'));
