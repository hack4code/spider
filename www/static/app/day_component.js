import React from "react";


const is_small_screen = screen.width < 600 ? true : false;

function decodeEntities(encodedString) {
    let textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
}

class NavSector extends React.Component  {
  render() {
    return (
      <div>
        <p>导航</p>
        <ul>
          <li><p>/d/Y-M-D: 按日期显示文章</p></li>
          <li><p>/l/p: 所有订阅源</p></li>
          <li><p>/feed/rss: 添加rss订阅源</p></li>
          <li><p>/feed/blog: 添加blog订阅源</p></li>
        </ul>
      </div>
    )
  }
};

class DeclareSector extends React.Component  {
  render() {
    return (
      <div>
        <p>声明</p>
        <ul>
          <li><p>所有文章标题处均附有原文链接</p></li>
          <li><p>所有内容来自互联网，任何商业用途请联系原作者</p></li>
        </ul>
      </div>
    )
  }
};

class SpiderButton extends React.Component  {
  render() {
    const style = {
      backgroundColor: "#eff6fa",
      border: "0.1em solid #eff6fa",
      borderRadius: "0.4em",
      boxSizing: "border-box",
      color: "#259",
      cursor: "pointer",
      display: "inline-block",
      fontSize: "0.6em",
      fontWeight: "bold",
      height: "3em",
      width: "92%",
      letterSpacing: "0.1rem",
      lineHeight: "3em",
      padding: "1 4em",
      textAlign: "center",
      textDecoration: "none"
    };

    return (
      <li><div>
        <p>{this.props.desc}</p>
        <a style={style} href={this.props.url} target="_blank">{this.props.title}</a>
      </div></li>
    )
  }
};

class SubmitSector extends React.Component  {
  render() {
    return (
      <div>
        <p>Spider</p>
        <ul>
          <SpiderButton desc="添加rss源，支持rss与atom" url="/feed/rss" title="生成RSS Spider" />
          <SpiderButton desc="添加blog,用于没有rss输出的blog" url="/feed/blog" title="生成Blog Spider" />
        </ul>
      </div>
    )
  }
};

class AddressSector extends React.Component  {
  render() {
    const style = {
      color: "#888",
      textDecoration: "none"
    };

    return (
      <div>
      <p>联系方式</p>
      <ul>
        <li>
        <p>email: <a style={style} href="mailto:code4hack@gmail.com">code4hack@gmail.com</a></p>
        </li>
      </ul>
      <p>项目地址</p>
      <ul>
        <li>
        <p>github: <a style={style} href="https://github.com/hack4code/BlogSpider" target="_blank">BlogSpider</a></p>
        </li>
      </ul>
      </div>
    )
  }
};

class FloatSide extends React.Component  {
  render() {
    const style = {
      float: "right",
      width: "300px",
      padding: "0 32px",
      fontFamily: "sans-serif",
      fontSize: "0.7em",
      fontWeight: "bold",
      color: "dimgray",
      display: is_small_screen ? "none" : "block"
    };

    return (
      <div style={style}>
        <NavSector />
        <Hr />
        <DeclareSector />
        <Hr />
        <SubmitSector />
        <Hr />
        <AddressSector />
      </div>
    )
  }
};

class Rank extends React.Component  {
  render() {
    const style = {
     color: "#c6c6c6",
     textAlign: "right",
     fontFamily: "arial",
     fontSize: "medium",
     fontWeight: "bold",
     width: is_small_screen ? "30px" : "40px",
     paddingRight: is_small_screen ? "15px" : "25px",
     flexShrink: 0
    };

    return (
      <span style={style}>
        {this.props.rank}
      </span>
    )
  }
};

class ArticleLink extends React.Component  {
  render() {
    const style = {
      fontFamily: "Helvetica Neue, Helvetica, Pingfang SC, Microsoft YaHei, arial, sans-serif",
      fontSize: "1em",
      fontWeight: "normal",
      lineHeight: "110%",
      margin: "0px",
      padding: "0px",
    };
    let url = "/a/" + this.props.aid;
    let title = decodeEntities(this.props.title);

    return (
      <span className="articlelink">
        <a style={style} href={url} target="_blank">{title}</a>
      </span>
    )
  }
};

class OrginalLink extends React.Component  {
  render() {
    const style = {
      margin: "0px",
      padding: "0 6px",
      fontSize: "x-small",
    };

    return (
      <span className="articlelink">
        <a style={style} href={this.props.url} target="_blank">
        <i className="fa fa-paper-plane-o" aria-hidden="true"></i>
        </a>
      </span>
    )
  }
};

class DomainLink extends React.Component  {
  render() {
    const style = {
      color: "#888",
      fontSize: "x-small",
      whiteSpace: "nowrap",
      textDecoration: "none",
      margin: "0px",
      padding: "0px",
    };
    let url = "http://" + this.props.domain;

    return (
      <span>
        <a style={style} href={url} target="_blank">({this.props.domain})</a>
      </span>
    )
  }
};

class EntryTitle extends React.Component  {
  render() {
    const style = {
      margin: "0px",
      padding: "0px"
    };

    return (
      <div style={style}>
        <ArticleLink aid={this.props.aid} title={this.props.title} />
        <OrginalLink url={this.props.url} />
        <DomainLink domain={this.props.domain} />
      </div>
    )
  }
};

class SpiderTag extends React.Component  {
  render() {
    const style = {
      color: "#999",
      fontSize: "x-small",
      fontWeight: "bold",
      marginRight: "4px",
      marginBottom: "2px",
      textDecoration: "none"
    };
    let spid = this.props.spider.spid;
    let spname = this.props.spider.spname;
    let url = "/p/" + spid;

    return (
      <span>
        <a style={style} href={url} target="_blank">[{spname}]</a>
      </span>
    )
  }
};

class ArticleTag extends React.Component  {
  render() {
    const style = {
      fontWeight: "normal",
      fontSize: "x-small",
      color: "#999",
      backgroundColor: "#eee",
      borderRadius: "30px",
      padding: "1px 10px",
      marginRight: "4px",
      marginBottom: "2px",
      whiteSpace: "nowrap"
    };

    return (
      <span style={style}>
        {this.props.tag}
      </span>
    )
  }
};

class EntryTags extends React.Component {
  render() {
    const style = {
      display: "flex",
      flexDirection: "row",
      flexWrap: "wrap",
      alignItems: "baseline",
      margin: "0px",
      padding: "0px",
    };
    let spider = this.props.spider;
    let tags = this.props.tags;

    return (
      <div style={style}>
        <SpiderTag spider={spider} />
        {tags.map(function(tag, index) { return <ArticleTag key={index} tag={tag} />; })}
      </div>
    )
  }
};

class Entry extends React.Component {
  render() {
    const style = {
      display: "flex",
      alignItems: "center",
      marginBottom: "12px"
    };

    let index = this.props.index;
    let entry = this.props.entry;
    let spider = {spid: entry[5], spname: entry[3]};
    let tags = (entry[4] == null) ? [] : entry[4];

    return (
        <div style={style}>
          <Rank rank={index} />
          <div>
            <EntryTitle aid={entry[0]} title={entry[1]} url={entry[7]} domain={entry[6]} />
            <EntryTags spider={spider} tags={tags} />
          </div>
        </div>
    )
  }
};

class Entries extends React.Component {
  render() {
    let entries = this.props.entries;
    return (
      <div>
        {entries.map(function(entry, index) {
          return <Entry key={index} index={index} entry={entry} />
        })}
      </div>
    )
  }
};

class Category extends React.Component {
  onClick(e, category) {
    e.preventDefault();
    e.stopPropagation();

    this.props.onCategoryClick(category);
  }

  render() {
    const listyle = {
      display: "inline-block",
      marginRight: is_small_screen ? "0.8em" : "1.6em"
    };

    const astyle = {
      fontFamily: "Pingfang SC, Microsoft YaHei",
      fontWeight: "bold",
      fontSize: "1.0em",
      color: "#666666",
      textDecoration: "none"
    };

    if (this.props.focus) {
      astyle["color"] = "#222222";
    }

    return (
      <li style={listyle}>
        <a href="#" style={astyle} onClick={(e)=>this.onClick(e, this.props.category)}>{this.props.category}</a>
      </li>
    )
  }
};

class CategoryDiv extends React.Component {
  render() {
    const style = {
      listStyle: "none",
      marginBottom: "0em",
      marginLeft: is_small_screen ? "0em" : "2em",
      paddingLeft: is_small_screen ? "0em" : "2em"
    };

    let categories = this.props.categories;
    let onCategoryClick = this.props.onCategoryClick;
    let categoryFocused = this.props.categoryFocused;

    return (
      <div>
        <ul style={style}>
          {categories.map(function(category, index) {
            let focus = (categoryFocused == category);
            return <Category key={index} focus={focus} category={category} onCategoryClick={onCategoryClick} />;
          })}
        </ul>
      </div>
    )
  }
};

class Hr extends React.Component {
  render() {
    const style = {
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
};

class ContentDiv extends React.Component {
  static defaultProps = {
    data: {"新闻": [],
           "技术": [],
           "科技": [],
           "数据库": [],
           "安全": [],
           "python": []}
  };

  constructor(props) {
    super(props);
    let categories = this.getCategories(props.data);
    this.state = {category: categories[0]};
  };

  getCategories(data) {
    let categories = [];

    for (let key in data) {
      if (data.hasOwnProperty(key)) {
        categories.push(key);
      }
    };
    return categories.sort(function(a, b) {
      const sortList = {
        "技术": 0,
        "python": 1,
        "数据库": 2,
        "安全": 3,
        "科技": 4,
        "新闻": 5
      };
      return (sortList[a] > sortList[b]) ? 1 : -1;
    });
  }

  componentWillReceiveProps(nextProps) {
    this.setState({category: this.getCategories(nextProps.data)[0]});
  }

  onCategoryClick(category) {
    this.setState({category: category});
  }

  render() {
    let data = this.props.data;
    let categories = this.getCategories(data);
    let entries = data[this.state.category];

    return (
      <div>
        <CategoryDiv categoryFocused={this.state.category} categories={categories} onCategoryClick={this.onCategoryClick.bind(this)} />
        <Hr />
        <FloatSide />
        <Entries entries={entries} />
        <Hr />
      </div>
    )
  }
};

class DayLink extends React.Component {
  onClick(e, day) {
    e.preventDefault();
    e.stopPropagation();

    this.props.onDayLinkClick(day);
  }

  render() {
    let cn = "";
    let style = {};

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
        <a href="#" onClick={(e)=>this.onClick(e, this.props.day)}>
          <i className={cn} aria-hidden="true"></i>
        </a>
      </span>
    )
  }
};

class DayLinkDiv extends React.Component {
  render() {
    const style = {
      paddingLeft: "30%",
      paddingRight: "30%"
    };

    return (
      <div style={style}>
        <DayLink handType="handleft" day={this.props.day_after} onDayLinkClick={this.props.onDayLinkClick} />
        <DayLink handType="handright" day={this.props.day_before} onDayLinkClick={this.props.onDayLinkClick} />
      </div>
    )
  }
};

export {ContentDiv, DayLinkDiv};
