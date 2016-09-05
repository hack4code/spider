var Title = React.createClass({
	render: function() {
		var style = {
			fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
			fontSize: "1.6em",
			fontWeight: "normal",
			textAlign: "center"
		};

		return (
			<div>
				<p style={style}>{this.props.title}</p>
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

var ErrMsg = React.createClass({
	render: function() {
		var style = {
			textAlign: "center",
			fontSize: "0.5em",
			color: "#888",
			marginBottom: "1em"
		};

		return (
			<div style={style}>
				<span></span>
			</div>
		)
	}
});

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
 			fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
			fontSize: "1.0em",
			fontWeight: "normal",
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
				var list = data["data"];
				this.setState({list: list});
				this.props.updateField(this.props.field, list[0]);
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
				{list.map(function(v, index) { return <option key={index} value={v}>{v}</option>; })}
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


var SubmitForm = React.createClass({
	getInitialState: function(){
		return {category: "",
						url: "",
						entry: "",
						item_title: "",
						item_link: "",
						item_content: ""}
	},

	submit: function() {
		var form = this.state;
		if (form["url"] == "" || form["entry"] == "" || form["item_title"] == "" || form["item_link"] == "" || form["item_content"] == "") {
			$("span").text("数据不能为空").show().fadeOut(2000);
			return;
		}

		$("span").text("正在提交 .....").show();
		$.ajax({type: "post",
						url: "/api/feed/feed",
						data: form,
						success: function(r){
					 		if (r['err'] == 0) {
								$("span").text("成功").show().fadeOut(1500);
				 			}
			      	else {
								$("span").text("失败: " + r["msg"]).show().fadeOut(1500);
			      	}
							this.setState({url: "", content: ""});
					  }.bind(this)}
		);
	},

	updateField: function(k, v) {
		this.setState({[k]: v});
	},

	render: function() {
		var style = {
			borderWidth: 0,
			padding: 0,
			paddingLeft: "36px"
		};

		return (
			<div>
				<ErrMsg />
				<form><fieldset style={style}>
					<EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
					<SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
					<EditBox desc="文章Selector:" updateField={this.updateField} type="text" field="entry" value={this.state.entry} />
					<EditBox desc="标题Selector:" updateField={this.updateField} type="text" field="item_title" value={this.state.item_title} />
					<EditBox desc="链接Selector:" updateField={this.updateField} type="text" field="item_link" value={this.state.item_link} />
					<EditBox desc="内容Selector:" updateField={this.updateField} type="text" field="item_content" value={this.state.item_content} />
					<Button submit={this.submit} />
				</fieldset></form>
			</div>
		)
	}
});

var App = React.createClass({
	render: function() {
		return (
			<div>
				<Title title="添加订阅源(Blog)" />
				<Hr />
				<SubmitForm />
			</div>
		)
	}
});

ReactDOM.render(<App />, document.getElementById('content'));
