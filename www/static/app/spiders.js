var Title = React.createClass({
	render: function() {
		var style = {
			fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
			fontSize: "normal",
			fontWeight: "bold",
			textAlign: "center"
		};

		return (
			<div>
				<p style={style}>{this.props.name}</p>
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

var Entry = React.createClass({
	render: function() {
		var style = {
			fontWeight: "600",
			fontSize: "0.8em",
			fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
			lineHeight: "2em",
			textDecoration: "none"
		};
		var url = "/p/" + this.props.spid;

		return (
			<li>
				<a style={style} href={url} target="_blank">{this.props.name}</a>
			</li>
		)
	}
});


var Entries = React.createClass({
	render: function() {
		var style = {
			listStyle: "square",
			color: "red",
			marginLeft: "4em"
		};
		var entries = this.props.entries;

		return (
			<ul style={style}>
				{entries.map(function(entry, index) {return <Entry key={index} spid={entry[0]} name={entry[1]} />;})}
			</ul>
		)
	}
});

var App = React.createClass({
	getInitialState: function() {
		return {entries: []}
	},

	componentDidMount: function() {
		$.getJSON("/api/spiders").done(function(data){
			var err = data["err"];
			if (!err) {
				this.setState({entries: data["entries"]});
			}
		}.bind(this))
	},

	render: function() {
		return (
			<div>
				<Title name="所有订阅网站" />
				<Hr />
				<Entries entries={this.state.entries} />
			</div>
		)
	}
});

ReactDOM.render(<App />, document.getElementById("content"));
