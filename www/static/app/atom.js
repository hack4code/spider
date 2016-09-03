var Input = React.createClass({
  handleChange: function(e) {
		var v = e.target.value;
		this.props.updateField(this.props.field, v);
  },

  render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "1px",
			boxShadow: "none",
			boxSizing: "border-box",
			height: "3.2em",
			width: "42em",
			margin: "0em 0em 1.2em 0em",
			display: "block"
		};

    return (
			<input style={style} value={this.props.value} onChange={this.handleChange} type={this.props.type}/>
		)
  }
});

var Label = React.createClass({
	render: function() {
		var style = {
			fontSize: "1.0em",
			fontWeight: "bold",
			marginBottom: "0.5em",
			display: "block"
		};

		return (
			<label style={style}>{this.props.desc}</label>
		)
	}
});

var EditBox = React.createClass({
	render: function() {
		return (
			<div>
				<Label desc={this.props.desc} />
				<Input type={this.props.type} updateField={this.props.updateField} field={this.props.field} value={this.props.value} />
			</div>
		)
	}
});

var Select = React.createClass({
	getInitialState: function() {
		return {list: ["null",]};
	},
	
	componentDidMount: function() {
		$.getJSON(this.props.url).done(function(data) {
			var err = data["err"];
			if (!err) {
				this.setState({list: data["data"]});
			}
		}.bind(this));
	},

  handleChange: function(e) {
		var v = e.target.value;
		this.props.updateField(this.props.field, v);
  },

	render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "1px",
			boxShadow: "none",
			boxSizing: "border-box",
			height: "3.2em",
			width: "42em",
			margin: "0em 0em 1.2em 0em",
			display: "block"
		};
		var list = this.state.list;

		return (
			<select style={style} value={this.props.value} onChange={this.handleChange}>
				{list.map(function(v) { return <option value={v}>{v}</option>; })}
			</select>
		)
	}
});

var SelectBox = React.createClass({
	render: function() {
		return (
			<div>
				<Label desc={this.props.desc} />
				<Select updateField={this.props.updateField} url={this.props.url} field={this.props.field} value={this.props.value} />
			</div>
		)
	}
});

var Button = React.createClass({
	handleClick: function(e) {
		e.preventDefault();
		e.stopPropagation();

		this.props.submit();
	},

	render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "0.4rem",
			boxSizing: "borderBox",
			cursor: "pointer",
			display: "inlineBlock",
			fontSize: "0.4rem",
			fontWeight: "700",
			height: "3.2em",
			letterSpacing: "0.3em",
			textAlign: "center",
			textDecoration: "none",
			textTransform: "uppercase",
			whiteSpace: "nowrap"
		};

		return (
			<input style={style} type="submit" value="提交" onClick={this.handleClick}/>
		)
	}
});


var App = React.createClass({
	getInitialState: function(){
		return {category: "null"};
	},

	submit: function() {
	},

	updateField: function(k, v) {
		this.setState({[k]: v});
	},

	render: function() {
		console.log(this.state);
		return (
			<form><fieldset>
				<EditBox desc="网址" type="url" field="url" value="" />
				<SelectBox desc="类别" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
				<EditBox desc="selector[用于非全文输出的feed]" type="url" field="content" value="" />
				<Button submit={this.submit} />
			</fieldset></form>
		)
	}
});

ReactDOM.render(<App />, document.getElementById('content'));
