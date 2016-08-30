var Rank = React.createClass({
	render: function() {
		return (
			<span className="rank">
				{this.props.rank}
			</span>
		)
	}
});

var ArticleLink = React.createClass({
	render: function() {
		return (
			<a target="_blank">{this.props.title}</a>
		)
	}
});

var OrginalLink = React.createClass({
	render: function() {
		return (
			<span className="orglink">
				<a target="_blank">
				<i className="fa fa-paper-plane-o" aria-hidden="true"></i>
				</a>
			</span>
		)
	}
});

var DomainLink = React.createClass({
	render: function() {
		return (
			<span className="domain">
				(<a href="#">{this.props.domain}</a>)
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
		console.log(tags);

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
	onClick: function(category) {
		this.props.onCategoryClick(category);
	},

	render: function() {
		return (
			<li className="link">
				<a href="#" onClick={this.onClick.bind(this, this.props.category)}>{this.props.category}</a>
			</li>
		)
	}
});

var CategoryDiv = React.createClass({
	render: function() {
		var categories = this.props.categories;
		var onCategoryClick = this.props.onCategoryClick;
		return (
			<div>
				<ul className="category">
					{categories.map(function(category) {
						return <Category category={category} onCategoryClick={onCategoryClick} />;
					})}
				</ul>
			</div>
		)
	}
});

var ContentDiv = React.createClass({
	getInitialState: function() {
		return {category: "新闻"};
	},

	onCategoryClick: function(category) {
		this.setState({category: category});
	},

	render: function() {
		var data = this.props.data;
		var categories = [];

		$.each(data, function(key, val) {
			categories.push(key);
		});

		var entries = data[this.state.category];
		return (
			<div>
				<CategoryDiv categories={categories} onCategoryClick={this.onCategoryClick} />
				<hr />
				<Entries entries={entries} />
				<hr />
			</div>
		)
	}
});

var DayLink = React.createClass({
	onClick: function(day) {
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
				<a href="#" onClick={this.onClick.bind(this, this.props.day)}>
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
