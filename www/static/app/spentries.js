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

var Entry = React.createClass({
	render: function() {
		var style = {
			fontWeight: "600",
			fontSize: "0.8em",
			fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
			lineHeight: "2em",
			textDecoration: "none"
		};
		var url = "/a/" + this.props.aid;

		return (
			<li>
				<a style={style} href={url} target="_blank">{this.props.title}</a>
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
				{entries.map(function(entry, index) {return <Entry key={index} aid={entry[0]} title={entry[1]} />;})}
			</ul>
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

var AidLink = React.createClass({
	onClick: function(e) {
		e.preventDefault();
		e.stopPropagation();

		this.props.onAidClick();
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
				<a href="#" onClick={this.onClick}>
					<i className={cn} aria-hidden="true"></i>
		  	</a>
			</span>
		)
	}
});

var AidLinkDiv = React.createClass({
	render: function() {
		var style = {
			paddingLeft: "40%",
			paddingRight: "40%"
		};

		return (
			<div style={style}>
				<AidLink handType="handleft" onAidClick={this.props.onLeftClick} />
				<AidLink handType="handright" onAidClick={this.props.onRightClick} />
			</div>
		)
	}
});

var App = React.createClass({
	getEntries: function(aid, q) {
		var spid = document.location.pathname.split("/").pop();
		var args = {spid: spid};
		if (aid != null) {
			args['aid'] = aid;
			args['q'] = q;
		}

		$.getJSON("/api/spider", args).done(function(data){
			var err = data["err"];
			if (!err) {
				var name = data["spider"][1];
				this.setState({name: name, entries: data["entries"]});
			}
		}.bind(this));
	},

	onLeftClick: function() {
		var entries = this.state.entries;
		if (entries.length == 0) {
			return;
		}
		var aid = entries[0][0];
		this.getEntries(aid, "p");
	},

	onRightClick: function() {
		var entries = this.state.entries;
		if (entries.length == 0) {
			return;
		}
		var aid = entries[entries.length-1][0];
		this.getEntries(aid, "n");
	},

	getInitialState: function() {
		return {name: "", entries: []}
	},

	componentDidMount: function() {
		this.getEntries();
	},

	render: function() {
		return (
			<div>
				<Title name={this.state.name} />
				<Hr />
				<Entries entries={this.state.entries} />
				<Hr />
				<AidLinkDiv onLeftClick={this.onLeftClick} onRightClick={this.onRightClick} />
			</div>
		)
	}
});

ReactDOM.render(<App />, document.getElementById("content"));
