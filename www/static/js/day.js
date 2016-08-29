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
	loadFromServer: function() {
		console.log("loadFromServer");
		$.getJSON("/api/day", {day: "2016-06-24"}).done(function(data) {
			var categories = [];
			var entries = data["entries"];
			$.each(entries, function(key, val) {
				categories.push(key);
			});
			this.setState({category: categories[0], data: entries});
		}.bind(this));
	},

	getInitialState: function() {
		return {category: "init", data: {init: []}};
	},

	componentDidMount: function() {
		this.loadFromServer();
	},

	onCategoryClick: function(category) {
		console.log(category);
		this.setState({category: category});
	},

	render: function() {
		var categories = [];
		$.each(this.state.data, function(key, val) {
			categories.push(key);
		});

		var entries = this.state.data[this.state.category];

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

ReactDOM.render(
  <ContentDiv />,
  document.getElementById('content')
);
