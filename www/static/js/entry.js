var Rank = React.createClass({
	render: function() {
		return (
			<span className="rank">
				{this.props.rank}
			</span>
		);
	}
});

var ArticleLink = React.createClass({
	render: function() {
		return (
			<a href=/a/{this.props.aid} target="_blank">{this.props.title}</a>
		)
	}
});

var OrginalLink = React.createClass({
	render: function() {
		return (
			<span className="orglink">
				<a href={this.props.url} target="_blank">
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

var SpiderName = React.createClass({
	render: function() {
		return (
			<li className="spider">
				<a href={this.props.spid}>[{this.props.spname}]</a>
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
		var spider= {}
	  var tags = {}
		return (
			<div className="bottom"><ul>
				<SpiderName spid={spider.id} spname={spider.name} />
				{tags.map(function(tag) {
					return <ArticleTag tag={tag} />;
				})}
			</ul></div>
		)
	}
});


var Entry = React.createClass({
	render: function() {
		var index = this.props.index;
		var entry = this.props.entry;
		return (
			<div className="entry">
				<Rank rank={index} />
				<EntryTitle aid={entry.aid} title={entry.title} url={entry.url} domain={entry.domain} />
				<EntryTags spider={entry.spider} tags={entry.tags} />
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
				{entries.map(function(entry) {
					return <Entry entry={entry} />
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
				<a>{this.props.category}</a>
			</li>
		)
	}
});

var CategoryDiv = React.createClass({
	render: function() {
		var categories = this.props.categoris;
		var onCategoryClick = this.props.onCategoryClick;
		return (
			<div>
				<ul className="category">
					{categories.map(function(category) {
						<CategoryEntry category={category} onCategoryClick={onCategoryClick} />
					})};
				</ul>
			</div>
		)
	}
});

var ContentDiv = React.createClass({
	getInitialState: function() {
		return {category: "null"};
	},

	onCategoryClick: function(category) {
		this.setState({category: category});
	},

	render: function() {
		return (
			<div>
				<CategoryDiv categories={this.props.categories}, onCategoryClick={this.onCategoryClick} />
				<hr />
				<Entries entries={this.props.data[this.state.category]} />
				<hr />
			</div>
		)
	}
});
