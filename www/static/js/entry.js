var Rank = React.createClass({
	render: function() {
		return (
			<span>
				{this.props.rank}
			</span>
		);
	}
});

var ArticleLink = React.createClass({
	render: function() {
		return (
			<a href={this.props.url}>{this.props.title}</a>
		)
	}
});

var OrginalLink = React.createClass({
	render: function() {
		return (
			<span>
				<a href={this.props.url}>
				<i class="fa fa-paper-plane-o" aria-hidden="true"></i>
				</a>
			</span>
		)
	}
});

var DomainLink = React.createClass({
	render: function() {
		return (
			<span>
				(<a href={this.props.url}>{this.props.domain}</a>)
			</span>
		)
	}
});

var EntryTitle = React.createClass({
	render: function() {
		return (
			<div><p>
			</p></div>
		)
	}
});
