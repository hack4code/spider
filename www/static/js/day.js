var Rank = React.createClass({
	render: function() {
		var style = {
		 float: "left",
		 color: "#c6c6c6",
		 textAlign: "right",
		 fontFamily: "arial",
		 fontSize: "medium",
		 fontWeight: "bold",
		 overflow: "hidden",
		 width: "3em",
		 paddingRight: "2em",
		 marginTop: "1.2em",
/*
		 paddingLeft: "1em",
		 marginLeft: "-2em"
*/
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
		var url = "/a/" + this.props.aid;
		return (
			<a href={url} target="_blank">{this.props.title}</a>
		)
	}
});

var OrginalLink = React.createClass({
	render: function() {
		var style = {
			padding: "0 6px",
		  fontSize: "x-small"
		};

		return (
			<span style={style}>
				<a href={this.props.url} target="_blank">
				<i className="fa fa-paper-plane-o" aria-hidden="true"></i>
				</a>
			</span>
		)
	}
});

var DomainLink = React.createClass({
	render: function() {
		var url = "http://" + this.props.domain;
		return (
			<span className="domain">
				(<a href={url} target="_blank">{this.props.domain}</a>)
			</span>
		)
	}
});

var EntryTitle = React.createClass({
	render: function() {
		return (
			<div><p className="title">
				<ArticleLink aid={this.props.aid} title={this.props.title} />
				<OrginalLink url={this.props.url} />
				<DomainLink domain={this.props.domain} />
			</p></div>
		)
	}
});

var SpiderTag = React.createClass({
	render: function() {
		var spid = this.props.spider.spid;
		var spname = this.props.spider.spname;
		return (
			<li className="spider">
				<a href="#">[{spname}]</a>
			</li>
		)
	}
});

var ArticleTag = React.createClass({
	render: function() {
		return (
			<li className="tag">
				{this.props.tag}
			</li>
	  )
	}
});

var EntryTags = React.createClass({
	render: function() {
		var spider = this.props.spider;
		var tags = this.props.tags;
		return (
			<div className="bottom"><ul>
				<SpiderTag spider={spider} />
				{tags.map(function(tag) { return <ArticleTag tag={tag} />; })}
			</ul></div>
		)
	}
});

var Entry = React.createClass({
	render: function() {
		var index = this.props.index;
		var entry = this.props.entry;
		var spider = {spid: entry[5], spname: entry[3]};
		var tags = entry[4];
		if (!tags) {
			tags = [];
		}

		return (
			<div className="entry">
				<Rank rank={index} />
				<EntryTitle aid={entry[0]} title={entry[1]} url={entry[7]} domain={entry[6]} />
				<EntryTags spider={spider} tags={tags} />
				<div className="clearleft"></div>
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
					return <Entry index={index} entry={entry} />
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
		var categories = this.props.categories;
		var onCategoryClick = this.props.onCategoryClick;
		var categoryFocused = this.props.categoryFocused;

		return (
			<div>
				<ul className="category">
					{categories.map(function(category) {
						var focus = (categoryFocused == category);
						console.log(focus);
						return <Category focus={focus} category={category} onCategoryClick={onCategoryClick} />;
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
	getCategories: function() {
		var data = this.props.data;
		var categories = [];
		$.each(data, function(key, val) {
			categories.push(key);
		});
		return categories;
	},

	getInitialState: function() {
		var categories = this.getCategories();
		return {category: categories[0]};
	},

	onCategoryClick: function(category) {
		this.setState({category: category});
	},

	render: function() {
		var data = this.props.data;
		var categories = this.getCategories();
		var entries = data[this.state.category];

		return (
			<div>
				<CategoryDiv categoryFocused={this.state.category} categories={categories} onCategoryClick={this.onCategoryClick} />
				<Hr />
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

		if (this.props.handType == "handright") {
			cn = "fa fa-hand-o-right";
		}
		else {
			cn = "fa fa-hand-o-left";
		}

		return (
			<span className={this.props.handType}>
				<a href="#" onClick={(e)=>this.onClick(e, this.props.day)}>
					<i className={cn} aria-hidden="true"></i>
		  	</a>
			</span>
		)
	}
});

var DayLinkDiv = React.createClass({
	render: function() {
		return (
			<div className="daylink">
				<DayLink handType="handleft" day={this.props.day_after} onDayLinkClick={this.props.onDayLinkClick} />
				<DayLink handType="handright" day={this.props.day_before} onDayLinkClick={this.props.onDayLinkClick} />
			</div>
		)
	}
});

var App = React.createClass({
	getInitialState: function() {
		return {day_before: null,
						day_after: null,
						data:{"新闻": [],
									"技术": [],
									"科技": [],
									"安全": []}}
	},

	setDay: function(day) {
		$.getJSON("/api/day", {day: day}).done(function(data) {
			var err = data["err"];

			if (!err) {
				document.title = day;
				this.setState({day_before: data["day_before"],
											 day_after: data["day_after"],
											 data: data["data"]});
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
