var Voter = React.createClass({
	getInitialState: function(){
		var s = window.localStorage;
		var aid = this.props.aid;
		if (s.getItem(aid) != null) {
			return {voted: 1};
		}
		else {
			return {voted: 0};
		}
	},

	onClick(e) {
		e.preventDefault();
		e.stopPropagation();

		var s = window.localStorage;
		var aid = this.props.aid;

		if (s.getItem(aid) != null) {
			return;
		}
		else {
			this.setState({voted: 1});
			$.post("/api/vote", {aid: aid}).done(function(data){
				if (!data['err']) {
					s.setItem(aid, 1);
				}
				else {
					this.setState({voted: 0});
				}
			}.bind(this));
		}
	},

	render: function() {
		var style = {
			fontSize: "1em",
			fontWeight: "bold"
		};
		style["color"] = this.state.voted ? "#004276" : "#999999";

		return (
			<div>
				<a style={style} href="#" onClick={this.onClick}>
					<i className="fa fa-thumbs-o-up"></i>
				</a>
			</div>
		)
	}
});

var Footer = React.createClass({
	render: function() {
		var style = {
			color: "#888",
			fontSize: "x-small",
		};
		var url = "/p/" + this.props.spid;

		return (
			<p style={style}>
				本文章来自
				<span>[<a href={url} target="_blank">{this.props.spname}</a>]</span>
				, 您可以对文章点赞
			</p>
		)
	}
});

var App = React.createClass({
	render: function() {
		var style = {
			display: "flex",
			flexDirection: "column",
			alignItems: "center"
		};
		var aid = $("#content").attr("aid");
		var spid = $("#content").attr("spid");
		var spname = $("#content").attr("spname");

		return (
			<div style={style}>
				<Voter aid={aid} />
				<Footer spid={spid} spname={spname} />
			</div>
		)
	}
});

ReactDOM.render(<App />, document.getElementById('content'));
