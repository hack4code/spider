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
				(<a href={this.props.url}>{this.props.domain}</a>)
			</span>
		)
	}
});

var EntryTitle = React.createClass({
	render: function() {
		return (
			<div><p>
				<Rank rank={} />
				<ArticleLink aid={} title={} />
				<OrginalLink url={} />
				<DomainLink url={} domain={} />
			</p></div>
		)
	}
});

var SpiderName = React.createClass({
	render: function() {
		return (
			<li>
				<a href={this.props.spid}>[{this.props.spname}]</a>
			</li>
		)
	}
});

var ArticleTag = React.createClass({
	render: function() {
		return (
			<li>
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
			<div><ul>
				<SpiderName spid={spider.id} spname={spider.name} />
				{tags.map(function(tag) {
					return <ArticleTag tag={tag} />;
				})}
			</ul></div>
		)
	}
});
