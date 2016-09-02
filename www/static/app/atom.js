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
      <input type={this.props.type} style={style} value={this.props.value} onChange={this.handleChange} />
    );
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
		return {list: []};
	}
	
	componentDidMount: function() {
		$.getJSON(this.props.url).done(function(data) {
			this.setState({list: data});
		});
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
			<select style={style} value={list[0]} onChange={this.handleChange}>
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
				<Select updateField={this.props.updateField} field={this.props.field} value={this.props.value} />
			</div>
		)
	}
});

var Button = React.createClass({
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
			<input style={style} type="submit" value={this.props.value} onClick={this.props.submit} >
		)
	}
});

var AtomForm = React.createClass({
	getInitialState: function() {
		return {};
	},

	updateField: function(k, v) {
		this.setState({k: v});
	},
	
	submit: function() {
	},

	render: function() {
		return (
			<form>
				<EditBox desc="网址" type="url" field="url" value="" />
				<Select desc="类别" field="category" url="" />
				<EditBox desc="selector[用于非全文输出的feed]" type="url" field="content" value="" />
				<Button submit={this.submit} />
			</form>
		)
	}
});
